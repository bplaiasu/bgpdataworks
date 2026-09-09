# BGP Data Works Website — v1.48 Local

This build is derived from the approved v1.43 local source of truth. It adds the fourth detailed Engineering project page. No GitHub changes are part of this package.

## v1.48 changes

### Engineering — Project 04 detailed page
- Added `projects/retail-monitoring-data-warehouse.html`.
- Linked the **Retail Monitoring Data Warehouse** homepage card to the new detailed page using a **View project →** action.
- Refined the homepage Project 04 card around confirmed implementation details.
- Expanded Project 04 using confirmed project information:
  - built from scratch on Microsoft SQL Server;
  - multiple transactional MySQL source systems;
  - sales, orders, inventory, products, pricing, customers, payments and logistics data;
  - normalized snowflake-schema modeling;
  - stored procedures and scheduled SQL jobs;
  - selected sub-minute refresh intervals for near-real-time operational reporting;
  - twice-daily refresh for less time-sensitive workloads;
  - linked-server connectivity to MySQL sources;
  - temp tables, partitioning and indexing for SQL performance engineering;
  - product performance, stock levels and operational KPI dashboards;
  - approximately 60 business users and stakeholders across analytics, operations, management and finance;
  - row-count and source-to-warehouse reconciliation.
- Kept client/employer names out of the public project page.
- Projects 01–03 remain unchanged in content.
- No GitHub changes are part of this release.
- Cache-busting version references updated to v1.48.

## Content boundaries
Project 04 uses only the confirmed architecture, refresh cadence, user count, reporting use cases and SQL engineering details provided for this project. It does not claim streaming architecture or unconfirmed performance metrics.

## Before production launch
1. Confirm the final public email address.
2. Decide whether Insights cards should link to real article pages.
3. Confirm the production domain, then add the canonical URL, `og:url`, absolute social image URL and `sitemap.xml`.
4. Run final Lighthouse/Core Web Vitals tests on the deployed production preview.

## Local run

From the parent directory:

```bash
python -m http.server 8080 -d BGP_Data_Works_Website_v1.48_Local
```

Then open `http://localhost:8080/index.html` and use **View project →** on any of the four Engineering projects.
