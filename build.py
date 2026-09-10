from pathlib import Path
import json
import shutil
import html
import re
import hashlib

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
CONFIG_PATH = ROOT / "site.json"

def load(path):
    return path.read_text(encoding="utf-8")

def render(template, context):
    result = template
    for key, value in context.items():
        result = result.replace("{{" + key + "}}", str(value))
    unresolved = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", result)))
    if unresolved:
        raise RuntimeError(f"Unresolved template values: {unresolved}")
    return result

def escaped(value):
    return html.escape(str(value), quote=True)

def file_revision(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]

def page_url(base_url, relative_path):
    if not base_url:
        return ""
    base = base_url.rstrip("/")
    if not relative_path:
        return base + "/"
    return base + "/" + relative_path.strip("/") + "/"

def url_tags(url):
    if not url:
        return "", ""
    canonical = f'  <link rel="canonical" href="{escaped(url)}">\n'
    og = f'  <meta property="og:url" content="{escaped(url)}">\n'
    return canonical, og

def organization_schema(company):
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": company["name"],
        "description": company["description"],
        "email": company["contact_email"],
        "knowsAbout": [
            "Data Engineering",
            "Databricks",
            "Delta Lake",
            "PySpark",
            "SQL",
            "Medallion Architecture"
        ]
    }
    if company.get("base_url"):
        data["url"] = company["base_url"].rstrip("/") + "/"
    return '  <script type="application/ld+json">\n' + json.dumps(data, indent=2) + '\n  </script>\n'

