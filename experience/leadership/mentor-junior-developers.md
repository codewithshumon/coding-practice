# Mentor Junior Developers

> **Category:** Technical Leadership
> **Relevant at:** Impressive Security, As-Sunnah Foundation, MVI Solutions
> **Related tech docs:** `case/code-quality/review-code-standards.md` (review as mentoring), `case/code-quality/write-quality-code.md` (standards to teach), `case/leadership/lead-sdlc.md` (growing ownership)

---

## 1. What This Means

Mentoring junior developers means actively **growing the engineers around you** — through knowledge sharing, constructive feedback, pair programming, code reviews, and fostering a **growth-oriented team culture** where people learn, take risks safely, and improve over time.

**Scope:**
- **Knowledge sharing** — explaining *why*, not just *what*; documenting patterns; lunch-and-learns
- **Constructive feedback** — feedback that builds up, not tears down
- **Pair programming** — teaching through doing, together
- **Code review as mentoring** — reviews that teach patterns, not just catch bugs
- **Culture** — psychological safety, growth mindset, celebrating learning

**Why it matters:** a team's capability is the sum of its members' growth. Mentoring multiplies impact — a senior who lifts three juniors creates far more value than one who codes alone. And teaching deepens your own understanding (you master what you explain).

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Mentoring is woven into everyday work, not a separate activity:**
- **Code review** becomes a teaching moment ("here's why we use the repository pattern")
- **Pair programming** on a hard problem transfers both skill and confidence
- **A junior asks a question** → you don't just answer, you help them find the answer
- **A junior makes a mistake** → you treat it as a learning opportunity, not a failure

**Real-world scenarios:**
- A junior's PR has a design flaw → instead of "rewrite this," you explain the tradeoff and guide them to a better approach
- A junior is stuck → you pair for 30 minutes; they learn the debugging approach, not just the answer
- A pattern keeps coming up → you write it up / do a short session so the whole team levels up
- A junior hesitates to ask "dumb" questions → you model curiosity and normalize not-knowing

**The culture dimension:**
- **Psychological safety** — juniors ask questions, admit mistakes, and take risks without fear
- **Growth mindset** — abilities improve with effort; mistakes are data, not character flaws
- **Celebrating learning** — "great question," "you figured out a tricky bug" — reinforce growth

**The principle:** your job isn't to be the smartest person in the room — it's to **make everyone in the room smarter**.

---

## 3. How to Implement

### Code Review as Mentoring

```markdown
## Instead of: "Change this."
## Use feedback that teaches:

❌ "Wrong. Use a repository."
✅ "Nice start! Right now the controller talks to the DB directly.
    We use the repository pattern here so business logic stays
    separate from data access — want to try extracting an OrderRepo?
    I can pair on it if helpful."

## Explain the WHY:
❌ "Add a test."
✅ "Add a test for the empty-cart case — if someone later changes the
    discount logic, this test catches the regression. Here's an example
    of how we structure these."

## Ask, don't tell (guides them to the answer):
❌ "The bug is on line 42."
✅ "What happens if `items` is empty here? Walk me through it."
```

### Pair Programming — Teach Through Doing

```markdown
## Effective pairing:
- **Driver/navigator** — one types, one thinks ahead; swap every 20-30 min
- **Narrate your thinking** — "I'm checking the DB index first because..."
- **Let them drive** on things they're learning; you navigate/guide
- **Ask questions** — "what do you think we should do next?"
- NOT: you typing while they watch (that's just watching, not learning)
```

### Knowledge Sharing — Multiply the Learning

```markdown
## Make individual knowledge into team knowledge:
- **Document patterns** — "how we structure a new service," "our testing conventions"
- **Short sessions** — 15-min walkthroughs of a tricky concept or recent learning
- **Answer questions publicly** (Slack channel) — others learn from each Q&A
- **Pair on onboarding** — walk a new hire through the codebase; they retain it
- **Explain the WHY** — understanding rationale beats memorizing rules
```

### Foster Psychological Safety

```markdown
## Make it safe to learn (and fail):
- **Normalize not-knowing** — "I don't know either, let's figure it out"
- **Model curiosity** — ask questions yourself; show learning is continuous
- **Separate the person from the mistake** — review the code, not the coder
- **Celebrate good questions and learning** — "great question" goes far
- **Share your own mistakes** — "I broke prod once by..." builds trust
```

### Mentorship Checklist

- [ ] **Code reviews teach**, not just correct (explain why, ask guiding questions)
- [ ] **Pair programming** used for hard problems / skill transfer
- [ ] **Knowledge documented** — patterns, conventions, "how to" guides
- [ ] **Questions welcomed** — no "dumb question" stigma
- [ ] **Feedback is constructive** — builds up, explains rationale
- [ ] **Psychological safety** fostered — mistakes are learning, not failure
- [ ] **Ownership grown gradually** — juniors take on more over time
- [ ] **Your own learning modeled** — seniors don't pretend to know everything

### Avoid These

- **"Just fix it" reviews** — corrects without teaching; the junior doesn't grow
- **Typing while they watch** — pair programming requires their hands on the keyboard
- **Answering instead of guiding** — handing answers blocks learning to find them
- **Harsh or personal feedback** — destroys psychological safety; people stop asking
- **Knowledge hoarding** — being the "only one who knows X" (bus factor = 1)
- **Treating questions as interruptions** — every question is a teaching moment
- **Perfectionism imposed on juniors** — they need room to make and learn from mistakes
