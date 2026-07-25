"""
scripts/generate_fig_supp3_decomposition.py

Generates Supplementary Figure S3:
Geometric Schematization of (4+1)D Stress-Energy Tensor Decomposition
and Boundary Mechanics (Figure 15 / Movie S15).
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.supplementary_metrics import (
    calculate_spatial_stress_integral,
    calculate_4plus1_tensor_decomposition,
    EPSILON_M,
    SOLAR_MASS
)


def plot_supplementary_tensor_decomposition():
    s_m_arr = np.linspace(0.1, 3.0, 400)
    m_test = 10.0 * SOLAR_MASS

    # Tensor decomposition outputs across S_M
    decomp_data = [calculate_4plus1_tensor_decomposition(sm) for sm in s_m_arr]
    j_flux_list = [d["j_flux_magnitude"] / 1.0e39 for d in decomp_data]
    s_tangent_list = [d["s_tangent_stress"] / EPSILON_M for d in decomp_data]

    # Setup 2-Panel Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Spatial Stress Ceiling Omega_stress vs Elastic Threshold epsilon_M
    ax1.plot(s_m_arr, s_tangent_list, color='#00838f', linewidth=2.5, label='3D Tangent Stress $\\mathcal{S}_{\\mu\\nu} / \\epsilon_M$')
    ax1.axhline(1.0, color='#d32f2f', linestyle='--', linewidth=1.8, label='Elastic Limit Ceiling ($\\epsilon_M$)')
    ax1.axvline(1.0, color='black', linestyle=':', label='Critical Threshold ($S_M = 1.0$)')

    ax1.set_xlabel('Metric Saturation Scalar $S_M$', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Normalized Tangent Stress $\\Omega_{\\text{stress}} / \\epsilon_M$', fontsize=11, fontweight='bold')
    ax1.set_title('A: 3D Spatial Stress Ceiling & Manifold Yield', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.legend(loc='upper left', fontsize=8.5)

    # Panel B: Orthogonal Energy Flux Vector J_flux Magnitude
    ax2.plot(s_m_arr, j_flux_list, color='#e65100', linewidth=2.5, label='Orthogonal Flux $\\mathbf{J}_{\\text{flux}}^{\\bar{\\mu}}$ [$10^{39}$ W]')
    ax2.axvline(1.0, color='black', linestyle=':', label='Critical Threshold ($S_M = 1.0$)')

    ax2.set_xlabel('Metric Saturation Scalar $S_M$', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Orthogonal Flux Drainage $\\mathbf{J}_{\\text{flux}}^{\\bar{\\mu}}$', fontsize=11, fontweight='bold')
    ax2.set_title('B: (4+1)D Bulk Flux Drainage Mechanics', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left', fontsize=8.5)

    # Annotation Box
    ax2.text(1.1, 0.2,
             "(4+1)D Decomposition Mechanics:\n"
             "• $\\nabla_{\\bar{\\mu}} T^{\\bar{\\mu}\\bar{\\nu}}_{(4+1)} = 0$ (Bulk Continuity)\n"
             "• Tangent Stress Clamped at Ceiling $\\epsilon_M$\n"
             "• Orthogonal Vector: $\\mathbf{J}_{\\text{flux}}^{\\bar{\\mu}} = \\kappa_{\\text{flux}} n^{\\bar{\\mu}}$\n"
             "• Prevents Infinite Density Singularities\n"
             "• Movie Anchor: Movie S15",
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#e0f7fa', edgecolor='#00838f', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure S3: $(4+1)$D Tensor Decomposition & Jump Mechanics ($S_M \\ge 1$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/FigureS3_Tensor_Decomposition.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_supplementary_tensor_decomposition()
