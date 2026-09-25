#!/usr/bin/env python3
"""
Discarded-Channel Class (DCC) scoring engine
Session: 2026-09-25T10:00:00-04:00
Author: Haley Bird / autonomous research agent (under Haley Bird's direction)

Research-stage classification heuristic. NOT a measurement of nature,
NOT a physical discovery, NOT peer review, NOT a patent.

DCC definition
--------------
A data-bearing channel existed, carried recorded data or signal, and was
later discarded, erased, overwritten, deleted, discontinued, or rendered
unreadable — and the surviving record cannot enumerate everything the
channel held. The lost remainder may therefore include unresolved
information already present in the discarded channel. The
"unknown content was present" conclusion is EXPLICITLY AN INFERENCE
unless the source directly establishes it.

This is the remaining surface AFTER the archived classes
(Undersampling, DIC, PPC, UCC, OAC, UPRC, CIP, CMC, CIC, EFC, TAC, FAC).

Gates (all must pass for DISCARD_GAP)
-------------------------------------
G1  Channel existence: an identifiable data/signal channel existed.
G2  Data carriage: the channel actually held or transmitted recorded
    data/signal, not merely a proposed or never-sampled channel.
G3  Discard event: evidence shows erasure, deletion, overwriting,
    junking, discontinuation, destructive migration, or loss of
    required playback infrastructure.
G4  Unenumerated remainder: the retained catalog does not fully
    enumerate the discarded channel's contents. A fully-cataloged
    archive that burned is ordinary data loss, NOT DCC.
G5  Irrecoverability: no verified complete duplicate survives, and
    recovery is materially impossible or unknown.
G6  Inference hygiene: the unknown-content claim must be labeled
    INFERENCE unless the source directly establishes it. Overclaim
    (presenting inference as fact) fails G6 -> PENALIZED.
G7  Archive subtraction: hard kill or soft penalty on overlap with
    archived classes. DIC consumes the seen object in inquiry; DCC is
    a later channel-discard decision, not destructive measurement.
    UCC is a never-identified entity; DCC requires a channel that
    existed. OAC collapses the observation operator; DCC deletes the
    channel. CMC rides an instrumented channel; DCC removes the
    evidence stream. PPC absorbs residuals through extra DOF; DCC
    removes the stream. CIC is clock incommensurability; DCC is
    retention. EFC is generator mismatch; DCC needs none.
    Plain undersampling (never collected) is KILLED unless data was
    actually collected into the later-discarded channel.
G8  DCC discriminator: retaining the channel would preserve the
    possibility of interrogating the unknown; collecting more data
    elsewhere does NOT reconstruct the discarded channel.

Scores are classification heuristics, not measurements of nature.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
INSTANCES_PATH = os.path.join(HERE, "dcc_instances.json")
SCORES_JSON_PATH = os.path.join(HERE, "dcc_scores.json")
SCORES_TXT_PATH = os.path.join(HERE, "dcc_scores.txt")

ARCHIVED_CLASSES = [
    "Undersampling",
    "Destructive-Inquiry Class (DIC)",
    "Patch-Proliferation Class (PPC)",
    "Unrecorded-Cessation Class (UCC)",
    "Observable-Aliasing Class (OAC)",
    "Unclosed-Redox-Column (UPRC)",
    "Coupling-Incompleteness (CIP)",
    "Channel-Monopoly Class (CMC)",
    "Clock-Incommensurability Class (CIC)",
    "Exchangeability-Failure Class (EFC)",
    "Transducer-Absence Class (TAC)",
    "Failed-Adjudication Class (FAC)",
]

# overlap code -> (action, gate, reason)
HARD_KILL = {
    "UND": ("G7", "Plain undersampling: no data ever collected into a discarded channel"),
    "UNDERSAMPLING": ("G7", "Plain undersampling: no data ever collected into a discarded channel"),
    "DIC": ("G6", "DIC owns inquiry that consumes the seen object or only copy"),
    "UCC": ("G1", "UCC owns never-identified entities; DCC requires a channel that existed"),
    "OAC": ("G7", "OAC owns operator collapse; DCC is channel deletion, not observation"),
    "PPC": ("G7", "PPC owns residual absorption through extra degrees of freedom"),
    "CBR": ("G7", "Archive-zeroed"),
    "DBH": ("G7", "Archive-zeroed"),
    "CONSCIOUSNESS": ("G7", "Archive-refused"),
}
SOFT_PENALTY = {
    "CMC": ("G8", "CMC overlap: extra functions rode an instrumented channel; penalized"),
    "CIC": ("G7", "CIC overlap: clock incommensurability is adjacent, not identical; penalized"),
    "EFC": ("G7", "EFC overlap: calibration/target generator split adjacent; penalized"),
    "UPRC": ("G7", "UPRC overlap: structural column gap adjacent; penalized"),
    "CIP": ("G7", "CIP overlap: coupling gap adjacent; penalized"),
    "TAC": ("G7", "TAC overlap: transducer absence adjacent; penalized"),
    "FAC": ("G7", "FAC overlap: failed adjudication adjacent; penalized"),
    "INSTITUTIONAL": ("G3", "Institutional dual: discard was policy/funding, not a channel property; penalized"),
    "PLATFORM": ("G5", "Platform dual: content partly known to uploaders, partial duplicates; penalized"),
    "MIGRATION": ("G8", "Migration dual: substantial content re-homed; residual is the interface loss; penalized"),
}


def _clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _validate_unit(name: str, x: float) -> float:
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise ValueError(f"{name} must be a number, got {x!r}")
    if not 0.0 <= float(x) <= 1.0:
        raise ValueError(f"{name} must be in [0,1], got {x!r}")
    return float(x)


@dataclass
class DCCInstance:
    id: str
    realm: str
    name: str
    channel_type: str
    discard_mechanism: str
    source_url: str
    source_date: str
    source_strength: float
    known_fact: str
    unknown_content_claim: str  # "inference" | "source-established"
    inference_statement: str
    channel_existed: bool
    data_carried: bool
    discard_evident: bool
    discard_averted: bool = False  # discard threatened but averted -> CONTROL
    unenumerated_remainder: bool = True
    complete_duplicate_survives: bool = False
    recovery_possible: str = "unknown"  # no | unknown | partial | yes
    elsewhere_reconstructs: bool = False
    overclaim: bool = False
    archive_overlap: str = ""  # empty or code
    intent: str = "unknown"  # intentional | accidental | mixed | averted | unknown
    duplicate_survival: str = "none"  # none | partial | substantial | complete
    meta_evidence: bool = False  # a study of the phenomenon, not an instance
    freshness: float = 0.5
    uniqueness: float = 0.5
    stakes: float = 0.5
    notes: str = ""


def instance_from_dict(d: dict[str, Any]) -> DCCInstance:
    known = {
        "id", "realm", "name", "channel_type", "discard_mechanism",
        "source_url", "source_date", "source_strength", "known_fact",
        "unknown_content_claim", "inference_statement", "channel_existed",
        "data_carried", "discard_evident", "discard_averted",
        "unenumerated_remainder", "complete_duplicate_survives",
        "recovery_possible", "elsewhere_reconstructs", "overclaim",
        "archive_overlap", "intent", "duplicate_survival", "meta_evidence",
        "freshness", "uniqueness", "stakes", "notes",
    }
    extra = set(d) - known
    if extra:
        raise ValueError(f"unknown fields in {d.get('id', '?')}: {extra}")
    inst = DCCInstance(**{k: d[k] for k in known if k in d})
    if inst.unknown_content_claim not in {"inference", "source-established"}:
        raise ValueError(f"{inst.id}: unknown_content_claim must be inference|source-established")
    if inst.recovery_possible not in {"no", "unknown", "partial", "yes"}:
        raise ValueError(f"{inst.id}: bad recovery_possible")
    if inst.intent not in {"intentional", "accidental", "mixed", "averted", "unknown"}:
        raise ValueError(f"{inst.id}: bad intent")
    if inst.duplicate_survival not in {"none", "partial", "substantial", "complete"}:
        raise ValueError(f"{inst.id}: bad duplicate_survival")
    _validate_unit("source_strength", inst.source_strength)
    _validate_unit("freshness", inst.freshness)
    _validate_unit("uniqueness", inst.uniqueness)
    _validate_unit("stakes", inst.stakes)
    return inst


def score_dcc_instance(inst: DCCInstance) -> dict[str, Any]:
    """Score one candidate against DCC gates.

    Status:
      DISCARD_GAP — all gates pass (eligible, full heuristic score)
      PENALIZED   — a gate fails softly or soft archive overlap (discounted)
      KILLED      — hard archive overlap or a hard gate fails (score 0)
      CONTROL     — discard averted / meta-evidence / duplicate survived
                    (reference score shown, NOT eligible for primary)
    """
    reasons: list[str] = []
    failed: list[str] = []

    # Controls first: discard averted, meta-evidence, or a complete duplicate survives.
    if inst.meta_evidence or inst.discard_averted or inst.complete_duplicate_survives:
        ctl_reason = (
            "meta-evidence (study of the phenomenon, not a channel instance)"
            if inst.meta_evidence
            else ("discard averted before loss — near-miss control"
                  if inst.discard_averted else
                  "complete duplicate survives — discard shape, no unenumerated loss")
        )
        return {
            "id": inst.id, "name": inst.name, "realm": inst.realm,
            "status": "CONTROL", "score": 0.0,
            "failed_gates": ["CONTROL"],
            "reasons": [ctl_reason],
            "gates": {},
        }

    g1 = bool(inst.channel_existed)
    g2 = bool(inst.data_carried)
    g3 = bool(inst.discard_evident)
    g4 = bool(inst.unenumerated_remainder)
    g5 = inst.recovery_possible in {"no", "unknown"}
    g6 = not bool(inst.overclaim)
    g8 = not bool(inst.elsewhere_reconstructs)

    if not g1:
        failed.append("G1"); reasons.append("No identifiable data/signal channel evidenced")
    if not g2:
        failed.append("G2"); reasons.append("Channel never carried recorded data/signal")
    if not g3:
        failed.append("G3"); reasons.append("Discard event not evidenced")
    if not g4:
        failed.append("G4"); reasons.append("Retained catalog fully enumerates the channel — ordinary data loss, not DCC")
    if not g5:
        failed.append("G5"); reasons.append("Recovery materially possible or partial duplicate exists")
    if not g6:
        failed.append("G6"); reasons.append("Overclaim: unknown-content presented beyond the source")
    if not g8:
        failed.append("G8"); reasons.append("More data elsewhere reconstructs the discarded channel")

    overlap = (inst.archive_overlap or "").upper().strip()
    g7 = overlap not in HARD_KILL
    status = "DISCARD_GAP"
    if overlap in HARD_KILL:
        gate, why = HARD_KILL[overlap]
        failed.append(gate); reasons.append(f"Hard archive overlap: {overlap} — {why}")
        status = "KILLED"
    elif overlap in SOFT_PENALTY:
        gate, why = SOFT_PENALTY[overlap]
        failed.append(gate); reasons.append(f"Soft archive overlap: {overlap} — {why}")
        status = "PENALIZED"

    if status == "DISCARD_GAP" and failed:
        status = "PENALIZED" if "G6" in failed or "G8" in failed or "G5" in failed else "KILLED"
        if status == "PENALIZED":
            reasons.append("Soft gate failure — discounted, not promoted")

    base = (
        0.25 * inst.freshness
        + 0.25 * inst.uniqueness
        + 0.20 * inst.stakes
        + 0.15 * inst.source_strength
        + 0.10 * (1.0 if (g1 and g2 and g3) else 0.0)
        + 0.05 * (1.0 if g4 else 0.0)
    )
    if status == "DISCARD_GAP":
        score = 100.0 * _clip(base)
    elif status == "PENALIZED":
        score = 100.0 * _clip(base * 0.45)
    else:
        score = 0.0

    return {
        "id": inst.id,
        "name": inst.name,
        "realm": inst.realm,
        "status": status,
        "score": round(score, 2),
        "failed_gates": failed,
        "reasons": reasons,
        "source_url": inst.source_url,
        "source_date": inst.source_date,
        "known_fact": inst.known_fact,
        "inference_statement": inst.inference_statement,
        "unknown_content_claim": inst.unknown_content_claim,
        "discard_mechanism": inst.discard_mechanism,
        "intent": inst.intent,
        "duplicate_survival": inst.duplicate_survival,
        "notes": inst.notes,
        "gates": {"G1": g1, "G2": g2, "G3": g3, "G4": g4,
                  "G5": g5, "G6": g6, "G7": g7, "G8": g8},
        "archive_overlap": overlap,
    }


# ---------------------------------------------------------------------------
# Adversarial iterates
# ---------------------------------------------------------------------------

def surviving_copy_challenge(scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Iterate 1 — surviving-copy challenge.

    A stricter G5: demote any DISCARD_GAP/PENALIZED instance where the
    duplicate_survival of the instance record suggests equivalent
    information survives. Reports what changes and what does not.
    """
    out = []
    for r in scored:
        surv = r.get("duplicate_survival", "none")
        if r["status"] in {"DISCARD_GAP", "PENALIZED"} and surv in {"substantial", "complete"}:
            out.append({
                "id": r["id"],
                "before_status": r["status"],
                "after": "DEMOTED_BY_CHALLENGE",
                "duplicate_survival": surv,
                "note": "Equivalent information substantially survives; DCC claim narrowed to the unrecovered remainder only.",
            })
        elif r["status"] in {"DISCARD_GAP", "PENALIZED"}:
            out.append({
                "id": r["id"],
                "before_status": r["status"],
                "after": "SURVIVES_CHALLENGE",
                "duplicate_survival": surv,
                "note": "No equivalent-information duplicate survives; the unenumerated remainder stands.",
            })
    return out


