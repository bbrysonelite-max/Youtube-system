# WORKFLOW.md
# Brent Bryson — AI for the Rest of Us
# Full 12-Layer Programmatic Production System
# Version: 1.0

---

## RULE ZERO
Read SOUL_DOCUMENT.md and CHANNEL_IDENTITY.md before executing any layer.
Every output must pass one test: Does this sound like Brent Bryson?
If no — rewrite it.

---

## SYSTEM OVERVIEW

One long-form video per week.
Daily Shorts auto-cut from that video.
Cross-platform posts 48 hours after YouTube.
Two human touchpoints per video: topic approval and script approval.
Everything else runs without Brent.

---

## TOOL STACK (Current — Phase 1)

| Function | Tool | Status |
|---|---|---|
| Research | Claude + web search | Active |
| Keyword research | VidIQ | Phase 2 — add after first 10 videos |
| Script generation | Claude API | Active |
| Voice rendering | ElevenLabs Professional Clone | Active |
| Avatar video | HeyGen Pro | Active |
| Captions | CapCut | Add — free |
| Thumbnail image gen | Higgsfield AI + Fal.ai | Active |
| Thumbnail layout | Ideogram | Evaluate — Phase 2 |
| Scheduling + cross-post | Buffer | Add — $6/month, replaces Biotoate |
| Approval notifications | Gmail | Active |
| Version control | GitHub (bbrysonelite-max/Youtube-system) | Active |

---

## THE 12 LAYERS

---

### LAYER 1 — Channel Identity System
STATUS: COMPLETE
FILES: identity/SOUL_DOCUMENT.md, identity/CHANNEL_IDENTITY.md,
       identity/AVATAR_SPECS.md, identity/VOICE_FORMATTING_RULES.md

This layer is the foundation. It does not repeat.
All downstream layers inherit from these four files.
When anything changes about the brand, audience, or voice — update here first.

---

### LAYER 2 — Trend & Research Intelligence
CADENCE: Every Monday morning
OUTPUT: research/topics_YYYY-MM-DD.json
HUMAN REQUIRED: No
TRIGGER: Manual run or future cron job

#### What It Does
Generates a ranked list of 10 candidate video topics for the week.
Each topic includes: search rationale, audience layer match, pillar assignment,
and a one-sentence hook angle.

#### How to Run It (Phase 1 — Manual)
Open Claude. Paste this prompt:

---
RESEARCH AGENT PROMPT (also saved in agents/research_agent_prompt.md):

You are the research agent for the YouTube channel "Brent Bryson — AI for the Rest of Us."

Read these files before doing anything:
- SOUL_DOCUMENT.md [paste contents]
- CHANNEL_IDENTITY.md [paste contents]

Today's date: [DATE]

Your job: Generate 10 candidate video topics for this week.

For each topic provide:
1. Topic title (as a working YouTube title)
2. Which audience layer it targets (Layer 1, 2, or 3)
3. Which content pillar (Pillar 1, 2, or 3)
4. Why this topic is timely RIGHT NOW
5. One-sentence hook angle in Brent's voice
6. Estimated search demand: Low / Medium / High

Rank them 1–10 by estimated value to the channel.
Output as clean JSON.

Rules:
- Topics must be actionable and specific. Not "AI for network marketing." More like
  "How I use a Claude agent to follow up with 200 prospects while I sleep."
- Every topic must teach ONE thing.
- At least 3 topics must connect to Brent's personal story or lived experience.
- At least 2 topics must target Layer 3 (The Late-Innings Rebuilder).
---

#### Phase 2 Upgrade
Add VidIQ API to pull actual YouTube search volume data.
Add Google Trends API for real-time topic validation.
This upgrades the output from estimated to data-confirmed.

---

### LAYER 3 — Subject Selection & Approval Gate
CADENCE: Every Monday — after Layer 2 runs
OUTPUT: Confirmed topic for the week
HUMAN REQUIRED: YES — Brent picks one topic
TIME REQUIRED: Under 5 minutes

#### How It Works
Layer 2 produces the ranked topic list.
A summary email is sent to Gmail with the top 5 topics.
Brent replies with a number (1–5).
That topic locks. Layer 4 begins.

#### Approval Email Format
Subject: [Youtube-system] Topic picks for week of [DATE] — pick one

Body:
This week's top 5 candidates. Reply with a number.

