"""Agreement between the automated pipeline and the authors' manual labels on the
110 Phase 1 responses (81.8%, Sec. III-D; Limitation vi). Writes a side-by-side file
so that every disagreement can be audited. Run from the repository root:
    python analysis/pipeline_vs_manual_labels.py
"""
import pandas as pd
rc = pd.read_csv("data/combined/combined_full_results_rechecked.csv")
auto = rc[rc["Batch"].str.startswith("Original")]
manual = pd.read_csv("data/phase1_original/phase1_manual_labels.csv").rename(columns={"Category": "Manual Category", "Note": "Manual Note"})
j = auto.merge(manual[["LLM", "Scenario", "Manual Category", "Manual Note"]], on=["LLM", "Scenario"])
norm = lambda s: s.astype(str).str.strip().str.lower().str.replace("non-existent", "nonexistent")
j["agree"] = norm(j["Automated Category"]) == norm(j["Manual Category"])
print(f"Agreement: {j['agree'].sum()}/{len(j)} = {100 * j['agree'].mean():.1f}%")
print(j.loc[~j["agree"], ["LLM", "Image Name", "Tag", "Automated Category", "Manual Category", "Automated Note"]].to_string(index=False))
j.to_csv("data/phase1_original/phase1_manual_vs_automated.csv", index=False)
