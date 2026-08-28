# Arabic (Saudi / GCC) editorial layer

Load when `locale = ar-SA-GCC`. This is a **localization layer over the same editorial engine**, not a translation formatter. Thesis, ledger, gates, and rubric are unchanged; language, terminology, geography, evidence sourcing, and examples are not.

An Arabic edition built from an approved English argument is a `localize` job, not a `translate` job. It shares the research backbone and may legitimately become a different article in rhetorical execution — different opening, different examples, different order.

## 1. Language base

Polished contemporary **Modern Standard Arabic** at professional register. Direct and respectful.

- No ceremonial throat-clearing. `في ظل التطورات المتسارعة التي يشهدها العالم اليوم` is the Arabic equivalent of "In today's fast-paced world" — cut it.
- No newspaper archaism unless the format genuinely calls for it.
- No colloquial dialect unless the requested format is deliberately conversational.
- Sentence and paragraph complexity suited to a senior business reader.

**Do not import English readability formulas.** Flesch and Flesch–Kincaid are calibrated on English syllable and word-length statistics and do not transfer to Arabic morphology. Judge Arabic complexity on Arabic terms — sentence length, subordination depth, nominal-chain length (`إضافة` chains), and density of unglossed specialist terms — or against an Arabic-native readability resource. Do not report an English readability score for Arabic text.

## 2. Author, do not calque

Translate meaning and rhetorical function. Reconstruct the sentence natively; do not preserve English syntax.

| Calque (reconstructable only via the English behind it) | Localized business Arabic |
|---|---|
| `تحتاج الشركات إلى رافعة قدراتها الرقمية من أجل قيادة القيمة عبر رحلة التحول.` | `تحتاج الشركات إلى تطوير قدراتها الرقمية بحيث ترتبط كل استثمارات التقنية بنتيجة تشغيلية أو مالية قابلة للقياس.` |

Tells that a passage is translated rather than authored: `عبر رحلة` for "across the journey", `قيادة القيمة` for "drive value", `رافعة` as a verb for "leverage", chained `من خلال`/`من أجل` where Arabic would subordinate differently, and English adverbial fronting preserved intact.

### Before / after

**Before** — grammatical, intellectually empty, and stacked with the standard Arabic AI-writing openers (`في ظل`, `يشهد`, `أصبح من الضروري`, `مواكبة`, `الاستفادة من الفرص`):

> في ظل التطورات المتسارعة التي يشهدها العالم اليوم، يشهد الذكاء الاصطناعي نمواً كبيراً في المملكة، وأصبح من الضروري على الشركات مواكبة هذا التطور من أجل الاستفادة من الفرص وتعزيز الكفاءة والابتكار وتحقيق التنافسية في المستقبل.

**After** — a proposition, a mechanism, and a management decision:

> التحدي أمام الشركات السعودية ليس في تبنّي الذكاء الاصطناعي بحد ذاته، بل في تحديد أين تنتهي توصية النظام وأين تبدأ مسؤولية الإنسان. فكلما توسعت الأتمتة من دون قواعد واضحة للصلاحيات والمساءلة، قد ترتفع سرعة التنفيذ بينما تصبح مسؤولية القرار أقل وضوحاً. لذلك، لا ينبغي أن يبدأ برنامج الذكاء الاصطناعي بقائمة للأدوات؛ بل بخريطة للقرارات التي يمكن للنظام أن ينفذها، وتلك التي يوصي بها فقط، وتلك التي يجب أن تبقى تحت مسؤولية بشرية مباشرة.

The rewrite still needs evidence. A well-formed sentence is not a verified one.

## 3. Geographic scope — hard gate

**Never widen Saudi evidence into a GCC-wide claim.** Label the scope of every geographic claim to match its evidence, and no wider:

```
السعودية            evidence covers Saudi Arabia only
الإمارات            evidence covers the UAE only
دول مجلس التعاون    evidence covers the GCC states (name which)
المنطقة             regional framing — only with regional evidence
```

