"""Data charts for the Denver tree inventory brief. Brand palette:
dark charcoal background, amber + teal bars, white text."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = pathlib.Path(__file__).resolve().parent.parent
s = json.loads((root / "stats.json").read_text())
BG, AMBER, TEAL, FG = "#1c1c1e", "#e8a33d", "#2a9d8f", "#f2f2f2"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG,
                     "text.color": FG, "axes.labelcolor": FG,
                     "xtick.color": FG, "ytick.color": FG,
                     "axes.edgecolor": "#555555", "font.size": 10})

# 1. Neighborhood ash share (rate, counts printed on each bar)
rows = s["top_ash_rate_neighborhoods"][::-1]
fig, ax = plt.subplots(figsize=(8.2, 4.6))
ax.barh([r[0] for r in rows], [r[3] for r in rows], color=AMBER)
for i, r in enumerate(rows):
    ax.text(r[3] + 0.5, i, f"{r[3]}%  ({r[1]:,} of {r[2]:,} trees)",
            va="center", fontsize=9)
ax.set_xlim(0, 38)
ax.set_xlabel("Ash (Fraxinus) as a share of the neighborhood's inventoried trees")
ax.set_title(f"Highest ash shares by neighborhood\nCitywide: {s['ash_share_of_trees_pct']}% of inventoried trees (33,479 of {s['tree_records']:,})",
             loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_neighborhood_rates.png", dpi=200)
plt.close(fig)

# 2. Ash diameter bins (recorded text bins, as filed)
order = ["0 to 6", "6 to 12", "12 to 18", "18 to 24", "24 to 30",
         "30 to 36", "36 to 42", "42 to 48", "48 +"]
dia = s["diameter_ash"]
vals = [dia.get(k, 0) for k in order]
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.bar(order, vals, color=TEAL)
for i, v in enumerate(vals):
    ax.text(i, v + 350, f"{v:,}", ha="center", fontsize=8.5)
ax.set_ylabel("Ash trees")
ax.set_xlabel("Recorded diameter bin (inches, as filed in the inventory)")
ax.set_title("Ash trees by recorded diameter bin (33,479 ash; 58 with no bin recorded)",
             loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_ash_diameter.png", dpi=200)
plt.close(fig)

# 3. Condition: ash vs non-ash trees, share of each group (same measure)
cats = ["Excellent", "Good", "Fair", "Poor", "Very Poor", "Dead"]
import collections
raw = json.loads((root / "data" / "raw_aggregates.json").read_text())
ca = dict(raw["condition_ash"]); cn = dict(raw["condition_non_ash_trees"])
ta = sum(ca.values()); tn = sum(cn.values())
pa = [100 * ca.get(c, 0) / ta for c in cats]
pn = [100 * cn.get(c, 0) / tn for c in cats]
x = range(len(cats)); w = 0.38
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.bar([i - w / 2 for i in x], pa, w, color=AMBER, label=f"Ash (n={ta:,})")
ax.bar([i + w / 2 for i in x], pn, w, color=TEAL, label=f"All other trees (n={tn:,})")
for i, (a, b) in enumerate(zip(pa, pn)):
    ax.text(i - w / 2, a + 1.2, f"{a:.1f}%", ha="center", fontsize=8.5)
    ax.text(i + w / 2, b + 1.2, f"{b:.1f}%", ha="center", fontsize=8.5)
ax.set_xticks(list(x)); ax.set_xticklabels(cats)
ax.set_ylabel("Share of the group (%)")
ax.set_title("Recorded condition: ash vs all other inventoried trees\n"
             "Shares use the full group counts; N/A or blank condition has no bar (25 ash, 797 other trees)",
             loc="left", fontsize=11)
ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_condition.png", dpi=200)
plt.close(fig)
print("charts done")
