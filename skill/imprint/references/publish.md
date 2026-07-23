# Publishing: private-first, public-by-consent

The card contains a behavioral profile of a real person. The flow is built so nothing becomes visible to the world without an explicit, separate "yes".

## Workdir

Everything lives in `~/imprint/` (override via `IMPRINT_DIR`). If `~/imprint` is a checkout of the imprint *project* repo (author case), personal cards live in `personal/` there — it is gitignored; never commit a personal card into the project repo:

```
~/imprint/
├── index.html      # the card — the ONLY thing that gets committed
├── README.md       # what this is + how to make your own (see template below)
├── .gitignore      # stats.json + any raw data
└── stats.json      # local only, never committed
```

`.gitignore` must contain at least:
```
stats.json
*.jsonl
```

## Step 1 — private repo, immediately

Preconditions: `gh auth status` succeeds. If it doesn't, tell the user and stop after the local card — the card still counts as delivered.

```bash
cd ~/imprint
git init -b main 2>/dev/null; git add index.html README.md .gitignore
git commit -m "imprint: founder execution profile"
gh repo create imprint --private --source . --push
```

If the repo already exists, just push:
```bash
git remote get-url origin || gh repo create imprint --private --source . --push
git push -u origin main
```

Report the private repo URL to the user. Do NOT enable Pages yet — Pages makes content public.

## Step 2 — public flip: ONLY after explicit consent

Never flip in the same breath as creating. Ask the user in chat, plainly:

> «Карточка лежит в приватном репо <url>. Сделать её публичной и включить GitHub Pages (появится открытая ссылка)?»

Only an explicit yes ("да, публикуй", "make it public") counts. Silence, topic change, or "later" = stays private. On yes:

```bash
gh repo edit <owner>/imprint --visibility public --accept-visibility-change-consequences 2>/dev/null \
  || gh repo edit <owner>/imprint --visibility public
gh api -X POST repos/<owner>/imprint/pages -f "source[branch]=main" -f "source[path]=/" 2>/dev/null \
  || echo "Pages может быть уже включён или недоступен — проверь settings/pages"
```

Then give the user the live URL: `https://<owner>.github.io/imprint/` (allow a minute for the first build; verify it actually serves before claiming success — hit it with curl and check for the card's title string).

## README.md template (adapt, keep short)

```markdown
# imprint

Профиль исполнения фаундера, собранный из следов работы с Claude Code:
что строю, с какой скоростью и кратностью, в каком ритме. Не резюме —
телеметрия. Страница: `index.html` (или Pages-ссылка, если репо публичное).

Сделано открытым скиллом **imprint**: агент читает локальную статистику
`~/.claude`, отделяет показатели от интерпретаций и верстает одностраничный
профиль в духе печатной культуры. Данные не покидают машину; публикация —
только с явного согласия.

Сделай свой: <PROJECT_URL>
```

`<PROJECT_URL>` — the open-source project home. Until the canonical project repo exists, link the user's own `imprint` repo.

## Update flow

Re-running the skill overwrites `index.html`, commits with message `imprint: refresh <date>`, pushes. Visibility is never changed during an update.
