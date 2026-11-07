# Evidence, inclusion and coverage

[简体中文](methodology.zh-CN.md)

This is a living **purposive scoping collection**, not an exhaustive systematic review or a claim that all eligible papers have been found. The 2026-11-02 edition contains **639 distinct research works**, including **44 supporting references**, plus **29 separately counted implementation observations**. Three industrial essays remain outside both counts. The catalogue records 635 arXiv works and four public reports; a report's unknown date is not replaced by its access date.

## How coverage grew

The prior edition contained 287 works (the original 275-work manuscript collection and a targeted 12-work follow-up). The 2026-11-02 expansion added **352** distinct works: 115 from world-model searches, 109 from VLA/visuomotor searches, and 128 from embodied-agent searches. Collection batch and scientific domain are deliberately separate: for example, a policy-memory work discovered during agent searches belongs in VLA.

Searches used official arXiv queries, selected-ID verification, prior reading and discovery leads from the two acknowledged community lists. Titles, authors, stable IDs, source versions, first arXiv submission dates and complete abstracts were checked for the additions. Raw evidence remains in local working caches; public [discovery metadata](../assets/discovery_log.json) lists the query provenance and accepted IDs without redistributing author abstracts.

| Discovery batch | Candidate records in that batch | Accepted additions |
|---|---:|---:|
| World models / WAM | 306 | 115 |
| VLA / visuomotor policies | 834 | 109 |
| Embodied agents / robotics | 483 | 128 |

Candidate pools overlap, search responses are capped, and not every discovered candidate received abstract review. **Do not add the candidate counts into a systematic-review flow diagram.** The VLA batch separately records 17 abstract-reviewed exclusions, 637 title-screened/not-selected records and 71 existing duplicates. The agent batch records 131 individually reviewed abstracts (128 accepted, three excluded), seven existing duplicates and 345 discovery-only candidates. The WAM working log distinguishes accepted, existing, deferred and neighboring-domain records.

## Inclusion and boundaries

Include a work when the primary source establishes a retained state and a later consumer, evaluates memory-sensitive behavior, or provides a specifically relevant precursor/baseline. Use `primary` for direct relevance, `context` for a boundary or precursor, and `survey` for an existing synthesis. These roles do not imply full-text reading, peer review, independent replication, or a new memory architecture.

World Models & WAM includes relevant long-video and world-state mechanisms; not every generator is an action-conditioned robot model. VLA includes memory-relevant visuomotor predecessors. Agentic Robotics covers embodied task/spatial/episodic/procedural memory and the planning/execution/harness system layer. General language-agent memory and selected baselines are visibly supporting material. One primary domain and method family supply non-duplicated counts; mechanism tags connect domains.

The 2026-11-02 snapshot had 485 directly relevant works, 148 contextual/boundary works and 6 surveys. Its domain counts were World Models & WAM 235, VLA 203, Agentic Robotics 157, Supporting Foundations 44.

## Reading depth and evidence hierarchy

All **352 additions are abstract-reviewed**. Existing records retain their original reading depth (abstract screening, abstract plus selected body passages, focused source audit, or code/source audit). Summaries are conservative independent paraphrases; analysis is editorial synthesis. No new performance numbers, full-paper audits or reproduced model results are implied by this expansion.

1. Primary paper/report and verified bibliographic metadata support source-level claims.
2. Pinned code/configuration supports a narrow implementation observation.
3. Contributor documentation is explicitly attributed.
4. Editorial analysis and suggested experiments are labeled as interpretation.

No training, simulation, robot rollout or leaderboard reproduction was conducted. Different evaluation protocols are not merged into a performance ranking. The original companion manuscript remains a **287-work snapshot** until its methodology and claims are separately revised.

## Citation and version integrity

Stable arXiv IDs, normalized titles and DOIs are checked for duplicates; versions do not create additional works. Known same-method preprint variants are consolidated when source evidence establishes continuity. A first arXiv submission date is not necessarily the earliest venue date. Publication venues are not invented or silently normalized. Source hashes specify whether they cover original HTML or a serialized official Atom entry, not interchangeable PDF checksums.

