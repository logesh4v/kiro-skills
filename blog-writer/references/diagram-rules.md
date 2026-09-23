# Architecture diagram rules

The diagram is the most-scrutinised object in the post and the one most often
wrong. It must describe the deployed system, not an improved system the author
wishes existed.

Load `references/diagram-patterns.md` and choose a pattern from the topology:

- application/serverless
- event-driven/workflow
- multi-Region/disaster recovery
- multi-account/landing zone
- hybrid/network
- data/analytics/ML
- CI/CD/software delivery
- migration/modernization

The editable templates live in `assets/diagram-patterns/`. Compose two focused
figures when the workload has two shapes; do not force multi-account,
multi-Region and request flow into one wall of icons.

## AWS diagram idiom

- **Frames are real boundaries.** AWS Cloud → account/organization → Region →
  Availability Zone → VPC → subnet/compute group, but draw only the boundaries
  proved by IaC or the author. A managed service does not belong inside a VPC
  merely because the application reaches it privately.
- **Actors outside AWS.** Users, staff, customers, on-premises systems and
  third-party services sit outside the AWS Cloud frame, with neutral glyphs.
- **Trust and ownership.** Account, Region, VPC, subnet, tenant and external
  boundaries are labelled. Cross-boundary arrows say what moves and which
  direction.
- **Arrows:** thin (1.4–1.6px), dark grey, labelled with the payload/event.
  Double-headed only for a real bidirectional/replication path. Dashed for
  optional, failover or asynchronous edges when the caption explains it.
- **Caption:** *Figure N: <system> — <what the reader should learn from this
  view>.* Each figure answers one question.
- **No decorative inventory.** If a service does not participate in the flow
  this figure explains, omit it. Put monitoring, security or delivery in a
  second view only when it matters to the story.

## Complete official icon corpus

The bundle is imported from AWS's official Q3 2026 Architecture Icons ZIP
published 31 July 2026. Provenance and duplicate handling are in
`assets/aws-icons/SOURCE.md`.

- `assets/aws-icons/`: **303 uniquely named service-level SVGs** — every unique
  64px Architecture Service icon in the package. `MANIFEST.json` maps file →
  service → category → colour.
- `assets/aws-resource-icons/`: **513 resource-level SVGs** — every Resource
  SVG in the package. Its manifest maps file → resource → category → theme.
- `assets/aws-icons/strands-agents-mark.svg`: separately sourced Strands Agents
  brand mark; it is not an AWS Architecture Icon.

Use service icons for service nodes. Use resource icons only when the resource
shape changes the explanation (public/private subnet, function, instance,
bucket, role, gateway). Prefer a light-theme resource icon on the white
canvas.

## Icon rules

- Embed the selected official SVG's path data verbatim. Do not redraw,
  recolour, round or add gradients. Verify path copying by matching `' d="'`
  (a leading space; `d="` alone also matches `id="`).
- One icon per actual service/resource instance. Repeated icons are correct
  when distinct instances matter; otherwise one node with a count is clearer.
- An AWS feature with no standalone icon uses its parent service icon and an
  exact feature label. Examples: Bedrock Guardrails, Bedrock Knowledge Bases,
  and Amazon Titan models use the Amazon Bedrock icon. Record the mapping in
  `brief.md`.
- Guardrails coupled to model invocation sit beside Amazon Bedrock on that
  invocation path, connected "every invocation". Do not depict the standalone
  `ApplyGuardrail` pattern unless the code uses it.
- Non-AWS logical components, customer systems and open-source software never
  get AWS icons. Use a neutral grey rectangle; use the Strands mark only for
  Strands Agents.
- Search both manifests before saying an icon is absent. Never fetch a random
  SVG or approximate one. Quarterly updates use
  `scripts/import_aws_icons.py` and `scripts/import_aws_resource_icons.py` on
  the official ZIP from https://aws.amazon.com/architecture/icons/.

## Common renamed files

| Service name readers use | Official file |
|---|---|
| Amazon MSK | `Arch_Amazon-Managed-Streaming-for-Apache-Kafka_64.svg` |
| Amazon SES | `Arch_Amazon-Simple-Email-Service_64.svg` |
| Amazon Data Firehose | `Arch_Amazon-Data-Firehose_64.svg` |
| Amazon EFS | `Arch_Amazon-EFS_64.svg` |
| Amazon SageMaker AI | `Arch_Amazon-SageMaker-AI_64.svg` |
| Amazon EC2 | `Arch_Amazon-EC2_64.svg` |
| Amazon RDS | `Arch_Amazon-RDS_64.svg` |
| Amazon Quick | `Arch_Amazon-Quick_64.svg` |

## Category colours

Never infer a category from this table when the manifest has the exact value.
The common palette is:

| Category | Hex |
|---|---|
| Artificial Intelligence | `#01A88D` |
| Compute / Containers | `#ED7100` |
| Networking & Content Delivery / Analytics | `#8C4FFF` |
| Storage | `#7AA116` |
| Databases | `#C925D1` |
| Security & Identity | `#DD344C` |
| Application Integration / Management | `#E7157B` |

## Pattern-specific correctness gates

- **Application:** VPC and subnet placement matches IaC; synchronous and
  asynchronous edges are distinct.
- **Event-driven:** event, ordering, retry owner, idempotency and dead-letter
  path are visible; do not invent a DLQ.
- **Multi-Region:** mode, health decision, replication direction, recovery time
  objective (RTO), recovery point objective (RPO) and failback owner are stated.
- **Multi-account:** account/OU ownership, delegated administrator, log archive,
  trust edges and service control policies match the organization.
- **Hybrid:** Direct Connect/VPN, transit ownership, routing, DNS and inspection
  points are explicit; do not call an internet path private.
- **Data/ML:** source, batch/stream ingest, raw/curated/serving zones, catalog,
  governance, transformation and consumer are traceable.
- **CI/CD:** source, tests, immutable artifact, account boundary, approval,
  deployment, rollback and observation are shown.
- **Migration:** source, wave, replication/transfer, cutover, validation,
  rollback and steady state are separate.

## Sizing

- Canvas 1520×860 (or 1600×920 for a dense view), landscape.
- Service icons 45–56px; resource icons 32–48px; repeated components 26–36px.
- Body labels ≥11px, headings ≥13px. Legible at 1000px published width.

## Rendering

Run `python3 scripts/render_diagram.py figure-1.svg`. It writes a 2× PNG using
headless Chrome. Open the PNG and inspect every label, arrow and frame. Do not
use macOS Quick Look (`qlmanage`); it can aspect-fill and crop wide SVGs.

## Before shipping

Reconcile the SVG against the fact sheet line by line:

- every AWS service/resource in the figure has a code or author source;
- account, Region, Availability Zone, VPC and subnet boundaries are proved;
- component counts and service variants match deployment;
- each arrow has a source, destination, direction and payload/event;
- optional/planned paths are dashed and explicitly labelled;
- failure, retry, DLQ, failover and replication paths are drawn only when real;
- the diagram and prose agree on what is live versus planned;
- account IDs, ARNs, CIDRs, hostnames, internal resource names and secrets are
  absent;
- every figure has one readable caption and one purpose.

If any check cannot be answered, put `[VERIFY: diagram — ...]` in the post and
brief. A polished diagram with an invented boundary is worse than no diagram.
