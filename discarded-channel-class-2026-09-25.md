# Invention Disclosure — Discarded-Channel Class (DCC) engine

**Status:** preparatory technical writing ONLY. Nothing filed, published, pushed, or changed in any repository.
**Source:** local buildout, `~/workspace/ip/buildout/discarded-channel/` (no GitHub repo exists; GitHub is not authenticated for this work)
**Seed:** autonomous research session 2026-09-12, authored by Haley Bird alone
**Buildout:** 2026-09-25, autonomous research agent under Haley Bird's direction
**Prepared:** 2026-09-25 (draft for Haley Bird's review)
**NOT legal advice. Requires patent-counsel review before any filing.**

---

## (a) Plain-English statement of the invention

A computer-implemented method for detecting and scoring a specific failure mode in research and archival practice: discarding a data-bearing *channel* (a tape set, film archive, database, or platform corpus) whose contents were never fully enumerated, destroying the ability to determine what unresolved information the channel contained. The method implements an archive-subtraction scoring pipeline (`dcc_engine.py`) that ranks candidate channel-discard events by eight gates — channel existence, data carriage, evidenced discard event, unenumerated remainder, irrecoverability, inference hygiene, archive subtraction, and a discriminator requiring that retaining the channel would preserve interrogation capacity which no other data source reconstructs — plus three adversarial iterates (surviving-copy challenge, known-content challenge, discard-intent ablation).

The core technical assertion, implemented as gate G4 plus the G8 discriminator: it is not the *data loss* that defines the class, it is the *loss of enumerability* — the surviving record cannot say what the channel held, and collecting more data elsewhere cannot restore that interrogation capacity.

---

## (b) The technical problem it solves

Archival and research practice routinely evaluates retention by the *known* value of a collection, while the actual exposure is the *unenumerated remainder*: what the channel held that no surviving catalog lists. Systematic evidence (Vines et al., *Current Biology* 2014: researcher-stewarded datasets decay at 17%/year; only 23% of 516 datasets confirmed extant) shows individual stewardship is the dominant discard mechanism, yet no existing research tooling tracks, against a local archive of already-claimed structural classes, whether a loss is: an unobserved place (undersampling), a consumed object (DIC), a nameless entity (UCC), a collapsed operator (OAC), a generator mismatch (EFC) — or specifically **a recorded channel that existed, carried data, and was discarded with its remainder unenumerated**. Digital-preservation tools audit *formats*; archival-appraisal frameworks weigh *value*; neither certifies non-enumerability of a discarded channel or stops a session from relabeling ordinary fully-cataloged data loss as a structural unknown.

---

## (c) How it works — enabling detail from the actual buildout contents

All detail below is drawn from `dcc_engine.py`, `dcc_instances.json`, and the engine run of 2026-09-25.

### Components

1. **`DCCInstance` dataclass** — each candidate carries: `id`, `realm`, `name`, `channel_type`, `discard_mechanism`, `source_url`, `source_date`, `source_strength` (1.0 = primary institution), `known_fact`, `unknown_content_claim` ("inference" | "source-established"), `inference_statement`, booleans `channel_existed`, `data_carried`, `discard_evident`, `discard_averted`, `unenumerated_remainder`, `complete_duplicate_survives`, `elsewhere_reconstructs`, `overclaim`, `recovery_possible` ("no"|"unknown"|"partial"|"yes"), `archive_overlap` code, `intent` (intentional|accidental|mixed|averted|unknown), `duplicate_survival` (none|partial|substantial|complete), `meta_evidence` bool, and four unit-interval heuristic weights (`freshness`, `uniqueness`, `stakes`, `source_strength`) plus `notes`. Constructor validation rejects unknown fields, bad enums, and out-of-range weights.

2. **`score_dcc_instance()`** — the scoring function. Meta-evidence, discard-averted, and complete-duplicate cases return CONTROL (reference only, score 0, not eligible for primary). Otherwise it evaluates gates:
   - G1 channel existed; G2 carried recorded data; G3 discard evidenced; G4 unenumerated remainder; G5 recovery impossible/unknown; G6 no overclaim (unknown-content must be labeled INFERENCE); G7 archive subtraction; G8 elsewhere cannot reconstruct.
   - `HARD_KILL` table: UND/UNDERSAMPLING, DIC, UCC, OAC, PPC, CBR, DBH, CONSCIOUSNESS → KILLED, score 0. `SOFT_PENALTY` table: CMC, CIC, EFC, UPRC, CIP, TAC, FAC, plus DCC-specific INSTITUTIONAL, PLATFORM, MIGRATION → PENALIZED (×0.45 discount).
   - Base score: `0.25·freshness + 0.25·uniqueness + 0.20·stakes + 0.15·source_strength + 0.10·(G1∧G2∧G3) + 0.05·G4`, ×100. DISCARD_GAP gets the full product.

3. **Iterates** —
   - `surviving_copy_challenge()`: a stricter G5 — demotes any eligible instance where substantial equivalent information survives. TOXNET was demoted (substantial duplicates at PubChem/PubMed/Bookshelf); all 11 DISCARD_GAP instances survived.
   - `known_content_challenge()`: synthetic negatives proving G4 does real work — a fully-cataloged archive that burns is ordinary loss (NOT DCC); an uncataloged vault that burns is the DCC shape; a wiped tape with a bit-identical clone fails G5.
   - `discard_intent_ablation()`: splits eligible instances by intent (intentional mean 53.03, accidental 61.04, mixed 69.67) — the class groups the loss shape, not the motive.

4. **Inputs/outputs** — `dcc_instances.json` (21 sourced instances) → `run_engine()` → `dcc_scores.json` / `dcc_scores.txt` (ranked list, per-instance gates, reasons, and iterate results).

### Reported results (reproduced by the engine run 2026-09-25, not independently validated)

- 21 instances: 11 DISCARD_GAP, 3 PENALIZED, 0 KILLED, 7 CONTROL.
- Primary: **NPRC_1973_FIRE at 75.5** (16–18M OMPFs, NARA-sourced), then Universal 2008 fire (74.75) and Apollo 11 slow-scan tapes (74.25).
- PENALIZED: MySpace (PLATFORM), GeoCities (PLATFORM), TOXNET (MIGRATION).
- CONTROL: Lunar Orbiter LOIRP, BBC Domesday, Apollo heat-flow tapes, Nimbus dark data, Landsat LGAC, CERN first website, Vines 2014 (meta-evidence).
- All three iterates completed; the surviving-copy challenge demoted one instance; the known-content challenge confirmed G4's discriminator; the intent ablation left the class coherent across motives.

---

## (d) Novelty relative to the archive's own prior classes

The SESSION.md contains an explicit archive-subtraction table. The buildout's position (quoted from the engine docstring): no prior archive class owns the *discard of a recorded channel with an unenumerated remainder*. Key distinctions it asserts:

| Prior class | DCC differs because |
|---|---|
| Undersampling | no data was ever collected; DCC requires a channel that existed and carried data (plain undersampling is hard-KILLED unless data was collected into the later-discarded channel) |
| DIC | inquiry consumes the seen object or only copy; DCC is a later channel-discard decision, not destructive measurement |
| UCC | the entity never had a durable identifier; DCC requires a recorded channel that existed |
| OAC | the observation operator collapses independent quantities; DCC deletes the channel itself |
| CMC | extra functions ride an already-instrumented channel; DCC removes the evidence stream |
| PPC | residuals are absorbed through extra degrees of freedom; DCC removes the stream |
| CIC | clocks are incommensurable; DCC is about channel retention |
| EFC | calibration and target generators differ; DCC needs no generator mismatch |

The falsification rule that separates DCC from all of these: "DCC is confirmed only if retaining the channel would preserve interrogation of an unenumerated remainder, and collecting more data elsewhere cannot reconstruct it" (G4 + G8).

**Prior art *outside* the archive:** the obvious adjacent bodies — digital preservation (format obsolescence, e.g. the Domesday case, which is standard preservation-literature material), archival appraisal theory, data-loss-prevention practice, and data-provenance/lineage literature — are *old* and directly adjacent. The buildout does not claim to have searched them; a thorough external prior-art search is needed before any claim. *Inference: the closest external art is likely to be found in the preservation/appraisal literature, not in science-method papers.*

---

## (e) Honest weaknesses

1. **Alice abstract-idea risk — severe.** The claimed advance is a classification framework: sorting known historical loss events into a taxonomy of error types using hand-set heuristic weights. Under *Alice/Mayo*, an abstract idea (classifying observations, applying a heuristic formula) does not become patent-eligible merely by running on a computer. The score formula is a mental-scale arithmetic combination of four subjective weights — the kind of abstract calculation the Federal Circuit has repeatedly struck down absent a concrete technical improvement to a specific machine or process.
2. **The primary instances are other people's documented events.** The leader (1973 NPRC fire) is NARA's documented disaster; the method claims no new data. A patent cannot claim the fires, the wiping, or any natural/historical fact; it can only claim the *classification procedure*.
3. **Scores are admitted heuristics, not measurements.** All weights (e.g., stakes=0.9 for NPRC) are human judgment inputs; the SESSION states "Nothing here measures nature." There is no validation against ground truth, no inter-rater reliability, no demonstration that the heuristic outperforms existing archival-audit methods.
4. **No concrete technical effect on a specific process.** The outputs are ranked lists and discriminator text specs — further from technical effect than most successful method patents. The class's honest finding is that it groups a *loss shape* for research prioritization, which reads more like appraisal methodology than a technical invention.
5. **External prior art is ancient and directly on point.** Digital preservation, archival appraisal, and data-provenance practice have addressed "what was in the box we threw away" for decades (the Domesday case is itself preservation-literature standard material). The archive-internal novelty argument (d) does not address this.
6. **AI-generated content.** The buildout was performed by an autonomous research agent under Haley Bird's direction; the seed was authored by Haley Bird alone. Per current USPTO guidance (Feb 2024), AI cannot be an inventor; a human must have made a significant contribution to each claim. Counsel must establish inventorship claim-by-claim; the extent of the agent's contribution to the specific code has not been decomposed.
7. **Overbreadth risk.** Framed loosely, "a method for identifying data loss" reads on routine data-governance and backup-audit practice. The defensible scope, if any, is the narrow eight-gate pipeline with the G4+G8 falsification rule — not the general observation that discarding records can destroy information.

---

## (f) Disclosure-bar date

- **First public disclosure:** none found. The seed (2026-09-12) was a private autonomous research session; the buildout is local. **No GitHub repo exists; nothing has been published.** This disclosure differs from the other eight: foreign rights are *not yet lost* (no public disclosure in an absolute-novelty regime) — pending counsel's view of the seed's distribution.
- **US §102(b)(1) grace-period bar — planning flag: 2027-09-12** (one year from the seed session). This is a planning flag requiring legal verification, not a confirmed deadline. If counsel treats the private seed as non-disclosing, the bar is un-triggered; if any seed detail reached a public recipient, the earlier date controls.
- Copyright: no license attached; all rights reserved by default.

---

## What a provisional would need to claim

The defensible claim set (counsel to confirm) would be drawn to the *computer-implemented method*: (i) receiving candidate channel-discard records each annotated with channel type, discard mechanism, source, and unknown-content labeling; (ii) computing a discarded-channel score through the eight-gate pipeline with archive-subtraction hard-kill and soft-penalty tables against a local archive of prior structural classes; (iii) applying the G4+G8 falsification predicate (unenumerated remainder AND non-reconstructability elsewhere) to distinguish structural channel loss from ordinary fully-cataloged data loss; (iv) outputting ranked candidates with per-gate reports; (v) the three adversarial-iterate validation loop (surviving-copy, known-content, intent ablation). Apparatus claims to the engine running on a computer. **Not** the DCC concept, any historical loss event, or any natural phenomenon.
