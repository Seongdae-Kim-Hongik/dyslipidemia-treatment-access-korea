# -*- coding: utf-8 -*-
# figs_lipt.py — 31호 LIPT 그림(figs_cogn.py 복제, 2026-11-12).
#  규칙: 컬러, 패널 문자 모두 같은 크기·11/10 기준 2배(48pt)·굵게, 방위표 3배, 그림 안 설명문 금지, 결합은 시군구 코드로만.
#  패널 문자 = 대문자 A·B(저자 11/10 규칙). 세종 = 미관측(회색 빗금 없이 연회색).
#  Fig 1 (A) 전 기간 잔차 공간 RR (B) 치료 SIR × 의심 SIR 사분면 · Fig 2 강건 3개 변수의 모형별 RR · 보충 Fig S1 (A) EHSA (B) 두 창 핫·콜드스팟
import os, unicodedata, numpy as np, pandas as pd, geopandas as gpd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from numbers_lipt import load, ROB, SHP, EDU, IMS, MPA
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(os.path.dirname(HERE)); RS = os.path.join(B, "results_std3")
FIG = os.path.join(HERE, "figs"); OUTF = os.path.join(os.path.dirname(HERE), "out", "Figures"); os.makedirs(FIG, exist_ok=True); os.makedirs(OUTF, exist_ok=True)
MM = 1 / 25.4; W = 174 * MM; DPI = 600; LW = 0.3; PANEL_LABEL_PT = 48
plt.rcParams.update({"font.family": "Arial", "font.size": 8, "legend.fontsize": 7.5, "legend.title_fontsize": 8, "axes.linewidth": 0.5, "pdf.fonttype": 42})
NFC = lambda s: unicodedata.normalize("NFC", str(s)).strip()
N = load()
G = gpd.read_file(SHP); G["cd"] = G.sigungu_cd.astype(str); G["sido"] = G.cd.str[:2]; SIDO = G.dissolve("sido")
XL = (G.total_bounds[0], G.total_bounds[2]); YL = (G.total_bounds[1], G.total_bounds[3])
rd = lambda f: pd.read_csv(os.path.join(RS, f), encoding="utf-8-sig", dtype={"sigungu_cd": str})
def letter(fig, ch, x, y):   # 그림 좌표 하나의 상수 크기
    fig.text(x, y, ch, fontsize=PANEL_LABEL_PT, fontweight="bold", va="top", ha="left")