1. [Topic title] — [One-sentence hook] — Pillar [X] — Layer [X]
2. [Topic title] — [One-sentence hook] — Pillar [X] — Layer [X]
3. [Topic title] — [One-sentence hook] — Pillar [X] — Layer [X]
4. [Topic title] — [One-sentence hook] — Pillar [X] — Layer [X]
5. [Topic title] — [One-sentence hook] — Pillar [X] — Layer [X]

Reply with 1, 2, 3, 4, or 5.

#### Phase 1 — Manual
Brent reads the JSON output from Layer 2 and picks the topic.
No automation required yet.

#### Phase 2 — Automated
n8n or Zapier workflow sends the digest email automatically.
Brent's reply triggers Layer 4 via webhook.

---

### LAYER 4 — Deep Research & Learning Synthesis
CADENCE: Monday or Tuesday — after topic is locked
OUTPUT: research/research_[topic-slug].md
HUMAN REQUIRED: No — but Brent READS the output
TIME REQUIRED: 15 minutes of Brent's reading time

#### What It Does
Produces a 3–5 page research brief on the chosen topic.
Written in plain English, as if briefing a busy CEO who needs to teach this
in 10 minutes. This is where Brent learns something. Non-negotiable.

#### Research Agent Prompt (also in agents/research_agent_prompt.md)
---
You are the research agent for "Brent Bryson — AI for the Rest of Us."

Topic: [TOPIC]
Target audience: [LAYER] — see CHANNEL_IDENTITY.md
Content pillar: [PILLAR]

Your job: Produce a research brief with these sections:

## What This Topic Actually Is
Plain English. No jargon. 150 words max.

## Why It Matters Right Now
3 specific reasons this is timely. Include stats or examples where possible.

## What Most People Get Wrong
The counterintuitive angle. This becomes the hook.

## The Three Key Points
Each point: one claim, one concrete example, one takeaway sentence.
These become the three sections of the video script.

## Brent's Angle
How does this connect to Brent's lived experience?
Reference SOUL_DOCUMENT.md. Be specific — not generic.

## Brent's Takeaway (first person)
3 bullets. What Brent thinks about this topic in his own voice.
Start each bullet with "I" and write as if Brent is speaking.

## Sources
List any URLs or data points used. Real sources only.

Rules:
- Write for Grade 8 reading level or below.
- No walls of text. Break every 2–3 sentences.
- Every section must be usable as raw material for the script agent.
---

#### Output File Format
Saved as: research/research_[topic-slug]_[YYYY-MM-DD].md
Committed to GitHub before Layer 5 begins.

---

### LAYER 5 — Script Generation
CADENCE: Tuesday
OUTPUT: scripts/script_v1_[topic-slug].md
HUMAN REQUIRED: No
DEPENDS ON: research/research_[topic-slug].md + SOUL_DOCUMENT.md + VOICE_FORMATTING_RULES.md

#### Script Agent Prompt (also in agents/script_agent_prompt.md)
---
You are the script agent for "Brent Bryson — AI for the Rest of Us."

Read these before writing a single word:
- SOUL_DOCUMENT.md [paste]
- VOICE_FORMATTING_RULES.md [paste]
- research/research_[topic-slug].md [paste]

Your job: Write a complete YouTube video script in Brent Bryson's voice.

Target length: 8–10 minutes spoken (approximately 1,200–1,500 words)
Avatar: [Black Hoodie / Sport Shirt / Suit — based on pillar]
Audience layer: [1 / 2 / 3]

Script structure — follow exactly:

[HOOK — 0-15 sec]
Pattern interrupt. Bold claim, question, or stat.
Maximum 2 sentences. This must stop a scroll.

[PROMISE — 15-30 sec]
What they will know or be able to do by the end.
Specific. Concrete. No vague promises.

[CREDIBILITY — 30-45 sec]
Why Brent is the one teaching this.
Story-based. One specific moment from his life. Not a resume.

[POINT 1 — ~2 min]
Claim. Story or example. Takeaway.
End with a rhetorical question that sets up Point 2.

[POINT 2 — ~2 min]
Claim. Story or example. Takeaway.
End with a rhetorical question that sets up Point 3.

[POINT 3 — ~2 min]
Claim. Story or example. Takeaway.
This point should be the most actionable. Give them something they can do today.

[CTA — 60 sec]
Based on video number in sequence — see CHANNEL_IDENTITY.md CTA Sequence.
Direct. One action only. No hedging.

Formatting rules — non-negotiable:
- Sentences max 20 words. Flag any that exceed this.
- Use ellipses for pause: "Here's what nobody tells you..."
- Use em dashes for rhythm: "This changes everything — and I mean everything."
- Rhetorical questions every 90 seconds minimum.
- Use [pause] tag between major sections.
- Flesch-Kincaid Grade 8 or below.
- At least one signature phrase from SOUL_DOCUMENT.md per script.
- Do NOT use: corporate language, filler phrases, passive voice.

