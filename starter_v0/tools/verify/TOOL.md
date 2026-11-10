---
name: verify
track: bonus
kind: local_knowledge
provider: local
requires_env: []
inputs: [claim, sources]
outputs: [claim, status, source_count, sources]
side_effect: false
---

Compare evidence for one claim and flag conflicting information. First gather
sources using lookup/fetch, read their text, then supply each URL, an evidence
quote, and its stance toward the claim: supports, contradicts, or unclear.
Never invent quotes or infer support from search rank alone.

Returns conflicting when evidence both supports and contradicts the claim,
corroborated or contradicted when at least two distinct hosts agree, and
insufficient_evidence otherwise (including unclear evidence). Empty sources
are insufficient; invalid input returns an error dict.

This tool compares supplied labels; it does not fetch URLs or independently
judge the text. Distinct hosts (ignoring www.) approximate independence, not
publisher ownership: exclude syndicated copies and related publishers before
calling. Results are evidence summaries, not proof that a claim is true.
