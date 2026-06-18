#!/usr/bin/env python3
"""
heygen_full_render.py
=====================
Full production video submission to HeyGen API.

RESEARCH FINDINGS (confirmed via API exploration):
  - v2/video/generate is THE endpoint for everything
  - Supports: multi-scene (multiple video_inputs), video backgrounds, image backgrounds,
    background music (any URL), avatar positioning/scaling, silence scenes
  - Does NOT natively support: text overlays, lower thirds, or title cards in the payload
    (those fields are silently accepted but ignored)
  - Text overlays MUST be done via: baked-in background images OR FFmpeg post-processing
  - No preset music library — use uploaded asset URLs or any public audio URL
  - Test mode (test=True): free watermarked renders, limit 5/day
  - Template system (/v2/template/{id}/generate) exists but templates have no variables

CONFIRMED WORKING PAYLOAD STRUCTURE:
  {
    "video_inputs": [
      {
        "character": { "type": "avatar", "avatar_id": "...", "avatar_style": "normal" },
        "voice": { "type": "text", "input_text": "...", "voice_id": "...", "speed": 1.0 },
        "background": { "type": "video", "url": "...", "play_style": "loop" }
      },
      ... more scenes ...
    ],
    "background_music": { "enable": true, "url": "...", "volume": 0.25 },
    "aspect_ratio": "16:9",
    "title": "My Video",
    "test": false
  }

video.play_style valid values: "fit_to_scene" | "freeze" | "loop" | "once"
"""

import urllib.request
import urllib.error
import json
import time
import sys
import os
import subprocess

# =============================================================================
# CONFIGURATION
# =============================================================================

API_KEY = os.environ.get("HEYGEN_API_KEY")
if not API_KEY:
    sys.exit("HEYGEN_API_KEY is not set. Export it before running "
             "(e.g. from your GitSync credentials). Never hardcode the key.")
AVATAR_ID = "524caea65d4a45b5aab1c649cde0d472"   # Brent Bryson - Black Hoodie
VOICE_ID = "50e70458c88d4afb8ec65ec4adee00bb"

# Uploaded assets on the account (from /v1/asset/list)
ASSETS = {
    "broll_multi_look": "https://resource2.heygen.ai/video/a11907efb19c4af289d7c99d6b606ca3/original.mp4",
    "broll_black_hoodie": "https://resource2.heygen.ai/video/9da9e26144054553b04187cbb075472f/original.mp4",
    "broll_podcast": "https://resource2.heygen.ai/video/662bf653f59e4725bf8c92fbee05f02e/original.mp4",
    "audio_elevenlabs": "https://resource2.heygen.ai/audio/1d02b909c2ca478494c73f914b233425/original.mp3",
}

# Free/public music URLs you can use (royalty-free sources)
# Replace with actual music URLs from your uploads or royalty-free sources
MUSIC_PRESETS = {
    "none": None,
    "uploaded_voice_sample": ASSETS["audio_elevenlabs"],
    # Add your own music assets via /v1/asset/upload then use the returned URL
}

BASE_URL = "https://api.heygen.com"


# =============================================================================
# API HELPERS
# =============================================================================

def api_get(path) -> dict:
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"X-Api-Key": API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result: dict = json.loads(r.read())
            return result
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.read().decode()[:500]}
    except Exception as e:
        return {"error": str(e)}


def api_post(path, data) -> dict:
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers={
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result: dict = json.loads(r.read())
            return result
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.read().decode()[:1000]}
    except Exception as e:
        return {"error": str(e)}


def poll_video(video_id, timeout=600, interval=15):
    """Poll until video is completed or failed. Returns final status dict."""
    print(f"  Polling video {video_id}...")
    elapsed = 0
    while elapsed < timeout:
        r = api_get(f"/v1/video_status.get?video_id={video_id}")
        data = r.get("data", {})
        status = data.get("status", "unknown")
        print(f"  [{elapsed}s] Status: {status}")
        if status == "completed":
            return data
        elif status in ("failed", "error"):
            print(f"  ERROR: {data.get('error', 'unknown error')}")
            return data
        time.sleep(interval)
        elapsed += interval
    print(f"  Timeout after {timeout}s")
    return {"status": "timeout"}


