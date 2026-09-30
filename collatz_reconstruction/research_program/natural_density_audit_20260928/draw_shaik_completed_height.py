"""Reproduce the exact completed-block illustration from checked integer data."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
e=json.loads((HERE/"shaik_completed_height_checks.json").read_text())["example"]
v=list(range(e["h"]+1))
fig,ax=plt.subplots(figsize=(12,7.3))
ax.plot(v,e["forward"],"--",color="#bd6331",label="Forward: floor(3^v (x+1) / 2^v) − 1",linewidth=2)
ax.plot(v,e["backward"],"--",color="#328987",label="Backward: 2^(h−v) y",linewidth=2)
ax.plot(v,e["path"],"o-",color="#25274f",label="Actual shortcut orbit = minimum of both bounds here",linewidth=3)
ax.axhline(e["budget"],color="#8561aa",linestyle=":",label="Shell-only B(10,9) = 15551")
ax.annotate("Exact peak 14336\nboth bounds meet at v = 5",xy=(5,14336),xytext=(6.0,64000),
            arrowprops=dict(arrowstyle="->",color="#25274f"),fontsize=12)
ax.annotate("x = 1887",xy=(0,1887),xytext=(0.5,850),arrowprops=dict(arrowstyle="->"),fontsize=12)
ax.annotate("y = 448 ≤ 2^9",xy=(10,448),xytext=(7,600),arrowprops=dict(arrowstyle="->"),fontsize=12)
ax.set_yscale("log",base=2)
ax.set_xticks(v);ax.set_xlabel("Shortcut time v (h = 10)",fontsize=12)
ax.set_ylabel("Positive integer orbit value (log₂ axis)",fontsize=12)
ax.set_title("A completed Collatz block is bounded from both ends",fontsize=18,pad=18)
ax.grid(alpha=.18);ax.legend(loc="upper right",fontsize=10)
fig.text(.08,.085,"The displayed example is an actual first passage: 1887 → 448 below 2⁹, with five odd inputs.\n"
         "Ordinary time is 10 + 5 = 15; its peak is 28672 = 2 × 14336.",fontsize=11)
fig.text(.08,.025,"Proof: audit.tex, prop:shaik-completed-block-height and cor:shaik-timeout-height-refinement.\n"
         "Application: Idris Ali Shaik's TimeoutRun / TimeoutOrbitCeiling, revision ef341084.",fontsize=10)
fig.subplots_adjust(bottom=.23,top=.89,left=.10,right=.97)
fig.savefig(HERE/"shaik_completed_height.png",dpi=160)