End the script with:
SCRIPT STATS:
- Word count: [X]
- Estimated spoken duration: [X min]
- Signature phrases used: [list them]
- Sentences over 20 words: [list them for revision]
- Flesch-Kincaid score: [X]
---

---

### LAYER 6 — Script Editing & Brent Approval Gate
CADENCE: Tuesday or Wednesday
OUTPUT: scripts/script_v2_[topic-slug].md
HUMAN REQUIRED: YES — Brent reads and approves
TIME REQUIRED: 15–20 minutes

#### Two-Pass Process

Pass 1 — AI Self-Edit (automatic before Brent sees it):
Claude reviews script_v1 and flags:
- Any sentence over 20 words
- Any corporate language or filler
- Any section where Brent's voice drops and it sounds generic
- Pacing issues (two long sections back to back with no short punchy line)
Output: script_v1 with inline flags as [FLAG: reason]

Pass 2 — Brent Review:
Brent reads script_v2 aloud once. Under 20 minutes.
If a line doesn't sound like him — he edits it.
If it reads clean — he replies "approved" to the Gmail notification.
Approved script is saved as script_v2_[topic-slug].md and committed to GitHub.

#### Approval Email Format
Subject: [Youtube-system] Script ready for review — [Topic title]

Body:
Script v1 is ready. Estimated read time: [X] min.
Flagged items: [X sentences over 20 words, X voice issues]

[Script pasted in full]

Reply "approved" to move to production.
Reply with edits inline if changes needed.

---

### LAYER 7 — Avatar Video Production (HeyGen)
CADENCE: Wednesday
OUTPUT: [topic-slug]_raw.mp4
HUMAN REQUIRED: Minimal — paste script, download output
TIME REQUIRED: 20–30 minutes active, 10–20 minutes render time

#### Step-by-Step Process

1. Open HeyGen Pro
2. Select avatar based on AVATAR_SPECS.md pillar assignment
3. Paste approved script from script_v2_[topic-slug].md
4. Set voice to ElevenLabs Professional Clone (Brent Bryson)
5. Set voice speed to 0.95
6. Set emotion to Expressive
7. If script exceeds 8 minutes: split into 2–3 minute segments, render separately
8. Preview first 60 seconds before full render
9. Download completed .mp4

#### Scene Segmentation Rule
Scripts over 8 minutes = render in segments.
Segment 1: Hook + Promise + Credibility + Point 1
Segment 2: Point 2 + Point 3
Segment 3: CTA + outro
Stitch in CapCut during Layer 8.

#### Output File Naming
[topic-slug]_seg1_raw.mp4
[topic-slug]_seg2_raw.mp4
[topic-slug]_seg3_raw.mp4 (if needed)

---

### LAYER 8 — Captions, B-Roll & Post-Production
CADENCE: Wednesday or Thursday
OUTPUT: [topic-slug]_final.mp4 + [topic-slug]_short_1.mp4 (and _2, _3 as applicable)
TOOL: CapCut (free)
HUMAN REQUIRED: Yes — light editing pass
TIME REQUIRED: 30–45 minutes

#### Steps

1. Import raw HeyGen segments into CapCut
2. Stitch segments if multi-part render
3. Apply auto-captions — review for accuracy, correct any errors
4. Apply "Studio Sound" filter to clean HeyGen audio artifacts
5. Add branded lower-third (name + channel handle)
6. Add outro card (final 10 seconds — subscribe prompt)
7. Export long-form: 1080p, .mp4

#### Shorts Extraction (same session)
From the long-form timeline, identify 3 moments:
- The hook (0–60 sec) — always becomes Short 1
- The most counterintuitive claim in the script — Short 2
- The most actionable tip — Short 3

Export each as vertical (9:16), 45–60 seconds.
File names: [topic-slug]_short_1.mp4, _short_2.mp4, _short_3.mp4

#### Caption Rules
- Captions are mandatory — 80% of YouTube is watched without sound at some point
- Font: Bold, high contrast, large enough to read on mobile without squinting
- Never leave auto-captions unchecked — review every video before export

---

### LAYER 9 — Thumbnail Production
CADENCE: Thursday
OUTPUT: production/thumbnail_[topic-slug]_v1.png (and _v2, _v3)
TOOLS: Higgsfield AI + Fal.ai for image generation
HUMAN REQUIRED: Brent picks one of three options
TIME REQUIRED: 20–30 minutes

