# Targeted memory-mechanism update — 2026-11-07

This update follows a focused set of recent model and deployment questions. Public annotations are grounded in the linked primary papers, author reports, model cards and pinned code. Private notes, screenshots and proposed experiments are not redistributed. This is not a new exhaustive literature search or a claim of full-paper review for the entire catalogue.

The public view contains **640 papers/reports + 22 pre-publication methods = 662 entries**. Twelve paper-associated deployment audits are attached to paper details, with old record IDs preserved as aliases. The canonical implementation file retains all 34 audits. “Pre-publication” means no matching standalone publication has been verified; the code itself may be officially released.

## Classification decisions

Keep **World Models & WAM → methods**, **VLA → methods**, and **Agentic Robotics → methods**, with Supporting Foundations as a separate supporting domain. WAM and VLA identify model interfaces, whereas Agentic Robotics describes the planning/execution system around models. They are not mutually exclusive capability claims. A primary home prevents duplicated totals; mechanism tags express overlaps.

The short label **VLA** is appropriate for navigation, provided the scope explicitly includes memory-relevant visuomotor precursors. HWM-0 and Liber-0 Preview primarily illustrate planner state and planner–policy handoff; classifying them only by their low-level WAM would hide this distinction.

Add four cross-domain tags: **visual compression**, **multiple time scales**, **memory routing**, and **planner–policy handoff**. Keep the 24 method families: compression, retrieval, temporal sampling and hierarchical control can coexist, so these details should not create competing top-level domains. Biological terms remain explanatory analogies, not evidence of implementation equivalence.

## Method-by-method reconciliation

