---
name: imprint
description: Generate a founder execution profile ("imprint") — a beautifully designed one-page HTML card built from the user's Claude Code usage traces, showing what they build, their shipping velocity, AI-leverage, and work rhythm — and publish it to a PRIVATE GitHub repo (public only after explicit consent). The audience is startup founders presenting themselves to investors and community. Use whenever the user runs /imprint, asks for their card / визитка / профиль фаундера / "who am I based on my data" / "покажи мой профиль по сессиям", wants to showcase their execution or AI-native workflow, or asks to (re)publish, update, or "make my imprint public".
compatibility: Requires python3 and local ~/.claude data. Publishing requires gh CLI (authenticated); without it, the skill still produces the local card.
---

# imprint — a founder execution profile from real traces

You are making a **credibility artifact for a startup founder**. The audience is investors, accelerators, and the startup community. Every founder claims to move fast and be AI-native; this card **proves it with telemetry** — numbers taken from real working sessions, not from a pitch deck. Design quality (print-culture, premium) is part of the credibility. So is honesty: the two-layer evidence/interpretation contract below is the product's differentiator — an investor must see that nothing here is inflated.

## Pipeline

1. **Collect** — run the bundled collector:
   ```bash
   python3 <skill-dir>/scripts/collect_stats.py ~/imprint/stats.json
   ```
   It scans `~/.claude` (session-meta, facets, project transcripts as fallback) and writes one `stats.json`. It never sends anything anywhere. If it errors, fix the environment, not the honesty of the data.

2. **Read the founder, not the data.** Study `stats.json` for the story an investor cares about:
   - **What they build** — the flagship own project (name it; it's the venture).
   - **Velocity** — sessions/day, commits, pushes, lines shipped, "reaches prod" signals.
   - **Leverage** — human-to-agent message ratio, parallel sessions, agent/subagent/workflow usage, own tooling: this founder multiplies themself. Capital efficiency is the message.
   - **Reliability** — rhythm (peak hours, protected nights, weekend pattern), marathon tolerance, response cadence: sustainable pace, not burnout.
   - **Quality discipline** — verification tooling (screenshots/preview), satisfaction/outcome facets, evidence-first habits.

3. **Two layers, never blurred.** The card's honesty contract:
   - **Показатели (Evidence)** — claims backed by numbers in `stats.json`, every one traceable to a field, with footnote-style source notes.
   - **Прочтение (Interpretation)** — the investor-read: what the numbers say about this founder. Visually distinct, explicitly labeled («интерпретация · не факты»), hedged honestly. Never state an interpretation as fact; never invent specifics about personal life — patterns only.

4. **Privacy pass (hard rules).** Before writing a single line of HTML:
   - No secrets, keys, tokens, emails, phone numbers, client names, or third-party personal data — even if they appear in prompts.
   - **Name only projects the user owns.** Client, employer, and NDA work appears strictly anonymized and aggregated («заказные проекты — N сессий»), with no names, domains, product specifics, or recognizable details. When ownership is unclear, treat it as NDA. A client must be unable to recognize their project on the card.
   - Quote prompts only as short fragments with zero work content (generic imperatives, voice specimens). When in doubt, paraphrase or drop.
   - Raw data (`stats.json`, transcripts) is NEVER committed or published. Only the finished card.

5. **Titling is professional.** The h1 is the **person's name** (from `git config user.name` or ask); the deck line is their positioning: what they build, in one confident sentence. No poetic archetypes in the title — the poetry lives quietly in the craft, not the copy.

6. **Design.** Read `references/design.md` — the binding art direction (print culture as premium differentiator, business-grade tone). If dedicated design skills are available (e.g. dataviz for charts), consult them for craft; the manifesto wins on style conflicts. Write the card to `~/imprint/index.html` in the user's dominant prompt language. Open it for the user.

7. **Publish (private-first).** Read `references/publish.md` and follow it exactly: private GitHub repo `imprint` immediately; public flip + Pages **only after an explicit yes in chat**.

8. **Offer the loop.** Show the card, ask what to fix. Done when the founder says "показал бы инвестору".

## Quality bar (check before showing)

- Reads as a **credibility artifact**: name + venture up top, velocity/leverage/reliability provable below.
- Every Evidence claim has a number behind it; every Interpretation is visibly labeled as such.
- The rhythm visualization (24h radial clock) is drawn from `hour_histogram`, not decorative.
- Tone: confident, concrete, zero буллшита — no "visionary", no superlatives without numbers; and vital, never grind-glorifying or melancholic.
- Works offline as a single file; survives missing web fonts.
- Footer colophon: methodology + «сделано скиллом imprint — сделай свой» linking the project repo. Quiet, tasteful.
- No AI-slop visuals (manifesto blacklist) and no client-recognizable details (privacy pass).