def shared_context(company, root_prefix, is_home):
    section_prefix = "" if is_home else root_prefix
    return {
        "ROOT": root_prefix,
        "SITE_ROOT_HREF": "./" if is_home else root_prefix,
        "COMPANY_NAME": escaped(company["name"]),
        "CONTACT_EMAIL": escaped(company["contact_email"]),
        "SECTION_PREFIX": section_prefix,
        "HOME_HREF": "#home" if is_home else root_prefix,
        "HOME_ACTIVE": ' class="active"' if is_home else "",
        "HEADER_ID": ' id="home"' if is_home else ""
    }

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def build():
    config = json.loads(load(CONFIG_PATH))
    company = config["company"]

    base_template = load(SRC / "templates" / "base.html")
    header_template = load(SRC / "templates" / "header.html")
    footer_template = load(SRC / "templates" / "footer.html")
    error_template = load(SRC / "templates" / "404.html")

    css_rev = file_revision(SRC / "styles.css")
    js_rev = file_revision(SRC / "script.js")

    # Recreate the generated output directory from scratch.
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    # Static assets.
    shutil.copytree(SRC / "assets", DIST / "assets")
    for filename in ["styles.css", "script.js", "robots.txt", "site.webmanifest"]:
        shutil.copy2(SRC / filename, DIST / filename)

    # Homepage.
    home = config["home"]
    home_shared = shared_context(company, "", True)
    header = render(header_template, home_shared)
    footer = render(footer_template, home_shared)
    home_main = render(load(SRC / "pages" / "home.html"), home_shared)

    home_url = page_url(company.get("base_url", ""), "")
    canonical_tag, og_url_tag = url_tags(home_url)

    home_context = {
        **home_shared,
        "TITLE": escaped(home["title"]),
        "META_DESCRIPTION": escaped(home["description"]),
        "CSS_REV": css_rev,
        "JS_REV": js_rev,
        "ROBOTS": "index, follow, max-image-preview:large",
        "THEME_COLOR": escaped(company["theme_color"]),
        "OG_TYPE": "website",
        "OG_TITLE": escaped(home["og_title"]),
        "OG_DESCRIPTION": escaped(home["og_description"]),
        "TWITTER_TITLE": escaped(home["twitter_title"]),
        "TWITTER_DESCRIPTION": escaped(home["twitter_description"]),
        "CANONICAL_TAG": canonical_tag,
        "OG_URL_TAG": og_url_tag,
        "HEAD_EXTRA": '  <link rel="preload" as="image" href="assets/hero-medallion-bgp.webp" type="image/webp" fetchpriority="high">\n',
        "STRUCTURED_DATA": organization_schema(company),
        "HEADER": header,
        "MAIN": home_main,
        "FOOTER": footer
    }
    write(DIST / "index.html", render(base_template, home_context))

    # Project pages.
    project_urls = []
    for project in config["projects"]:
        slug = project["slug"]
        root_prefix = "../../"
        shared = shared_context(company, root_prefix, False)
        header = render(header_template, shared)
        footer = render(footer_template, shared)
        fragment = render(load(SRC / project["source"]), shared)

        project_url = page_url(company.get("base_url", ""), f"projects/{slug}")
        canonical_tag, og_url_tag = url_tags(project_url)

        context = {
            **shared,
            "TITLE": escaped(project["title"]),
            "META_DESCRIPTION": escaped(project["description"]),
            "CSS_REV": css_rev,
            "JS_REV": js_rev,
            "ROBOTS": "index, follow, max-image-preview:large",
            "THEME_COLOR": escaped(company["theme_color"]),
            "OG_TYPE": "article",
            "OG_TITLE": escaped(project["og_title"]),
            "OG_DESCRIPTION": escaped(project["og_description"]),
            "TWITTER_TITLE": escaped(project["twitter_title"]),
            "TWITTER_DESCRIPTION": escaped(project["twitter_description"]),
            "CANONICAL_TAG": canonical_tag,
            "OG_URL_TAG": og_url_tag,
            "HEAD_EXTRA": "",
            "STRUCTURED_DATA": organization_schema(company),
            "HEADER": header,
            "MAIN": fragment,
            "FOOTER": footer
        }

        output = DIST / "projects" / slug / "index.html"
        write(output, render(base_template, context))
        if project_url:
            project_urls.append(project_url)

    # Insight pages.
    insight_urls = []
    for insight in config.get("insights", []):
        slug = insight["slug"]
        root_prefix = "../../"
        shared = shared_context(company, root_prefix, False)
        header = render(header_template, shared)
        footer = render(footer_template, shared)
        fragment = render(load(SRC / insight["source"]), shared)

        insight_url = page_url(company.get("base_url", ""), f"insights/{slug}")
        canonical_tag, og_url_tag = url_tags(insight_url)

        context = {
            **shared,
            "TITLE": escaped(insight["title"]),
            "META_DESCRIPTION": escaped(insight["description"]),
            "CSS_REV": css_rev,
            "JS_REV": js_rev,
            "ROBOTS": "index, follow, max-image-preview:large",
            "THEME_COLOR": escaped(company["theme_color"]),
            "OG_TYPE": "article",
            "OG_TITLE": escaped(insight["og_title"]),
            "OG_DESCRIPTION": escaped(insight["og_description"]),
            "TWITTER_TITLE": escaped(insight["twitter_title"]),
            "TWITTER_DESCRIPTION": escaped(insight["twitter_description"]),
            "CANONICAL_TAG": canonical_tag,
            "OG_URL_TAG": og_url_tag,
            "HEAD_EXTRA": "",
            "STRUCTURED_DATA": organization_schema(company),
            "HEADER": header,
            "MAIN": fragment,
            "FOOTER": footer
        }

        output = DIST / "insights" / slug / "index.html"
        write(output, render(base_template, context))
        if insight_url:
            insight_urls.append(insight_url)

    # 404.
    error_context = {
        "THEME_COLOR": escaped(company["theme_color"]),
        "COMPANY_NAME": escaped(company["name"]),
        "CSS_REV": css_rev
    }
    write(DIST / "404.html", render(error_template, error_context))

    # Sitemap becomes available automatically when the final base URL is configured.
    if company.get("base_url"):
        urls = [home_url, *project_urls, *insight_urls]
        sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for url in urls:
            sitemap.append(f"  <url><loc>{html.escape(url)}</loc></url>")
        sitemap.append("</urlset>")
        write(DIST / "sitemap.xml", "\n".join(sitemap) + "\n")

    print("Build complete.")
    print(f"Output directory: {DIST}")
    print(f"Generated homepage: {DIST / 'index.html'}")
    print(f"Generated project pages: {len(config['projects'])}")
    print(f"Generated insight pages: {len(config.get('insights', []))}")
    print(f"Shared email: {company['contact_email']}")

if __name__ == "__main__":
    build()