#### Thumbnail Formula (Top 10% Standard)
- One dominant image (Brent's avatar screenshot or AI-generated visual)
- 3–5 words max in large bold high-contrast text
- One visual element creating curiosity or mild controversy
- Consistent color palette from CHANNEL_IDENTITY.md

#### Thumbnail Agent Prompt (also in agents/metadata_agent_prompt.md)
---
You are the thumbnail copy agent for "Brent Bryson — AI for the Rest of Us."

Topic: [TOPIC]
Script hook: [PASTE HOOK SECTION]
Audience layer: [LAYER]

Generate 3 thumbnail text options.

For each option provide:
- The 3–5 word text (this goes on the image in large bold type)
- The visual concept (what should be in the image behind the text)
- Why this will get clicked (one sentence)

Rules:
- Use the formula: [Specific Result] + [Timeframe or Method] + [Curiosity Gap]
- No clickbait that the video cannot deliver on
- No more than 5 words on the thumbnail — fewer is better
- Must work as a thumbnail even if you cover the text
- Think: would a 45-year-old woman scrolling YouTube at 10pm stop for this?
---

#### Image Generation
Use Higgsfield AI or Fal.ai to generate the background visual.
Prompt should describe: scene, lighting, mood, color palette.
Overlay text in post (CapCut or any basic image editor).

Produce 3 complete thumbnail variants.
Save as: thumbnail_[topic-slug]_v1.png, _v2.png, _v3.png
Commit to production/ folder in GitHub.
Brent picks one — note the winner in analytics_log.md for future reference.

---

### LAYER 10 — Metadata & SEO Package
CADENCE: Thursday (same session as thumbnail)
OUTPUT: production/metadata_[topic-slug].md
HUMAN REQUIRED: Brent picks final title from 3 options
TIME REQUIRED: 10 minutes

#### Metadata Agent Prompt
---
You are the SEO metadata agent for "Brent Bryson — AI for the Rest of Us."

Topic: [TOPIC]
Script: [PASTE FULL SCRIPT]
Audience layer: [LAYER]
Pillar: [PILLAR]

Generate the complete YouTube metadata package:

## Title Options (3)
Use formula: [Specific Result] + [Timeframe or Method] + [Curiosity Gap]
Each title under 60 characters. Include primary keyword near the front.

## Description
250 words. Primary keyword in first 2 sentences.
Paragraph 1: What the video teaches (2–3 sentences)
Paragraph 2: Who this is for (reference the audience layer without jargon)
Paragraph 3: About Brent (2 sentences — pattern recognizer, rebuilding in real time)
Paragraph 4: CTA with link placeholder [LINK]
Timestamps: [auto-generate from script structure]

## Tags (15)
Mix of broad and specific. Include channel name as one tag.

## Chapters
Based on script structure. Format: 0:00 Hook, 0:45 [Point 1 title], etc.

## End Screen Placement Note
Flag the 60-second mark before the end for end screen card placement.
---

---

### LAYER 11 — Multi-Platform Publishing
CADENCE: Friday (long-form) + rolling daily (Shorts)
TOOL: Buffer ($6/month — replaces current tool)
HUMAN REQUIRED: Minimal — queue review
TIME REQUIRED: 20 minutes to schedule the week

#### Buffer Setup (One-Time)
Connect these accounts to Buffer:
- YouTube (primary)
- Instagram
- TikTok
- LinkedIn
- Facebook (if active)
- X / Twitter

#### Publishing Sequence — Non-Negotiable
DO NOT post everywhere simultaneously.
YouTube is the primary platform. Algorithm integrity depends on this order.

Day 1 (Friday): YouTube long-form goes live
Day 1 (Friday): YouTube Short 1 goes live (same day is fine for Shorts)
Day 2 (Saturday): Short 2 on YouTube + all platforms get Short 1
Day 3 (Sunday): Short 3 on YouTube
Day 3 (Sunday): Long-form cross-posts to LinkedIn and Facebook
Day 4 (Monday): Long-form cross-posts to Instagram Reels and TikTok
Daily: Remaining Shorts roll out across all platforms via Buffer queue

#### X / Twitter — Text Thread
Claude generates a 5-tweet thread from the script's three key points.
Post same day as YouTube. Link to full video in tweet 1.

#### Buffer Queue Structure
Each week load into Buffer:
- 1 long-form video (YouTube only, Friday)
- 3 Shorts (YouTube + all platforms, staggered)
- 1 LinkedIn post (long-form video + 2-paragraph text summary)
- 1 Facebook post (same as LinkedIn)
- 1 Twitter/X thread (5 tweets)
Total: 7 scheduled items per week, loaded in one 20-minute session.

---

### LAYER 12 — Analytics Feedback Loop
CADENCE: Every Monday morning (before Layer 2 runs)
OUTPUT: analytics/analytics_log.md (updated weekly)
HUMAN REQUIRED: Brent reads the brief — 10 minutes

#### What Gets Tracked Per Video

| Metric | Why It Matters |
|---|---|
| Click-through rate (CTR) | Thumbnail + title effectiveness |
| Average view duration | Script and pacing quality |
| Views in first 48 hours | Algorithm push signal |
| Subscriber conversion rate | Trust and CTA effectiveness |
| Top traffic source | Where the audience is finding us |
| Winning thumbnail variant | Informs future thumbnail direction |

#### Analytics Brief Format (generated by Claude weekly)
---
ANALYTICS BRIEF — Week of [DATE]

Video published: [Title]
Views: [X] | CTR: [X%] | Avg duration: [X min] | New subscribers: [X]

What worked:
[2–3 bullets — specific observations]

What to adjust:
[1–2 bullets — specific recommendations]

Thumbnail winner: v[X] — [why it likely won]

Topic recommendation shift:
Based on last 4 weeks of data, [Pillar X] is outperforming [Pillar Y] by [X]%.
Suggested ratio adjustment: [X]% Pillar 1, [X]% Pillar 2, [X]% Pillar 3.
---

#### The Learning Loop
Analytics brief is committed to GitHub weekly.
Script agent reads last 4 weeks of analytics before generating new scripts.
The system gets smarter every single week without additional effort from Brent.

---

## WEEKLY PRODUCTION SCHEDULE

| Day | Layer | Time Required | Human? |
|---|---|---|---|
| Monday AM | Layer 12 — Read analytics brief | 10 min | YES — read |
| Monday AM | Layer 2 — Run research agent | 20 min | NO |
| Monday AM | Layer 3 — Pick topic | 5 min | YES — pick |
| Monday PM | Layer 4 — Research brief generated | 30 min | NO |
| Monday PM | Layer 4 — Brent reads brief | 15 min | YES — read |
| Tuesday | Layer 5 — Script generated | 20 min | NO |
| Tuesday | Layer 6 — Script review + approval | 20 min | YES — approve |
| Wednesday | Layer 7 — HeyGen render | 30 min active | YES — paste + download |
| Wednesday | Layer 8 — CapCut captions + Shorts | 45 min | YES — light edit |
| Thursday | Layer 9 — Thumbnail production | 30 min | YES — pick one |
| Thursday | Layer 10 — Metadata package | 10 min | YES — pick title |
| Friday AM | Layer 11 — Buffer queue loaded | 20 min | YES — review + schedule |
| Friday | VIDEO GOES LIVE | — | — |

TOTAL BRENT TIME PER VIDEO: Approximately 2.5–3 hours
TOTAL ELAPSED DAYS: Monday to Friday

---

## PHASE 2 UPGRADES (after first 10 videos)

1. Add VidIQ API to Layer 2 for real search volume data
2. Add n8n automation to send approval gate emails automatically
3. Add Canva API for programmatic thumbnail generation from locked template
4. Add YouTube Data API for automatic video upload (removes manual step from Layer 11)
5. A/B thumbnail testing via TubeBuddy once channel reaches 1,000 subscribers
6. Build Tiger Claw agent to handle admin layers automatically

---

## FILE NAMING CONVENTIONS

Research: research/research_[topic-slug]_[YYYY-MM-DD].md
Script v1: scripts/script_v1_[topic-slug].md
Script v2: scripts/script_v2_[topic-slug].md
Thumbnail: production/thumbnail_[topic-slug]_v[1/2/3].png
Metadata: production/metadata_[topic-slug].md
Raw video: [topic-slug]_raw.mp4 (local only — not committed to GitHub)
Final video: [topic-slug]_final.mp4 (local only — not committed to GitHub)
Shorts: [topic-slug]_short_[1/2/3].mp4 (local only)

---

## CROSS-REFERENCE FILES
- identity/SOUL_DOCUMENT.md
- identity/CHANNEL_IDENTITY.md
- identity/AVATAR_SPECS.md
- identity/VOICE_FORMATTING_RULES.md
- agents/research_agent_prompt.md
- agents/script_agent_prompt.md
- agents/metadata_agent_prompt.md
- analytics/analytics_log.md

