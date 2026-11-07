# Domain and method taxonomy

The primary home supplies non-duplicated counts; mechanism tags support cross-domain discovery. Domains are not mutually exclusive capability claims. Original manuscript mappings remain in each record’s legacy fields.

## World Models & WAM

Video and latent world models, persistent world state, and world-action models. Video generation is a relevant precursor, not automatically a robot policy.

- **History windows & caches** (`world-models--observed-history`): Observed history at one or more temporal scales, initial anchors, rolling windows, and cache retention policies.
- **Compression & recurrent dynamics** (`world-models--compression-recurrence`): Compact historical states, latent recurrence, and state-space dynamics.
- **Retrieval & spatial grounding** (`world-models--retrieval-spatial`): Addressable evidence through retrieval, geometry, maps, and view consistency.
- **Persistent world state** (`world-models--persistent-state`): Entity persistence, object permanence, state revision, and shared worlds.
- **Imagination & action coupling** (`world-models--predictive-control`): World prediction linked to planning and control; predictions are distinguished from observed memory.
- **Learning, adaptation & runtime** (`world-models--learning-runtime`): Memory-relevant training, consolidation, adaptation, cache validity and execution timing; labeled contextual when no online memory mechanism is established.
- **Evaluation & world consistency** (`world-models--evaluation`): Recall, revisits, hidden-state evolution, and world-model evaluation.

## VLA

History-conditioned action policies: visual-language-action models and memory-relevant visuomotor precursors. Action chunks alone do not establish memory.

- **History inputs & temporal caches** (`vla--observed-history`): Observation histories and cache interfaces consumed by action policies.
- **Compressed & recurrent memory** (`vla--compression-recurrence`): Visual token pooling, learned history compression, recurrent tokens, and compact belief states for action policies.
- **Episodes, keyframes & retrieval** (`vla--episodic-retrieval`): Retained episodes and keyframes, selective writes, and retrieval of task-relevant past evidence.
- **Task progress & plan state** (`vla--task-progress`): Progress records, language scratchpads, latent plans, and action continuity; intended actions are not executed facts.
- **Spatial, action & touch history** (`vla--action-touch`): Object traces, geometry, executed actions, proprioception, contact and tactile history.
- **Learning, adaptation & runtime** (`vla--learning-runtime`): Memory-relevant training, consolidation, adaptation, cache validity and execution timing; labeled contextual when no online memory mechanism is established.
- **Memory-sensitive policy evaluation** (`vla--evaluation`): Non-Markovian tasks, interference, control dependence, and policy evaluation context.

## Agentic Robotics

Embodied agents that retain task, spatial, episodic, or procedural state; VLM planners, VLA/WAM executors, and runtime harnesses. Navigation and mapping precursors are labeled by scope.

- **Episodic experience & retrieval** (`agentic-robotics--episodic-retrieval`): Time-indexed experience that an embodied agent can revisit and use.
- **Semantic & spatial memory** (`agentic-robotics--semantic-spatial`): Maps, scene graphs, entities, and grounded knowledge across observations.
- **Task state & long-horizon planning** (`agentic-robotics--task-state-planning`): Persistent subgoals, progress records, semantic updates, and visual cues passed from planners to VLA/WAM executors.
- **Skills, programs & harnesses** (`agentic-robotics--procedural-harness`): Executable skills, program state, tool runtimes, and state handoff.
- **Reflection & experience adaptation** (`agentic-robotics--reflection-adaptation`): Failure analysis, experience consolidation, and adaptation across attempts.
- **Embodied-agent evaluation** (`agentic-robotics--evaluation`): Embodied tasks and tests of persistent experience, reasoning, and interaction.

## Supporting Foundations

General memory architectures, language-agent systems, selected model/control baselines, evaluation tools and surveys. Supporting references are not additional embodied-memory methods.

- **Architectures & model baselines** (`foundations--architectures`): Transferable memory architectures and selected model/control baselines used to interpret memory claims.
- **General agent memory & runtimes** (`foundations--agent-memory`): Language-agent memory and harness designs without a verified embodied deployment in this record.
- **Surveys & perspectives** (`foundations--surveys`): Prior syntheses and conceptual framing.
- **General evaluation & datasets** (`foundations--evaluation`): Supporting memory benchmarks and datasets outside direct robot-memory evaluation.

## Six evidence axes

- **Information source**: Observed evidence, execution receipts, demonstrations, generated hypotheses, reflections, or weights; forecasts are not observations.
- **Representation**: Frames/latents, KV states, recurrent states, slots, trajectories, maps, text, graphs, or skill parameters.
- **Address**: Address by physical time, space, entity, event, task stage, action effect, or semantic query.
- **Read/write and revision**: Write, read, compress, merge, update, forget, invalidate, verify, and recompute.
- **Temporal scope**: Within-query, chunk, episode, cross-episode, or deployment persistence; retain event time and validity.
- **Consumer interface**: Video predictor, action expert, high-level planner, verifier, or harness; useful state must reach the correct reader.
