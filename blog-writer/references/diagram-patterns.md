# Diagram pattern selector

Choose a pattern from the **shape of the deployed system**, not from the blog
title. Copy the SVG into `blog-assets/figure-1.svg`, remove sample nodes that
are not in the fact sheet, then replace remaining sample icons and labels.
The pattern is a layout, never architecture evidence.

| Fact-sheet signal | Start from | Must make explicit |
|---|---|---|
| Browser/API/compute/data path in one Region | `application-serverless.svg` | actor, entry point, compute boundary, sync/async edges, data stores; delete the VPC when none exists |
| Events, topics, queues, streams, workflows | `event-driven.svg` | producer, event type, ordering, retry owner, idempotency boundary, dead-letter queue |
| Two or more Regions, failover or replication | `multi-region-dr.svg` | active-active vs active-passive vs pilot light vs backup/restore, health decision, Route 53/Global Accelerator/CloudFront role, replication direction, RTO and RPO |
| AWS Organizations, OUs, shared/security accounts | `multi-account-landing-zone.svg` | account ownership, organizational units, delegated administrator, log archive, trust edges, service control policies |
| On premises, branches, edge, Direct Connect or VPN | `hybrid-network.svg` | route direction, BGP/VPN/Direct Connect, DNS resolution, inspection point, encryption boundary, transit ownership |
| Data lake, ETL, streaming, analytics, ML | `data-analytics-ml.svg` | source, ingest, raw/curated/serving zones, catalog, governance, transformation, consumers, batch vs stream |
| Build/test/deploy/runtime path | `cicd-delivery.svg` | source, test gate, immutable artifact, account boundary, approval, deploy method, rollback, observation |
| Discovery, replication, cutover or modernization | `migration-modernization.svg` | source estate, assessment, migration waves, data sync, cutover, validation, rollback, steady state |

## Compose patterns when the system needs more than one view

A single figure should answer one question. If the architecture is both
multi-account and multi-Region, do **not** squeeze both into one unreadable
page. Use:

1. **Figure 1 — deployment/topology:** accounts, Regions, VPCs and trust
   boundaries (`multi-account` + `multi-region`).
2. **Figure 2 — request/data flow:** services and arrows
   (`application`, `event-driven` or `data-analytics-ml`).
3. **Figure 3 — delivery/operations**, only when it is part of the story
   (`cicd-delivery` or `migration-modernization`).

The blog structure says one figure per major section, not one figure per post.
Two focused figures are better than one wall of icons.

## Selection gate

Before drawing, answer these in `brief.md`:

- Which actors and external systems are outside AWS?
- How many AWS accounts, organizational units, Regions and VPCs exist **in code**?
- Which path is synchronous? Which is asynchronous?
- Where does state live, and what crosses a trust, account or Region boundary?
- What retries, buffers, deduplicates, fails over and sends to a dead-letter queue?
- What is encrypted in transit/at rest, and which identity authorizes each edge?
- For resilience: recovery time objective (RTO), recovery point objective (RPO), health signal and failback owner.
- For data: classification, retention, lineage and deletion owner.
- For cost: the services or flows that dominate spend, with evidence.

If the code cannot answer one, tag it `[VERIFY: diagram — ...]`. Never infer a
VPC, Availability Zone, multi-Region deployment, encryption path, private
endpoint, retry, backup, or failover merely because AWS recommends it.

## Icon level

- `assets/aws-icons/`: all 303 uniquely named **service-level** icons in the
  official Q3 2026 package. Use for a managed-service node.
- `assets/aws-resource-icons/`: all 513 official **resource-level** SVGs. Use
  when the resource distinction changes the story (public/private subnet,
  bucket, function, instance, role, gateway). Prefer the light-theme version
  on the templates' white background.
- Neutral grey box: non-AWS system, customer system, open-source component or
  logical component you wrote.

Always search `MANIFEST.json` by service/resource name. If a current AWS service
has no standalone icon, use the parent service icon and an exact label; record
that mapping in `brief.md`. Never approximate an icon.
