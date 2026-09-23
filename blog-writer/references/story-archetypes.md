# Technical story archetypes

The **genre** controls publication voice and editorial constraints. The
**archetype** controls the story order. Choose both. Do not force every subject
into "I built X".

| Reader's main question | Archetype | Required story order |
|---|---|---|
| What did you build and what broke? | **build story** | TL;DR → problem → why this approach → architecture → core loop → decisions → ≥3 numbered gaps → proof → live/next → cost → lessons → try it |
| How do I reproduce one outcome? | **tutorial / how-to** | outcome + prerequisites → final architecture → numbered build steps → verify after each major step → failure modes → cleanup/cost → next step |
| Why is the system shaped this way? | **architecture deep dive** | forces/constraints → context diagram → component/data flow → boundaries → key decisions + rejected alternatives → failure model → operations → cost → trade-offs |
| How did you move from old to new? | **migration / modernization** | before → drivers → assessment → target architecture → waves → data/cutover → validation/rollback → measured result → what remains |
| How did you make it faster or cheaper? | **performance / cost** | baseline + window → bottleneck/cost driver → hypotheses → experiment design → changes → before/after per metric → regressions/trade-offs → repeatable method |
| What failed and how do we prevent it? | **incident / lesson learned** | impact + timeline → architecture context → detection → root cause → contributing factors → fix → proof → prevention/ownership; redact sensitive operational details |
| Which option should I choose? | **comparison / decision** | decision context → non-negotiable criteria → candidates → same workload test → evidence table → decision → where the losers still win → migration/reversal cost |
| What business/customer outcome did the solution produce? | **case study** | customer problem → partner role → solution → architecture → implementation → security/shared responsibility → measured results → conclusion/CTA |

## Publication voice

- **Builder Center / personal:** first person, direct, evidence-rich. Load
  `structure-builder.md` for a build story; for other archetypes use the table
  above plus the builder voice and 2,000–2,500-word default.
- **Partner / APN:** third person, named roles, no unsupported superlatives,
  shared-responsibility sentence, ≤1,500 words ideal / 1,800 cap. Load
  `structure-partner.md`; the case-study order above is canonical.
- **Team engineering / general technical:** first person singular or neutral
  team voice, chosen once and kept consistent; 1,500–2,500 words unless the
  publication gives a limit. Use the archetype order above and `aws-style.md`.

## Archetype-specific proof gate

- Tutorial: every command was run or is tagged `[VERIFY: command not run]`;
  cleanup is present when resources cost money.
- Architecture deep dive: rejected alternatives and failure behavior are not
  optional.
- Migration: before/after, rollback and what did **not** migrate are explicit.
- Performance/cost: same measurement method and window on both sides; avoid
  changing load and calling it an improvement.
- Incident: timeline comes from logs/tickets, not recollection; never expose
  an exploitable detail, credential, account id, customer data or hostname.
- Comparison: same workload, Region, scale and scoring criteria for every
  candidate; disclose missing tests.
- Case study: every result has a customer-approved source/date; planned work
  never appears in Results.

The heading names may adapt to the publication, but every required beat must
appear. Record the chosen genre + archetype at the top of `brief.md` so the
reviewer can tell which gate applies.
