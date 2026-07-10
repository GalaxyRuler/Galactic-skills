---
name: research-grounding
description: Use when giving recommendations, comparing or choosing a tool/library/model/service, estimating costs or pricing, proposing a plan or architecture the user will act on, or stating version/benchmark/"state-of-the-art"/best-option/latest claims that could be outdated. Also use when the user asks "is this grounded?", "are your suggestions online-search grounded?", or to verify a plan before calling it solid.
---

# Research Grounding

## Overview

Recommendations, comparisons, version facts, prices, and benchmarks drift; training data lags reality. **Before presenting any such claim as solid, verify it with a current web search and cite the source.** This is a standing, repeatedly-stated user requirement across projects — not optional polish.

## When to use

- Recommending or ranking tools, libraries, models, services, or approaches
- "Best", "latest", "cheapest", "fastest", "state-of-the-art" claims
- Version numbers, release status, deprecations, API/SDK shapes
- Cost / pricing / quota / token-spend estimates
- Proposing a plan or architecture the user will act on
- Any external fact that could have changed since training
- User asks: "is this grounded?", "are your suggestions online-search grounded?"

**When NOT:** pure reasoning about the user's own code/files, clearly-labeled opinion, or facts the user just supplied.

## Workflow

1. Before asserting, list the claims that could be stale.
2. Search for each — WebSearch for general facts/prices/benchmarks; Context7 for library/SDK/API docs.
3. Cite sources inline (name + link). Prefer official/primary sources; check the page date.
4. State assumptions explicitly. Label anything you could NOT verify as **unverified**.
5. Only then present the recommendation/plan as "solid."

## Red flags — STOP, search first

- About to say "best / latest / cheapest / state-of-the-art" with no citation
- Quoting a price, version, model name, or benchmark from memory
- A plan hinges on an external tool's *current* capabilities
- Thinking "I'm pretty sure this is still true"

## Rationalizations — all wrong

| Excuse | Reality |
|---|---|
| "I already know this" | Training lags; verify anyway. |
| "Searching is slower" | A wrong recommendation costs far more rework. |
| "It probably hasn't changed" | Prices, models, and APIs change monthly. Check. |
| "User is in a hurry" | Ground at least the load-bearing claims. |

## Common mistakes

- Citing a source without reading its date (stale page).
- Grounding the easy claims, asserting the hard ones from memory.
- Burying assumptions instead of stating them up front.