def mapax(ax):
    SIDO.boundary.plot(ax=ax, color="#404040", linewidth=0.45); ax.set_xlim(*XL); ax.set_ylim(*YL); ax.set_axis_off(); ax.set_aspect("equal")
    x0, x1 = XL; y0, y1 = YL; W_ = x1 - x0; H_ = y1 - y0
    bx, by = x0 + 0.60 * W_, y0 + 0.03 * H_
    ax.plot([bx, bx + 100000], [by, by], color="black", lw=1.2, solid_capstyle="butt"); ax.text(bx + 50000, by + 0.012 * H_, "100 km", ha="center", va="bottom", fontsize=7)
    ax.annotate("N", xy=(x0 + 0.93 * W_, y0 + 0.99 * H_), xytext=(x0 + 0.93 * W_, y0 + 0.80 * H_), ha="center", va="center", fontsize=24, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>,head_length=0.9,head_width=0.45", color="black", lw=2.4))
def save(fig, k):
    p = os.path.join(FIG, f"Fig{k}.png"); fig.savefig(p, dpi=DPI, facecolor="white"); plt.close(fig)
    im = Image.open(p).convert("RGB"); im.save(p, dpi=(DPI, DPI))
    if not str(k).startswith("S"): im.save(os.path.join(OUTF, f"Figure_{k}.tif"), dpi=(DPI, DPI), compression="tiff_lzw")
    return im.size

S6 = rd("S6_spatial_RR.csv"); S6 = S6[S6.observed]; assert len(S6) == 228
UNOBS = "#e6e6e6"
CD = dict(zip(S6.fbd_region.map(NFC), S6.sigungu_cd))   # 같은 파이프라인 출력의 코드표로만 연결
GAP = pd.read_csv(os.path.join(RS, "S50_lipt_suspect_gap.csv"), encoding="utf-8-sig"); GAP["cd"] = GAP.fbd_region.map(NFC).map(CD); assert GAP.cd.notna().all() and len(GAP) == 228
QL = ["treated high / suspected low", "treated low / suspected high", "both high", "both low"]
assert GAP.quadrant.value_counts().to_dict() == N["gap"]["all_2011-24"]["quadrants"]

# Fig 1
BR = [0, 0.67, 0.8, 0.9, 1, 1.1, 1.25, 1.5, 99]; LB = ["<0.67", "0.67-0.79", "0.80-0.89", "0.90-0.99", "1.00-1.09", "1.10-1.24", "1.25-1.49", "≥1.50"]
PAL = ["#2166AC", "#4393C3", "#92C5DE", "#D1E5F0", "#FDDBC7", "#F4A582", "#D6604D", "#B2182B"]
assert BR[0] < N["rr_min"] < BR[1] and BR[-2] < N["rr_max"] < BR[-2] + 0.1
fig = plt.figure(figsize=(W, 4.6)); a0 = fig.add_axes([0.00, 0.27, 0.49, 0.62]); a1 = fig.add_axes([0.51, 0.27, 0.49, 0.62])
d = S6.set_index("sigungu_cd"); gg = G.copy(); gg["v"] = gg.cd.map(d.RR); gg["c"] = gg.cd.map(d["class"]); assert int(gg.v.isna().sum()) == 1
gg[gg.v.isna()].plot(ax=a0, color=UNOBS, edgecolor="#a0a0a0", linewidth=LW); gg = gg[gg.v.notna()]
gg.plot(ax=a0, column="v", cmap=ListedColormap(PAL), norm=BoundaryNorm(BR, len(PAL)), edgecolor="#a0a0a0", linewidth=LW); mapax(a0)
gg[gg.c == "coldspot"].boundary.plot(ax=a0, color="#2171B5", linewidth=0.6, linestyle=(0, (2.0, 1.2))); gg[gg.c == "hotspot"].boundary.plot(ax=a0, color="black", linewidth=0.6)
h = [Patch(facecolor=c, edgecolor="#777777", linewidth=LW, label=l) for c, l in zip(PAL, LB)] + [Patch(facecolor="none", edgecolor="black", linewidth=0.8, label="Hot spot"), Patch(facecolor="none", edgecolor="#2171B5", linewidth=0.8, linestyle="--", label="Cold spot"), Patch(facecolor=UNOBS, edgecolor="#777777", linewidth=LW, label="No data")]
a0.legend(handles=h, title="Residual spatial RR", loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False, columnspacing=0.8, handlelength=1.3)
QP = {"treated high / suspected low": "#B2182B", "treated low / suspected high": "#2166AC", "both high": "#F4A582", "both low": "#D1E5F0"}
QT = {"treated high / suspected low": "Treated ratio >1, suspected ratio ≤1", "treated low / suspected high": "Treated ratio ≤1, suspected ratio >1", "both high": "Both >1", "both low": "Both ≤1"}
g2 = G.copy(); g2["q"] = g2.cd.map(GAP.set_index("cd").quadrant); assert int(g2.q.isna().sum()) == 1
g2[g2.q.isna()].plot(ax=a1, color=UNOBS, edgecolor="#a0a0a0", linewidth=LW); g2 = g2[g2.q.notna()]
g2.plot(ax=a1, color=[QP[q] for q in g2.q], edgecolor="#a0a0a0", linewidth=LW); mapax(a1)
qc = g2.q.value_counts()
a1.legend(handles=[Patch(facecolor=QP[q], edgecolor="#777777", linewidth=LW, label=f"{QT[q]} ({qc[q]})") for q in QL], title="Districts, 2011-2024", loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=1, frameon=False, handlelength=1.3)
letter(fig, "A", 0.005, 0.995); letter(fig, "B", 0.515, 0.995)
s1 = save(fig, 1)

# Fig 2 — 강건 3개 변수의 모형별 RR
LAB = {EDU: "Tertiary education", IMS: "Internal-medicine specialists\nper population", MPA: "Moderate-or-vigorous\nphysical activity"}
ORD = [EDU, IMS, MPA]; assert set(ORD) == set(ROB)
MOD = [("Principal model", lambda v: (N["main"][v]["IRR"], N["main"][v]["lo"], N["main"][v]["hi"]), "#000000", "o"),
       ("Knorr-Held type II (best fitting)", lambda v: N["s43"][("KH_typeII", v)][:3], "#2166AC", "s"),
       ("Knorr-Held type IV", lambda v: N["s43"][("KH_typeIV", v)][:3], "#B2182B", "D"),
       ("2011-2017 only", lambda v: N["win_irr"][(v, "W1_2011-17")][:3], "#1b7837", "v"),
       ("2018-2024 only", lambda v: N["win_irr"][(v, "W2_2018-24")][:3], "#E08214", "P"),
       ("Expected numbers from residents", lambda v: N["epop"][v][:3], "#7f7f7f", "^")]
lo_all = min(f(v)[1] for v in ORD for _, f, _, _ in MOD); hi_all = max(f(v)[2] for v in ORD for _, f, _, _ in MOD)
fig, ax = plt.subplots(figsize=(W, 3.2)); fig.subplots_adjust(left=0.26, right=0.98, top=0.97, bottom=0.32)
off = np.linspace(-0.32, 0.32, len(MOD))
for i, v in enumerate(ORD):
    for (lab, f, col, mk), o in zip(MOD, off):
        e, lo, hi = f(v); ax.plot([lo, hi], [i + o] * 2, color=col, lw=0.8); ax.plot(e, i + o, marker=mk, color=col, ms=3.4, mew=0, ls="none")
ax.axvline(1, color="#404040", lw=0.5, ls=":"); ax.set_yticks(range(len(ORD))); ax.set_yticklabels([LAB[v] for v in ORD]); ax.invert_yaxis()
xt = [0.94, 0.97, 1.00, 1.03, 1.06, 1.09, 1.12, 1.15]; assert xt[0] <= lo_all and hi_all <= xt[-1], (lo_all, hi_all)
ax.set_xlim(xt[0], xt[-1]); ax.set_xticks(xt); ax.set_xticklabels([f"{x:.2f}" for x in xt]); ax.minorticks_off()
ax.set_xlabel("Rate ratio per 1 SD (95% credible interval)"); ax.spines[["top", "right"]].set_visible(False)
ax.legend(handles=[Line2D([0], [0], color=c, marker=m, lw=0.8, ms=3.4, mew=0, label=l) for l, _, c, m in MOD], loc="upper center", bbox_to_anchor=(0.36, -0.18), ncol=3, frameon=False)
s2 = save(fig, 2)

# 보충 Fig S1
EH = rd("S11_ehsa.csv")
CATS = [f"{a} {b}" for b in ("hot", "cold") for a in ("New", "Consecutive", "Intensifying", "Persistent", "Diminishing", "Sporadic", "Oscillating", "Historical")] + ["No pattern"]
EPAL = {"New hot": "#fdd0a2", "Consecutive hot": "#fdae6b", "Intensifying hot": "#a50f15", "Persistent hot": "#de2d26", "Diminishing hot": "#fc9272", "Sporadic hot": "#fee0d2", "Oscillating hot": "#d6a5c9", "Historical hot": "#bcbddc",
        "New cold": "#c6dbef", "Consecutive cold": "#9ecae1", "Intensifying cold": "#08519c", "Persistent cold": "#3182bd", "Diminishing cold": "#6baed6", "Sporadic cold": "#deebf7", "Oscillating cold": "#a1d99b", "Historical cold": "#c7e9c0", "No pattern": "#f7f7f7"}
WM = rd("S4b_window_spatialRR.csv"); WM = WM[WM["class"] != "unobserved"]
nh = WM[WM["class"] == "hotspot"].groupby("sigungu_cd").size(); nc = WM[WM["class"] == "coldspot"].groupby("sigungu_cd").size()
assert int((nh == 2).sum()) == N["hot_all_windows"] and int((nc == 2).sum()) == N["cold_all_windows"]
fig = plt.figure(figsize=(W, 5.0)); a0 = fig.add_axes([0.00, 0.30, 0.49, 0.60]); a1 = fig.add_axes([0.51, 0.30, 0.49, 0.60])
gg = G.copy(); gg["c"] = gg.cd.map(EH.set_index("sigungu_cd").EHSA); assert int(gg.c.isna().sum()) == 1
gg[gg.c.isna()].plot(ax=a0, color=UNOBS, edgecolor="#a0a0a0", linewidth=LW); gg = gg[gg.c.notna()].copy()
gg.plot(ax=a0, color=[EPAL[c] for c in gg.c], edgecolor="#a0a0a0", linewidth=LW); mapax(a0)
cnt = EH.EHSA.value_counts(); pres = [c for c in CATS if c in cnt.index]
a0.legend(handles=[Patch(facecolor=EPAL[c], edgecolor="#777777", linewidth=LW, label=f"{c} ({cnt[c]})") for c in pres], title="Category (districts)", loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False, columnspacing=0.8, handlelength=1.2)
hh = gg.cd.map(nh).fillna(0).astype(int); cc = gg.cd.map(nc).fillna(0).astype(int)
gg["k"] = np.where((hh > 0) & (cc > 0), 9, hh - cc)
KP = {-2: "#2166AC", -1: "#92C5DE", 0: "#f7f7f7", 1: "#F4A582", 2: "#B2182B", 9: "#c2a5cf"}
KL = {-2: "Cold spot in both windows", -1: "Cold spot in one", 0: "Neither", 1: "Hot spot in one", 2: "Hot spot in both windows", 9: "Hot or cold by window"}
gg.plot(ax=a1, color=[KP[k] for k in gg.k], edgecolor="#a0a0a0", linewidth=LW); mapax(a1)
kc = gg.k.value_counts()
a1.legend(handles=[Patch(facecolor=KP[k], edgecolor="#777777", linewidth=LW, label=f"{KL[k]} ({kc.get(k, 0)})") for k in (2, 1, 0, -1, -2, 9) if kc.get(k, 0)], title="Windows 2011-2017 and 2018-2024", loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False, columnspacing=0.8, handlelength=1.2)
letter(fig, "A", 0.005, 0.995); letter(fig, "B", 0.515, 0.995)
s3 = save(fig, "S1")
for k, s in zip((1, 2, "S1"), (s1, s2, s3)): print(f"Fig{k}: {s[0]}x{s[1]} px = {s[0]/DPI*25.4:.0f} x {s[1]/DPI*25.4:.0f} mm")