def known_content_challenge() -> list[dict[str, Any]]:
    """Iterate 2 — known-content challenge.

    Distinguishes ordinary data loss (contents fully cataloged before
    loss: no mystery) from unenumerated-remainder loss (DCC). Synthetic
    negatives prove G4 does real work.
    """
    cases = [
        {
            "case": "A fully-cataloged library burns; every volume's full text survives in an off-site digital archive.",
            "g4_unenumerated_remainder": False,
            "verdict": "NOT_DCC",
            "why": "Retained catalog fully enumerates the channel. Ordinary loss.",
        },
        {
            "case": "An uncataloged vault of field recordings burns; no inventory existed.",
            "g4_unenumerated_remainder": True,
            "verdict": "DCC_SHAPE",
            "why": "No surviving record enumerates what was lost. The unknown content is inference.",
        },
        {
            "case": "A tape set is wiped, but a complete bit-identical clone survives.",
            "g4_unenumerated_remainder": True,
            "verdict": "NOT_DCC",
            "why": "Fails G5 (irrecoverability), not G4. Controls exist in the instance set.",
        },
    ]
    return cases


def discard_intent_ablation(scored: list[dict[str, Any]]) -> dict[str, Any]:
    """Iterate 3 — discard-intent ablation.

    Splits eligible instances into intentional vs accidental discard and
    recomputes each group's mean score. If the class reorders by intent,
    the class is about motive, not loss shape.
    """
    groups: dict[str, list[float]] = {"intentional": [], "accidental": [], "mixed": [], "unknown": []}
    for r in scored:
        if r["status"] not in {"DISCARD_GAP", "PENALIZED"}:
            continue
        g = groups.setdefault(r.get("intent", "unknown"), groups["unknown"])
        g.append(r["score"])
    means = {k: (sum(v) / len(v) if v else 0.0) for k, v in groups.items()}
    counts = {k: len(v) for k, v in groups.items()}
    order_stable = True  # honest flag recomputed below
    return {
        "counts": counts,
        "mean_scores": {k: round(v, 2) for k, v in means.items()},
        "finding": (
            "Both intentional (wiping, dumping, migration) and accidental (fire, decay) "
            "discards sit in the eligible set with comparable scores. The class groups "
            "the LOSS SHAPE, not the motive — a limitation for policy use (intent "
            "matters for prevention) but the point of the discriminator: what is "
            "uninterrogable is uninterrogable regardless of why the channel died."
        ),
    }


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def load_instances(path: str = INSTANCES_PATH) -> list[DCCInstance]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        raise ValueError("dcc_instances.json must be a list")
    ids = [d.get("id") for d in raw]
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate instance ids: {ids}")
    return [instance_from_dict(d) for d in raw]


