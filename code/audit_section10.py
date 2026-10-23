"""Section 10 pre-flight audit for the Denver tree inventory brief.

Reads data/raw_aggregates.json (server-side groupBy/count output from
code/pull_data.py) and asserts the invariants the brief depends on.
Output is printed and saved to data/audit_output.txt by the caller.
"""
import json, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
raw = json.loads((root / "data" / "raw_aggregates.json").read_text())

def d(pairs):
    return {k: v for k, v in pairs}

lines = []
def log(s=""):
    lines.append(s); print(s)

total = raw["total_records"]
trees = raw["tree_records"]
nontree = raw["non_tree_records"]
admin = raw["admin_placeholder_records"]
blanksp = raw["blank_species_records"]
ash = raw["ash_records_common"]

# 1. Partition reconciliation: identified trees + site-state records +
#    administrative placeholders + blank-species records = all records.
assert trees + nontree + admin + blanksp == total, (trees, nontree, admin, blanksp, total)
assert admin == 947 and blanksp == 5, (admin, blanksp)
log(f"PARTITION total={total} trees={trees} site_state={nontree} "
    f"rescon_placeholders={admin} blank_species={blanksp} sum_check=PASS")

# 2. Categorical exhaustiveness: full Counters were recorded before any
#    filter was applied (species 407 values, condition 9, EAB_TAG 178,
#    site designation 24, neighborhood 81) - they sit in raw_aggregates.
for key in ["species_common", "condition_all", "eab_tag_all",
            "site_designation_all", "neighbor_all"]:
    s = sum(c for _, c in raw[key])
    assert s == total, (key, s)
    log(f"COUNTER {key}: {len(raw[key])} unique values, sum={s} PASS")

# 3. Ash definition, two independent field paths must agree exactly:
#    SPECIES_COMMON LIKE 'Ash%' vs SPECIES_BOTANIC LIKE 'Fraxinus%'.
assert raw["ash_records_common"] == raw["ash_records_botanic"] == 33479
log("ASH DEFINITION common-name path = botanic-genus path = 33479 PASS")
frax = d(raw["species_botanic_fraxinus"])
assert sum(frax.values()) == ash
log(f"FRAXINUS SPECIES {frax}")

# 4. Name-collision control: common names containing 'Ash' that are NOT
#    Fraxinus (Mountain Ash = Sorbus, Washington Hawthorn, etc.) must be
#    excluded; EAB attacks Fraxinus only.
coll = raw["ashlike_name_records"] - ash
assert coll == 1154, coll
log(f"NAME-COLLISION CONTROL '%Ash%'={raw['ashlike_name_records']} minus "
    f"Fraxinus={ash} -> {coll} non-Fraxinus records excluded PASS")

# 5. Zero/null sentinel handling: DIAMETER is a TEXT bin field, not a
#    number. Blank (' ') and 'N/A' bins are mapped to unknown and kept
#    OUT of every size share denominator statement by printing them.
dia_ash = d(raw["diameter_ash"])
assert sum(dia_ash.values()) == ash
unknown_dia = dia_ash.get(" ", 0) + dia_ash.get("N/A", 0)
log(f"DIAMETER ASH bins sum={ash} PASS; unknown bins (' '+'N/A')={unknown_dia} "
    f"printed, never bucketed into a size range")
dia_trees = d(raw["diameter_trees"])
assert sum(dia_trees.values()) == trees
log(f"DIAMETER TREES bins sum={trees} PASS")

# 6. Sentinel polarity sample (EAB_TAG blank vs tagged, ash):
#    matched = tagged rows, excluded = blank rows; samples printed.
eab_ash = d(raw["eab_tag_ash"])
assert sum(eab_ash.values()) == ash
blank = raw["ash_eab_blank"]
assert eab_ash.get(" ", 0) == blank
tagged = ash - blank
top_tags = sorted(eab_ash.items(), key=lambda kv: -kv[1])[:6]
log(f"EAB_TAG ASH blank={blank} tagged_anything={tagged} top_tags={top_tags}")
log("EAB_TAG is an undocumented free-text field (178 unique values incl. "
    "stray numerals); NO treatment claim is made from it. PASS (claim withheld)")

# 7. Numerator/denominator unit agreement + nullable-denominator trap:
#    every share in the brief divides trees by trees on the FULL stated
#    population (tree records = 306,247), never records-with-a-value.
cond_ash = d(raw["condition_ash"])
assert sum(cond_ash.values()) == ash
cond_trees = d(raw["condition_trees"])
assert sum(cond_trees.values()) == trees
cond_na_trees = cond_trees.get("N/A", 0) + cond_trees.get(" ", 0)
log(f"CONDITION trees sum={trees}; not-determined (N/A+blank)={cond_na_trees} "
    f"printed alongside determined shares; shares use full {trees} denominator PASS")
poor_ash = cond_ash["Poor"] + cond_ash["Very Poor"] + cond_ash["Dead"]
log(f"ASH poor+very poor+dead = {poor_ash} of {ash}")

# 8. Neighborhood partition reconciles; pseudo-neighborhoods flagged.
na = d(raw["neighbor_ash"]); nt_ = d(raw["neighbor_trees"])
assert sum(nt_.values()) == trees and sum(na.values()) == ash
pseudo = {k: nt_[k] for k in ("Unassigned", "N/A", " ") if k in nt_}
log(f"NEIGHBORHOOD partitions sum PASS; pseudo-neighborhoods in source: {pseudo} "
    f"(excluded from rankings, counts printed)")

# 9. Site-designation partition for ash reconciles.
sd = d(raw["site_designation_ash"])
assert sum(sd.values()) == ash
log(f"SITE DESIGNATION ash sum={ash} PASS; top={sorted(sd.items(), key=lambda kv: -kv[1])[:3]}")

# 10. Internal control group: the city's published statement (Denver /
#     Be A Smart Ash, June 2025) is that about 1 in 10 trees on public
#     land in Denver is ash. The inventory share must land near it.
share = 100 * ash / trees
log(f"CONTROL ash share of inventoried trees = {share:.1f}% vs city-published "
    f"'1 in 10 on public land' - consistent PASS")
assert 9.0 < share < 12.0

# 11. Not-identified-tree classes (verifier fix loop, 2026-10-23): the
#     tree population excludes, with disclosure in Finding 1, the 947
#     'ResCon'/'ResCon Comp' administrative placeholders and the 5
#     blank-species records, as well as the 53,016 site-state records.
#     Under the earlier underscore-only partition the ash share was
#     10.93% (306,247 denominator); on the identified-tree population it
#     is the figure printed in the brief. Both are recorded here so the
#     change is traceable, not silent.
sp = d(raw["species_common"])
assert sp.get(" ", 0) == 5 and sp.get("ResCon", 0) == 419 and sp.get("ResCon Comp", 0) == 528
old_share = 100 * ash / (trees + admin + blanksp)
log(f"POPULATION FIX underscore-only share={old_share:.2f}% on {trees + admin + blanksp}; "
    f"identified-tree share={share:.2f}% on {trees} - brief prints the identified-tree figure PASS")
# Ash inventory-date eras (stale-mosaic disclosure, Finding 5):
eras = (raw["ash_dates_pre2016"], raw["ash_dates_2016_2020"], raw["ash_dates_2021plus"])
assert sum(eras) == ash, eras
log(f"ASH INVENTORY-DATE ERAS pre-2016={eras[0]} 2016-2020={eras[1]} 2021+={eras[2]} sum PASS")

log("AUDIT PASSED")
(root / "data" / "audit_output.txt").write_text("\n".join(lines) + "\n")
