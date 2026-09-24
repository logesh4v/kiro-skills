---
name: blog-writer
description: Write any evidence-based AWS technical blog end to end — build story, tutorial, architecture deep dive, migration, performance/cost, incident lesson, comparison, Builder Center, APN or partner case study — with topology-correct diagrams. Gathers facts from code, checks current AWS docs and all six Well-Architected pillars, interviews the author, selects from eight diagram patterns using the complete official AWS service/resource icon corpus, traces every claim to evidence, and blocks unsupported claims.
license: Apache-2.0
metadata:
  author: logesh4v
  version: 0.2.0
  genres: builder-center, partner-apn
---

# blog-writer

Turns "I built X on AWS" into a blog post a reviewer will pass first time, with a
diagram that matches the deployed system. Two genres are supported and they are
NOT interchangeable — pick one in Phase 2 and load only that reference.

The rules below exist because each one was learned the hard way on a real post.
Do not skip a phase to save time; the phases are ordered so that facts are
established before prose is written.

## When to use

- "Write a blog / article / case study about what we built"
- "Builder Center post", "APN blog", "partner blog", "AWS blog"
- "Draw the architecture for the blog"
- Reviewing or refreshing an existing draft against code or new metrics

Do not use for marketing copy, product pages, or internal design docs.

## Outputs

Everything lands in `blog-assets/` next to the working directory:

| File | What |
|---|---|
| `brief.md` | Interview answers + fact sheet + every claim's source. The review artefact. |
| `<slug>.md` | The post, in the chosen genre's structure |
| `figure-N.svg` / `figure-N.png` | One or more focused architecture views, vector + 2× raster |
| `lint-report.txt` | Output of `scripts/check_blog.py` — must be clean before "done" |

## Phase 1 — Locate the source of truth

Ask first: **"Is there a codebase for this? Give me the path or repo URL."**

If YES, build the fact sheet BEFORE any prose, using the file tools directly
(not sub-agents — they cannot read the project tree in some environments).
**Always exclude build output first** — `cdk.out*`, `node_modules`, `.venv`,
`__pycache__`, `dist`, `demo-assets` — or synthesised templates and vendored
code will swamp every count with false hits.

1. `glob` the tree two levels deep. Note the language, where the IaC lives
   (it is often nested: `infra/<name>/`, not `infra/`), and where config lives.
