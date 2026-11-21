"""Reproduces Table II, the Mainstream vs. Niche rates (Fig. 3), the Fisher's exact
tests and the knowledge-cutoff adjustment (Sec. IV-B), and the cutoff placement of
Outdated Tags (Sec. IV-F). Run from the repository root:
    python analysis/overall_and_mainstream_niche.py
"""
import pandas as pd
from scipy.stats import fisher_exact

c = pd.read_csv("data/combined/combined_full_results_rechecked.csv")
ins = c[c["Automated Category"] != "OUT OF SCOPE"].copy()
print(f"Collected: {len(c)}  in scope (Docker Hub): {len(ins)}  out of scope: {len(c) - len(ins)}")

# ---- Table II ----
vc = ins["Automated Category"].value_counts()
resolved = ins[ins["Automated Category"] != "NEEDS MANUAL CHECK"]
t2 = pd.DataFrame({"Count": vc, "%": (100 * vc / len(ins)).round(1),
                   "% resolved": (100 * resolved["Automated Category"].value_counts() / len(resolved)).round(1)})
print("\nTable II\n", t2.to_string())

# ---- Mainstream vs. Niche, three definitions ----
cat = ins["Automated Category"]
NE = {"Nonexistent Tag", "Non-Existent Image"}
BROAD = cat != "Valid Official Image"
REFINED = BROAD & (cat != "Non-Official Image")
STRICT = cat.isin(NE | {"Outdated Tag"})
for name, m in [("Broad", BROAD), ("Refined", REFINED), ("Strict", STRICT)]:
    r = m.groupby(ins["Popularity"]).mean().mul(100).round(1).to_dict()
    print(f"{name:8s} {r}")

# ---- Cutoff placement of Outdated Tags (documented knowledge cutoffs, ref. [14]) ----
CUTOFF = {"ChatGPT": "2026-02-16", "Claude": "2026-01-31", "Gemini": "2026-03-31", "GPT-OSS-120B": "2024-06-01"}
UPPER = {"DeepSeek": "2026-04-24"}  # no documented cutoff; release date used as upper bound
ins["eol"] = pd.to_datetime(ins["Automated Note"].str.extract(r"eol date (\d{4}-\d{2}-\d{2})")[0])
def place(r):
    if r["Automated Category"] != "Outdated Tag": return None
    if pd.isna(r.eol): return "undetermined"
    if r.LLM in CUTOFF: return "before" if r.eol <= pd.Timestamp(CUTOFF[r.LLM]) else "after"
    if r.LLM in UPPER and r.eol > pd.Timestamp(UPPER[r.LLM]): return "after"
    return "undetermined"
ins["placement"] = ins.apply(place, axis=1)
print("\nOutdated Tags vs. knowledge cutoff:", ins["placement"].value_counts().to_dict())

# ---- Fisher's exact tests for the Strict reversal ----
def fisher(mask, label):
    g = mask.groupby(ins["Popularity"]).agg(["sum", "size"])
    a, n1 = int(g.loc["Mainstream", "sum"]), int(g.loc["Mainstream", "size"])
    b, n2 = int(g.loc["Niche", "sum"]), int(g.loc["Niche", "size"])
    p = fisher_exact([[a, n1 - a], [b, n2 - b]])[1]
    print(f"{label}: Mainstream {a}/{n1} = {100*a/n1:.1f}%  Niche {b}/{n2} = {100*b/n2:.1f}%  Fisher p = {p:.3f}")
print()
fisher(STRICT, "Strict (current EOL)")
fisher(cat.isin(NE) | (ins["placement"] == "before"), "Strict (EOL at model cutoff)")
