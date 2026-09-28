"""Reproducible illustration of the exact envelope and its separate phase.

The curves are floating-point samples of the displayed formulas, not
numerical certification of the asymptotic theorem.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    folder = Path(__file__).resolve().parent
    lam = math.log(3) / math.log(2)
    a = 2 - lam
    z = 10000.0
    t = np.linspace(8000, 12000, 3001)
    envelope = np.exp(-a*a*(t-z)**2/(4*t)) / np.sqrt(np.pi*t)
    phase = np.linspace(0, 1, 1001)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4), gridspec_kw={"width_ratios": [1.65, 1]})
    fig.subplots_adjust(bottom=.31, top=.84, wspace=.3)
    axes[0].plot(t, envelope, color="#174d75", lw=2)
    axes[0].fill_between(t, envelope, color="#174d75", alpha=.12)
    radius = math.sqrt(z)*math.log(z)
    for boundary in (z-radius, z+radius):
        axes[0].axvline(boundary, color="#925300", ls="--", lw=1)
    axes[0].set(title=r"Smooth envelope, $z=10{,}000$", xlabel=r"Continuous time coordinate $t$", ylabel=r"$g_z(t)$")
    axes[0].text(.03, .91, r"$\int_0^\infty g_z(t)\,dt=2/a$", transform=axes[0].transAxes)
    axes[0].text(.03, .79, r"$a=2-\log_2 3$", transform=axes[0].transAxes)
    axes[1].plot(phase, 2**(-phase), color="#865600", lw=2)
    axes[1].scatter([0], [1], color="#865600", zorder=4)
    axes[1].scatter([1], [.5], facecolors="white", edgecolors="#865600", zorder=4)
    axes[1].plot([1,1],[.5,1],ls=":",color="#865600")
    axes[1].scatter([1],[1],color="#865600",zorder=4)
    axes[1].set(title="Periodic phase factor", xlabel=r"$\theta=\{r\lambda+u\}$", ylabel=r"$f(\theta)=2^{-\theta}$", ylim=(.45,1.07), xlim=(-.02,1.04))
    axes[1].text(.08,.12,r"$\int_0^1 f(\theta)\,d\theta=1/(2\log 2)$",transform=axes[1].transAxes,fontsize=10)
    for ax in axes:
        ax.grid(alpha=.16)
    fig.suptitle("Why the uniform fibre kernel has constant 1 / log(4/3)", fontsize=15)
    fig.text(.08,.19,r"Exact mass $2/a$  ×  rotation average $1/(2\log 2)$  =  $1/\log(4/3)$",fontsize=13)
    fig.text(.08,.105,"Left dashed lines: the retained integer-time window, shown with L=z.\nRight: the periodic jump is retained in the variation. Curve samples illustrate\nthe formulas; the proof uses exact integration and a uniform Abel discrepancy bound.",fontsize=10)
    fig.savefig(folder/"kernel_mechanism.png",dpi=160)
    plt.close(fig)
    print(folder/"kernel_mechanism.png")


if __name__ == "__main__":
    main()
