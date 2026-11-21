"""Redraw of Fig. 1 (workflow) with corrected labels. Coordinates are in a 2000 x 780 canvas, y downward."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle
from matplotlib import font_manager

plt.rcParams["font.family"] = "Liberation Serif"
plt.rcParams["pdf.fonttype"] = 42

W, H = 2000, 780
fig = plt.figure(figsize=(13.0, 13.0 * H / W))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")

def box(x, y, w, h, fc, ec, lw=1.6, r=14, ls="-", z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))

def text(x, y, s, size=13, weight="bold", z=5, **kw):
    ax.text(x, y, s, ha="center", va="center", fontsize=size, fontweight=weight, zorder=z,
            linespacing=1.15, **kw)

def arrow(x0, y0, x1, y1, ls="-", z=6):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=z,
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#222", ls=ls,
                                shrinkA=0, shrinkB=0, mutation_scale=13))

def line(xs, ys, ls="-"):
    ax.plot(xs, ys, color="#222", lw=1.5, ls=ls, zorder=6, solid_capstyle="butt")

TOP, BOT, HEAD = 6, 700, 88
cols = [  # x, w, header colour, body colour, edge, title
    (6, 360, "#b3dcef", "#e9f2fb", "#7fb3d5", "SCENARIO\nDERIVATION"),
    (432, 352, "#f4c194", "#fdf0d0", "#e0a64a", "PROMPTING &\nCOLLECTION"),
    (838, 346, "#a9d18e", "#e3f1dc", "#82b366", "AUTOMATED\nVALIDATION"),
    (1240, 352, "#b3dcef", "#dbe9f7", "#4a86c5", "PRIORITY\nCLASSIFICATION"),
    (1646, 348, "#f4c194", "#fdf0d0", "#e0a64a", "EVALUATION &\nFEEDBACK"),
]
for i, (x, w, hc, bc, ec, t) in enumerate(cols):
    bot = BOT - 130 if i == 0 else BOT
    box(x, TOP, w, bot - TOP, bc, ec, lw=1.8, r=18, z=1)
    box(x, TOP, w, HEAD, hc, ec, lw=1.8, r=18, z=1.5)
    text(x + w / 2, TOP + HEAD / 2, t, size=15)

# --- column 1
c1x, c1w = 6, 360; cx1 = c1x + c1w / 2
ax.add_patch(Rectangle((cx1 - 160, 128), 320, 190, fc="#e9f2fb", ec="#4a7fb5", lw=1.8, zorder=2))
ax.add_patch(Ellipse((cx1, 128), 320, 30, fc="#e9f2fb", ec="#4a7fb5", lw=1.8, zorder=3))
ax.add_patch(Ellipse((cx1, 318), 320, 30, fc="#e9f2fb", ec="none", zorder=2.5))
ax.add_patch(matplotlib.patches.Arc((cx1, 318), 320, 30, theta1=180, theta2=360, ec="#4a7fb5", lw=1.8, zorder=3))
text(cx1, 228, "Henkel et al.\nDataset\n(178k+ Dockerfiles)", size=15)
box(cx1 - 160, 372, 320, 180, "#e9f2fb", "#4a7fb5", lw=1.8)
text(cx1, 462, "Data Retrieval\n(77 Scenarios\nDerived)", size=15)
arrow(cx1, 334, cx1, 370)

# legend
box(6, 600, 360, 120, "#c9d3dc", "#8a99a6", lw=1.2, r=6)
ax.text(24, 626, "Legend", fontsize=12, fontweight="bold", va="center", zorder=5)
line([24, 350], [642, 642])
line([24, 74], [668, 668]); ax.text(84, 668, "standard process flow", fontsize=11.5, va="center", zorder=5)
line([24, 74], [700, 700], ls="--"); ax.text(84, 700, "repair re-prompting loop", fontsize=11.5, va="center", zorder=5)

# --- column 2
x2, w2 = 432 + 26, 300; cx2 = x2 + w2 / 2
ax.add_patch(matplotlib.patches.Polygon([(x2, 110), (x2 + w2 - 22, 110), (x2 + w2, 132), (x2 + w2, 210), (x2, 210)],
                                        closed=True, fc="#fff8e1", ec="#e0a64a", lw=1.6, zorder=2))
text(cx2 - 8, 160, "Fixed Prompt\nTemplate", size=14)
b2 = [(250, 112, "Phase 1: Manual\nWeb Batch\n(22 Scenarios)"),
      (404, 112, "Phase 2: Automated\nAPI Batch\n(55 Scenarios)"),
      (558, 118, "Regex Extraction\nPipeline\n(Image & Tag Split)")]
for y, h, t in b2:
    box(x2, y, w2, h, "#fff8e1", "#e0a64a")
    text(cx2, y + h / 2, t, size=14)
arrow(cx2, 212, cx2, 248); arrow(cx2, 364, cx2, 402); arrow(cx2, 518, cx2, 556)
# data retrieval -> phases
line([cx1 + 160, 400], [462, 462]); line([400, 400], [306, 462]); arrow(400, 306, x2 - 2, 306)

# --- column 3
x3, w3 = 838 + 24, 298; cx3 = x3 + w3 / 2
box(838 + 12, 112, 322, 576, "none", "#82b366", lw=2.2, ls=(0, (6, 4)), r=14)
box(x3, 188, w3, 170, "#d5e8d4", "#82b366", r=24)
text(cx3, 273, "Docker Hub API\n(Existence &\nNamespace Check)", size=15)
box(x3, 436, w3, 170, "#d5e8d4", "#82b366", r=24)
text(cx3, 521, "endoflife.date API\n(Lifecycle Status\nCheck)", size=15)
line([x2 + w2, 812], [617, 617]); line([812, 812], [273, 617])
arrow(812, 273, x3 - 2, 273); arrow(812, 521, x3 - 2, 521)

# --- column 4
x4, w4 = 1240 + 30, 292; cx4 = x4 + w4 / 2
box(1240 + 14, 112, 324, 576, "none", "#4a86c5", lw=2.2, ls=(0, (6, 4)), r=14)
text(cx4, 140, "Rules in Priority Order", size=13)
rules = ["Non-Existent Image", "Non-Existent Tag", "Non-Official Image",
         "Risky Latest Tag", "Outdated Tag (EOL)", "Valid Official Image"]
for i, t in enumerate(rules):
    y = 168 + i * 86
    box(x4, y, w4, 64, "#dae8fc", "#6c8ebf", r=8)
    text(cx4, y + 32, f"{i+1}. {t}", size=13)
arrow(1184, 400, 1238, 400)

# --- column 5
x5, w5 = 1646 + 26, 296; cx5 = x5 + w5 / 2
evals = ["Overall / Per-LLM", "Mainstream vs. Niche", "Batch Comparison",
         "Linter Baseline &\nRisk Scan", "Robustness Checks", "Repair Study"]
for i, t in enumerate(evals):
    y = 112 + i * 96
    box(x5, y, w5, 74, "#fff8e1", "#e0a64a", r=8)
    text(cx5, y + 37, t, size=14)
    if i < 5:
        arrow(cx5, y + 74, cx5, y + 94)
arrow(1592, 400, 1644, 400)

# --- dashed repair loop: Repair Study -> back to the prompt template
ry = 112 + 5 * 96 + 74
line([cx5, cx5], [ry, 752], ls="--"); line([396, cx5], [752, 752], ls="--")
line([396, 396], [160, 752], ls="--"); arrow(396, 160, x2 - 2, 160, ls="--")

fig.savefig("fig1_workflow_v2.pdf"); fig.savefig("fig1_workflow_v2.png", dpi=250)
