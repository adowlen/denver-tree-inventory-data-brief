"""Pull Denver park/street tree inventory aggregates from the ArcGIS service.

Source: ODC_PARK_TREEINVENTORY_P, FeatureServer layer 241
https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_PARK_TREEINVENTORY_P/FeatureServer/241

All analysis in this package is built from server-side groupBy/count
queries (the service supports statistics and pagination); the returned
aggregate tables are saved verbatim to data/raw_aggregates.json so every
figure can be recomputed without re-pulling 359,263 rows.
"""
import json, pathlib, urllib.parse, urllib.request

BASE = ("https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/"
        "ODC_PARK_TREEINVENTORY_P/FeatureServer/241/query")

NON_TREE_SPECIES = ['_Vacant Site', '_Vacant site-not plantable', '_Stump',
                    '_Stump not plantable', '_Tree requested', '_unknown',
                    '_Vacant site - new', '_Ash on property']
NT = "SPECIES_COMMON IN ('%s')" % "','".join(NON_TREE_SPECIES)
# Not-an-identified-tree classes beyond the site-state values, found by the
# independent verifier (2026-10-23): 'ResCon' / 'ResCon Comp' administrative
# placeholders (947) and blank-species records (5).
ADMIN = "SPECIES_COMMON IN ('ResCon','ResCon Comp')"
BLANKSP = "SPECIES_COMMON=' '"
NOT_IDENTIFIED = f"({NT} OR {ADMIN} OR {BLANKSP})"
TREES = f"NOT {NOT_IDENTIFIED}"
ASH = "SPECIES_COMMON LIKE 'Ash%'"


def q(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())


def count(where):
    return q({"where": where, "returnCountOnly": "true", "f": "json"})["count"]


def group(field, where="1=1", limit=2000):
    d = q({"where": where, "groupByFieldsForStatistics": field,
           "outStatistics": json.dumps([{"statisticType": "count",
                                          "onStatisticField": "OBJECTID",
                                          "outStatisticFieldName": "cnt"}]),
           "orderByFields": "cnt DESC", "resultRecordCount": limit, "f": "json"})
    return [[f["attributes"][field], f["attributes"]["cnt"]]
            for f in d.get("features", [])]


def one(order):
    d = q({"where": "1=1", "outFields": "INVENTORY_DATE",
           "orderByFields": order, "resultRecordCount": 1, "f": "json"})
    return d["features"][0]["attributes"]["INVENTORY_DATE"]


def main():
    out = {
        "total_records": count("1=1"),
        "non_tree_records": count(NT),
        "admin_placeholder_records": count(ADMIN),
        "blank_species_records": count(BLANKSP),
        "tree_records": count(TREES),
        "ash_dates_pre2016": count(f"{ASH} AND INVENTORY_DATE < '2016-01-01'"),
        "ash_dates_2016_2020": count(f"{ASH} AND INVENTORY_DATE >= '2016-01-01' AND INVENTORY_DATE < '2021-01-01'"),
        "ash_dates_2021plus": count(f"{ASH} AND INVENTORY_DATE >= '2021-01-01'"),
        "ash_records_common": count(ASH),
        "ash_records_botanic": count("SPECIES_BOTANIC LIKE 'Fraxinus%'"),
        "ashlike_name_records": count("SPECIES_COMMON LIKE '%Ash%'"),
        "species_common": group("SPECIES_COMMON"),
        "species_botanic_fraxinus": group("SPECIES_BOTANIC",
                                          "SPECIES_BOTANIC LIKE 'Fraxinus%'"),
        "condition_all": group("CONDITION"),
        "condition_non_tree": group("CONDITION", NT),
        "condition_trees": group("CONDITION", TREES),
        "condition_ash": group("CONDITION", ASH),
        "condition_non_ash_trees": group("CONDITION", f"{TREES} AND NOT ({ASH})"),
        "diameter_trees": group("DIAMETER", TREES),
        "diameter_ash": group("DIAMETER", ASH),
        "diameter_non_tree": group("DIAMETER", NT),
        "site_designation_all": group("SITE_DESIGNATION"),
        "site_designation_ash": group("SITE_DESIGNATION", ASH),
        "site_designation_trees": group("SITE_DESIGNATION", TREES),
        "neighbor_ash": group("NEIGHBOR", ASH),
        "neighbor_trees": group("NEIGHBOR", TREES),
        "neighbor_all": group("NEIGHBOR"),
        "location_ash_park": group("LOCATION_NAME", f"{ASH} AND SITE_DESIGNATION='Park'"),
        "location_ash": group("LOCATION_NAME", ASH),
        "eab_tag_all": group("EAB_TAG"),
        "eab_tag_ash": group("EAB_TAG", ASH),
        "risk_tag_all": group("RISK_TAG"),
        "disease_ash": group("DISEASE_PEST_DEF", ASH),
        "structural_ash": group("STRUCTURAL_DEFEC", ASH),
        "inventory_date_min": one("INVENTORY_DATE ASC"),
        "inventory_date_max": one("INVENTORY_DATE DESC"),
        "ash_eab_blank": count(f"{ASH} AND EAB_TAG=' '"),
        "eab_zero_all": count("EAB_TAG='0'"),
        "eab_zero_ash": count(f"{ASH} AND EAB_TAG='0'"),
    }
    dest = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw_aggregates.json"
    dest.write_text(json.dumps(out, indent=2))
    print("total", out["total_records"], "trees", out["tree_records"],
          "ash", out["ash_records_common"])


if __name__ == "__main__":
    main()
