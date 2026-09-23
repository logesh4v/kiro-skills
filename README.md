# kiro-skills

Reusable [Agent Skills](https://agentskills.io) for the team, loadable by Kiro
IDE, Kiro CLI, Kiro Crew, and (as workspace skills) Kiro Web.

| Skill | Ask Kiro… | What you get |
|---|---|---|
| **blog-writer** | "write a blog about what I built", "APN blog", "architecture deep dive", "migration story", "how-to" | A publishable AWS technical post, one or more topology-correct diagrams, and a brief tracing every claim to code, measurements, AWS documentation or the author. |

**Status:** v0.2 candidate. The fact-sheet and lint phases have been exercised
against real repos and published posts; one complete Builder run produced a
2,327-word draft and diagram, correctly stopping on four author-only facts.
The eight diagram families and full Q3 2026 AWS icon corpus are new in v0.2;
treat first use of each family as verification and
[tell us what broke](#feedback-and-contributions).

## Coverage

- **Story shapes:** build story, tutorial/how-to, architecture deep dive,
  migration/modernization, performance/cost, incident/lesson learned,
  comparison/decision, and customer case study.
- **Publication voices:** Builder Center/personal, Partner/APN, and general
  engineering.
- **Diagram families:** application/serverless, event-driven, multi-Region/DR,
  multi-account/landing zone, hybrid/network, data/analytics/ML, CI/CD, and
  migration/modernization. Complex systems use two focused views rather than
  one icon wall.
- **Official assets:** all 303 uniquely named 64px AWS service icons and all
  513 AWS resource SVGs from the official Q3 2026 package, plus the Strands
  Agents mark. Nothing is hand-drawn or recoloured.
- **AWS steering:** current service claims can be checked through the AWS
  Documentation MCP server (when installed) or official AWS documentation;
  every architecture gets a six-pillar Well-Architected claim review.

Coverage does not mean the skill invents missing facts. It blocks on `[VERIFY]`
when code, measurements, AWS documentation or the author cannot support a
claim, boundary or arrow.

## Prerequisites

- Kiro IDE, Kiro CLI, or Kiro Crew with Agent Skills support.
- `python3` (3.9+, standard library only) for helper scripts.
- Google Chrome for `render_diagram.py` (SVG → PNG). Without it the skill still
  writes SVG; render it yourself before publication.
- `git` to clone and update.
- Optional: the AWS Documentation MCP server for current service/feature
  verification. The skill falls back to official `docs.aws.amazon.com` pages.

## Install

macOS / Linux:

```bash
git clone https://github.com/logesh4v/kiro-skills.git ~/kiro-skills && ~/kiro-skills/install.sh
```

Windows (PowerShell):

```powershell
git clone https://github.com/logesh4v/kiro-skills.git $env:USERPROFILE\kiro-skills; & $env:USERPROFILE\kiro-skills\install.ps1
```

The installer symlinks every skill into `~/.kiro/skills/` (IDE + CLI) and
`~/.kiro/crew/skills/` (Crew). Restart Kiro or start a new chat. Re-running is
safe.

**Kiro Web or Mobile:** they read workspace skills only. From the project:

```bash
cd /path/to/your/project && ~/kiro-skills/install.sh --workspace
```

Commit the resulting `.kiro/skills/` folder. A workspace skill wins over a
global skill with the same name.

**No terminal:** in Kiro IDE choose *Agent Steering & Skills → + → Import a
skill → GitHub* and paste the skill-folder URL:

https://github.com/logesh4v/kiro-skills/tree/main/blog-writer

Imported skills are copies — re-import to update.

## Update

```bash
git -C ~/kiro-skills pull
```

Symlinked installs update immediately. Imported or `--copy` installs need a
re-import / re-run.

## Using blog-writer

Type `/blog-writer` or describe the outcome. The skill will:

1. Ask for the codebase and build a fact sheet (services, resources, models,
   component counts, config, topology and tests) before prose.
2. Select a publication voice and one of eight story archetypes.
3. Verify current AWS service claims against official AWS docs; apply the six
   Well-Architected pillars as a claim/trade-off review, not an audit.
4. Interview you with eight evidence-seeking questions, one at a time.
5. Select one or more topology templates, replace sample services only with
   fact-sheet evidence, render every SVG and visually inspect every PNG.
6. Draft with every claim tagged `[code:]`, `[dash:]`, `[aws-doc:]`, `[author]`
   or `[VERIFY]`.
7. Run the mechanical lint, archetype proof gate and Well-Architected
   contradiction gate. Any `[VERIFY]` blocks "done". Once clear,
   `finalize_blog.py` writes the provenance ledger into `brief.md` and emits a
   clean `<slug>-publish.md` with internal source tags removed.

Outputs land in `blog-assets/` next to your working directory. Nothing is
published automatically.

## Repo layout

```text
blog-writer/
├── SKILL.md
├── references/
│   ├── structure-builder.md / structure-partner.md
│   ├── story-archetypes.md
│   ├── aws-style.md
│   ├── aws-docs-well-architected.md
│   ├── diagram-patterns.md
│   └── diagram-rules.md
├── assets/
│   ├── aws-icons/              303 service SVGs + manifest + source record
│   ├── aws-resource-icons/     513 resource SVGs + manifest
│   ├── diagram-patterns/       8 editable topology templates
│   └── diagram-skeleton.svg    compact application fallback
└── scripts/
    ├── check_blog.py / finalize_blog.py / render_diagram.py
    └── import_aws_icons.py / import_aws_resource_icons.py
```

## Feedback and contributions

Pull requests and issues are welcome — a wrong rule, missing/renamed icon,
layout that does not fit, or lint false positive. Include the smallest redacted
input that reproduces it.

**How a change lands:** open a PR against `main`. CI validates frontmatter,
references, script compilation/size, both icon manifests, XML, leak scans,
linter fixtures, installer behavior on Linux/macOS and shellcheck. `main` is
protected: CI must pass and the code owner must approve.

**Adding a skill:** one folder, a `SKILL.md` whose `name` equals the folder and
whose `description` uses phrases people ask. Keep procedures in `SKILL.md` and
long guidance in `references/`. Scripts are stdlib Python, under 4 KB, with no
credentials or network calls to unknown hosts.

**Updating icons:** download the quarterly Icon package from the official AWS
Architecture Icons page and run both import scripts. Review removals/renames,
render all eight templates, visually inspect them, then update the source record.

## Licences

Repo-authored content: [MIT](LICENSE).

The AWS service/resource SVGs come unmodified from the official
[AWS Architecture Icons](https://aws.amazon.com/architecture/icons/) package;
AWS's terms govern those files. The Strands Agents mark is from
[strandsagents.com](https://strandsagents.com).
