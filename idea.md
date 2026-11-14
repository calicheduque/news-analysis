# Let’s slow down. What we’re building and why.

## The problem (in one sentence)

**People say one thing in public and do another in private.** Media reports what officials, statistics, and headlines say. But it doesn’t report what affected people actually live. That gap is where the uncomfortable truth lives.

Real example:
- **Public headline:** “Rent prices are falling in NYC.”
- **Private experience:** renters in Harlem say their rent went up 12% this year.
- **The gap:** the statistic is true on average, but false for a huge segment.

Today nobody connects those two things in one place. Journalists have public data but no access to the private. Surveys have access to the private but don’t verify the public.

## What we’re building (in one sentence)

**An agent that takes a public claim, searches public evidence, consults affected people via Flashpoint.AI, and writes a short article showing where they agree and where they diverge — labeling every statement as human, synthetic, public, or unverified.**

That’s it. Not a platform. Not a full app. It’s **one flow** that produces **one article**.

## What it looks like in practice

A judge types into the UI:

> “Rent prices are falling in NYC.”

The agent automatically does this:

1. **Decomposes** the claim into verifiable sub-claims:
   - Which metric? Which period? Which neighborhood? For whom?

2. **Searches public evidence:**
   - News, official data, reports. Finds: “Median asking rent fell 2.1% borough-wide.”

3. **Consults affected people via Flashpoint.AI:**
   - Asks renters in Harlem: “Did your rent go up in the last 12 months?”
   - Answer: “Yes, ~12%.”
   - Asks small landlords in Queens: “Have you lowered rent?”
   - Answer: “No, I kept it flat but gave concessions.”

4. **Synthesizes with Anthropic:**
   - Compares public with private.
   - Detects the divergence.
   - Assigns a confidence score.

5. **Produces the article:**

```
# Claim: “Rent prices are falling in NYC.”
**Confidence: 58% — Partially verified**

## What was claimed
...

## What public evidence shows
[HUMAN] Median asking rent fell 2.1% borough-wide (source: X).
[SYNTHETIC] Simulated small landlords in Queens expect to hold rents flat.

## What affected people say privately
[HUMAN] Renters in Harlem report renewals up 10–15% (n=34).
[SYNTHETIC] Simulated renters in Brooklyn report mixed experience.

## Where narrative and experience diverge
The average is falling. The experience is not. Renters in Harlem
are seeing increases while the borough-wide median drops.

## What we could NOT verify
Whether this trend continues next quarter.
Whether our sample is representative.

## Methodology and limitations
...
```

## Why this matters (and why it wins)

1. **It uses Flashpoint.AI’s core capability:** reaching people surveys don’t reach. That is literally what the company sells.
2. **It uses Anthropic for what it’s good at:** reasoning, decomposing, synthesizing, writing with nuance.
3. **It produces something a journalist or decision-maker would use tomorrow:** a short, verifiable article that’s honest about its limits.
4. **Honesty is the differentiator:** the “What we could NOT verify” section and the provenance badges make the output credible. Any AI can write an article. Very few can tell you what they don’t know.
5. **It’s demoable in 2 minutes:** one claim, one button, one article with colored badges. The jury understands it without a technical explanation.

## Why track #4 and not another

The other tracks are valid too, but #4 is the easiest to demo in one day because:
- **The input is trivial:** a text string.
- **The output is tangible:** an article you can read.
- **The comparison is visual:** public vs. private, side by side.
- **It doesn’t require financial validation** (like #5) or live market data (like #2).
- **The jury can judge it without being technical:** “Does this article tell me something I didn’t know? Is it honest about what it doesn’t know?”

## What each person does (in one sentence)

- **A** connects the agent to Flashpoint.AI and Anthropic: receives the claim, calls the APIs, returns the article.
- **B** builds the screen: claim input, button, article with colored badges, chat box.
- **C** writes the prompts that make the agent think well, picks the demo claim, defines the confidence logic, and writes the pitch.

## The sentence that sums it all up

**“We take a public claim, contrast it with the private experience of real people via Flashpoint.AI, and write an article that says what’s true, what’s synthetic, what’s public, and what we don’t know.”**

That’s what we’re building. That’s what track #4 demonstrates. And that’s what the jury will remember.
