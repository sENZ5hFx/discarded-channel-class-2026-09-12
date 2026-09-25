# SESSION.md — Discarded-Channel Class (DCC) buildout

**Date:** 2026-09-25
**Seed:** autonomous research session 2026-09-12: "Discarded-Channel Class (DCC). The unknown is already in the file. Research-stage classification — not a physical discovery, not peer review, not a patent. Author: Haley Bird."
**Worker:** autonomous research agent under Haley Bird's direction
**Status:** buildout complete; nothing filed, published, pushed, or changed in any repository

---

## 1. What this session built

The three-line seed became a full local research/code package in `~/workspace/ip/buildout/discarded-channel/`:

| File | What it is |
|---|---|
| `dcc_engine.py` | Scoring engine: 8 gates (G1–G8), hard-kill and soft-penalty archive subtraction, weighted heuristic scoring, 3 adversarial iterates, deterministic outputs |
| `dcc_instances.json` | 21 sourced instances, every one carrying source URL + date, known fact, inference labeled INFERENCE, channel type, discard mechanism, duplicate/recovery status, archive overlap, intent, and heuristic weights |
| `dcc_scores.json` / `dcc_scores.txt` | Engine outputs (machine + human readable) |
| `SESSION.md` | This file |
| `discarded-channel-class-2026-09-25.md` | Invention disclosure in the existing disclosure format; canonical copy in `~/workspace/your_files/ip-protection/` |

Nothing was filed. Nothing was published. GitHub is not authenticated for this work and was not touched.

## 2. The claim, narrowed

DCC requires all of: (G1) a channel actually existed; (G2) it carried recorded data or signal; (G3) a discard event is evidenced; (G4) the retained catalog does not fully enumerate the channel's contents; (G5) no verified complete duplicate survives; (G6) the "unknown content was present" conclusion is explicitly labeled **inference** unless the source directly establishes it; (G7) the loss is not better classified under an archived class; (G8) retaining the channel would preserve interrogation capacity that more data elsewhere cannot reconstruct.

This is narrower than "every deleted archive contained discoveries." It is a method for identifying cases where **discarding a data-bearing channel destroyed the ability to determine what unresolved information the channel contained**. Deliberately excluded: fully-cataloged archives that burned (ordinary data loss, G4 fail), channels never built (G1 fail), cases where complete duplicates survive (G5 fail), and the question of *what* was lost beyond labeled inference (honesty, G6).

## 3. Instance research log

All instances were sourced in-session from the public web on 2026-09-25. Search strategy: start from known discard archetypes (tape reuse, junking, vault fires, platform shutdowns, discontinued databases, dark scientific data), then verify each against the strongest available source (primary institutions first: NARA, Library of Congress, USGS, NLM, NSIDC, NASA OIG).

### Included (21)

| # | Instance | Best source | Source strength |
|---|---|---|---|
| 1 | Apollo 11 raw SSTV tapes degaussed/reused | space.com (Nafzger quotes) | 0.85 |
| 2 | Universal 2008 fire, ~175k master tapes | Metal Insider account of NYT Magazine investigation (2019); corroborated by class-action filing | 0.75 |
| 3 | 70% of US silent features lost | Library of Congress 2013 survey | 1.0 |
| 4 | 1937 Fox vault fire | Wikipedia (corroborated across film-preservation lit) | 0.65 |
| 5 | 1965 MGM Vault 7 fire | Wikipedia (corroborated across lost-film lit) | 0.65 |
| 6 | 1890 Census destroyed (1921 fire + 1933 disposal) | NARA | 1.0 |
| 7 | 1973 NPRC fire, 16–18M OMPFs | NARA | 1.0 |
| 8 | NBC wiped Carson Tonight Show 1962–72 | Wikipedia (DVIDS corroboration) | 0.6 |
| 9 | DuMont network archive destroyed | Internet Archive blog (flags lore as unverified) | 0.75 |
| 10 | Pioneer 10/11 + Helios reels in engineer's basement | NASA OIG FOIA report | 0.85 |
| 11 | BBC wiped Doctor Who 1967–78 | phys.org | 0.7 |
| 12 | MySpace migration loss (2003–15 uploads) | The Fader | 0.75 |
| 13 | GeoCities shutdown 2009 | PCWorld (Archive Team rescue) | 0.7 |
| 14 | TOXNET retired 2019-12-16 | NLM Technical Bulletin | 1.0 |
| 15 | Lunar Orbiter tapes nearly scrapped (CONTROL) | American Libraries Magazine | 0.75 |
| 16 | BBC Domesday unreadable by 2002 (CONTROL) | Computing UK (CAMiLEON rescue) | 0.7 |
| 17 | Apollo heat-flow tapes lost then recovered (CONTROL) | phys.org | 0.75 |
| 18 | Nimbus tapes "dark," recovered (CONTROL) | NSIDC | 0.85 |
| 19 | Landsat LGAC repatriation (CONTROL) | USGS | 1.0 |
| 20 | First website deleted/restored (CONTROL) | CERN birth-of-web page | 1.0 — see §5 |
| 21 | Vines et al. 2014 data-decay 17%/yr (META) | arXiv preprint of published paper | 0.95 |

### Care points enforced per instance