2. `grep` for the things blogs get wrong. Each has a trap the naïve grep misses:
   - **AWS services.** Do NOT grep for `aws_lambda.Function(` — CDK code aliases
     imports (`from aws_cdk import aws_lambda as lambda_`). Two steps: first
     collect the aliases from every `from aws_cdk import … as X` line, then
     count `X.<Construct>(` for each alias. Separately grep the raw
     CloudFormation types `AWS::Service::Resource` — that catches L1 constructs
     and preview services (Bedrock AgentCore, for example) that have no L2.
     For non-CDK repos use `Type: AWS::` (CFN/SAM) or `resource "aws_` (Terraform).
     For app code, `boto3.client("` and `new [A-Z][A-Za-z]+Client(` name the
     services actually called at runtime.
   - **Model identifiers.** `(amazon|anthropic|openai|cohere|meta)\.[a-z0-9-]+(-v\d+:\d+)?`
     in source files only; drop hits on `amazon.com` and `amazon.awscdk`.
   - **Config values.** Region, temperature, token limits, timeouts, dimensions.
   - **Component roster** (agents, tools, handlers, harnesses). Look for the
     *declaration*, not the usage: `AGENTS: tuple[...] = (`, `AGENTS = [`,
     `@tool(name="`, `class Agent`, a `key="…"` field in a config module. Read
     that declaration and count. Do not trust a list found in a `spike/` or
     `scripts/` folder — it is usually a subset.
   - **Feature flags and kill switches.** `^(ENABLE|FEATURE|USE)_[A-Z_]+ = ` and
     `getattr(settings, "…", False)` → what is **optional vs always-on**. Read the
     comment above each flag; a `False` may be a measured, dated decision.
   - **Tests.** `find . -name "test_*.py"` (or the language's equivalent) across
     the whole tree — tests often live per-package, not under one `tests/`.
     Report the count per package; it tells the reader where the rigour is.
3. `read` the entry points, the orchestrator, the component declaration, and
   the IaC stacks. Confirm every grep hit against the code that uses it.
4. Write the fact sheet into `brief.md` under `## Fact sheet (from code)`.
   Every line cites a path: `- 7 agents — infra/<stack>/config.py:120 (AGENTS tuple)`.

If NO codebase: say so plainly, write `## Fact sheet: none — author's account only`,
and every technical claim later carries `[VERIFY: no code]`. Do not soften this.

In Kiro Crew, also run `search_chat_history` for the project name — the build
sessions often hold the "what broke and how we fixed it" material verbatim.

## Phase 2 — Choose publication voice AND story archetype

Load `references/story-archetypes.md`. Choose the reader's question first:
build story, tutorial/how-to, architecture deep dive, migration/modernization,
performance/cost, incident/lesson learned, comparison/decision, or customer
case study. Record `Genre:` and `Archetype:` at the top of `brief.md`.

Then choose one publication voice:

| Signal | Genre | Load |
|---|---|---|
| "I built", Builder Center, dev.to, personal | **builder** | `references/structure-builder.md` for build stories; otherwise the archetype order |
| Named customer, partner, APN, case study | **partner** | `references/structure-partner.md` |
| Team engineering / general technical | **technical** | the archetype order in `story-archetypes.md` |

Confirm both choices with the author in one line. Do not mix first-person
builder voice into a partner case study. Always load `references/aws-style.md`.

## Phase 2.5 — Current AWS docs + Well-Architected steering

Load `references/aws-docs-well-architected.md`.

After code proves what the workload deploys, verify every publication-critical
claim about current feature names, Region support, service behavior, quotas or
integration shapes against official AWS documentation. When the AWS
Documentation MCP server is available, use `search_documentation` then
`read_sections` / `read_documentation`; otherwise retrieve the same page from
`docs.aws.amazon.com`. Record the URL, section and read date under
`## AWS documentation checks` in `brief.md`. Search snippets are not evidence.

Review the architecture through all six AWS Well-Architected pillars:
operational excellence, security, reliability, performance efficiency, cost
optimization and sustainability. For each write `evidence`, `trade-off`, `not
in scope`, or `[VERIFY]` in the brief. This is a constructive design/claim
review, not a Well-Architected audit. Never add architecture to make the review
look green.

## Phase 3 — The interview

Ask these one at a time. Write each answer into `brief.md` under `## Interview`.
Push back once on any hand-wave ("*which* number, from *where*?"), then move on.

1. What was slow, broken, or manual before? One concrete example a reader can picture.
2. The single number that proves it is better — and its source (dashboard,
   log query, measurement). No source, no number.
3. The architecture **as deployed**. Walk the Phase 1 fact sheet with them;
   record every mismatch between what they say and what the code shows.
4. The three hardest problems. For each: what broke, what you tried first,
   what actually fixed it. This is the section readers value most and authors
   skip most.
5. What is live today versus planned. Never blend these in the post.
6. What it costs to run, or what it saved.
7. What you would do differently.
8. One thing the reader can try in fifteen minutes.

If the author gives a metric that differs from a prior published figure, record
both and the dates; the post will state the trend, not just the new number.

## Phase 4 — Diagram

Load `references/diagram-rules.md` and `references/diagram-patterns.md`. Then:

1. Choose from the eight topology templates in `assets/diagram-patterns/`:
   application/serverless, event-driven, multi-Region/DR, multi-account,
   hybrid/network, data/analytics/ML, CI/CD, or migration/modernization.
   `diagram-skeleton.svg` remains the compact application fallback. If the
   system has two shapes, use two focused figures; never make one icon wall.
2. Answer the pattern's topology gate in `brief.md`: actors, external systems,
   accounts/OUs, Regions/AZs/VPCs, sync/async paths, state, trust crossings,
   retries/DLQs, failover/RTO/RPO, data lifecycle and cost drivers. Anything
   code cannot prove is `[VERIFY: diagram — ...]`.
3. Every AWS node must appear in the fact sheet. Non-AWS components use neutral
   glyphs. Never infer a VPC, private endpoint, Multi-AZ/Region placement,
   encryption path, backup or failover because it is recommended.
4. Service icons come from `assets/aws-icons/` (all 303 unique official Q3 2026
   service SVGs). Resource-level precision comes from
   `assets/aws-resource-icons/` (all 513 official resource SVGs). Search each
   `MANIFEST.json`, embed the SVG verbatim, and never redraw or recolour.
5. Label below each icon, centred. Arrows thin and labelled with what flows.
   Caption every view: *Figure N: …*.
6. Render every figure with `python3 scripts/render_diagram.py figure-N.svg`
   at 2×. **Open every PNG and look at it.** Check clipping, overlapping labels,
   arrow endpoints, frame membership and legibility at 1000px width.
7. Scan every SVG for anything that must never ship: account IDs, ARNs, CIDRs,
   hostnames, secrets. `check_blog.py` does this too, but look yourself.

## Phase 5 — Draft

Write to the genre's section order from the loaded reference. While drafting,
tag every technical claim inline with its provenance:

- `[code: src/path.py]` — read it in Phase 1
- `[dash: <screenshot name>]` — from a dashboard or metrics view
- `[aws-doc: <URL>#<section>, read <date>]` — current official AWS documentation
- `[author]` — the author said so, not otherwise verified
- `[VERIFY]` — no source yet; **blocks completion**

The tags are stripped by the lint at the end and copied into
`brief.md → ## Claim sources`. That table is what makes review with an AWS SA
or a client take minutes instead of days.

Rules that apply to both genres:
- Every AWS service in full on first mention — `Amazon Elastic Container Service (Amazon ECS)` — short form after.
- Every acronym expanded on first use.
- Numbers carry their window: not "6,591 users" but "6,591 users between 31 Dec and 20 Jul".
- A metric that improved over time is stated as a trend with both endpoints.
- No sentiment/feedback figure without saying what fraction of interactions were rated.
- "Live" and "planned" never share a sentence.

## Phase 6 — Gate

Run `python3 scripts/check_blog.py <slug>.md --genre <builder|partner> --svg figure-1.svg` (`technical` uses `builder` for the mechanical voice-neutral gate).
It checks: word budget for the genre, banned vocabulary, first-mention service
names, unexpanded acronyms, remaining `[VERIFY]` tags, figure captions, and
leaked identifiers in the SVG. Fix everything it reports. It writes
`lint-report.txt`.

Then apply the archetype proof gate in `story-archetypes.md` and the
Well-Architected contradiction gate in `aws-docs-well-architected.md`. Any
unsupported high-availability, disaster-recovery, security/compliance,
scalability, cost or sustainability claim becomes `[VERIFY]` and blocks done.

When every gate passes, run
`python3 scripts/finalize_blog.py <slug>.md brief.md`. It fails closed on any
`[VERIFY]`, copies every `[code:]` / `[dash:]` / `[aws-doc:]` / `[author]`
source into a generated table in `brief.md`, and writes
`<slug>-publish.md` with internal provenance tags removed. Never publish the
working draft.

Then hand over: the sourced draft, the clean publish copy, every SVG + PNG,
`brief.md`, and `lint-report.txt`.

## Gotchas

- **The blog is not the design doc.** Phase 1 exists because the deployed
  system drifts from the plan. A diagram showing five agents when the code
  registers seven is the kind of error a reviewer catches in ten seconds.
- **Do not put AWS icons on non-AWS things.** It misrepresents the architecture
  and is a review flag on any AWS channel.
- **Never trust `qlmanage` / Quick Look to rasterise a wide SVG** — it crops
  edges silently. `render_diagram.py` uses headless Chrome for this reason.
- **Verify pasted icon assets by path data**, not by eye. A `d="` regex also
  matches `id="` — anchor it with a leading space.
- **A dashboard screenshot with empty date filters is a lifetime total**, not a
  window. Ask for the filtered view, or state the cut-off date explicitly.
- **Projections scale by metric, not by one number.** If a prior projection
  implied +25% users but +70% requests, re-basing it means applying each
  multiplier to its own metric, and saying so.
- **Read the PDF annotation layer programmatically** when reviewing a marked-up
  draft. Visual scanning of rendered pages missed seven of nine reviewer
  comments once.
- **The `description` field is the trigger.** Kiro matches user phrasing against
  it; keep the verbs people actually use ("write a blog", "APN blog",
  "Builder Center") in it.
