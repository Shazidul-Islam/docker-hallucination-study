"""Re-draws Fig. 1 (workflow), Fig. 2 (per-LLM breakdown) and Fig. 3 (Mainstream vs. Niche)
into figures/. Run from the repository root:  python analysis/make_figures.py
"""
import runpy, os, sys
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(here, "..", "figures"))
runpy.run_path(os.path.join(here, "_fig1_workflow.py"))
sys.argv = ["x", "../data/combined/combined_full_results_rechecked.csv"]
runpy.run_path(os.path.join(here, "_fig2_fig3.py"))
for a, b in [("fig1_workflow_v2.pdf", "fig1_workflow.pdf"), ("fig2_perllm_print.pdf", "fig2_per_llm.pdf"),
             ("fig3_mainniche_print.pdf", "fig3_mainstream_niche.pdf")]:
    os.replace(a, b)
for f in os.listdir("."):
    if f.endswith(".png"): os.remove(f)
print("Figures written to figures/")