# =============================================================================
# SCENE BUILDERS
# =============================================================================

def avatar_scene(script_text, background_type="color", background_value="#1a1a2e",
                 background_url=None, background_play_style="loop",
                 avatar_id=AVATAR_ID, voice_id=VOICE_ID,
                 avatar_style="normal", speed=1.0):
    """
    Build a single scene with avatar speaking.

    background_type: "color" | "image" | "video"
    background_value: hex color (e.g. "#1a1a2e") for type=color
    background_url: URL for type=image or type=video
    background_play_style: for video: "fit_to_scene" | "freeze" | "loop" | "once"
    """
    scene = {
        "character": {
            "type": "avatar",
            "avatar_id": avatar_id,
            "avatar_style": avatar_style
        },
        "voice": {
            "type": "text",
            "input_text": script_text,
            "voice_id": voice_id,
            "speed": speed
        }
    }

    if background_type == "color":
        scene["background"] = {"type": "color", "value": background_value}
    elif background_type == "image":
        scene["background"] = {"type": "image", "url": background_url}
    elif background_type == "video":
        scene["background"] = {
            "type": "video",
            "url": background_url,
            "play_style": background_play_style
        }
    else:
        scene["background"] = {"type": "color", "value": "#1a1a2e"}

    return scene


def silence_scene(duration_seconds=3, background_type="color", background_value="#000000",
                  background_url=None, background_play_style="freeze",
                  avatar_id=AVATAR_ID):
    """
    Build a silent pause scene (avatar is visible but silent).
    Use for CTA cards, title cards, b-roll pauses.
    NOTE: You must add text overlays via FFmpeg after rendering.
    """
    scene = {
        "character": {
            "type": "avatar",
            "avatar_id": avatar_id,
            "avatar_style": "normal"
        },
        "voice": {
            "type": "silence",
            "duration": duration_seconds
        }
    }

    if background_type == "color":
        scene["background"] = {"type": "color", "value": background_value}
    elif background_type == "image":
        scene["background"] = {"type": "image", "url": background_url}
    elif background_type == "video":
        scene["background"] = {
            "type": "video",
            "url": background_url,
            "play_style": background_play_style
        }

    return scene


# =============================================================================
# MAIN GENERATION FUNCTIONS
# =============================================================================

def generate_full_production_video(
    scenes,
    title="TigerClaw YouTube Video",
    aspect_ratio="16:9",
    background_music_url=None,
    background_music_volume=0.2,
    test_mode=False
):
    """
    Submit a full production video to HeyGen.

    Args:
        scenes: list of scene dicts (from avatar_scene() or silence_scene())
        title: video title
        aspect_ratio: "16:9" | "9:16" | "1:1"
        background_music_url: URL to background music file (None = no music)
        background_music_volume: 0.0 to 1.0 (0.2 = 20% volume, good for background)
        test_mode: True = free watermarked render (limit 5/day), False = production render

    Returns:
        video_id string or None on failure
    """
    payload = {
        "video_inputs": scenes,
        "aspect_ratio": aspect_ratio,
        "title": title,
    }

    if test_mode:
        payload["test"] = True

    if background_music_url:
        payload["background_music"] = {
            "enable": True,
            "url": background_music_url,
            "volume": background_music_volume
        }

    print(f"\nSubmitting video: {title}")
    print(f"  Scenes: {len(scenes)}")
    print(f"  Aspect ratio: {aspect_ratio}")
    print(f"  Background music: {background_music_url or 'None'}")
    print(f"  Test mode: {test_mode}")

    r = api_post("/v2/video/generate", payload)

    if "error" in r and r.get("error") not in (None, "null"):
        print(f"  API Error: {r}")
        return None

    data = r.get("data", {})
    video_id = data.get("video_id")

    if video_id:
        print(f"  Submitted! video_id: {video_id}")
        print(f"  Track at: https://app.heygen.com/videos/{video_id}")
    else:
        print(f"  Unexpected response: {r}")

    return video_id


