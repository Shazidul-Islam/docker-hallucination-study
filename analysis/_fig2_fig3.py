"""Fig. 2 and Fig. 3 re-drawn at print size (larger text, no redundant in-plot titles)."""
import sys, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.ticker as mticker
c = pd.read_csv(sys.argv[1]); ins = c[c["Automated Category"] != "OUT OF SCOPE"].copy()
ins["Cat"] = ins["Automated Category"].replace({"NEEDS MANUAL CHECK": "Needs Manual Review", "Nonexistent Tag": "Non-Existent Tag"})
print(len(ins))
plt.rcParams.update({"font.family": "Liberation Serif", "axes.spines.top": False, "axes.spines.right": False,
                     "savefig.dpi": 400, "font.size": 8, "pdf.fonttype": 42})
COL = {"Valid Official Image": "#1a9850", "Outdated Tag": "#fdae61", "Non-Official Image": "#4575b4",
       "Risky Latest Tag": "#f46d43", "Non-Existent Tag": "#d73027", "Non-Existent Image": "#7f0000",
       "Needs Manual Review": "#878787"}
llms = ["ChatGPT", "Claude", "Gemini", "DeepSeek", "GPT-OSS-120B", "Copilot"]
pct = pd.crosstab(ins["LLM"], ins["Cat"], normalize="index").mul(100).reindex(llms)
cols = [k for k in COL if k in pct.columns]
fig, ax = plt.subplots(figsize=(3.3, 2.75))
bottom = pd.Series(0.0, index=llms)
for k in cols:
    ax.bar(range(6), pct[k], bottom=bottom, color=COL[k], edgecolor="black", linewidth=0.4, width=0.7, label=k)
    for i, l in enumerate(llms):
        v = pct.loc[l, k]
        if v >= 8.5:
            ax.text(i, bottom[l] + v / 2, f"{v:.0f}", ha="center", va="center", fontsize=7.5, fontweight="bold",
                    color="black" if k == "Outdated Tag" else "white")
    bottom += pct[k]
ax.set_xticks(range(6)); ax.set_xticklabels(["ChatGPT", "Claude", "Gemini", "DeepSeek", "GPT-OSS", "Copilot"], fontsize=7.2)
ax.set_ylim(0, 100); ax.yaxis.set_major_formatter(mticker.PercentFormatter()); ax.set_ylabel("% of in-scope responses")
fig.subplots_adjust(left=0.15, right=0.99, top=0.98, bottom=0.33)
fig.legend(*ax.get_legend_handles_labels(), loc="lower center", bbox_to_anchor=(0.55, 0.0), ncol=2, frameon=False,
           fontsize=7.5, columnspacing=0.8, handlelength=1.0, handletextpad=0.4, labelspacing=0.25)
fig.savefig("fig2_perllm_print.pdf"); fig.savefig("fig2_perllm_print.png"); plt.close()

E_BROAD = {"Non-Official Image", "Risky Latest Tag", "Outdated Tag", "Non-Existent Tag", "Non-Existent Image", "Needs Manual Review"}
E_REF = E_BROAD - {"Non-Official Image"}; E_STRICT = {"Outdated Tag", "Non-Existent Tag", "Non-Existent Image"}
rates = {p: [100 * g["Cat"].isin(s).mean() for s in (E_BROAD, E_REF, E_STRICT)] for p, g in ins.groupby("Popularity")}
print(rates)
nm, nn = (ins["Popularity"] == "Mainstream").sum(), (ins["Popularity"] == "Niche").sum()
fig, ax = plt.subplots(figsize=(3.3, 2.1)); w = 0.38
b1 = ax.bar([i - w/2 for i in range(3)], rates["Mainstream"], w, color="#2166ac", edgecolor="black", lw=0.4, label=f"Mainstream (n={nm})")
b2 = ax.bar([i + w/2 for i in range(3)], rates["Niche"], w, color="#b2182b", edgecolor="black", lw=0.4, label=f"Niche (n={nn})")
for bs in (b1, b2):
    for b in bs:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1.5, f"{b.get_height():.1f}%", ha="center", fontsize=7.5)
ax.set_xticks(range(3)); ax.set_xticklabels(["Broad", "Refined", "Strict"], fontsize=8.5)
ax.set_ylim(0, 100); ax.set_ylabel("Error rate (%)")
ax.annotate("reversal", xy=(2.05, rates["Mainstream"][2] + 9), xytext=(2.15, 62), fontsize=8, style="italic",
            arrowprops=dict(arrowstyle="->", lw=0.9))
ax.legend(loc="upper right", frameon=False, fontsize=7.5)
fig.subplots_adjust(left=0.14, right=0.99, top=0.97, bottom=0.12)
fig.savefig("fig3_mainniche_print.pdf"); fig.savefig("fig3_mainniche_print.png"); plt.close()