| Work or deployment | Primary home | Reconciled observation |
|---|---|---|
| [Video Prediction Policy 2: Predict Better, Act Better](https://arxiv.org/abs/2610.10270v4) | World Models & WAM → Imagination & action coupling | Keep the core paper and RoboDojo Action2B history/episode-anchor deployment distinct; the deployment audit is attached to the paper. |
| [Awomo-0.5 Technical Report](https://awomo-westlakedi.github.io/Awomo-0.5-page/assets/awomo-0.5-report.pdf) | World Models & WAM → Imagination & action coupling | Distinguish image-action visual/semantic history from causal video history; model-family names do not imply an identical cache lifecycle. |
| [Simate-beta](https://github.com/XPolicyLab/XPolicyLab/blob/0075cc96a1bf24c5d66a4a3a5e29eae6d739fef3/policy/Simate_beta/README.md#L152-L171) | VLA → Compressed & recurrent memory | Move to compressed VLA memory: 25 sampled frames become 400 historical tokens in the inspected configuration. |
| [Liber-0 Lite](https://github.com/XPolicyLab/XPolicyLab/blob/6baccd57ff958570d0db1588370289ee36c8bb70/policy/Liber_0_lite/model.py#L77-L100) | World Models & WAM → History windows & caches | New method: a fixed initial head-camera cue accompanies current views; this is an episode anchor, not a retrieved long-term archive. |
| [Liber-0 Preview](https://github.com/XPolicyLab/XPolicyLab/blob/6baccd57ff958570d0db1588370289ee36c8bb70/policy/Liber_0_preview/generation.py#L186-L213) | Agentic Robotics → Task state & long-horizon planning | New method: retain plan and prior-subtask state, with a visual cue refreshed at subtask transitions; appending a prior subtask is not proof of completion. |
| [Rex-M1-preview](https://github.com/XPolicyLab/XPolicyLab/blob/0075cc96a1bf24c5d66a4a3a5e29eae6d739fef3/policy/Rex_M1_preview/rex_m1/configs/data/robodojo_all_arx_x5.yaml#L20-L30) | VLA → History inputs & temporal caches | Retain the history-input family and add visual compression as a cross-cutting tag; sampled observations and their token budget are separate properties. |
| [InternW0-Delta: A World Action Model Bridging Predictive Dynamics and Actions with 20K+ Hours of Open Data](https://arxiv.org/abs/2609.31394v1) | World Models & WAM → Imagination & action coupling | Attach the RoboDojo audit of anchor, recent and current observation conditioning; do not generalize the adapter recipe to every checkpoint. |
| [DM0.5 / OpenDM MEM](https://github.com/dexmal/opendm) | VLA → Compressed & recurrent memory | New method: the inspected RoboDojo recipe uses 20 head-history slots at 1 Hz and 16 tokens per image; the 32-slot training example is a different configuration. |
| [Long-WAM: Scaling the Context of World-Action Models](https://arxiv.org/abs/2610.10528v1) | World Models & WAM → History windows & caches | Keep context length separate from evidence of history use; the reported long-history benefit depends on autoregressive initialization. |
| [Flex-π: A Multi-Stream World-Action Model with Compute Flexibility](https://arxiv.org/abs/2608.10860v3) | World Models & WAM → Imagination & action coupling | Retain as a boundary case: multiple prediction streams and action queues do not establish retained observation memory in the inspected deployment. |
| [HWM-0 Preview](https://github.com/Antu3heng/XPolicyLab/blob/1ddc01bd90396ef37f8345697caf5b7c0fd882d9/policy/HWM_0_preview/hwm/model/memory.py#L68-L80) | Agentic Robotics → Task state & long-horizon planning | Move to agentic task-state planning: gated semantic/subtask updates interact with compressed visual history and downstream world/action conditioning. |
| [WALL-OSS 1.0 Lite](https://github.com/StarrickLiu/XPolicyLab/blob/8e7838e9e076862737922cc54429ec6d42ef2c2d/policy/WallX/model.py#L60-L79) | VLA → Episodes, keyframes & retrieval | Use the author release name WALL-OSS 1.0 Lite and retain Wall-X aliases; selective keyframes belong under episodic/keyframe retrieval. |
| [G07-preview](https://github.com/yuantianyuan01/XPolicyLab/blob/719a8600fd90e381a42b2140c5d4711022d100ac/policy/G07_preview/src/galaxea_va/inference/memory_router.py#L15-L18) | World Models & WAM → History windows & caches | Add memory routing: an episode-level instruction decision controls short/long history use in the inspected implementation. |
| [Phoenix-MWA](https://github.com/ssssxt/XPolicyLab/blob/40a71e9f1e83543996eb0629173ca6b998a25d46/policy/Phoenix_MWA/runtime/configs/inference/phoenix_robotwin.yaml#L218-L229) | World Models & WAM → Imagination & action coupling | Preserve the enabled-configuration boundary: history-capable shared code does not imply active visual memory in the inspected release. |
| [WorldBridge: Bridging Video and Action for Task Generalization in World Action Models](https://arxiv.org/abs/2610.40748v1) | World Models & WAM → History windows & caches | New paper: short/long observed history is compressed into causal-VAE conditioning. Interpret the controlled memory ablation separately from leaderboard totals and latency checkpoints. |
| [MEM: Multi-Scale Embodied Memory for Vision Language Action Models](https://arxiv.org/abs/2603.03596v2) | VLA → Task progress & plan state | Separate short visual history from semantic memory; in-context recovery is conditioned on correction-data training, not established by memory alone. |

## What these cases suggest

1. **Memory ownership matters.** Record who writes state, who consumes it, what crosses the planner–policy boundary and when it resets. A text plan inside a VLM, a visual cue sent to a policy and a policy KV cache are different states even in one robot system.
2. **Capacity is not utilization.** Distinguish observation span, temporal sampling, token compression and retrieval. Compare memory interventions while holding training recipe, policy, inference budget and task protocol fixed; total benchmark ranks do not isolate a memory contribution.
3. **Hierarchy introduces update errors.** A retained subtask list can preserve useful progress or preserve a mistaken transition. Evaluate stale goals, missing visual evidence, recovery after corrections and whether a handoff exposes enough information to the lower-level model.
4. **Compression needs task-sensitive evidence.** Uniform pooling and causal video encoding offer different retention costs. Accuracy or success should be assessed alongside write/read latency, temporal gaps, missing-history masks and sensitivity to the historical event needed by the task.
5. **Runtime memory should be auditable.** Keep episode identity, observation times, source/version provenance, reset events and correction history in the surrounding harness. The value of a larger or cross-episode memory must be measured under an explicit persistence and retrieval policy. These are design questions, not experimentally established recommendations from this curation update.

## Primary evidence added in this update

- [WorldBridge v1](https://arxiv.org/html/2610.40748v1): Sections 2.1.2, 2.1.4 and 2.3.3; Table 6 memory ablations; Table 8 latency checkpoint scope.
- [MEM v1](https://arxiv.org/html/2603.03596v1): visual/semantic memory and correction-data conditions for in-context adaptation. The existing catalogue citation remains pinned to its recorded v2 source.
- [XPolicyLab pinned commit](https://github.com/XPolicyLab/XPolicyLab/tree/6baccd57ff958570d0db1588370289ee36c8bb70): Liber-0 Lite, Liber-0 Preview, OpenDM, VPP2, InternW0 and updated WallX deployment documentation. Individual records retain exact files, line ranges and SHA-256 hashes.
- [OpenDM pinned commit](https://github.com/dexmal/opendm/tree/03f799120d425ead51d9482bb1da950b6dabade9): history encoding, token pooling and deployment/training recipe distinctions.
- [WALL-OSS 1.0 Lite author model card](https://huggingface.co/x-square-robot/wall-oss-1.0-lite-robodojo): release identity and deployment scope. Older Wall-X source evidence is retained rather than silently relabeled as a new code audit.

No models, robot rollouts or benchmark experiments were run. Publication placeholders remain in the [pending reference list](pending-references.md), not in the paper bibliography.
