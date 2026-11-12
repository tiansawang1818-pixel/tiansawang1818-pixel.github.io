# Tiansawang Suetrong Internship Portfolio

A buildless, responsive portfolio for software engineering internship applications. Public claims come from the supplied resume and verified project documentation.

**Website:** https://tiansawang1818-pixel.github.io/

**Repository:** https://github.com/tiansawang1818-pixel/tiansawang1818-pixel.github.io

## Project structure

```text
.
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
├── assets/
│   └── images/
│       ├── favicon.svg
│       ├── heat-shift-live.jpg
│       ├── portfolio-preview.jpg
│       ├── tiansawang-profile.jpg
│       ├── wasmbot-live-dashboard.jpg
│       └── wasmbot-live-rules.jpg
├── resume.pdf
├── robots.txt
├── sitemap.xml
└── .nojekyll
```

## Local preview

From this directory, run:

```sh
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

## Deploy to GitHub Pages

1. Use the public repository `tiansawang1818-pixel/tiansawang1818-pixel.github.io`.
2. Extract `tiansawang-portfolio-github-pages.zip` and upload its contents to the repository root. Keep `index.html` at the root. Do not upload the ZIP itself or the legacy `sites/` directory.
3. Commit the files to the `main` branch.
4. In the repository, open **Settings → Pages**.
5. Under **Build and deployment**, select **Deploy from a branch**.
6. Select the `main` branch and `/ (root)`, then save.
7. After GitHub finishes publishing, open `https://tiansawang1818-pixel.github.io/`.

## Easy edits

- Search for `EDIT:` in `index.html` and `css/style.css` to find the main replacement points.
- Change the internship role in the hero for each application.
- Add a confirmed LinkedIn URL in the Contact section when available.
- Keep `resume.pdf` current whenever the resume changes. Regenerate it with `python3 tools/make_resume.py resume.pdf` (needs `reportlab`; the PDF must stay one A4 page).

## Project evidence and image sources

- **WasmBot Studio:** `wasmbot-live-dashboard.jpg` and `wasmbot-live-rules.jpg` were captured from the live app at https://wasmbot-studio.vercel.app/ on 11 November 2026 while signed in. The app requires sign-in, so the portfolio also links to the source code and the rule-editor screenshot. The 12 operators, 7 Edge Functions, and contributions are documented in the supplied resume and project source.
- **HEAT//SHIFT:** live public pilot at https://heatshift.hostless.app/. The screenshot `heat-shift-live.jpg` was captured from the live City Explorer on 11 November 2026. Source code is public at https://github.com/tiansawang1818-pixel/HEAT; admin tools require authorised sign-in.
- **Sharing image:** `portfolio-preview.jpg` is a screenshot of this portfolio.

The static website has no analytics, backend, API keys, or contact form. Contact buttons open the visitor's email application.
