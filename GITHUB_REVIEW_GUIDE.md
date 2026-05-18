# GitHub Review Cheat Sheet
**Brent's YouTube Production Workspace**
Repo: github.com/bbrysonelite-max/Youtube-system

---

## 1. HOW TO REVIEW A SCRIPT

1. Go to github.com/bbrysonelite-max/Youtube-system
2. Click the **scripts/** folder
3. Click any file that starts with `script_v1_` — it ends in `.md`
4. GitHub shows it as a clean, readable page. Just read it like a doc.

**To make edits:**
- Click the **pencil icon** in the top-right corner of the file
- Change whatever you want directly in the box
- When done, scroll down to the "Commit changes" section
- Type a short message like: `approved with edits`
- Click **Commit changes** (green button)
- Done. Your version is saved.

**To approve it as-is (no edits needed):**
- Go back to the **scripts/** folder
- Click **Add file** > **Create new file** (top right)
- Name the file: `APPROVED_[slug].txt`
  - Example: `APPROVED_stoic-morning-routine.txt`
- In the file body, type just the word: `approved`
- Scroll down, click **Commit new file**
- Done. That's your approval signal.

---

## 2. HOW TO REVIEW METADATA (Titles, Descriptions, Tags)

1. Click the **production/** folder
2. Open the metadata file for your video
3. You'll see 3 title options. Pick the one you want.
4. Click the **pencil icon** to edit
5. Delete the 2 titles you don't want. Keep only one.
6. Scroll down, type a commit message like: `chose title 2`
7. Click **Commit changes**

Same process for descriptions or tags — just edit and save.

---

## 3. HOW TO PICK TOPICS

1. Click the **research/** folder
2. Open a file named `topics_YYYY-MM-DD.json` (the date is in the filename)
3. GitHub shows it with color-coded formatting so it's easy to read
4. Find the topic you want

**To mark it chosen:**
- Click the **pencil icon**
- Find the topic entry you like
- Add this line inside that topic's block: `"selected": true`
- Commit with a message like: `picked topic: stoic habits`

> Note: In the future, you'll just reply to an email to pick topics. For now, edit the file directly.

---

## 4. HOW TO TRIGGER THE NEXT STEP

Right now this is manual. After you approve a script, do this:

**Send one message to Hermes:**

```
Script approved: [slug]. Go.
```

Example:
```
Script approved: stoic-morning-routine. Go.
```

That's it. Hermes takes it from there — formatting, metadata, scheduling, everything.

---

## 5. FOLDER MAP — What Lives Where

| Folder | What's in it | Touch it? |
|---|---|---|
| `identity/` | Your brand: voice, style, audience | Only if rebranding |
| `scripts/` | All video scripts | Yes — read and approve here |
| `research/` | Topic lists and research briefs | Yes — pick topics here |
| `production/` | Titles, descriptions, thumbnails, final files | Yes — approve metadata here |
| `analytics/` | Weekly performance logs | Read-only, for reference |
| `agents/` | AI prompt templates | Leave alone |

---

## 6. USING GITHUB ON YOUR PHONE

You don't need a computer. GitHub has a mobile app.

1. Download **GitHub** from the App Store or Google Play
2. Log in as `bbrysonelite-max`
3. Go to your repo: `Youtube-system`
4. Everything works the same — browse files, tap the pencil to edit, commit changes

Review and approve videos from anywhere. Takes 5 minutes.

---

## QUICK REFERENCE

| Task | Where to go |
|---|---|
| Read a script | scripts/ → open any script_v1_*.md |
| Approve a script (no edits) | scripts/ → Add file → APPROVED_[slug].txt |
| Approve a script (with edits) | scripts/ → pencil icon → edit → commit |
| Pick a title | production/ → open metadata file → pencil → delete 2, keep 1 |
| Pick a topic | research/ → open topics JSON → add "selected": true |
| Trigger next step | Message Hermes: "Script approved: [slug]. Go." |

---

*Questions? Message Hermes. It knows the whole system.*