def add_text_overlays_ffmpeg(input_video_path, output_video_path, overlays):
    """
    Post-process a video to add text overlays using FFmpeg.
    This is the ONLY way to add lower thirds/text cards to HeyGen videos.

    overlays: list of dicts with:
        {
            "text": "Subscribe Now!",
            "fontsize": 48,
            "fontcolor": "white",
            "box": 1,              # 1 = box background
            "boxcolor": "black@0.5",
            "x": "(w-text_w)/2",   # centered
            "y": "h-100",          # near bottom
            "start_t": 0,          # show from second 0
            "end_t": 5             # hide at second 5 (None = show till end)
        }
    """
    if not overlays:
        return

    # Check ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING: FFmpeg not found. Install with: sudo apt install ffmpeg")
        return

    vf_parts = []
    for ov in overlays:
        text = ov["text"].replace("'", "\\'").replace(":", "\\:")
        fontsize = ov.get("fontsize", 48)
        fontcolor = ov.get("fontcolor", "white")
        x = ov.get("x", "(w-text_w)/2")
        y = ov.get("y", "h-100")
        box = ov.get("box", 1)
        boxcolor = ov.get("boxcolor", "black@0.5")
        start_t = ov.get("start_t", 0)
        end_t = ov.get("end_t", None)

        enable_expr = f"between(t,{start_t},{end_t})" if end_t else f"gte(t,{start_t})"

        part = (
            f"drawtext=text='{text}'"
            f":fontsize={fontsize}"
            f":fontcolor={fontcolor}"
            f":x={x}"
            f":y={y}"
            f":box={box}"
            f":boxcolor={boxcolor}"
            f":boxborderw=10"
            f":enable='{enable_expr}'"
        )
        vf_parts.append(part)

    vf = ",".join(vf_parts)
    cmd = ["ffmpeg", "-i", input_video_path, "-vf", vf, "-c:a", "copy", "-y", output_video_path]

    print(f"\nApplying FFmpeg text overlays...")
    print(f"  Input: {input_video_path}")
    print(f"  Output: {output_video_path}")
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        print("  Done!")
    else:
        print(f"  FFmpeg error: {result.stderr.decode()[:500]}")


def download_video(video_url, output_path):
    """Download completed video from HeyGen CDN."""
    print(f"\nDownloading video to {output_path}...")
    req = urllib.request.Request(video_url)
    with urllib.request.urlopen(req, timeout=120) as r:
        with open(output_path, "wb") as f:
            f.write(r.read())
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"  Downloaded {size_mb:.1f} MB")


# =============================================================================
# PRE-BUILT PRODUCTION TEMPLATES
# =============================================================================

def render_test_video(test_mode=True):
    """
    Test render: 'This is a test of the full production system.'
    Short 3-sentence script with video background and music.
    """
    scenes = [
        avatar_scene(
            script_text=(
                "This is a test of the full production system. "
                "Real AI. Real distribution. Real results."
            ),
            background_type="video",
            background_url=ASSETS["broll_multi_look"],
            background_play_style="loop"
        )
    ]

    return generate_full_production_video(
        scenes=scenes,
        title="Full Production System Test",
        aspect_ratio="16:9",
        background_music_url=None,  # Add music URL here when ready
        test_mode=test_mode
    )


