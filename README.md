# ZYVORA ULTRA — Termux Lab

A responsive, cyberpunk-styled, copy-first command library for Termux and Linux.

## Features
- Search across command names, descriptions, categories and snippets
- Category filters, sorting and browser-saved favorites
- Copy commands with clipboard fallback
- Quick setup cards and safety notes
- Programming starters: Python, JavaScript/Node.js, TypeScript, Java, C, C++, Go, Rust, PHP, Ruby, Lua, Perl, Bash and SQL/SQLite
- Git/GitHub, SSH/VPS, web development, networking, Android Termux:API, files and utilities
- Responsive desktop/mobile layout, keyboard shortcuts, reduced-motion support
- GitHub Pages deployment with HTML parsing and JavaScript syntax checks

## Run locally
Open `index.html` in a modern browser. Clipboard access may require HTTPS or localhost.

## Deploy
The workflow at `.github/workflows/deploy-pages.yml` validates and deploys the static website on pushes to `main`. In repository Settings → Pages, select **GitHub Actions** as the build and deployment source if it is not already selected.

Expected Pages URL: https://teamzyvorax.github.io/team-zyvorax-termux/

## Safety
This static reference site never executes commands on your device and never asks for passwords, API keys, or tokens. Read commands before running them; package availability may vary by Termux version and repository.