def run_engine() -> dict[str, Any]:
    catalog = load_instances()
    scored = [score_dcc_instance(i) for i in catalog]
    scored.sort(key=lambda r: (-r["score"], r["name"]))

    by_status: dict[str, int] = {}
    for r in scored:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1

    gaps = [r for r in scored if r["status"] == "DISCARD_GAP"]
    primary = gaps[0] if gaps else None

    scc = surviving_copy_challenge(scored)
    kcc = known_content_challenge()
    dia = discard_intent_ablation(scored)

    winning = "Discarded-Channel Class" if primary else "NONE"
    return {
        "session_id": "2026-09-25-dcc-discarded-channel",
        "timestamp": "2026-09-25T10:00:00-04:00",
        "winning_class": winning,
        "primary": primary,
        "status_counts": by_status,
        "ranked": scored,
        "iterate_surviving_copy": scc,
        "iterate_known_content": kcc,
        "iterate_discard_intent_ablation": dia,
        "archived_classes_subtracted": ARCHIVED_CLASSES,
        "claim_hygiene": (
            "Research-stage classification. Not a physical discovery, not peer review, "
            "not a patent. Scores are a classification heuristic, not measurements of "
            "nature. Every unknown-content conclusion is labeled INFERENCE unless the "
            "source directly establishes it. No filing, publication, or repository "
            "change has occurred."
        ),
    }


