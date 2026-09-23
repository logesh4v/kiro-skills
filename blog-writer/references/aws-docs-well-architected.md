# AWS documentation and Well-Architected steering

Use this after the code-derived fact sheet and before drafting. Code proves
**what this workload does**. Current AWS documentation proves **what a service
supports and calls the feature today**. The Well-Architected Framework helps
surface trade-offs; AWS describes the review as a constructive conversation,
not an audit.

Official sources:

- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Six pillars: https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html
- AWS Architecture Icons: https://aws.amazon.com/architecture/icons/

## When the AWS Documentation MCP server is available

Use the `awslabs.aws-documentation-mcp-server` tools. Never guess a tool or
feature name from memory:

1. `search_documentation(search_phrase=..., search_intent=...)` — find the
   current service guide and the exact relevant section.
2. `read_sections(url=..., section_titles=[...])` — read only the sections
   needed to verify a claim. Use `read_documentation` if section titles are
   unavailable.
3. `search_table(...)` — use for a large support, quota, Region or feature
   table instead of copying the whole page.
4. `recommend(url=...)` — optional, when one service page points to a related
   architecture decision the fact sheet uses.

Record each result in `brief.md` under `## AWS documentation checks`:

```text
- Claim: EventBridge Pipes supports <feature>
  Code: infra/.../stack.py:123
  AWS doc: <URL>#<section>, read <date>
  Status: confirmed | code uses legacy name | conflict — VERIFY
```

Documentation **never overrides deployed code**. If docs and code conflict,
write both in the brief, say which version/Region the code uses, and leave a
`[VERIFY]` tag until resolved. Do not cite search-result snippets; cite the
page/section you read.

## Without the MCP server

Use the same official `docs.aws.amazon.com` pages through normal web retrieval.
If neither MCP nor web retrieval is available, say "AWS docs not checked in
this run" in the brief. The skill still works from code, but must not call a
preview feature generally available or claim current Region support.

## Six-pillar steering (all workloads)

The official pillars are operational excellence, security, reliability,
performance efficiency, cost optimization and sustainability. This is a
**claim/design review**, not a full Well-Architected Review.

For each pillar, write one of: `evidence`, `trade-off`, `not in scope`, or
`[VERIFY]`. Never turn an absence into invented architecture.

| Pillar | Ask the code/author | What may enter the post |
|---|---|---|
| Operational excellence | deployment, observability, runbook, ownership, rollback, change process | only mechanisms shown in code or an author-owned operating procedure |
| Security | identity, least privilege, data classification, encryption, secrets, network boundaries, detection | controls actually configured; include shared responsibility, never imply AWS secures customer configuration/data |
| Reliability | failure modes, retries, queues, health checks, backup/restore, multi-AZ/Region, RTO/RPO | measured/tested behavior; distinguish design target from demonstrated recovery |
| Performance efficiency | workload shape, scaling, quotas, latency percentiles, chosen service/resource type | measured window and load; no list-price or benchmark claim without source |
| Cost optimization | bill window, dominant services, unit cost, utilization, lifecycle/rightsizing | measured cost or an explicit `[VERIFY: cost]`; never estimate and present as a bill |
| Sustainability | utilization, managed/serverless choice, idle capacity, data lifecycle, Region/service efficiency | a concrete workload decision; omit generic "greener cloud" claims |

## Well-Architected contradiction gate

Before `done`, fail the run when the prose claims any of these without evidence:

- high availability without the deployed Availability Zone/Region topology;
- disaster recovery without tested restore/failover, RTO and RPO;
- secure/compliant without named controls and the customer's responsibility;
- scalable without a scaling mechanism and a tested/expected load;
- cost-efficient without a bill or unit-cost source;
- sustainable without a concrete utilization/data-lifecycle decision.

A diagram can expose a missing decision, but cannot prove that the decision
was implemented. Put the gap in `brief.md`; do not quietly "improve" the
architecture while drawing it.