- **Apollo 11:** NASA reportedly said no unseen moonwalk video was lost — that is accepted as the record on that point. The DCC claim is raw signal quality / reprocessing capacity, marked INFERENCE.
- **DuMont:** the East River bay-dumping is partly unverified lore; the source itself says "no one really knows for sure what happened." Recorded as such, not as settled fact. The ~1958 silver-recovery destruction is the firmer mechanism.
- **MySpace:** "server migration" is the documented explanation; intentional-deletion speculation is not repeated.
- **BBC Doctor Who:** counts disagree across sources (95/97/106) — the discrepancy is preserved, not resolved.
- **Carson Tonight Show:** the Dean Martin April 1973 anecdote (erased tape) is unverified YouTube lore and was NOT used as evidence.
- **Universal fire:** the NYT Magazine piece is paywalled; the accessible source is Metal Insider's account, corroborated by the 2019 class-action filing.

### Failed searches / excluded cases

- **2MASS survey tapes:** searched for a discard story; found only that the data and images are public at IPAC. No discard evidenced — excluded rather than padded.
- **IRAS data products:** products exist on tape at data centers; not a discard — excluded.
- **Broad VHS/analog-telemetry searches:** turned up the Apollo heat-flow recovery story instead — which became a control (discard averted), not an eligible instance.
- **NBC/Carson "Dean Martin" video:** unverified lore — excluded (noted above).
- **BBC Radiophonic Workshop / Delia Derbyshire tapes:** considered; dropped for time, and the partial recovery there would have made it another control rather than new coverage.

## 4. Engine results

Run `python3 dcc_engine.py`:

- **11 DISCARD_GAP** (eligible), **3 PENALIZED**, **0 KILLED**, **7 CONTROL**.
- **Primary: NPRC_1973_FIRE at 75.5**, followed by Universal 2008 fire (74.75) and Apollo 11 SSTV (74.25).
- PENALIZED: MySpace (PLATFORM overlap — many uploaders kept originals), GeoCities (PLATFORM — Archive Team rescued a partial fraction), TOXNET (MIGRATION — most content re-homed at PubChem/PubMed/Bookshelf).
- CONTROL: Lunar Orbiter (discard averted), Domesday (rescued), Apollo heat-flow (recovered), Nimbus (recovered), Landsat LGAC (being repatriated), CERN first website (complete duplicate survived), Vines 2014 (meta-evidence).

### Iterates

1. **Surviving-copy challenge:** TOXNET demoted (substantial duplicate survival). All 11 DISCARD_GAP instances survived. Finding: the class's G5 bar holds — eligible instances are the ones where no equivalent information survives.
2. **Known-content challenge:** synthetic negatives show G4 doing real work — a fully-cataloged archive that burns is ordinary loss, not DCC. The engine refuses the broad claim "every deleted archive contained discoveries."
3. **Discard-intent ablation:** intentional (mean 53.03, n=6), accidental (61.04, n=5), mixed (69.67, n=3). Both intents sit in the eligible set with comparable scores. The class groups the *loss shape*, not the motive — a documented limitation for policy use (intent matters for prevention), but the discriminator's point: what is uninterrogable is uninterrogable regardless of why the channel died.

## 5. Honesty ledger (what we do NOT know)

- The CERN first-website instance's URL was taken from search results and was not re-verified by opening the page in-session; the instance notes flag this. It is a CONTROL and does not affect the primary.
- 1937 Fox fire, 1965 MGM fire, and Carson Tonight Show rely on secondary sources (Wikipedia / forums); events are corroborated in preservation literature but the per-instance source strength reflects this (0.6–0.65).
- Whether every item in the MySpace corpus lacked an independent copy is unknown; whether the mold-damaged Pioneer/Helios reels remain readable is unknown; the full contents of the DuMont archive before destruction are unknown. All marked accordingly.
- No KILLED instances appear in the final set — not because the class kills nothing, but because the catalog was curated to discard-shaped candidates; the synthetic negatives in iterate 2 are the kills the real set lacks.
- Scores are heuristics: `0.25·freshness + 0.25·uniqueness + 0.20·stakes + 0.15·source_strength + 0.10·(G1∧G2∧G3) + 0.05·G4`, PENALIZED discounted ×0.45. Nothing here measures nature.

## 6. Archive subtraction

Subtracted per G7 hard kills: DIC, UCC, OAC, PPC, Undersampling, TAC, FAC, CBR, DBH, consciousness (refused). Soft penalties: CMC, CIC, EFC, UPRC, CIP, plus DCC-specific overlap codes INSTITUTIONAL (none used in final set), PLATFORM (MySpace, GeoCities), MIGRATION (TOXNET). Key distinctions recorded in the engine docstring: DIC consumes the seen object in inquiry (a later channel-discard decision is not DIC); UCC is a never-identified entity (DCC requires a channel that existed); OAC collapses the operator; CMC rides the channel; PPC eats residuals; CIC mismatches clocks; EFC mismatches generators; none of those is *deleting the channel*.

## 7. Inventorship and credit

- **Seed (2026-09-12):** authored by Haley Bird alone.
- **This buildout:** performed by an autonomous research agent under Haley Bird's direction, at her explicit grant of autonomy on 2026-09-25 to build the full program.
- AI is not a human inventor; inventorship must be reconstructed claim-by-claim with patent counsel before any filing.
- Planning bar: **2027-09-12** — a planning flag requiring legal verification, not a confirmed deadline. Nothing public has been disclosed (no repo exists), so unlike the other eight disclosures this one does not report a lost foreign right.

## 8. Next actions (need Haley's election)

- None may be taken without her explicit decision: filing, publication, repository creation or push, licensing, sharing outside her control.
- If a GitHub repo is created later, this working directory is the complete build source.
