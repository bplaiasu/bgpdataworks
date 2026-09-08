v1.37 cleanup: removed obsolete favicon.svg and hero-medallion-bgp.png. The hero now uses the optimized WebP asset directly.

BGP Data Works local website v1.36

Changes from v1.34 stable baseline:
- Integrated approved BGP circular favicon package.
- Added favicon.ico, PNG sizes, Apple touch icon, Android icons and site.webmanifest.
- Updated index.html and 404.html favicon references.

# BGP Data Works Website — v1.34 Local

This build is derived from the approved v1.33 stable baseline. Visual design and responsive layout are intentionally unchanged.

## v1.34 changes

### Performance
- Added a WebP hero image variant (PNG retained as fallback).
- Preloads the hero/LCP image and sets `fetchpriority="high"`.
- Added intrinsic image dimensions to reduce layout shift.
- Lazy-loads below-the-fold technology logo images.
- Removed unused legacy assets from previous iterations.

### Accessibility
- Active header/footer navigation now exposes `aria-current="location"`.
- Phone reveal areas use polite live regions.
- Mobile menu toggle now has a 44×44 CSS touch target.
- Phone reveal controls have expanded invisible hit areas without changing appearance.

### SEO
- Added robots, theme-color, Open Graph and basic Twitter metadata.
- Added Organization JSON-LD using only currently established company information.
- Added `noindex` to the 404 page.

### Content cleanup
- Updated stale version comments and phone configuration documentation.
- Removed unused assets while keeping all assets currently rendered by the site.

## Before production launch
1. Replace the test phone number `+40 745 123 456` with the real number.
2. Confirm `hello@bgpdataworks.com` is the final public email.
3. Confirm the production domain. Then add the canonical URL, `og:url`, absolute social image URL and `sitemap.xml`.
4. Decide whether Engineering and Insights cards should link to real project/article pages.
5. Run final Lighthouse/Core Web Vitals tests on the deployed preview.

## Local run
From the parent directory:

```bash
python -m http.server 8080 -d BGP_Data_Works_Website_v1.34_Local
```

Then open `http://localhost:8080/index.html`.
