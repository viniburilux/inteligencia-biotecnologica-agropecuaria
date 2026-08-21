# ASIE V0 — Public Boundary

## Decision

The public laboratory preserves the **evidence of adaptive behavior**, not a general-purpose implementation of the adaptive engine.

The executable scripts used to analyze the corpus, generate autonomous questions, run reformulations and replay fixed versus adaptive exploration are maintained in the private Lux-Lab under `asie_experiment_v0/`. The public repository keeps the resulting reports, logs, provenance, metadata-only source references and bounded reconstruction artifacts.

This boundary is deliberate and reversible. It does not claim that ASIE is a product, a patentable invention or a general autonomous system. It records that a specific experiment produced an observable sequence in which corpus state generated signals, signals changed the next question, results changed the representation of the problem and the cycle stopped or continued based on evidence.

## Public layer

The following classes remain appropriate for this repository:

| Class | Examples |
|---|---|
| Evidence | Patent and literature findings, negative results, blocked states and bounded interpretations |
| Provenance | URLs, timestamps, hashes, source identifiers and query execution records |
| Demonstration | `PATENT-ASIE-2026-08-21-001`, cycle reports and fixed-versus-adaptive replay results |
| Contract | Schemas, metadata-only manifests and generic TraceFoundry interfaces |
| Knowledge | Explanations of observed operators, limits and reconstruction procedure |

## Private layer

The following classes remain in Lux-Lab until a separate publication decision:

| Class | Reason |
|---|---|
| Experimental scripts | They encode one exploration run and are not a stable public API. |
| General question-generation policy | This is the part whose value and scope are still being discovered. |
| Question prioritization and ranking | The public experiment observed choices but did not validate a general ranking function. |
| Reformulation heuristics as a reusable method | Public artifacts show examples; they do not yet define a tested general algorithm. |
| Adaptive memory and stopping policy | These depend on operational context and should not be inferred from one experiment. |

## Interpretation

The public repository therefore answers **what happened and how it can be audited**. The private laboratory preserves **the executable working material used to produce and study what happened**. The private OI repository remains a separate core and is not copied into either layer.

Future publication of any adaptive code requires an isolated review of license, dependencies, local paths, secrets, reproducibility, stable contracts and whether the code reveals a general policy rather than a case-specific experiment.
