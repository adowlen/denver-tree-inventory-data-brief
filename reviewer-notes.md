# Reviewer notes - Denver tree inventory brief (2026-10-23)

## Publication status

The independent verifier reproduced all 17 assigned figures exactly (verification-ledger-independent.md). Its traps were adjudicated and the package rebuilt where they bit (identified-tree population, stale-mosaic disclosure, 28-character truncation, City Park scope line); the full fix loop is in verification.md. The Section 10 audit passes on the rebuilt package and the hero and charts were regenerated and re-viewed. Under Alex's 2026-10-20 rule the brief is published to GitHub in this run (repo creation, push, catalog and Pages updates recorded in the morning report).

## Claims most likely to be challenged

- "11.0 percent of inventoried trees are ash" will be read against the city's "1 in 6 trees are ash" line. The brief separates the two bases explicitly: 1 in 6 is the city's estimate for ALL Denver trees (330,000 ash); 11.0 percent is the measured share in the Parks-managed inventory, and the city's own public-land figure is 1 in 10, which the inventory matches. Note the population sensitivity the verifier caught: on an underscore-only partition the share is 10.93 percent; the brief prints the identified-tree figure (11.0) and records both in verification.md. Expect a reader to conflate them anyway; the distinction is in Finding 2, in the same paragraph as the number.
- The 43.0 percent "two smallest diameter bins" figure sits next to the city's removal-and-replacement eligibility (12 inches or less, declining or dead). The brief states it is NOT an eligibility count, because the 6-to-12 bin cannot be split at exactly 12 and the program has further conditions. This is the figure most likely to be quoted without its caveat.
- Finding 6 (EAB_TAG) reflects on the dataset, and by extension on Denver Parks and Recreation / the Office of the City Forester: the public dataset's only EAB field is blank for 87.1 percent of ash and otherwise undefined. Flagged for extra review per the standards (a finding that reflects on a specific department). The brief's Who can act asks for a codebook as a low-cost operational change and reports the city's own treated count (6,000, from Be A Smart Ash) as reported, in the same finding.

## Methods checks that could not be completed

- EAB treatment coverage cannot be computed from the public data at all (Finding 6). No workaround exists in this dataset; the city-reported 6,000 treated figure is carried as reported, not measured.
- Inventory-date currency per tree: condition and diameter are as of each record's inventory date, which varies and cannot be turned into a clean "as of" date per neighborhood from the published field (dates are text; 2 impossible values exist). The brief makes no per-neighborhood currency claim.
- LOCATION_NAME and SITE_DESIGNATION values are truncated in the source (about 30 characters). Park counts are reported as filed per location value; Wallace (George M) Park's two values (195 + 84) are printed separately rather than merged by guesswork.

## Findings that surprised us

- One record in seven in a "tree inventory" is not a tree: 53,016 vacant sites, stumps, and requests. Any quick pull of this dataset that divides by 359,263 understates every tree share.
- The name-collision trap is real in both directions: a naive "contains ash" search adds 1,154 non-Fraxinus trees (mountain ash is Sorbus), while the two-field genus check agrees to the record.
- Ash condition is close to all other trees (11.4 percent poor or worse, vs 10.7 percent), and most ash condition ratings are old: 60.2 percent of ash inventory dates fall in 2010 to 2015 and only 7.2 percent in 2021 or later. The condition distribution is a last-visit mosaic, not a 2026 health reading, and the brief now says so in Finding 5 with the era counts printed.
- The verifier's population catch: 947 'ResCon' administrative placeholders and 5 blank-species records were inside the first build's tree count. The package was rebuilt on the identified-tree population (305,295) before publication; the fix loop is recorded in verification.md.
