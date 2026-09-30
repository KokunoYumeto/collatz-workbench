"""Reproducible illustration of the exact ND115 low-branch calculation."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from check_shaik_low_schedule import duration_set,low_run,Q
HERE=Path(__file__).resolve().parent
assert duration_set(5,Q(3,5),6)=={1,3,4,5}
ok,d,path,rec,why=low_run(37,5,Q(3,5),6)
assert path==[37,56,28,14,7]
fig,axes=plt.subplots(1,2,figsize=(11,4.8),gridspec_kw={"width_ratios":[1.5,1]})
ax=axes[0]
ax.plot(range(5),path,"o-",label="Interior first passage: x = 37",color="#196f82")
for i,x in enumerate(path):ax.annotate(str(x),(i,x),xytext=(5,7),textcoords="offset points")
ax.plot([0,1],[64,32],"s--",label="Dyadic completion: x = 64",color="#9a4b26")
ax.axhline(8,color="#196f82",alpha=.55,linestyle=":",label="Interior target: 2^3 = 8")
ax.axhline(32,color="#9a4b26",alpha=.55,linestyle=":",label="Terminal ceiling: 2^5 = 32")
ax.set(xlabel="Shortcut steps",ylabel="Actual integer orbit value",ylim=(0,75),xticks=range(5))
ax.grid(alpha=.2);ax.legend(fontsize=8,loc="upper right")
ax=axes[1]
for t in range(1,6):
    ax.scatter(t,0,s=140,facecolors="#196f82" if t in {1,3,4,5} else "white",
               edgecolors="#196f82")
ax.annotate("Missing scalar duration",(2,0),xytext=(2,0.45),ha="center",
            arrowprops={"arrowstyle":"->"})
ax.text(3,-.42,"D(6) = {1, 3, 4, 5}\nNot the whole interval [1, 5]",ha="center",fontsize=11)
ax.set(xlabel="Scalar duration",xlim=(.5,5.5),ylim=(-.8,.85),xticks=range(1,6),yticks=[])
ax.set_title("Scalar possibilities, not orbit attainability",fontsize=10)
fig.suptitle("The dyadic branch must be kept: L = 5, K₀ = 4, r = 3/5, p = 6",fontsize=13)
fig.text(.5,.015,"Shaik's timeout run (revision ef341084); exact refinement: audit.tex, prop:shaik-low-schedule.\nThe two plotted paths are actual orbits. The scalar set is an outer bound, not a realization theorem.",
         ha="center",fontsize=9)
fig.tight_layout(rect=(0,.11,1,.94))
fig.savefig(HERE/"shaik_low_schedule.png",dpi=160)
