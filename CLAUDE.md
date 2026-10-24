# CLAUDE.md

## What this is
Static marketing site for **levy-platform.com** (Levy Platform — custom business platforms), hosted on GitHub Pages from `main` of https://github.com/levy-platform/levy-platform-site. Backup URL: https://matan2502.github.io/levy-platform-site/.

## Structure
- `index.html` — the main site markup: Hebrew, `lang="he" dir="rtl"`, Heebo font. All graphics are inline `<svg>` icons (no base64 images). Styles and behavior are split out (below).
- `css/styles.css` — all styles for the main site (color tokens live in `:root` here). Linked from `index.html`'s `<head>`.
- `js/main.js` — all JS for the main site (scroll-reveal animations + the impact counter), one IIFE. Loaded at the end of `<body>`.
- `learn-api/index.html` — standalone Hebrew/RTL API practice page (live requests to `https://api.frankfurter.dev/v1/latest`), styled to match the main site. Deliberately self-contained (its own inline CSS/JS) as a single teaching file.
- `email-signature.html` — HTML email signature; intentionally keeps CSS inline (mail clients strip external styles). Do not split it.
- `CNAME` — contains `levy-platform.com`; connects the custom domain to GitHub Pages.
- `amirnet/` — Amirnet (English placement test) prep app, live at levy-platform.com/amirnet/. `index.html` is GENERATED — edit `_amirnet_src/page.html` and run `python3 -I _amirnet_src/build.py`. The JSON files are the content (vocab, questions, lessons, past-exam keys, updates).
- `_amirnet_src/` — not served (Jekyll skips `_` folders): `page.html` (single source, also published as the claude.ai artifact https://claude.ai/artifact/FzAoZE5YbUduteKbLLbJj7), `build.py`, `nite_snapshot.json` (facts for the weekly NITE check), `plan.html` (original study plan).
- `_firebase/` — Firebase project `amirnet-levy` config: Firestore rules (each user reads/writes only `users/{uid}/...`), email/password auth. Deploy with `firebase deploy --only firestore --project amirnet-levy` from that folder.
- A weekly scheduled task ("עדכון שבועי לאתר מכינת אמירנט") checks NITE's site, updates `amirnet/updates.json`/`lessons.json`, rebuilds, pushes to main and republishes the artifact.
- `deploy.sh` — publish script (see below).
- `edit.command` / `publish.command` — double-click helpers for the owner; gitignored (local-only) along with `.vscode/`, `dbg*.html`, `*.tmp`.

## Deploy flow
- `deploy.sh [msg]`: `git add -A`, commit (default message "עדכון אתר <timestamp>" if none given), `git push` to `main`. GitHub Pages rebuilds in ~1 minute — pushing IS deploying live.
- `publish.command` just runs `./deploy.sh`; `edit.command` opens the folder in VS Code (local preview via the "Go Live" extension on localhost:5500).

## RTL / Hebrew
All pages are Hebrew RTL. Keep `dir="rtl"` and RTL-aware layout; code/URL snippets in `learn-api` use `.mono` with `direction:ltr`.

## Warnings
- Do NOT touch `CNAME` — breaks the custom domain.
- `deploy.sh` / `publish.command` publish straight to the live site; don't run them unless asked.
- No build step exists — `index.html`, `css/styles.css` and `js/main.js` are served as-is. When editing the main site, put markup in `index.html`, styles in `css/styles.css`, and JS in `js/main.js` (don't reintroduce inline `<style>`/`<script>` blocks).
