# Contributing

[简体中文](CONTRIBUTING.zh-CN.md)

Bring a primary source and a clear account of the memory mechanism. A paper need not use the word “memory,” but its relevance must be specific. Correcting a boundary or removing an unsupported claim is as valuable as adding a work.

## Add a research work

1. Check `data/papers.json` for its unversioned arXiv ID, DOI and normalized title. A journal or conference version of the same work does not automatically create a second entry.
2. Verify title, authors, first publication date, actual source version and primary URL. Preserve a source SHA-256 and state exactly what was hashed. Do not substitute access date for publication date.
3. Read enough of the source to establish retained information, lifetime and consumer. Abstract screening is allowed, but must be labeled; do not call it a full-paper audit. If those facts are unclear, mark scope as contextual or defer inclusion.
4. Assign one `primary_domain` and one `method_family` from `data/taxonomy.json`. Add mechanism tags for overlap. Keep research role (`primary`, `context`, `survey`) separate from reading depth and publication status.
5. Write independent `summary_en` / `summary_zh` and `analysis_en` / `analysis_zh`. Summaries describe the source; analysis states a limitation, comparison or research question. Do not manufacture quantitative gains, hardware facts, ablations or peer review.
6. Include `memory_relevance_en/zh`, a truthful `review_depth`, an evidence locator, discovery provenance and BibTeX. Use `first_included` and `inclusion_batch` to preserve release history.

Add a complete, compact sentence in `tldr_en` and `tldr_zh` for the table: target 12–22 English words and 25–55 Chinese characters (hard limits: 30 words / 75 characters). State the distinctive mechanism; retain material boundaries such as training-only retrieval. Keep the fuller summary and analysis for the website's notes.

Only add `code_url` or `project_url` with a matching `link_evidence` entry identifying its primary source, date and field. An empty repository, webpage template, announced release or unrelated redirect is not released implementation code. Preserve unavailable links in provenance with their status, rather than presenting a normal Code badge. `publication_label` requires `publication_evidence`; distinguish author-reported venue information from independently checked publisher records, and do not relabel the first arXiv date as a conference publication date.

The schema and validator are the executable specification. Existing records preserve legacy taxonomy fields so the companion manuscript can remain a fixed snapshot.

## Add or update a code observation

Use `data/implementations.json`. Record the fixed commit, exact file/line evidence, enabled configuration, state lifetime, reset behavior, and consumer/handoff. Translate both the six axes and deployment notes. Keep `Method: TODO ref` when no matching standalone publication has been verified. A parent model's paper does not automatically cite a later deployment variant. Preserve older inspected commits when a PR head changes.

Pending methods appear in the unified Research list under **Pre-publication methods**. When a matching paper is verified, populate `related_ids`; the build attaches that audit to the paper and preserves the old record ID as an alias. Do not merge distinct methods solely because they share a backbone. README code badges show live stars for actual repositories; benchmark PR/fork evidence stays a plain Code link.

## Build and check

Python 3.9+ is sufficient; the site has no runtime dependencies.

```sh
python3 scripts/validate.py
python3 scripts/build.py
python3 scripts/check_site.py
node --check website/assets/app.js
node --check website/assets/i18n.js
node --check website/assets/constellation.js
python3 -m http.server 8765 --directory website
```

Check both languages, a domain/method query, empty results, a paper detail, a code detail, citation export, and three-way comparison. Do not hand-edit the generated README or `website/assets/catalogue.*`.

For visual changes, also check constellation → catalogue filtering, year filters, keyboard navigation, reduced-motion/pause behavior, and a narrow mobile viewport. The star map represents the editorial taxonomy, not citation relations or performance rankings.

## Evidence and permissions

AI assistance must not be represented as full independent human reading. Keep unsupported or ambiguous claims visibly bounded. Do not add private experiments, credentials, complete paper PDFs, copied repository trees, or raw third-party abstracts to the public package. Editorial content is contributed under CC BY 4.0, code under MIT, subject to [NOTICE.md](NOTICE.md); only contribute material you have the right to contribute.
