"""
scripts/generate_fig_supp7_tov_limit_sensitivity.py

Generates Supplementary Figure S7:
Numerical Sensitivity Sweep of Tolman-Oppenheimer-Volkoff Mass Limits Across Equations of State
(Figure 18 / Movie S18).
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.supplementary_metrics import simulate_eos_tov_trajectory


def plot_supplementary_tov_sensitivity():
    # Simulate trajectory data for Soft and Stiff Equations of State
    data_soft = simulate_eos_tov_trajectory("soft")
    data_stiff = simulate_eos_tov_trajectory("stiff")

    # Setup Plot
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

    # 1. Super-Critical Black Hole Conduit Zone (S_M >= 1.0)
    ax.axhspan(2.15, 2.7, color='cyan', alpha=0.12, label='Super-Critical Black Hole Regime ($S_M \\ge 1.0$)')
    ax.axhline(2.15, color='#00838f', linestyle='--', linewidth=1.5)

    # 2. Pre-Critical Metric Bottleneck Interval Zone (0.92 <= S_M <= 0.98)
    ax.axhspan(1.85, 2.15, color='purple', alpha=0.12, label='Pre-Critical Bottleneck ($0.92 \\le S_M \\le 0.98$)')
    ax.axhline(1.85, color='#6a1b9a', linestyle=':', linewidth=1.5)

    # 3. Soft Equation of State Curve (SLy)
    ax.plot(
        data_soft["log_rho_c"], 
        data_soft["mass_msun"], 
        color='#1565c0', 
        linewidth=2.5, 
        label='Soft EoS (SLy) — Direct $R_d$ Materialization'
    )

    # 4. Stiff Equation of State Curve (MS1)
    ax.plot(
        data_stiff["log_rho_c"], 
        data_stiff["mass_msun"], 
        color='#8e24aa', 
        linewidth=2.5, 
        label='Stiff EoS (MS1) — Trapped in Bottleneck Engine'
    )

    # Styling and Labels
    ax.set_xlabel('Central Mass Density [$\\log_{10}(\\rho_c / \\text{g cm}^{-3})$]', fontsize=11, fontweight='bold')
    ax.set_ylabel('Total Core Mass ($M / M_\\odot$)', fontsize=11, fontweight='bold')
    ax.set_title('Figure S7: TOV Mass Limits & Pre-Critical Bottleneck Phase Space ($S_M \\to 1^-$)', fontsize=12, fontweight='bold')

    ax.set_xlim(14.0, 15.8)
    ax.set_ylim(0.5, 2.7)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', fontsize=9)

    # Annotation Box
    ax.text(
        14.85, 0.75,
        "EoS Dynamics & Bottleneck Engines:\n"
        "• Soft EoS (SLy): Rapid density spike $\\rightarrow S_M \\ge 1.0$\n"
        "  Direct $R_d$ boundary opening into stellar-mass black hole\n"
        "• Stiff EoS (MS1): Degeneracy locks core in $0.92 \\le S_M \\le 0.98$\n"
        "  $\\kappa_{\\text{flux}} = 0 \\implies$ Structural shear powers Pulsars & Magnetars\n"
        "• Movie Anchor: Movie S18",
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f3e5f5', edgecolor='#8e24aa', alpha=0.9),
        fontsize=8.5, fontweight='bold'
    )

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/FigureS7_TOV_Limit_Sensitivity.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_supplementary_tov_sensitivity()