def render_youtube_video(script_sections, title, music_url=None, test_mode=False):
    """
    Render a full YouTube video with multiple sections.

    script_sections: list of (text, broll_url) tuples
        e.g. [("Intro text here...", ASSETS["broll_multi_look"]),
              ("Main point one...", ASSETS["broll_podcast"]),
              ...]

    Returns video_id
    """
    scenes = []

    for i, (text, broll_url) in enumerate(script_sections):
        bg_type = "video" if broll_url else "color"
        scene = avatar_scene(
            script_text=text,
            background_type=bg_type,
            background_url=broll_url,
            background_play_style="loop",
            background_value="#1a1a2e",
        )
        scenes.append(scene)

    # Add a 3-second outro silence scene (for CTA overlay via FFmpeg)
    outro = silence_scene(
        duration_seconds=3,
        background_type="color",
        background_value="#FF0000"  # Red background for subscribe CTA
    )
    scenes.append(outro)

    return generate_full_production_video(
        scenes=scenes,
        title=title,
        aspect_ratio="16:9",
        background_music_url=music_url,
        background_music_volume=0.2,
        test_mode=test_mode
    )


def full_production_pipeline(script_sections, title, music_url=None,
                              output_dir="/tmp", test_mode=False):
    """
    Complete pipeline:
    1. Submit to HeyGen
    2. Poll until complete
    3. Download raw video
    4. Apply FFmpeg text overlays (lower thirds + subscribe CTA)
    5. Return final output path

    script_sections: list of (text, broll_url, lower_third_text) tuples
    """
    # Build scenes and collect overlay timing info
    scenes = []
    overlay_plan = []
    current_t = 0  # approximate timing (HeyGen doesn't return per-scene timestamps)

    for i, section in enumerate(script_sections):
        text = section[0]
        broll_url = section[1] if len(section) > 1 else None
        lower_third = section[2] if len(section) > 2 else None

        bg_type = "video" if broll_url else "color"
        scene = avatar_scene(
            script_text=text,
            background_type=bg_type,
            background_url=broll_url,
            background_play_style="loop",
            background_value="#1a1a2e",
        )
        scenes.append(scene)

        # Estimate duration: ~150 words/min = 2.5 words/sec
        word_count = len(text.split())
        est_duration = max(3, word_count / 2.5)

        if lower_third:
            overlay_plan.append({
                "text": lower_third,
                "fontsize": 36,
                "fontcolor": "white",
                "box": 1,
                "boxcolor": "black@0.6",
                "x": "80",  # left-aligned lower third
                "y": "h-120",
                "start_t": current_t + 1,
                "end_t": current_t + min(5, est_duration - 1)
            })

        current_t += est_duration

    # Add subscribe CTA outro (3-second silence scene)
    scenes.append(silence_scene(
        duration_seconds=5,
        background_type="color",
        background_value="#0F0F0F"
    ))

    # CTA overlay for the outro
    cta_start = current_t
    overlay_plan.append({
        "text": "LIKE + SUBSCRIBE for Daily AI Insights",
        "fontsize": 52,
        "fontcolor": "#FFDD00",
        "box": 1,
        "boxcolor": "black@0.7",
        "x": "(w-text_w)/2",
        "y": "(h-text_h)/2",
        "start_t": cta_start + 0.5,
        "end_t": None  # show till end
    })
    overlay_plan.append({
        "text": "@TigerClaw",
        "fontsize": 32,
        "fontcolor": "white",
        "box": 0,
        "x": "(w-text_w)/2",
        "y": "(h-text_h)/2 + 80",
        "start_t": cta_start + 1,
        "end_t": None
    })

    # Step 1: Submit to HeyGen
    video_id = generate_full_production_video(
        scenes=scenes,
        title=title,
        aspect_ratio="16:9",
        background_music_url=music_url,
        background_music_volume=0.2,
        test_mode=test_mode
    )

    if not video_id:
        print("Submission failed.")
        return None

    # Step 2: Poll until complete
    result = poll_video(video_id, timeout=600, interval=15)

    if result.get("status") != "completed":
        print(f"Video did not complete: {result.get('status')}")
        return None

    video_url = result.get("video_url")
    if not video_url:
        print("No video URL in response.")
        return None

    # Step 3: Download raw HeyGen output
    raw_path = os.path.join(output_dir, f"{video_id}_raw.mp4")
    download_video(video_url, raw_path)

    # Step 4: Apply text overlays via FFmpeg
    final_path = os.path.join(output_dir, f"{video_id}_final.mp4")
    if overlay_plan:
        add_text_overlays_ffmpeg(raw_path, final_path, overlay_plan)
    else:
        final_path = raw_path

    print(f"\nFinal video: {final_path}")
    print(f"HeyGen page: https://app.heygen.com/videos/{video_id}")
    return final_path


