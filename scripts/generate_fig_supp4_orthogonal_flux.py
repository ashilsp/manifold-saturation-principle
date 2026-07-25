"""
scripts/generate_fig_supp4_orthogonal_flux.py

Generates Supplementary Figure S4:
Orthogonal Flux Mechanics (kappa_flux) and Boundary Jump Integration (Figure 15 / Movie S15).
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.supplementary_metrics import (
    calculate_kappa_flux,
    calculate_boundary_jump_integral
)


def plot_supplementary_orthogonal_flux():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Convergence of Boundary Jump Integral as delta -> 0
    delta_arr = np.logspace(-4, 0, 200)  # Boundary thickness delta from 10^-4 to 10^0
    s_m_targets = [1.2, 1.5, 2.0, 3.0]
    colors = ['#00838f', '#1565c0', '#e65100', '#d32f2f']

    for sm, color in zip(s_m_targets, colors):
        jump_vals = [calculate_boundary_jump_integral(sm, d) / 1.0e39 for d in delta_arr]
        ax1.semilogx(delta_arr, jump_vals, label=f'$S_M = {sm:.1f}$', color=color, linewidth=2.0)

    ax1.set_xlabel('Boundary Layer Thickness $\\delta$', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Boundary Jump Integral $\\kappa_{\\text{flux}}$ [$10^{39}$ W]', fontsize=11, fontweight='bold')
    ax1.set_title('A: Boundary Jump Integral Limit ($\\delta \\to 0$)', fontsize=11, fontweight='bold')
    ax1.grid(True, which='both', linestyle=':', alpha=0.5)
    ax1.legend(loc='upper right', fontsize=8.5)

    # Panel B: Orthogonal Flux Profile kappa_flux vs S_M
    s_m_sweep = np.linspace(0.1, 3.0, 400)
    kappa_sweep = [calculate_kappa_flux(sm) / 1.0e39 for sm in s_m_sweep]

    ax2.plot(s_m_sweep, kappa_sweep, color='#d32f2f', linewidth=2.5, label='Orthogonal Flux $\\kappa_{\\text{flux}}(S_M)$')
    ax2.axvline(1.0, color='black', linestyle=':', label='Phase Transition Boundary ($S_M = 1.0$)')
    
    # Shade Confinement vs Drainage Regimes
    ax2.axvspan(0.1, 1.0, color='gray', alpha=0.15, label='3D Confinement ($\kappa_{\\text{flux}} = 0$)')
    ax2.axvspan(1.0, 3.0, color='cyan', alpha=0.08, label='Orthogonal Drainage Channel')

    ax2.set_xlabel('Metric Saturation Scalar $S_M$', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Orthogonal Flux $\\kappa_{\\text{flux}}$ [$10^{39}$ W]', fontsize=11, fontweight='bold')
    ax2.set_title('B: Orthogonal Flux Drainage & Singularity Avoidance', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='center right', fontsize=8.5)

    # Annotation Box
    ax2.text(0.15, 0.65,
             "Flux Conservation Laws:\n"
             "• $\\nabla_{\\bar{\\mu}} T^{\\bar{\\mu}\\bar{\\nu}}_{(4+1)} = 0$\n"
             "• $S_M < 1 \\implies \\kappa_{\\text{flux}} = 0$ (Bound 3D state)\n"
             "• $S_M \\ge 1 \\implies \\kappa_{\\text{flux}} = \\kappa_{\\text{crit}}(1 - 1/S_M^2)$\n"
             "• Prevents $r \\to 0$ infinite density singularities\n"
             "• Movie Anchor: Movie S15",
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#e0f7fa', edgecolor='#00838f', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure S4: Mathematical Mechanics of Orthogonal Flux Drainage ($\kappa_{\\text{flux}}$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/FigureS4_Orthogonal_Flux_Mechanics.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_supplementary_orthogonal_flux()
