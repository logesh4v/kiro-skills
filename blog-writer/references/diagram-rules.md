# Architecture diagram rules

The diagram is the most-scrutinised object in the post and the one most often
wrong. These rules produce the idiom AWS's own blogs use. They were confirmed
against four published AWS/APN posts and one round of AWS SA review.

## Layout idiom

```
 actors            ┌──────────────────────── AWS Cloud ──────────── Region: xx-xxxx-1 ┐
 (stick figures,   │  ┌──────────── Virtual private cloud (VPC) ─────────────────┐   │   systems of
  OUTSIDE the      │  │  [ALB]  ┌── Amazon ECS / EKS / Lambda group ───────────┐ │   │   record
  cloud frame)     │  │         │  orchestrator → specialist components         │ │   │   (OUTSIDE,
                   │  │         └───────────────────────────────────────────────┘ │   │   neutral
       ──────────► │  └────────────────────────────────────────────────────────────┘   │ ◄──── glyphs)
                   │   [Bedrock] [Embeddings] [OpenSearch] [KB] [S3] [RDS]  ← service row │
                   └──────────────────────────────────────────────────────────────────────┘
                                   Figure 1: <caption>
```

- **Nested group frames, corner-badged.** AWS Cloud (dark frame, `aws` badge
  top-left) → Region label top-right → VPC frame (purple, VPC icon badge) →
  compute group frame (orange for ECS/EKS, with the service icon as badge).
- **Actors outside the cloud.** Users, staff, customers as stick figures with a
  label below. Third-party gateways (WhatsApp vendor, payment gateway, a
  customer's core system) also outside, in a "Systems of record" or
  "External" frame, with **neutral glyphs**.
- **Service row** along the bottom inside the Cloud: the managed services the
  compute layer calls. Icon above, label centred below, sub-label in muted text.
- **Arrows:** thin (1.4px), dark grey, labelled with what flows ("delegates",
  "video clips", "policy · CKYC · payment"). Double-headed for request/response.
  No numbered callout circles — label the arrow instead. No legend.
- **Caption** below the frame: *Figure 1: <System> solution architecture —
  <one sentence>.*

## Icons

- Use only `assets/aws-icons/*.svg`. These are the official AWS Architecture
  Icons (`Arch_<Service>_64`), flat category-coloured squares with a white
  glyph. `MANIFEST.json` gives file → service → category → hex.
- **Embed the icon's path data verbatim.** Copy the `<path d="…">` and the
  background `fill` exactly. Do not redraw, recolour, add gradients or round
  the corners — the official icons are square with a flat fill.
- Verify embedding by matching `' d="'` (leading space — `d="` alone also
  matches `id="`) against the source file.
- **One icon per AWS service instance.** Amazon Bedrock appears once for the
  model, again for Knowledge Bases, again for Guardrails if drawn — each with
  its own label. That is how AWS's own diagrams do it.
- **Guardrails placement:** if the code passes `guardrail_id` into the model
  call (coupled mode), draw Guardrails *beside Amazon Bedrock on the invocation
  path* with an "every invocation" connector. Do NOT draw it as a separate
  service node with its own connector to the app — that depicts the standalone
  `ApplyGuardrail` pattern, which is a different design.
- **Non-AWS components never get AWS icons.** Strands Agents has its own mark
  (`strands-agents-mark.svg`, brand green `#00FF77`); everything else
  third-party gets a neutral grey rectangle or document glyph.

## Category colours (from the official package)

| Category | Hex |
|---|---|
| Machine Learning / AI | `#01A88D` |
| Compute (incl. ECS, EKS, Lambda) | `#ED7100` |
| Networking & Content Delivery / Analytics | `#8C4FFF` |
| Storage | `#7AA116` |
| Database | `#C925D1` |
| Security, Identity & Compliance | `#DD344C` |
| Application Integration / Management | `#E7157B` |

## Icon availability — what the bundle has and what it does not

`assets/aws-icons/` holds 63 official AWS icons plus the Strands mark; `MANIFEST.json` is the index. For a
GenAI / agentic system on AWS the coverage is complete — a 17-service KYC
pipeline (Lambda, DynamoDB, Step Functions, EventBridge, IAM, KMS, Cognito,
CloudWatch, SQS, S3, Bedrock, AgentCore, Rekognition, Textract, API Gateway,
X-Ray, Scheduler) needed nothing outside it.

**Some services are in the AWS package under a newer name than you may expect.**
Use the file that exists:

| You may look for | Bundled as |
|---|---|
| Amazon MSK | `Arch_Amazon-Managed-Streaming-for-Apache-Kafka_64.svg` |
| Amazon SES | `Arch_Amazon-Simple-Email-Service_64.svg` |
| Kinesis Data Firehose | `Arch_Amazon-Data-Firehose_64.svg` |
| Amazon EFS | `Arch_Amazon-EFS_64.svg` |
| Amazon SageMaker | `Arch_Amazon-SageMaker-AI_64.svg` |

**Services with NO standalone icon in the official package** — do not invent
one; use the parent service's icon with a distinct label, which is what AWS's
own diagrams do:

| Component | Draw as |
|---|---|
| Amazon Bedrock Guardrails | Bedrock icon, label "Bedrock Guardrails" |
| Amazon Bedrock Knowledge Bases | Bedrock icon, label "Bedrock Knowledge Bases" |
| Amazon Titan / any foundation model | Bedrock icon, sub-label with the model id |
| An agent, tool or handler you wrote | neutral component glyph from the skeleton, never an AWS icon |

**Adding an icon.** Fetch `Arch_<Service>_64.svg` from a mirror of the official
package, confirm it carries `Icon-Architecture/64/` in a group id (or the newer
export shape: an 80×80 `viewBox`, one `<rect>` with a category fill, one
`_Squid` path), drop it in `assets/aws-icons/`, and regenerate `MANIFEST.json`.
Never hand-draw a service icon — an approximation in the right colour reads as
wrong to anyone who knows the real one.

## Sizing

- Canvas 1520×800 (or 1600×920 for a dense diagram). Landscape.
- Icons 50px in the service row, 40–46px inside groups, 26px for repeated
  small components (agents, tools).
- Body labels ≥ 11px, headings ≥ 13px. Legible at 1000px published width.

## Rendering

`python3 scripts/render_diagram.py figure-1.svg` writes `figure-1.png` at 2×
using headless Chrome via an HTML wrapper. Then **open the PNG and look**:
clipped edges, overlapping labels, an arrow that ends in space — each of these
has shipped once.

Do not use macOS Quick Look (`qlmanage`) — it applies aspect-fill and silently
crops the edges of a wide SVG, losing whole columns.

## Before shipping

Check against the Phase 1 fact sheet:
- Every AWS service in the diagram is in the fact sheet, and vice versa
- The component count (agents, functions, queues) matches the code
- The database is the real engine (the code's connection string), not the plan
- Optional/flagged components are drawn dashed or omitted, and the prose says which
- No account IDs, ARNs, CIDRs, hostnames, resource names, secrets