# =============================================================================
# EXAMPLE: SUBMIT A FULL PRODUCTION VIDEO RIGHT NOW
# =============================================================================

EXAMPLE_SCRIPT_SECTIONS = [
    (
        "The AI revolution is happening faster than most people realize. "
        "While everyone's debating whether AI will take jobs, the smart players are already using it "
        "to build an unfair advantage.",
        ASSETS["broll_multi_look"],
        "The AI Revolution"  # lower third text
    ),
    (
        "Today I'm going to show you the exact three tools I use every single day "
        "to automate content, research, and distribution at scale.",
        ASSETS["broll_podcast"],
        "3 Tools That Changed Everything"
    ),
    (
        "Tool number one: automated video generation. "
        "I use AI to script, produce, and publish YouTube videos without ever touching a camera. "
        "This video you're watching right now? Fully AI-produced.",
        ASSETS["broll_black_hoodie"],
        "Tool #1: AI Video"
    ),
]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="HeyGen Full Production Video Renderer")
    parser.add_argument("--mode", choices=["test", "full", "pipeline", "poll", "list"],
                        default="test", help="Mode to run")
    parser.add_argument("--video-id", help="Video ID to poll")
    parser.add_argument("--music-url", help="Background music URL", default=None)
    parser.add_argument("--output-dir", default="/tmp", help="Output directory for downloaded videos")
    args = parser.parse_args()

    if args.mode == "list":
        # List recent videos
        r = api_get("/v1/video.list?limit=20")
        videos = r.get("data", {}).get("videos", [])
        print(f"Recent videos ({len(videos)}):")
        for v in videos:
            print(f"  {v['video_id']} | {v['status']:12s} | {v.get('video_title','')[:50]}")

    elif args.mode == "poll":
        # Poll a specific video
        if not args.video_id:
            print("--video-id required for poll mode")
            sys.exit(1)
        result = poll_video(args.video_id, timeout=300)
        print(json.dumps(result, indent=2))

    elif args.mode == "test":
        # Submit test render (free, watermarked, 5/day limit)
        print("Submitting test render...")
        vid = render_test_video(test_mode=True)
        if vid:
            print(f"\nTest video submitted: {vid}")
            print(f"View at: https://app.heygen.com/videos/{vid}")
            print(f"Poll with: python3 heygen_full_render.py --mode poll --video-id {vid}")

    elif args.mode == "full":
        # Submit full production video (uses credits, no watermark)
        print("Submitting full production video...")
        vid = render_youtube_video(
            script_sections=[(s[0], s[1]) for s in EXAMPLE_SCRIPT_SECTIONS],
            title="3 AI Tools That Built My Unfair Advantage",
            music_url=args.music_url,
            test_mode=False
        )
        if vid:
            print(f"\nProduction video submitted: {vid}")
            print(f"View at: https://app.heygen.com/videos/{vid}")
            print("\nNote: Poll status then download and run FFmpeg overlays.")
            print(f"Poll: python3 heygen_full_render.py --mode poll --video-id {vid}")

    elif args.mode == "pipeline":
        # Full pipeline: submit -> poll -> download -> FFmpeg overlays
        print("Running full production pipeline...")
        final = full_production_pipeline(
            script_sections=EXAMPLE_SCRIPT_SECTIONS,
            title="3 AI Tools That Built My Unfair Advantage",
            music_url=args.music_url,
            output_dir=args.output_dir,
            test_mode=False  # Set True for watermarked test
        )
        if final:
            print(f"\nPipeline complete: {final}")
        else:
            print("Pipeline failed.")


