# Genre: Builder Center / personal technical post

First person. The author built it and is telling a peer how, including what
went wrong. Readers are engineers who will try to reproduce parts of it.

**Budget:** 2,000–2,500 words. Below 1,800 it reads thin; above 3,000 it loses
the reader before "Try it".

**Voice:** "I built", "I hit", "the fix was". Direct. Short paragraphs. It is
fine — expected — to name what the platform could not do at the time and how
you engineered around it. Vocabulary like "gap", "bypass", "blocked",
"couldn't" is normal here; it is banned in the partner genre, so do not carry
this voice across.

## Section order

Use these headings in this order. Every section is required unless marked.

### 1. Title
Pattern: *I built <what> that <outcome> — on <primary AWS service>*.
Concrete outcome, not a category. Under 90 characters.

### 2. TL;DR (100–150 words)
Four beats: what it does, what it runs on, the one safety/quality property
that matters, and proof it is live. End with "Here's how I built it — and
<the thing readers will actually want>."

### 3. The Problem (150–250 words)
The forces that pull against each other. Three or four bullets, each a
single noun-phrase demand ("Speed — incidents need sub-minute response").
Then one sentence on what most existing answers get wrong, and one on what
you wanted instead.

### 4. Why <this approach> (250–400 words)
The design philosophy and the evidence for it. If you wrote a spec first,
say how many requirements and show one. If you used property-based tests,
show one property and one test — ten lines max each. State the final counts:
tests, invariants proven, lint status.

### 5. Architecture (200–300 words + Figure 1)
The Figure. Then one paragraph per layer, left to right as drawn. Name every
AWS service in full on first mention. Say where the model runs and which one.
Say what is inside the VPC and what is not, and why.

### 6. The core loop (150–250 words)
The thing the system does, as a numbered sequence a reader can trace on the
diagram. Six to ten steps. Each step one line.

### 7. Design decisions that mattered (300–450 words)
Four to six, each as a bold lead phrase and two or three sentences: what you
chose, what you rejected, why. This is where judgment lives.

### 8. The hard part: <what actually broke> (500–800 words) — THE KEY SECTION
Number the gaps. For each:

**Gap N — <symptom in one line>**
- What you saw (the actual error, the actual behaviour)
- What you tried first and why it did not work
- The fix, concretely — the config key, the resource type, the code shape
- One sentence on why the platform behaves that way, if you know

Three to six gaps. This section is why engineers share the post. Do not
compress it to save words; compress sections 4 and 7 instead.

### 9. <Distinctive capability> (150–300 words each, 1–3 sections) — optional
Mid-session model switching, human-in-the-loop, policies that evolve from
incidents — whatever is genuinely novel. One section per capability, each
with a concrete example.

### 10. Proof it's real (100–200 words)
What actually ran, end to end, against real resources. Dates. IDs are fine
if they are not sensitive. A screenshot or a log excerpt. If something is not
yet proven, say so here — readers trust the post more, not less.

### 11. What's live (bulleted)
Present tense only. Planned items go in a separate "What's next" list or are
omitted.

### 12. Cost (50–150 words)
Real numbers from the bill, not list-price arithmetic. Say what you measured
and over what period.

### 13. What I learned (5–7 bullets)
Each a bold principle and one sentence of why. Transferable, not project
-specific.

### 14. Try it (50–100 words)
Repo link, the one command to get started, and what the reader should see in
fifteen minutes.

## Checks specific to this genre

- Section 8 exists and has ≥3 numbered gaps with all four beats each
- Section 10 distinguishes proven from unproven
- Section 11 contains no future tense
- At least one code block ≤ 15 lines, and none longer than 25
- TL;DR ends with a forward hook
