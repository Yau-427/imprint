# imprint

**Not a résumé — telemetry.** A one-page founder execution profile generated from your own Claude Code traces: what you build, how fast you ship, how much an agent system multiplies you, and the rhythm you live in.

Every founder claims to move fast and be AI-native. `imprint` proves it with numbers taken from real working sessions — and separates evidence from interpretation, so nothing reads as inflated.

## What it makes

One beautifully designed HTML page (print-culture aesthetic, zero AI-slop) with:

- **Now** — a native journal of your last 30 days: real commit subjects from your own flagship repo, styled as a live `git log`
- **Velocity** — sessions/day, commits, pushes, lines shipped; a language spectrum in official brand colors
- **Leverage** — human-to-agent message ratio, parallel-session share, total agent output: the capital-efficiency story
- **Rhythm** — a 24-hour radial clock of when you actually work, weekday pattern, marathon stats
- **Portfolio** — your own projects by name; client/NDA work strictly anonymized
- **Reading** — the investor-read, visibly labeled «interpretation, not facts»

The design is a **mixtape of your actual materials**: the project that dominated your last month lends the page its ground (its own design language), your top tool earns its panel (terminal for Bash-heavy profiles), languages appear in their brand colors. Someone else's imprint will look like *their* month, not yours.

## Privacy by design

- **Local only.** The collector reads `~/.claude` on your machine and writes one local `stats.json`. Nothing is sent anywhere.
- **Own projects only.** Client, employer, and NDA work is aggregated namelessly («client projects — N sessions»). A client must be unable to recognize their project on your card. Unclear ownership = treated as NDA.
- **No secrets.** Keys, emails, third-party names, and work content from prompts never reach the page. Prompt quotes are limited to contentless voice specimens.
- **Private-first publishing.** The card goes to a *private* GitHub repo. Making it public happens only after your explicit yes. Raw data is never committed.

## Install

Requires [Claude Code](https://claude.com/claude-code), `python3`, and (optionally, for publishing) the `gh` CLI.

```bash
git clone https://github.com/Yau-427/imprint
cp -r imprint/skill/imprint ~/.claude/skills/
```

## Use

In any Claude Code session:

```
/imprint
```

The agent collects your local stats, drafts the profile, shows it to you, and iterates until you'd show it to an investor. Cards render in your dominant prompt language.

## Share it

If you choose to publish (your call, always), open a PR adding your page at `claude-code-profiles/p/<your-github-login>/index.html` — see the [PR guide](claude-code-profiles/p/README.md). After merge your profile goes live at **[iris.direct/claude-code-profiles](https://iris.direct/claude-code-profiles)**, the community gallery of Claude Code founders.

## How it works

```
~/.claude (session-meta · facets · transcripts)
        │  collect_stats.py — local, zero deps
        ▼
   stats.json ──► the agent reads the founder, not the data
        │         evidence layer ◁─▷ interpretation layer (labeled)
        ▼
   index.html — mixtape design derived from YOUR materials
        │
        ▼ private repo → (explicit consent) → public + Pages → gallery
```

The skill lives in [`skill/imprint/`](skill/imprint/): `SKILL.md` is the pipeline, `references/design.md` is the binding art direction, `references/publish.md` is the consent-gated publishing flow, `scripts/collect_stats.py` is the collector.

## License

[MIT](LICENSE) © 2026 Max Munchak
