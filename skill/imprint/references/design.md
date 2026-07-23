# Art direction: печатная культура, деловой тон

The card is a **printed object that happens to live in a browser** — an annual-report spread from a great print house, a catalog page about one founder. Not a SaaS landing, not a dashboard. An investor should want to keep it.

## Why this direction

Every AI-generated page today looks the same: purple gradients, glass cards, rounded-2xl grids, emoji confetti. That sameness is the enemy — a founder's credibility card must say "a specific person, verified numbers". Print culture (books, catalogs, annual reports) carries that specificity: committed palette, typographic hierarchy, asymmetry, restraint. The craft is premium; the copy is business-grade.

## The rules

**Palette — a mixtape of the user's actual materials, bound by one binder.**
The page is a mixtape liner: a committed print «binder» (paper/ink/one accent as base, chosen from the person's rhythm: day-worker → warm paper + near-black ink + vermilion/IKB; night-worker → deep ink ground + bone + one phosphor) — with **track panels whose material is derived from the data**:
- The dominant tool earns its material: Bash-heavy → a terminal panel (dark ground, mono, prompt marks) for the velocity track.
- The flagship product lends its own design language to the section about leverage/venture (e.g. the user's product uses dark glass + cyan → that panel wears it).
- Languages appear in their **official brand colors** (TypeScript blue, JS yellow, HTML orange…) in a labeled spectrum bar — color follows the entity.
- The human sections (rhythm, interpretation, colophon) stay in the print binder.
Cohesion rules: one grid, one type system, same section headers with a small «трек NN · материал: …» label; ≤3 track materials per page beyond the binder; contrast validated per surface (body ≥ 7:1, captions ≥ 4.5:1). Data-derived ≠ chaos: every color must be traceable to a thing the user actually worked with.

**Recency weighting — the last month decides the mix.**
Material shares follow the last ~30 days of sessions, not the whole span. If one project dominates the recent month (>50%), **its design language becomes the page ground** and the other materials become inserts (paper tracks for human time/voice, terminal for velocity). Compute the shares from session-meta before choosing; state them in the liner note («в этом месяце звучит: …»).

**Native narrative — «Сейчас», the month's journal.**
Right after the title, a section tells what the person is building THIS month, natively: 1–2 sentences of prose + a journal of 5–8 verbatim commit subjects from the user's OWN flagship repo (`git log --since="30 days ago"`), styled as a live log (type prefixes colored: feat/fix/docs). Commit subjects are the person's own poetry — don't paraphrase them. NEVER source this journal from client/NDA repos; own repos only.

**Typography — the design IS the typography.**
- Display serif with real Cyrillic: Playfair Display, Spectral, Cormorant Garamond, or Literata. Huge sizes for the archetype title (clamp 3.5–7rem), tight leading, optical margins.
- Text: same serif at reading size, or a quiet humanist sans (IBM Plex Sans).
- Data/numbers: a mono with Cyrillic (JetBrains Mono, IBM Plex Mono) — numbers are typographic specimens: large, tabular, footnoted.
- Google Fonts allowed with system fallbacks (`Georgia, serif` / `ui-monospace`); the page must survive offline.

**Layout — asymmetric, editorial.**
- One column of meaning with wide margins; marginalia in the margins (that's where «Между строк» lives).
- Numbered sections like a catalog (01, 02, 03…), thin rules, generous whitespace.
- Max-width ~1000px; must read beautifully at 375px too (margins collapse, marginalia become inline asides).
- Subtle paper grain or ink texture via CSS (radial-gradient noise, low opacity) is welcome; keep it under 3% visual weight.

**Data as engravings, not widgets.**
- 24h rhythm → inline SVG **radial clock** (hand-drawn feel: thin strokes, small caps labels «полночь/полдень»), bars from `hour_histogram`.
- Projects → a constellation or a catalog list with em-dash annotations, weight = session count.
- Language/tool mix → tiny inline marks (ex-libris style), not pie charts.
- Every chart drawn in the palette's ink; no chart libraries, no gridlines-by-default; label directly on the mark, no legends if avoidable.
- If a dataviz skill is available, consult it for form/accessibility; its neutral palette does NOT apply — this page's palette wins.

**«Прочтение» — visibly different voice.**
The interpretation layer (investor-read) is italic serif with an accent rule, prefixed with a small label «интерпретация · не факты». The reader must never confuse interpretation with evidence.

**Tone — vital, proud, lightly witty.**
This is a визитка the person will show with pride, not a burnout diagnosis. The same fact can read as sacrifice or as strength — always choose strength: «работал без отпуска» → «семьдесят пять дней музыка не останавливалась»; «одиночка» → «команда из одного человека и ста агентов»; «календарь подчинён работе» → «сам решает, когда начинается неделя». Celebrate rhythm, freedom, and craft; never diagnose. Melancholy, grind-vibes, and loneliness framings are blacklisted alongside the visual slop.

**Blacklist (instant fail):**
- Purple/blue gradients on dark, glassmorphism, `border-radius: 16px+` card grids
- Emoji as decoration, progress bars for "skills", star ratings
- Corporate hero sections, CTA buttons (nothing on this page is clickable except the colophon link)
- Theme toggles, cookie-banner aesthetics, drop shadows deeper than a whisper

## Structure contract (sections, in order)

1. **Титул** — the person's NAME as h1 (no poetic archetypes), deck line = positioning: what they build, one confident sentence naming the flagship venture; then «ниже — телеметрия, не резюме» framing and dates span.
1b. **01 · Сейчас** — the native month journal (see Recency/Native narrative above): recent-month share stats + verbatim own-repo commit log.
2. **02 · Скорость** — shipping velocity: sessions/day, commits, pushes, lines, files, projects; prose: reaches prod, not just branches.
3. **02 · Кратность** — the AI-leverage story: human:agent ratio, parallel-session %, tokens produced, verification volume, response cadence. The capital-efficiency message. Voice-specimen marginalia (contentless imperatives) may live here.
4. **03 · Ритм** — radial clock + night %, weekday pattern, marathon stats; prose: sustainable pace, founder controls the calendar.
5. **04 · Портфель** — projects catalog: own flagship named; client/NDA work aggregated namelessly (may note it funds independence); factory/experiments.
6. **05 · Прочтение** — the labeled interpretation layer: what an investor should conclude; hedged, honest.
7. **Колофон** — methodology: «Составлено Claude по N сессиям · период · данные не покидали машину», quiet link to the imprint project.
