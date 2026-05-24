# GitHub Pages Project Website

Build 35 adds a polished static website under `site/` for reviewer-facing project navigation.

The site explains what CARSF is, why the project exists, what the model currently calculates, what it does not calculate, what public aggregate data has been loaded, which placeholders remain boundary-limited, what data and review are still missing, how to read the generated reports, and how to run the model locally.

## Files

- `site/index.html`
- `site/styles.css`
- `site/app.js`
- `site/assets/carsf-logo.svg`
- `site/site_manifest.json`
- `site/README.md`
- `scripts/build_github_pages_site.py`
- `reports/github_pages_site.md`
- `reports/github_pages_site.json`

## Validation

Run:

```powershell
python scripts/build_github_pages_site.py
```

The validator checks that required static files exist, required website sections are present, source report counts reconcile with `site/site_manifest.json`, non-claim boundaries remain visible, and no external CDN, analytics, tracking, API fetch, or scraping dependency is introduced.

## GitHub Pages Setup

GitHub Pages must still be enabled in repository settings:

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

This is a static project website only. It does not load new data, does not scrape sources, does not call external APIs, does not calibrate the model, does not validate the model, does not prove the model works, does not determine actual tax payable, does not determine firm-level liability, and does not claim law, legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, official policy, legal sufficiency, operational readiness, or implementation readiness.

Public aggregate values remain boundary-limited. Placeholder replacement mapping remains mapping only. Calibration-boundary mapping remains a boundary artifact only. Scenario constraints remain constraints only. The full repo integrity audit documents coverage and gaps; it does not resolve missing data or external review dependencies.
