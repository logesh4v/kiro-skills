# kiro-skills

Reusable [Agent Skills](https://agentskills.io) for the team, loadable by Kiro
IDE, Kiro CLI, Kiro Crew, and (as workspace skills) Kiro Web.

| Skill | Ask Kiro… | What you get |
|---|---|---|
| **blog-writer** | "write a blog about what I built", "APN blog", "Builder Center post" | A publishable technical post in one of two proven structures, an architecture diagram with official AWS icons, and a brief that traces every claim to its source. |

**Status:** v0.1. The fact-sheet and lint phases have been exercised against
real repos and real published posts; the full interview → diagram → draft flow
has not yet produced a published article. Treat the first few runs as a test
and [tell us what broke](#feedback-and-contributions).

## Prerequisites

- Kiro IDE, Kiro CLI, or Kiro Crew with Agent Skills support.
- `python3` (3.9+, standard library only) for the two helper scripts.
- Google Chrome, for `render_diagram.py` (SVG → PNG). Without it the skill
  still writes the SVG; you just render it yourself.
- `git`, to clone and update.

## Install (one line)

```bash
git clone https://github.com/logesh4v/kiro-skills.git ~/kiro-skills && ~/kiro-skills/install.sh
```

Windows (PowerShell):

```powershell
git clone https://github.com/logesh4v/kiro-skills.git $env:USERPROFILE\kiro-skills; & $env:USERPROFILE\kiro-skills\install.ps1
```

The installer symlinks each skill into `~/.kiro/skills/` (IDE + CLI) and
`~/.kiro/crew/skills/` (Crew). Restart Kiro or start a new chat. Re-running
is safe.

**Using Kiro Web or Mobile?** They read only workspace skills. From inside
the project you are writing about:

```bash
cd /path/to/your/project && ~/kiro-skills/install.sh --workspace
```

then commit the resulting `.kiro/skills/` folder. A workspace skill wins over
a global one with the same name.

**No terminal?** In Kiro IDE: *Agent Steering & Skills → + → Import a skill →
GitHub*, and paste the URL of the **skill folder**, not the repo root:

```
https://github.com/logesh4v/kiro-skills/tree/main/blog-writer
```

Imported skills are copies, not links — re-import to pick up updates.

## Update

```bash
git -C ~/kiro-skills pull
```

Symlinked installs pick it up immediately. Imported or `--copy` installs need
a re-import / re-run of the installer.

## Using blog-writer

Type `/blog-writer` or just describe what you want. The skill will:

1. Ask for the codebase and build a fact sheet from it (services, models,
   component counts, config) before writing anything. Numbers in the post
   come from the code, not from memory.
2. Ask which genre — **Builder Center** (first person, ~2,200 words, "gaps I
   hit and how I fixed them") or **Partner/APN** (third person, ≤1,500 words,
   AWS editorial rules).
3. Interview you: eight questions, one at a time, pushed back on once if vague.
4. Draw the diagram from the fact sheet using official AWS icons, render it,
   and look at the result.
5. Draft with every claim tagged to its source (`[code:]`, `[dash:]`,
   `[author]`, `[VERIFY]`).
6. Lint (`scripts/check_blog.py`) and hand over the post, the SVG + PNG, and
   `brief.md` for review.

Everything lands in `blog-assets/` in your working directory. Nothing is
published; you review and post.

## Repo layout

```
blog-writer/
├── SKILL.md                    procedure (loaded on activation)
├── references/                 loaded only when the procedure says so
│   ├── structure-builder.md    Builder Center genre
│   ├── structure-partner.md    Partner / APN genre
│   ├── aws-style.md            naming, numbers, vocabulary, leak rules
│   └── diagram-rules.md        AWS group-box idiom, icon rules, render recipe
├── assets/
│   ├── aws-icons/              63 official Arch_*_64.svg + Strands mark + MANIFEST.json
│   └── diagram-skeleton.svg    Cloud → Region → VPC frame, ready to populate
└── scripts/
    ├── check_blog.py           lint: budget, vocabulary, first-mention names, leaks
    └── render_diagram.py       SVG → 2× PNG via headless Chrome (never Quick Look)
install.sh / install.ps1        symlink every skill folder into Kiro's skill dirs
```

## Feedback and contributions

Pull requests and issues are welcome — a wrong rule, a missing icon, a
structure that did not fit your post, a lint false positive. Include the
input that broke it (a redacted paragraph or the service name is enough).

**How a change lands.** Open a PR against `main`. CI runs
`tests/validate_skill.py` (skill structure, script size, manifest, leak scan),
`tests/test_check_blog.py` (linter behaviour on the fixtures), the installer
on Linux and macOS, and shellcheck. `main` is protected: CI must be green and
the repo owner (see `.github/CODEOWNERS`) must approve before merge. Run the
two test scripts locally first — they are stdlib Python and take a second.

**Adding a skill:** one folder per skill, `SKILL.md` with `name` (= folder
name) and `description` (≤1,024 chars — it is the trigger, so write it the
way people ask). Keep `SKILL.md` to the procedure; put long material in
`references/`. Scripts are Python, standard library only, under 4 KB, no
credentials, no network calls to unknown hosts.

**Adding an icon:** see the *Icon availability* section of
`blog-writer/references/diagram-rules.md` — official assets only, and
regenerate `MANIFEST.json`.

## Licences

Repo contents: [MIT](LICENSE).

`blog-writer/assets/aws-icons/` contains the official
[AWS Architecture Icons](https://aws.amazon.com/architecture/icons/),
redistributed unmodified for use in architecture diagrams per AWS's terms;
AWS's own licence governs those files. The Strands Agents mark is from
[strandsagents.com](https://strandsagents.com).
