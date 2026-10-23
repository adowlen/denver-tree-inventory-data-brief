# Independent verification ledger - Denver park/street tree inventory brief

Date of this pass: 2026-10-23
Verifier method: independent implementation (Python/urllib against the live ArcGIS
REST query endpoint, server-side count and groupBy statistics only). The package's
code in `code/` was NOT used or read for computation. Only `stats.json` was read,
as the list of claims to test.

Source: ODC_PARK_TREEINVENTORY_P, FeatureServer layer 241
https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_PARK_TREEINVENTORY_P/FeatureServer/241/query

Verdict key: REPRODUCED = my independent query returns the builder's number.
CORRECTED = builder's number is wrong; mine is given. CAVEATED = number is right
but the claim built on it needs a qualification printed with it.

## Headline result

Every builder figure assigned for verification REPRODUCED exactly. No figure
required a correction. Several figures carry caveats (below), the most important
being inventory-date staleness for condition, string-field truncation in the
source, and the scope of the inventory itself.

## Figure-by-figure ledger

| # | Claim (builder) | My independent result | Verdict |
|---|---|---|---|
| 1 | Total records 359,263 | 359,263 (returnCountOnly, where 1=1; also sums of every groupBy partition) | REPRODUCED |
| 2 | Non-tree records 53,016 | 53,016, summed in Python from the SPECIES_COMMON groupBy (407 distinct values) over the 8 underscore values | REPRODUCED |
| 2a | _Vacant Site 26,222 | 26,222 | REPRODUCED |
| 2b | _Vacant site-not plantable 10,563 | 10,563 | REPRODUCED |
| 2c | _Stump 8,171 | 8,171 | REPRODUCED |
| 2d | _Stump not plantable 4,626 | 4,626 | REPRODUCED |
| 2e | _Tree requested 3,026 | 3,026 | REPRODUCED |
| 2f | _unknown 385 | 385 | REPRODUCED |
| 2g | _Vacant site - new 22 | 22 | REPRODUCED |
| 2h | _Ash on property 1 | 1 (see trap T5 - this record looks like a real tree) | REPRODUCED, CAVEATED |
| 3 | Tree records 306,247 | 306,247 (= 359,263 - 53,016; also reproduced as the sum of per-neighborhood tree counts after subtracting the 8 non-tree values neighborhood by neighborhood) | REPRODUCED, CAVEATED (T4) |
| 4 | Ash (Fraxinus) 33,479 by SPECIES_COMMON LIKE 'Ash%' | 33,479 | REPRODUCED |
| 5 | Ash 33,479 by SPECIES_BOTANIC LIKE 'Fraxinus%' | 33,479; cross-checks: Fraxinus-but-not-'Ash%' = 0 and 'Ash%'-but-not-Fraxinus = 0. The two definitions are perfectly concordant. Fraxinus species split also matches stats.json exactly (pennsylvanica 23,244; americana 10,123; species 55; nigra 32; quadrangulata 10; mandshurica 8; velutina 'Modesto' 3; angustifolia 2; excelsior 2) | REPRODUCED |
| 6 | Ash share of trees 10.9% | 33,479 / 306,247 = 10.93% | REPRODUCED, CAVEATED (T4: excluding ResCon placeholders it is 10.97%, which rounds to 11.0%) |
| 7 | Name-collision records 1,154 (SPECIES_COMMON LIKE '%Ash%' minus Fraxinus) | '%Ash%' total 34,633; 34,633 - 33,479 = 1,154. Breakdown in T6 | REPRODUCED |
| 8 | Ash condition Poor+Very Poor+Dead 3,802 (11.4%) | Poor 2,991 + Very Poor 631 + Dead 180 = 3,802; 3,802 / 33,479 = 11.36% -> 11.4%. Full ash condition distribution matches stats.json cell for cell (Fair 21,188; Good 8,440; Excellent 24; N/A 24; blank ' ' 1). Control also reproduced: non-ash trees Poor+Very Poor+Dead = 28,978 / 272,768 = 10.6% | REPRODUCED, CAVEATED (T2) |
| 9 | Ash in two smallest diameter bins (0 to 6, 6 to 12) 14,401 (43.0%) | 2,724 + 11,677 = 14,401; 43.02% of all ash. Full ash diameter distribution matches stats.json cell for cell and sums to 33,479 | REPRODUCED, CAVEATED (T7) |
| 10 | Ash at 24+ inch bins 2,505 (7.5%) | 1,691 + 597 + 162 + 37 + 18 = 2,505; 7.48% -> 7.5% | REPRODUCED |
| 11 | Ash SITE_DESIGNATION 'Private Maintained Street Tr' 22,574 (67.4%) | 22,574; 67.43%. Full ash site-designation distribution matches stats.json cell for cell | REPRODUCED, CAVEATED (T3: the label itself is truncated in the source) |
| 12 | Ash SITE_DESIGNATION Park 2,612 | 2,612 (7.8%) | REPRODUCED |
| 13 | EAB_TAG blank for ash 29,176 | 29,176. The "blank" is the literal single-space value ' ' (the service returns no null/empty EAB_TAG for ash; the space count and the null-or-empty count coincide at 29,176). Remainder tagged with anything: 4,303 (87.1% / 12.9% split as in stats.json) | REPRODUCED, CAVEATED (T8) |
| 14 | Top ash-count neighborhood: Gateway - Green Valley Ranch 2,374 | 2,374 ash, of 18,544 trees (12.8%) - matches stats.json. Next: Central Park 1,961; South Park Hill 1,203; Congress Park 1,068; Indian Creek 924 | REPRODUCED |
| 15 | Top ash-share neighborhood: Marston 29.6% (815 of 2,757) | 815 / 2,757 = 29.56% -> 29.6%. Holds with NO minimum-count filter: ranking all 78 real neighborhoods by share, Marston is still #1 (next Indian Creek 27.6%, Windsor 22.7%, City Park West 21.6%, Congress Park 18.4%). Bottom of the table also matches stats.json (Union Station 3.1% lowest) | REPRODUCED |
| 16 | City Park location (Park designation) ash 400 | 400 where SPECIES_BOTANIC LIKE 'Fraxinus%' AND SITE_DESIGNATION='Park' AND LOCATION_NAME='City Park'. It is the #1 park location; next Wallace (George M) Park 195, Sloan's Lake Park 132 | REPRODUCED, CAVEATED (T9) |
| 17 | Inventory dates pre-2000: count 2 | 2, via string comparison INVENTORY_DATE < '2000-01-01'. The two records: 1604-09-07 and 1899-12-29, both _Vacant Site records. String min/max for the whole layer: 1604-09-07 / 2026-06-30, matching the builder's inventory_date_note, including the single additional record in 2000-2013 | REPRODUCED |

