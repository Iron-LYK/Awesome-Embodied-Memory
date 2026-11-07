# Publish the repository and website

[简体中文](deployment.zh-CN.md)

- Repository: [Iron-LYK/Awesome-Embodied-Memory](https://github.com/Iron-LYK/Awesome-Embodied-Memory)
- Website after the first successful deployment: [iron-lyk.github.io/Awesome-Embodied-Memory/](https://iron-lyk.github.io/Awesome-Embodied-Memory/)

These URLs are configured in `data/project.json`. Preparing these files does not upload them or deploy the website.

## What to upload

Upload the **complete contents of the clean `Awesome-Embodied-Memory` folder** to the repository root. README alone is insufficient: its map, link badges and documentation are separate files. The data and build scripts keep the catalogue and its website consistent.

| Path | Purpose |
|:---|:---|
| `README.md`, `assets/` | English paper index, taxonomy figure and local link badges |
| `data/`, `references.bib`, `implementation-references.bib` | Canonical records, taxonomy, evidence metadata and citations |
| `scripts/` | Validation, deterministic catalogue/map generation and clean exports |
| `docs/`, `CONTRIBUTING*` | Classification, evidence policy, provenance and maintenance guides |
| `LICENSE*`, `NOTICE.md` | Content CC BY 4.0 and website/build code MIT |
| `website/` | Complete bilingual static site, including local assets and resources |
| `.github/`, `.gitignore` | Quality checks, manual Pages deployment and contribution templates |

The separate `Awesome-Embodied-Memory-website` folder is an identical export of `website/`. It is useful for another static host; it does not need a second GitHub repository. Development caches, old artwork, screenshots, local work logs, private PDFs and manuscript files are excluded.

## 1. Upload the source

The following commands assume the destination repository is empty. Run them from the clean source folder; use your existing GitHub authentication when prompted.

```sh
git init -b main
git add .
git commit -m "Initial public release"
git remote add origin https://github.com/Iron-LYK/Awesome-Embodied-Memory.git
git push -u origin main
```

If the remote already contains commits, clone it and copy the clean files into that checkout instead of replacing its history. The repository root should contain `README.md`, `.github/` and `website/` directly, not an additional enclosing folder. Include the hidden `.github/` directory.

GitHub Description:

> A curated collection of embodied memory research for world models & WAM, VLA, and agentic robotics — with papers, code, and an interactive atlas.

The README is English-only; the website is bilingual. The wordmark in both website languages links to the repository.

## 2. Enable GitHub Pages

In the repository, open **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**. Do not choose a branch or upload the site into a separate user-site repository.

Open **Actions → Deploy website → Run workflow**, select `main`, and run it. The included `.github/workflows/pages.yml` validates the catalogue, rebuilds the site and deploys only `website/`. The website URL appears in the successful deployment. First publication can take several minutes.

This is a **project site**, so the expected address is `https://iron-lyk.github.io/Awesome-Embodied-Memory/`. A repository named `iron-lyk.github.io` is not required. Relative asset paths allow the site to run under the project prefix. See GitHub's [project-site URL rules](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) and [custom workflow instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Deployment is manual: a push triggers quality checks, but does not publish the site. After future updates, run **Deploy website** again when ready. No custom domain, backend, Node dependency installation or external font service is needed.

## 3. Create a versioned Release (optional)

A GitHub **Release** records a version; it is separate from publishing the README or deploying Pages. After the initial source commit and checks pass, open **Releases → Draft a new release**, create tag `v1.0.0` targeting `main`, add release notes and publish. GitHub supplies source archives automatically. You can additionally attach the standalone website ZIP produced below.

## Maintain and export

Edit canonical records in `data/` and website source in `website/`, then run:

```sh
python3 scripts/validate.py
python3 scripts/build.py
python3 scripts/check_site.py
python3 scripts/package_release.py
```

The last command produces clean source/site folders, ZIP files, a SHA-256 manifest and checksums in ignored `dist/`. It uses explicit file allowlists and verifies the source can rebuild independently. Do not upload `dist/` into the repository.

Local preview:

```sh
python3 -m http.server 8765 --directory website
```

Open `http://localhost:8765/?lang=en` or `http://localhost:8765/?lang=zh`. For the standalone export, serve that folder instead. Keep `index.html`, `assets/` and `resources/` together. The language choice and bookmarks are stored only in the visitor's browser.

Before a release, inspect both languages, domain/method filters and the mobile layout; confirm record counts and citation status. The catalogue contains both research publications and clearly marked pre-publication methods. Updating this living index does not change the companion manuscript's fixed search scope or evidence claims.
