# Sources - Denver park and street tree inventory brief (2026-10-23)

Every figure in brief-draft.md, with its source. Derived figures are labeled derived.

## Primary source (all counted figures)

- City and County of Denver, Denver Open Data Catalog: ODC_PARK_TREEINVENTORY_P, "point representation of trees managed by the Department of Parks and Recreation in the City and County of Denver," ArcGIS FeatureServer layer 241, services1.arcgis.com/zdB7qR0BtYrg0Xpl. Service description: data based on GPS locations of trees in parks, medians, parkways, and along streets; for planning, design, and cartographic purposes. Pulled October 23, 2026 via server-side count and groupBy queries recorded in code/pull_data.py; aggregate output saved as data/raw_aggregates.json.
  - Total records 359,263; species Counter (407 values); condition Counter (9 values); EAB_TAG Counter (178 values); site designation Counter (24 values); neighborhood Counter (81 values): all from that pull.
  - Non-tree records 53,016 (derived): records whose SPECIES_COMMON is one of the eight site-state values listed in Finding 1, counted from the species Counter and cross-checked by a direct count query.
  - Not-an-identified-tree records 53,968 (derived): the 53,016 site-state records above, plus 947 'ResCon' (419) / 'ResCon Comp' (528) administrative placeholder records and 5 blank-species records, each counted by direct query in the pull (the ResCon and blank classes were added after the independent verifier's pass, 2026-10-23).
  - Tree records 305,295 (derived): 359,263 minus 53,968, cross-checked by a direct count query on the combined exclusion.
  - Ash 33,479: counted two ways from the same pull, SPECIES_COMMON LIKE 'Ash%' and SPECIES_BOTANIC LIKE 'Fraxinus%', exact agreement. Fraxinus species split (pennsylvanica 23,244; americana 10,123; others 112, derived by summing the remaining Fraxinus values) from the botanical Counter filtered to Fraxinus.
  - Name-collision count 1,154 (derived): SPECIES_COMMON LIKE '%Ash%' count (34,633) minus Fraxinus count (33,479), both direct count queries in the pull.
  - Ash shares 11.0 percent of trees and 9.3 percent of all records (derived). On the earlier underscore-only partition (306,247 trees) the share was 10.93 percent; the identified-tree figure is the one the brief prints, and both are recorded in verification.md.
  - Condition, diameter-bin, site-designation, neighborhood, and park-location figures for ash: groupBy counters in the pull, reproduced in stats.json.
  - EAB_TAG for ash: blank 29,176, tagged 4,303 (derived: 33,479 minus 29,176); code values from the EAB_TAG Counter filtered to ash.
  - Inventory-date anomalies and eras: direct queries in the pull and verification pass (2 records with INVENTORY_DATE before 2000; none after 2026-06-30; none blank or null; ash inventory-date eras pre-2016 20,160, 2016-2020 10,894, 2021 or later 2,425).

## City context (reported figures, labeled as reported in the brief)

- Denver, June 2025: EAB confirmed in Denver on June 17, 2025, identified by Colorado State University entomology experts and the Office of the City Forester; city figures of 330,000 ash trees in the City and County of Denver, about 1 in 6 trees citywide, and 1 in 10 trees on public land. City announcement as syndicated from denvergov.org (Denver Parks and Recreation, Executive Director Jolon Clark; City Forester Luke Killoran), republished at treeandlawncareco.org, "Emerald Ash Borer Detected in Denver," June 26, 2025; same figures on the city's Be A Smart Ash site (beasmartash.org, "EAB Found in Denver," June 27, 2025).
- Be A Smart Ash (beasmartash.org, city campaign site): 6,000 ash trees treated in parks and parkways since the 2016 campaign launch; more than 1,000 removed; about 1,500 new trees planted per year. Reported as city figures in the brief.
- Be A Smart Ash, Ash Removal and Replacement Program page (beasmartash.org/ashreplacement): eligibility includes ash in the public right of way, 12 inches or less in diameter, in declining or dead condition; program created 2020; east side in 2025, west side in 2026.
- Denver City Council news release, denvergov.org, published October 9, 2026: 2027 budget dates (final proposal October 19, hearing October 26, amendment vote November 2, passage November 9). Citation carried from the 2026-10-18 traffic-accidents package, where it was verified live.
- Denver Council Bill 26-1451 (Legacy Tree designation), listed for Parks, Art and Culture Committee consideration October 6, 2026, per the city's Legistar matter record as reported by The Badger (denver.thebadger.news, October 2, 2026). Context only; no figure in the brief depends on it.