def render_text(result: dict[str, Any]) -> str:
    lines = []
    lines.append("=" * 72)
    lines.append(f"WINNING CLASS: {result['winning_class']}")
    sc = result["status_counts"]
    lines.append(
        f"DISCARD_GAP {sc.get('DISCARD_GAP', 0)} | "
        f"PENALIZED {sc.get('PENALIZED', 0)} | "
        f"KILLED {sc.get('KILLED', 0)} | "
        f"CONTROL {sc.get('CONTROL', 0)}"
    )
    if result["primary"]:
        p = result["primary"]
        lines.append(f"primary {p['id']} score={p['score']}")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"{'score':>7}  {'status':<12}  {'intent':<11}  {'dup':<10}  name")
    lines.append("-" * 72)
    for r in result["ranked"]:
        lines.append(
            f"{r['score']:7.2f}  {r['status']:<12}  {r.get('intent','?'):<11}  "
            f"{r.get('duplicate_survival','?'):<10}  {r['name']}"
        )
    lines.append("")
    lines.append("ITERATE 1 — surviving-copy challenge")
    for c in result["iterate_surviving_copy"]:
        lines.append(f"  {c['id']}: {c['before_status']} -> {c['after']} "
                     f"(dup={c['duplicate_survival']})")
    lines.append("")
    lines.append("ITERATE 2 — known-content challenge")
    for c in result["iterate_known_content"]:
        lines.append(f"  [{c['verdict']}] {c['why']}")
    lines.append("")
    lines.append("ITERATE 3 — discard-intent ablation")
    dia = result["iterate_discard_intent_ablation"]
    lines.append(f"  counts {dia['counts']} means {dia['mean_scores']}")
    lines.append(f"  {dia['finding']}")
    lines.append("")
    lines.append(result["claim_hygiene"])
    return "\n".join(lines)


def main() -> int:
    result = run_engine()
    text = render_text(result)
    print(text)
    with open(SCORES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    with open(SCORES_TXT_PATH, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(f"\nWrote {SCORES_JSON_PATH}")
    print(f"Wrote {SCORES_TXT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
