"""
scripts/generate_fig_supp2_israel_junction.py

Generates Supplementary Figure S2:
Mathematical Mechanics of the R_d Phase Transition & Israel Junction Conditions (Figure 14 / Movie S14).
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.supplementary_metrics import (
    calculate_extrinsic_curvature_jump,
    calculate_israel_surface_stress,
    calculate_stress_energy_decoupling,
    SOLAR_MASS
)


def plot_supplementary_israel_junction():
    # Sweep metric saturation parameter S_M from 0.1 to 3.0
    s_m_arr = np.linspace(0.1, 3.0, 400)
    m_test = 10.0 * SOLAR_MASS

    # Calculate Israel Junction terms across S_M
    surface_stress_list = [calculate_israel_surface_stress(sm, m_test) for sm in s_m_arr]
    curvature_jump_list = [calculate_extrinsic_curvature_jump(m_test, sm)["extrinsic_curvature_jump"] for sm in s_m_arr]
    
    # Calculate Decoupling Components
    decoupling_res = [calculate_stress_energy_decoupling(sm) for sm in s_m_arr]
    kappa_flux_list = [d["orthogonal_flux_kappa"] / 1.0e39 for d in decoupling_res]
    s_weight_list = [d["surface_stress_weight"] for d in decoupling_res]

    # Setup Figure with 2 Panels
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Extrinsic Curvature Jump [K_ij] & Surface Stress S_ij
    color1 = '#00838f'
    ax1.plot(s_m_arr, surface_stress_list, color=color1, linewidth=2.5, label='Surface Stress $\\mathcal{S}_{ij}$')
    ax1.set_xlabel('Metric Saturation Scalar $S_M$', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Surface Stress $\\mathcal{S}_{ij}$ [Normalized]', fontsize=11, fontweight='bold', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax1_twin = ax1.twinx()
    color2 = '#d32f2f'
    ax1_twin.plot(s_m_arr, curvature_jump_list, color=color2, linestyle='--', linewidth=2.0, label='Extrinsic Curvature Jump $[K_{ij}]$')
    ax1_twin.set_ylabel('Curvature Discontinuity $[K_{ij}]$ [m$^{-1}$]', fontsize=11, fontweight='bold', color=color2)
    ax1_twin.tick_params(axis='y', labelcolor=color2)

    ax1.axvline(1.0, color='black', linestyle=':', label='Critical Threshold ($S_M = 1.0$)')
    ax1.set_title('A: Israel Junction Conditions & Curvature Jump $[K_{ij}]$', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.5)

    # Panel B: Stress-Energy Tensor Decoupling (S_ij vs. Orthogonal Flux K_flux)
    ax2.plot(s_m_arr, kappa_flux_list, color='#e65100', linewidth=2.5, label='Orthogonal Metric Flux $\\kappa_{\\text{flux}}$ [$10^{39}$ W]')
    ax2.plot(s_m_arr, s_weight_list, color='#1565c0', linestyle='--', linewidth=2.0, label='3D Surface Weight $\\mathcal{S}_{ij} \\delta(\\Sigma_d)$')
    ax2.axvline(1.0, color='black', linestyle=':', label='Critical Threshold ($S_M = 1.0$)')

    ax2.set_xlabel('Metric Saturation Scalar $S_M$', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Tensor Decoupling Components', fontsize=11, fontweight='bold')
    ax2.set_title('B: Stress-Energy Decoupling Across $\\Sigma_d$', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='center right', fontsize=8.5)

    # Annotation Box
    ax2.text(1.2, 0.2,
             "Israel Junction Mechanics:\n"
             "• $T_{\\mu\\nu}^{(3D)} = \\mathcal{S}_{\\mu\\nu} \\delta(\\Sigma_d) + n_\\mu n_\\nu \\kappa_{\\text{flux}}$\n"
             "• $[K_{ij}] \\neq 0$ across null boundary $\\Sigma_d$\n"
             "• Regularized $r=R_d$ laminar shell\n"
             "• Movie Anchor: Movie S14",
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#e0f7fa', edgecolor='#00838f', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure S2: Mathematical Mechanics of the $R_d$ Phase Transition ($S_M = 1$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/FigureS2_Israel_Junction_Mechanics.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_supplementary_israel_junction()
