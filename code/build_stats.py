"""Build stats.json + neighborhood panel CSV from data/raw_aggregates.json."""
import csv, json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
raw = json.loads((root / "data" / "raw_aggregates.json").read_text())

def d(pairs):
    return {k: v for k, v in pairs}

def pct(n, den):
    return round(100 * n / den, 1)

total = raw["total_records"]; trees = raw["tree_records"]
nontree = raw["non_tree_records"]; ash = raw["ash_records_common"]

species = d(raw["species_common"])
nontree_species = {k: species[k] for k in
                   ['_Vacant Site', '_Vacant site-not plantable', '_Stump',
                    '_Stump not plantable', '_Tree requested', '_unknown',
                    '_Vacant site - new', '_Ash on property']}
assert sum(nontree_species.values()) == nontree

cond_ash = d(raw["condition_ash"]); cond_trees = d(raw["condition_trees"])
cond_nonash = d(raw["condition_non_ash_trees"]); nonash = trees - ash
poor = lambda c: c.get("Poor", 0) + c.get("Very Poor", 0) + c.get("Dead", 0)

dia_ash = d(raw["diameter_ash"])
size_le12 = dia_ash.get("0 to 6", 0) + dia_ash.get("6 to 12", 0)
size_ge18 = sum(v for k, v in dia_ash.items()
                if k in ("18 to 24", "24 to 30", "30 to 36", "36 to 42",
                         "42 to 48", "48 +"))
size_ge24 = sum(v for k, v in dia_ash.items()
                if k in ("24 to 30", "30 to 36", "36 to 42", "42 to 48", "48 +"))

sd_ash = d(raw["site_designation_ash"]); sd_trees = d(raw["site_designation_trees"])
na = d(raw["neighbor_ash"]); nt_ = d(raw["neighbor_trees"])
panel = []
for name, t in nt_.items():
    a = na.get(name, 0)
    panel.append({"neighborhood": name, "trees": t, "ash": a,
                  "ash_share_pct": pct(a, t) if t else 0.0})
panel.sort(key=lambda r: -r["ash"])
ranked = [r for r in panel if r["trees"] >= 100
          and r["neighborhood"] not in ("Unassigned", "N/A", " ")]
by_rate = sorted(ranked, key=lambda r: -r["ash_share_pct"])

loc_park = raw["location_ash_park"]
eab_ash = d(raw["eab_tag_ash"])

stats = {
    "source_pull_date": "2026-10-23",
    "source_dataset": "ODC_PARK_TREEINVENTORY_P (Denver Open Data, ArcGIS FeatureServer layer 241)",
    "total_records": total,
    "non_tree_records": nontree,
    "non_tree_share_pct": pct(nontree, total),
    "non_tree_by_species": nontree_species,
    "admin_placeholder_records": raw["admin_placeholder_records"],
    "blank_species_records": raw["blank_species_records"],
    "not_identified_tree_records": nontree + raw["admin_placeholder_records"] + raw["blank_species_records"],
    "ash_inventory_date_eras": {"pre_2016": raw["ash_dates_pre2016"],
                                "y2016_2020": raw["ash_dates_2016_2020"],
                                "y2021_plus": raw["ash_dates_2021plus"]},
    "vacant_plantable": species["_Vacant Site"] + species["_Vacant site - new"],
    "stumps": species["_Stump"] + species["_Stump not plantable"],
    "tree_records": trees,
    "ash_records": ash,
    "ash_share_of_trees_pct": pct(ash, trees),
    "ash_share_of_all_records_pct": pct(ash, total),
    "name_collision_excluded": raw["ashlike_name_records"] - ash,
    "fraxinus_by_species": d(raw["species_botanic_fraxinus"]),
    "green_ash": species["Ash, Green"],
    "white_ash": species["Ash, White"],
    "top_tree_species": [[k, v, pct(v, trees)] for k, v in
                         sorted(((k, v) for k, v in species.items()
                                 if not k.startswith("_")),
                                key=lambda kv: -kv[1])[:5]],
    "condition_ash": cond_ash,
    "ash_poor_verypoor_dead": poor(cond_ash),
    "ash_poor_verypoor_dead_pct": pct(poor(cond_ash), ash),
    "nonash_poor_verypoor_dead_pct": pct(poor(cond_nonash), nonash),
    "ash_good_excellent_pct": pct(cond_ash.get("Good", 0) + cond_ash.get("Excellent", 0), ash),
    "ash_fair_pct": pct(cond_ash.get("Fair", 0), ash),
    "diameter_ash": dia_ash,
    "ash_le12_bins": size_le12, "ash_le12_pct": pct(size_le12, ash),
    "ash_ge18": size_ge18, "ash_ge18_pct": pct(size_ge18, ash),
    "ash_ge24": size_ge24, "ash_ge24_pct": pct(size_ge24, ash),
    "ash_diameter_unknown": dia_ash.get(" ", 0) + dia_ash.get("N/A", 0),
    "site_designation_ash": sd_ash,
    "ash_private_maintained_street": sd_ash.get("Private Maintained Street Tr", 0),
    "ash_private_maintained_street_pct": pct(sd_ash.get("Private Maintained Street Tr", 0), ash),
    "ash_park_designation": sd_ash.get("Park", 0),
    "ash_park_designation_pct": pct(sd_ash.get("Park", 0), ash),
    "ash_school": sd_ash.get("School", 0),
    "eab_tag_ash_blank": raw["ash_eab_blank"],
    "eab_tag_ash_blank_pct": pct(raw["ash_eab_blank"], ash),
    "eab_tag_ash_tagged": ash - raw["ash_eab_blank"],
    "eab_tag_unique_values_all": len(raw["eab_tag_all"]),
    "neighborhood_values_with_trees": len([r for r in panel if r["trees"] > 0]),
    "real_neighborhoods_with_trees": len([r for r in panel if r["trees"] > 0
                                          and r["neighborhood"] not in ("Unassigned", "N/A", " ")]),
    "top_ash_count_neighborhoods": [[r["neighborhood"], r["ash"], r["trees"],
                                     r["ash_share_pct"]] for r in panel[:5]],
    "top_ash_rate_neighborhoods": [[r["neighborhood"], r["ash"], r["trees"],
                                    r["ash_share_pct"]] for r in by_rate[:5]],
    "bottom_ash_rate_neighborhoods": [[r["neighborhood"], r["ash"], r["trees"],
                                       r["ash_share_pct"]] for r in by_rate[-5:]],
    "top_parks_by_ash": loc_park[:8],
    "inventory_date_min": raw["inventory_date_min"],
    "inventory_date_max": raw["inventory_date_max"],
}
(root / "stats.json").write_text(json.dumps(stats, indent=2))
with open(root / "data" / "neighborhood_panel_trees.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["neighborhood", "trees", "ash", "ash_share_pct"])
    w.writeheader(); w.writerows(panel)
print(json.dumps({k: stats[k] for k in
                  ["ash_share_of_trees_pct", "ash_poor_verypoor_dead_pct",
                   "ash_le12_pct", "ash_ge24_pct"]}, indent=1))
print("top rate", stats["top_ash_rate_neighborhoods"])
print("top count", stats["top_ash_count_neighborhoods"])