## Traps and semantic attacks

T1. SCOPE - this is not a census of Denver's trees. The layer description says it
covers trees managed by Denver Parks and Recreation. The ash population is
dominated by street trees in front of private homes (67.4% 'Private Maintained
Street Tr'); only 664 ash carry SITE_DESIGNATION 'Private Property Tree'.
Every share in the brief is a share of INVENTORIED trees. Any wording like
"10.9% of Denver's trees" is misleading; "10.9% of the 306,247 inventoried
trees" is the defensible form.

T2. CONDITION IS A STALE MOSAIC, NOT A 2026 HEALTH READING. INVENTORY_DATE for
ash records: 20,160 (60.2%) fall in 2010-2015, 10,894 (32.5%) in 2016-2020,
only 2,425 (7.2%) in 2021 or later, none before 2010. Condition, diameter and
EAB_TAG are values recorded at each tree's last inventory visit, spread over
roughly 16 years. "11.4% of ash are Poor, Very Poor or Dead" means "were rated
so when last visited", and trees rated Dead a decade ago may since have been
removed or replaced while still appearing here. The brief must not present the
condition mix as current, and must not attribute the ash-vs-non-ash condition
gap (11.4% vs 10.6%, both reproduced) to emerald ash borer: the gap is small,
the ratings mostly predate any plausible local EAB effect window in this data,
and rating era and tree size are uncontrolled confounders.

T3. TRUNCATION IS SYSTEMIC IN THE SOURCE (LOCATION_NAME / SITE_DESIGNATION).
The ArcGIS schema declares these fields length 50, but stored values are cut at
much shorter legacy widths: LOCATION_NAME max length 28 (15,607 records sit
exactly at the cap), NEIGHBOR max 28, SITE_DESIGNATION max 28, COMMENTS max 30,
WORKGROUP max 8 (values are literally 'Inspecti', 'Operatio', 'Sister A',
'Unassign'). Consequences:
- 'Private Maintained Street Tr' (28 chars, 191,250 records layer-wide) is a
  truncated label, near-certainly 'Private Maintained Street Tree' - compare
  'City maintained street tree' (27 chars), which survives whole. Print the
  label as it appears in the data, or expand it only with a note.
- LOCATION_NAME values end mid-word: 'Wallace (George M) Park Nort',
  'Weir Gulch Park - North of A', 'Wellshire Municipal Golf Cou',
  'Williams (Dr. Daniel Hale) P'. Park-level counts for truncated names may be
  splits of one real place. Robustness check: merging the two Wallace values
  (195 + 84 = 279 ash) still ranks #2 behind City Park's 400, and merging Weir
  Gulch North + South + Marina (81 + 35 + 1 = 117) still ranks below Sloan's
  Lake Park's 132, so the published top-parks ordering survives. Individual
  truncated-name counts should still be described as counts of that recorded
  location string, not clean park totals.

T4. THE "TREE" DENOMINATOR INCLUDES ADMINISTRATIVE PLACEHOLDERS. The builder's
partition counts everything not starting with '_' as a tree. That sweeps in
947 records whose species (common AND botanic) is literally 'ResCon' (419) or
'ResCon Comp' (528) - residential-construction administrative records, 932 of
them with condition 'N/A', sample comments about admin fees - plus 5 records
with blank (' ') species. None is an identified tree. Excluding the 947 ResCon
records, ash share is 33,479 / 305,300 = 10.97%, which rounds to 11.0% rather
than 10.9%. This does not make 10.9% wrong - it is correct under the stated
underscore partition - but the brief should disclose that the denominator
includes ~950 unclassified administrative records, because the headline share
sits exactly on that rounding edge.

T5. '_Ash on property' IS PROBABLY A REAL ASH TREE COUNTED AS A NON-TREE. The
single record under that underscore value has SPECIES_BOTANIC 'Ash on property',
condition Good, diameter 12 to 18, 1 stem, SITE_DESIGNATION 'Private Property
Tree'. The underscore rule classifies it as a non-tree and it also sits inside
the 1,154 name-collision count. Reclassifying it would make ash 33,480 and
trees 306,248 - immaterial to every percentage, but it shows the non-tree rule
is a naming convention, not a botanical test.

T6. HOW THE NAME COLLISION ACTUALLY WORKS (1,154). The '%Ash%' substring search
catches: Hawthorn, Washington 766 ('ash' inside 'Washington'), Maple, Flashfire
Sugar 209 ('ash' inside 'Flashfire'), Mountain Ash (Sorbus, a different genus)
148 across three values, Peashrub, Siberian 30 ('ash' inside 'Peashrub'), and
the 1 '_Ash on property'. A naive common-name search would overstate ash by
3.4%. The builder's Fraxinus-based count avoids this, and the two ash
definitions agreeing exactly (33,479 both ways, zero mismatches in either
direction) is the strongest single check in the package.

T7. DIAMETER BINS ARE COARSE STRINGS WITH SHARED EDGES. Bins are pre-binned
labels ('0 to 6', '6 to 12', ...) - a tree at exactly 6 inches fits both labels
as printed, so claims must be about bin membership, not exact size thresholds.
58 ash (0.2%) have blank diameter ' '; the 43.0% figure includes them in the
denominator (excluding them gives 43.1%). Small diameter also does not by
itself prove a tree is young or recently planted; the brief should not convert
the 43.0% into an age or planting-era claim without a separate source.

T8. EAB_TAG CANNOT SUPPORT A TREATMENT CLAIM. Layer-wide it has 178 distinct
values; the ash values include unexplained codes ('xx' 1,733, 'BB' 1,481, 'TI'
545, '0' 329, 'BB?' 67) and stray note fragments truncated mid-word ('basal
woun', 'Tree is mostly dead should come d'). Blank (' ') at 87.1% therefore
means only "no tag text recorded". It must not be rendered as untreated,
uninspected, or untreated-by-the-city. The builder withheld a treatment claim;
that restraint is correct and should stay.

T9. CITY PARK: TWO DIFFERENT NUMBERS, BOTH TRUE. LOCATION_NAME 'City Park'
with Park designation = 400 ash (the park grounds). NEIGHBOR 'City Park' (the
neighborhood) = 790 ash of 7,722 trees, because it also counts street trees on
the surrounding blocks. The brief must label the 400 as the park itself and
never let it be read as the neighborhood figure, or vice versa.

T10. "81 NEIGHBORHOODS" OVERCOUNTS REAL NEIGHBORHOODS BY 3. stats.json says
neighborhoods_with_trees: 81. The NEIGHBOR field (the field is literally named
NEIGHBOR) has 81 distinct values, but three are pseudo-values: 'Unassigned'
(4,282 trees, 32 ash), 'N/A' (170 trees, 6 ash), ' ' (12 trees, 1 ash). Real
named neighborhoods with trees: 78. Rankings are unaffected (the builder
excluded the pseudo-values from rankings, correctly), but any prose saying
"81 neighborhoods" should say 78, or "81 recorded values, 78 of them real
neighborhoods". Marked CAVEATED rather than CORRECTED because the underlying
count is a true count of distinct values.

T11. QUERY TRAP WORTH RECORDING FOR FUTURE PASSES: in ArcGIS SQL, '_' is a
single-character wildcard, so SPECIES_COMMON LIKE '_%' matches ALL 359,263
records, not just underscore-prefixed ones. (My first neighborhood pass hit
exactly this and returned a non-tree total of 359,263; it was caught and
redone with an explicit IN list of the 8 values and with Python-side prefix
filtering of the groupBy result, which agree at 53,016.) Any future
verification that uses LIKE '_%' server-side will silently reproduce nothing.

## Overall assessment

The package's numbers are sound: 17 of 17 assigned figures reproduced exactly
from the live source with an independent implementation, including both ash
definitions, the condition and diameter distributions cell for cell, and both
neighborhood rankings. Nothing needs correcting before publication. The brief
should carry four disclosures: (1) shares are of inventoried, DPR-managed
trees, not all Denver trees; (2) condition/diameter/EAB values date from each
tree's last inventory visit, mostly 2010-2020 for ash; (3) source labels are
truncated at 28 characters, including the top site designation and several
park names; (4) the tree denominator includes ~950 'ResCon' administrative
records, on which the 10.9% headline sits at a rounding edge (10.97% without
them).
