# BGP Data Works Website

This repository uses a small static-site generator so shared content is maintained once while the deployed website remains fully static and SEO-friendly.

## How it works

Edit the source files under `src/` and the shared values in `site.json`, then run:

```bash
python build.py
```

The build generates the deployable files directly in the repository root:

- `index.html`
- `404.html`
- `projects/<project-slug>/index.html`
- `styles.css`
- `script.js`
- `assets/`

This means GitHub Pages can continue serving the repository root without a JavaScript application router or a separate deployment framework.

## Centralized configuration

Shared company values live in `site.json`.

For example, the public email address is defined once:

```json
"contact_email": "contact@bgpdataworks.com"
```

Run `python build.py` after changing it and the homepage, all project footers and structured data are regenerated consistently.

The future production domain can also be added once in:

```json
"base_url": ""
```

When `base_url` is populated, the build automatically adds canonical URLs, `og:url` and a `sitemap.xml`.

## Shared templates

The reusable page structure is under:

```text
src/templates/
├── base.html
├── header.html
├── footer.html
└── 404.html
```

Homepage content:

```text
src/pages/home.html
```

Project content:

```text
src/projects/
├── enterprise-data-validation-framework.html
├── high-performance-financial-data-pipeline.html
├── enterprise-data-platform-modernization.html
└── retail-monitoring-data-warehouse.html
```

Each generated project receives its own static URL and full HTML metadata.

## Local development

From this folder:

```bash
python build.py
python -m http.server 8080
```

Then open:

```text
http://localhost:8080/index.html
```

## Editing workflow

1. Change shared settings in `site.json`.
2. Change shared layout only in `src/templates/`.
3. Change homepage content in `src/pages/home.html`.
4. Change an Engineering project in its matching file under `src/projects/`.
5. Run `python build.py`.
6. Test locally.
7. Commit both the source files and generated static files.

There is no framework dependency and no package installation step.