# =============================================================================
# QUICK REFERENCE: THE FULL PAYLOAD STRUCTURE
# =============================================================================
"""
FULL WORKING PAYLOAD (annotated):

POST https://api.heygen.com/v2/video/generate
Headers: X-Api-Key: YOUR_KEY, Content-Type: application/json

{
  "title": "My YouTube Video",
  "aspect_ratio": "16:9",          # "16:9" | "9:16" | "1:1"
  "test": false,                    # true = free watermarked (5/day), false = production
  "callback_id": "my-webhook-ref",  # optional, for webhooks

  "background_music": {             # OPTIONAL - applies to whole video
    "enable": true,
    "url": "https://cdn.example.com/music.mp3",  # direct audio URL or HeyGen asset URL
    "volume": 0.2                   # 0.0-1.0, 0.2 is good for background
  },

  "video_inputs": [
    // SCENE 1: Avatar speaking over B-roll video
    {
      "character": {
        "type": "avatar",
        "avatar_id": "524caea65d4a45b5aab1c649cde0d472",
        "avatar_style": "normal",    # "normal" | "circle" | "closeUp"
        "scale": 1.0,                # optional float, default 1.0
        "offset": {"x": 0, "y": 0}  # optional float -1 to 1
      },
      "voice": {
        "type": "text",
        "input_text": "Your script here.",
        "voice_id": "50e70458c88d4afb8ec65ec4adee00bb",
        "speed": 1.0,                # 0.5-2.0
        "pitch": 0,                  # -50 to 50
        "emotion": "Excited"         # if voice supports emotions
      },
      "background": {
        "type": "video",
        "url": "https://resource2.heygen.ai/video/ID/original.mp4",
        "play_style": "loop"         # "fit_to_scene" | "freeze" | "loop" | "once"
      }
    },

    // SCENE 2: Avatar over solid color (e.g. dark studio look)
    {
      "character": {
        "type": "avatar",
        "avatar_id": "524caea65d4a45b5aab1c649cde0d472",
        "avatar_style": "normal"
      },
      "voice": {
        "type": "text",
        "input_text": "Second scene script.",
        "voice_id": "50e70458c88d4afb8ec65ec4adee00bb"
      },
      "background": {
        "type": "color",
        "value": "#1a1a2e"
      }
    },

    // SCENE 3: Silent CTA card (avatar visible, no speech)
    // Add text to this scene via FFmpeg post-processing
    {
      "character": {
        "type": "avatar",
        "avatar_id": "524caea65d4a45b5aab1c649cde0d472",
        "avatar_style": "normal"
      },
      "voice": {
        "type": "silence",
        "duration": 4              // seconds
      },
      "background": {
        "type": "color",
        "value": "#0F0F0F"
      }
    }
  ]
}

RESPONSE:
{
  "error": null,
  "data": {
    "video_id": "abc123..."
  }
}

POLL STATUS:
GET https://api.heygen.com/v1/video_status.get?video_id=abc123...
Returns: { "data": { "status": "processing"|"completed"|"failed", "video_url": "...", "duration": 12.5 } }

ADDING TEXT OVERLAYS (FFmpeg):
ffmpeg -i input.mp4 \
  -vf "drawtext=text='SUBSCRIBE':fontsize=52:fontcolor=yellow:x=(w-text_w)/2:y=h-150:box=1:boxcolor=black@0.7:boxborderw=10" \
  -c:a copy output.mp4

ADDING LOWER THIRDS (FFmpeg):
ffmpeg -i input.mp4 \
  -vf "drawtext=text='John Doe - CEO':fontsize=36:fontcolor=white:x=80:y=h-120:box=1:boxcolor=black@0.6:enable='between(t,1,5)'" \
  -c:a copy output.mp4
"""