A brief asking for "GCC" backed by Saudi-only sources gets one of two answers: narrow the claim to Saudi Arabia, or research the other states. Never split the difference with vague regional phrasing. Treat this as an evidence gate, not a style preference — it is the most common way an Arabic business article becomes false.

The same rule applies in reverse: GCC-aggregate data does not license a claim about Saudi Arabia specifically.

## 4. Terminology

Check the project termbase before coining a term. Prefer the established official Arabic term over an invented transliteration. Where no settled Arabic equivalent exists, give the Arabic explanatory term with the English in parentheses **on first occurrence only**.

Termbase entry format:

```yaml
terms:
  - concept: artificial intelligence
    preferred_ar: الذكاء الاصطناعي
    forbidden_ar: الذكاء الصناعي
    domain: technology

  - concept: governance
    preferred_ar: الحوكمة
    domain: management
    context_notes:
      - Do not substitute الإدارة when governance is meant — it loses the
        accountability sense and reads as day-to-day management.

  - concept: decision rights
    preferred_ar: صلاحيات اتخاذ القرار
    domain: management

  - concept: private equity
    preferred_ar: الملكية الخاصة
    alternatives: [الاستثمار في الملكية الخاصة]
    domain: finance
```

Seed the termbase per project and verify domain terms against a recognized Arabic terminology authority rather than model memory. Consistency inside a project matters more than picking the single "best" variant: one concept, one term, every article.

**Institution and program names:** on first mention use the verified official Arabic name. Never translate a regulator, ministry, fund, or national-program name from memory — look it up or mark `[VERIFY]`. A plausible-sounding but wrong official name is a fabrication.

## 5. Numbers

- One numeral convention per publication, applied consistently.
- Every figure carries currency, period, denominator, and comparison basis.
- Explain a large percentage change when the base is small — "grew 300%" off a base of four is a different fact from the one the number implies.
- Convert or gloss units and fiscal periods where a local reader would otherwise mis-read them.

## 6. Evidence routing

Route legal, economic, statistical, and regulatory claims to the relevant Saudi or GCC authority **first** — the regulator, the official statistics body, the primary text — before any international summary or secondary report. An English-language summary of a Saudi regulation is a tier-B source describing a tier-A one; cite the tier-A source.

Local context, regulatory depth, and figures interpreted against local conditions are the differentiating value of Arabic business analysis. Numbers restated without local comparison, indicator, or regulatory framing are the commodity part — the part that is worth the least.

Ask of every Arabic piece: **what does this mean in Saudi Arabia specifically?** An article that would read identically about any market has not been localized.

## 7. Cultural care

- Do not generalize personal, religious, family, or gender norms.
- Do not use religious expressions as decorative business rhetoric.
- No "Saudi consumers prefer X" without evidence — audience claims are factual claims and go in the ledger like any other.
- Do not treat "GCC culture" as one reader persona. The states differ; so do sectors and generations inside them. Validate register choices against actual audience data, not assumption.

## 8. Arabic-specific checks

Add to the standard gate pass:

| Check | Fail condition |
|---|---|
| Geographic scope | Any claim labeled broader than its evidence supports |
| Institution names | An official name written from memory rather than verified |
| Calque scan | Sentences reconstructable only through the English behind them |
| Termbase compliance | A concept rendered inconsistently across the piece or against the termbase |
| Transliteration discipline | An invented transliteration where an established Arabic term exists |
| Register | Ceremonial filler, dialect leakage, or archaism inappropriate to the format |
| Readability method | An English readability score reported for Arabic text |
| Numbers | A figure without currency, period, denominator, or comparison basis |

## 9. Bilingual editions

When producing both editions from one research backbone:

**Preserve** — thesis, evidence integrity, every factual qualification and hedge.
**Rebuild** — opening, examples, idiom, sentence structure, terminology, headline, and the closing implication.

Flag every English example that should be replaced by a Saudi or GCC one. Re-run the evidence audit on the Arabic edition; localization moves claims, and a qualification lost in the rebuild is an evidence regression, not a style change.

Do not publish the Arabic edition as a mirror of the English on the assumption that a translated article is an equivalent article.