In the 2026-11-02 snapshot, nineteen implementation variants retained `Method: TODO ref`. This means a matching standalone publication was not verified, not that no paper exists anywhere or will necessarily appear. Parent-paper links do not validate every later configuration. See [pending references](pending-references.md).

## Reuse and maintenance

AI assisted discovery, synthesis, translation and validation; this is not a declaration of independent human full-paper reading. Corrections are welcome. Public packages exclude private logs, full PDFs, raw abstracts and source trees. Original editorial content is CC BY 4.0; code is MIT, with boundaries in [NOTICE](NOTICE.md).

## 2026-11-07 resource and presentation update (before the targeted follow-up)

At this stage the research corpus was unchanged. All 639 works now have an additional one-sentence bilingual TL;DR derived from the existing annotations, not a new full-text audit. We checked author-supplied resource links in 635 arXiv records and four reports, then followed project pages and inspected 241 candidate code destinations. The display includes 219 links with visible matching implementation or benchmark files and 267 author-linked project sites. We suppressed 18 empty, announced-only, website-only, outdated or mismatched code destinations and four unreachable links; the latter are not labeled empty. Status and provenance remain in each record. This inspection did not install, execute or reproduce the code.

There are 167 paper venue labels from author metadata, including 15 explicitly marked workshops, plus four technical-report labels. Author comments/journal references or an author repository support these labels; this is not independent publisher verification for every entry. Dates remain first public arXiv/report records, and can differ from a venue year. See [resource audit counts](../assets/resource_audit.json).

The star map is an editorial taxonomy visualization: a domain connects to its method families. It does not encode citation, anatomical, performance or causal relationships. Timeline counts refer to the selected domain/method corpus, independently of keyword and other filters.

## 2026-11-07 targeted memory-mechanism follow-up

The current catalogue contains **640 papers and reports** (636 arXiv works, four reports) and **22 pre-publication methods**, yielding **662 public entries**. The canonical data retain **34 deployment audits**: 22 pending methods plus 12 audits attached to matching paper details. Attached audits do not add another public work. Three industrial essays remain outside these counts.

This targeted follow-up adds WorldBridge, three code methods (Liber-0 Lite, Liber-0 Preview and DM0.5/OpenDM MEM), and two paper-associated deployment audits (VPP2 and InternW0). It also revises selected annotations and classification boundaries. This is a focused primary-text/code inspection, not another exhaustive search or a full review of all catalogue entries. The 352-work expansion's abstract-review status is unchanged.

Paper roles are now 486 primary, 148 contextual/boundary and 6 surveys. Paper domains are WAM 236, VLA 203, Agentic Robotics 157 and Supporting Foundations 44. Including pending methods, the public domain counts are 242, 209, 167 and 44. The source filter distinguishes pre-publication methods from papers/reports; it does not imply their code is unofficial.

The hierarchy remains three main domains plus supporting foundations and 24 method families. Four cross-domain tags add visual compression, multiple time scales, memory routing and planner–policy handoff. VLA is the concise display name; explicitly relevant visuomotor precursors remain within its scope. See the [method-by-method update](curation-update-2026-11-07.md).

Years through 2017 share one timeline bucket. An undated method remains undated; its inspection date is displayed as “Checked” and is never used as a publication year. Deployment variants retain separate source pins even when their notes appear beside a paper. The living catalogue update does not change the companion manuscript's fixed corpus.

## 2026-11-07 timeline date reconciliation

The 22 pending methods and three reports previously left in Undated now use verified code/PR or repository-record dates for the timeline. All belong to 2026. This supplements the timeline without replacing uncertain bibliographic publication dates or TODO references. [Per-record dates and primary evidence](date-audit-2026-11-07.md) state the exact basis. The time axis is a public-record chronology, not a uniform peer-reviewed publication chronology.
