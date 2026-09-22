# Genre: Partner / APN / AWS-channel case study

Third person. A named customer had a problem; a named partner built the
solution on AWS. The reader is a prospective customer or an AWS reviewer.
The post must pass AWS editorial review, which is stricter than any other
channel this skill targets.

**Budget:** ≤1,500 words body (AWS's stated ideal). Up to ~1,800 is tolerated
if the technical depth earns it — say so to the AWS reviewer rather than
cutting the strongest section. Above 2,000 will be sent back.

**Voice:** "SBIGI partnered with AWS and ShellKode to…", "the orchestrator
agent delegates…". Never "I" or "we built". Present tense for what is live.

## Hard constraints (fail the review if violated)

- **Banned vocabulary:** leading, best-in-class, world-class, seamless,
  revolutionary, cutting-edge, robust, game-changing, "we believe". Also
  "the cloud" (write "the AWS Cloud"), "platform" and "ecosystem" as loose
  descriptors.
- **No FUD framing.** Do not describe an AWS service by what it cannot do, and
  do not use "bypass", "exploit", "jailbreak", "attack". Recast constraints as
  design principles: "the streaming filter holds back a tail buffer" not "the
  model leaked".
- **Full service names on first mention** with the short form in parentheses:
  *Amazon Simple Storage Service (Amazon S3)*. Services whose official name is
  already an abbreviation are never expanded (Amazon EC2, Amazon RDS, Amazon
  ECS is *Amazon Elastic Container Service (Amazon ECS)*).
- **Shared responsibility language** in any security section: AWS secures the
  infrastructure; the customer and partner secure the OS, applications and data.
- **Every metric has a window and a source**, and needs written customer
  sign-off before submission.
- **Forward-looking numbers are legal exposure.** Keep projections only if the
  customer insists; label them "projected" in the table header; note in the
  brief that AWS Legal may strip them.
- **At least one attributed customer quote** (full name, title). Leave a marked
  placeholder if not yet available — never invent one.
- **Partner tier is an eligibility gate**, not a style detail: only Advanced or
  Premier tier partners may publish on the APN Blog. Confirm before drafting.
- **Byline convention:** the AWS employee (PSA / PDM) is author of record;
  partner contributors are credited in the body. Confirm with the AWS contact.

## Section order

### About <Customer> (40–60 words)
At the TOP if the AWS reviewer asks for it (they often do); otherwise at the
end. Legal name, promoter/parent, founding year, HQ, product lines. No adjectives.

### Introduction (100–150 words)
Open with a concrete user moment ("A customer who types '…' is asking the
insurer to…"). Then: who partnered with whom, on what AWS services, to do what.
One sentence on the shape of the solution.

### Business challenge (60–100 words)
What was slow or impossible before, and the constraints a regulated or
enterprise context imposed (data residency, audit, entitlements). Name the
regulator where relevant.

### Solution overview (150–250 words)
One paragraph on the design principle. Then a bold-led paragraph or bullet per
AWS service: **Amazon Bedrock** does X; **Amazon OpenSearch Serverless** does Y.
Model name, region, and any config that matters (temperature, dimensions).

### Solution architecture (80–120 words + Figure 1)
Request path in one paragraph, left to right on the figure. Then the figure
with a caption: *Figure 1: <System> solution architecture. <One sentence>.
All resources run in <region>.*

### <Component deep-dive> (100–200 words each, 1–3 sections)
The distinctive parts: the agent topology, the retrieval design, the
transactional journey. One line per component if there is a list. Explain
one design decision per section.

### <Hardest engineering problem> (250–450 words) — the differentiator
The partner genre's version of "the hard part". Explain the mechanism
accurately, name the fix by its properties (default-open, tail buffer,
regression-tested at N chunk sizes), and cite the test that proves it. Keep
the vocabulary constraints — describe what you *built*, not what *failed*.

### Security and governance (80–150 words)
Controls in one paragraph. End with the shared-responsibility sentence.

### Rollout (80–120 words)
Phases, audiences, what changed between them. Present tense for live, future
for planned, never in the same sentence.

### Results (100–200 words + table)
One sentence with the window. A two-column table: Metric | Phase (measured).
Five or six rows max. Then a bridging sentence stating the **trend** if there
is a prior figure. Optional second table for projections, same shape, header
says "projected". Then the customer quote.

### Lessons learned (4–6 bullets)
Bold principle, one sentence each. Transferable.

### Conclusion (60–100 words)
What the customer can now do that it could not before. One sentence on what
is next. Then the "To learn more" CTA linking the AWS service pages, and one
sentence on how to reach the partner.

## Checks specific to this genre

- Body ≤ 1,800 words; flag if > 1,500
- Zero banned-vocabulary hits
- Every AWS service full-named on first mention
- Shared-responsibility sentence present
- Results table has a stated window
- Quote placeholder or real attributed quote present
- No first-person pronouns outside the quote
