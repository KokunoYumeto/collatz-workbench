from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch,FancyBboxPatch
out=Path(__file__).resolve().parent
fig,ax=plt.subplots(figsize=(12,5.7))
ax.set(xlim=(0,12),ylim=(0,5.7));ax.axis("off")
ax.text(.3,5.3,"Two clocks, one actual Collatz orbit",fontsize=19,weight="bold")
ax.text(.3,4.88,"Case B < Y: the first hit of B cannot precede the first hit of Y.",fontsize=12)
for x,text,color in [(1.0,"odd start\nn","#174667"),(6,"first odd landing\nz ≤ Y","#175D4A"),(10.7,"first odd hit\n≤ B","#58316F")]:
    ax.add_patch(FancyBboxPatch((x-.85,2.6),1.7,.9,boxstyle="round,pad=.12",fc=color,ec="none"))
    ax.text(x,3.05,text,ha="center",va="center",color="white",fontsize=13)
for a,b in [(1.98,5.0),(6.98,9.72)]:ax.add_patch(FancyArrowPatch((a,3.05),(b,3.05),arrowstyle="-|>",mutation_scale=18,lw=2,color="#34465a"))
ax.text(3.5,3.78,"High prefix: s returns",ha="center",fontsize=12,weight="bold")
ax.text(3.5,2.15,"s = log(n)/d + O(√(log(n) loglog(n)))\nordinary height ≤ 2n^(1+η)",ha="center",fontsize=11,linespacing=1.6)
ax.text(8.45,3.78,"Remaining: r = σ − s",ha="center",fontsize=12,weight="bold")
ax.text(8.5,2.15,"r ≤ K(n) − s = O((log n)^(4/5))\nordinary height ≤ 2^(r+1) Y",ha="center",fontsize=11,linespacing=1.6)
ax.text(.4,1.24,"Exact example: 27 reaches shortcut value 10 in 65 steps; one halving gives 5.",fontsize=11)
ax.text(.4,.84,"Y = 16, B = 2: s = 40 odd returns to 5; σ = 41 returns to 1; r = 1.",fontsize=11)
ax.text(.4,.37,"d = log(4/3). Schematic above, computed example below. Proof: ND116 in audit.tex.\nHigh prefix: Shaik; total timed count: Allikvere–Tao reconstruction. No resampling at z.",fontsize=10,color="#39485a")
fig.subplots_adjust(left=.01,right=.99,bottom=.01,top=.99)
fig.savefig(out/"shaik_allikvere_splice.png",dpi=165)

