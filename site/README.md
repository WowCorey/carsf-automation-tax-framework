# CARSF GitHub Pages Site

This folder contains a static GitHub Pages-ready reviewer website for the CARSF Automation Tax Framework.

It is a static site only. It has no backend, no analytics, no tracking, no scraping, no external API calls, no external CDN dependency, and no private or restricted data.

## Local Preview

From the repository root:

```powershell
python -m http.server 8000 --directory site
```

Then open:

```text
http://localhost:8000/
```

## Validation

Run:

```powershell
python scripts/build_github_pages_site.py
```

The validator checks that the site files exist, required sections are present, generated report summaries are represented, external dependencies are absent, and non-claim boundaries remain visible.

## GitHub Pages Setup

GitHub Pages usually has to be enabled in repository settings:

1. Go to repository Settings.
2. Open Pages.
3. Set the source to GitHub Actions or deploy from a branch/folder.
4. If using branch/folder, choose `main` and `/site` if GitHub Pages exposes that folder option for this repository.
5. Save.
6. Open the Pages URL shown by GitHub.

Expected project URL shape:

```text
https://wowcorey.github.io/carsf-automation-tax-framework/
```

## Non-Claims

This site is a reviewer-facing project website only. It does not calibrate the model, does not validate the model, does not prove the model works, does not determine actual tax payable, does not determine firm-level liability, and does not claim law, legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, official policy, legal sufficiency, operational readiness, or implementation readiness.
