"""
scripts/generate_fig_supp8_rotation_sweep.py

Generates Supplementary Figure S8:
Two-Dimensional Contour Sweep of Metric Saturation S_M(r, theta) Across Kerr Angular Momentum Space (J -> 1)
(Figure 19 / Movie S19).
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.supplementary_metrics import (
    generate_polar_sm_contour_data,
    SOLAR_MASS
)


def plot_supplementary_rotation_sweep():
    # Setup test mass
    m_test = 10.0 * SOLAR_MASS
    
    # Generate datasets for 3 scenarios: static (a*=0), intermediate (a*=0.5), extremal (a*=0.98)
    data_static = generate_polar_sm_contour_data(mass_kg=m_test, a_star=0.0)
    data_inter = generate_polar_sm_contour_data(mass_kg=m_test, a_star=0.5)
    data_extreme = generate_polar_sm_contour_data(mass_kg=m_test, a_star=0.98)

    # Setup Plot
    fig, ax = plt.subplots(figsize=(8, 7), dpi=300)

    # Plot S_M = 1.0 Phase Boundary Iso-contours
    cs_static = ax.contour(
        data_static["x_grid"], data_static["y_grid"], data_static["sm_grid"], 
        levels=[1.0], colors=['#1565c0'], linewidths=2.5
    )
    
    cs_inter = ax.contour(
        data_inter["x_grid"], data_inter["y_grid"], data_inter["sm_grid"], 
        levels=[1.0], colors=['#7b1fa2'], linewidths=2.5, linestyles='--'
    )
    
    cs_extreme = ax.contour(
        data_extreme["x_grid"], data_extreme["y_grid"], data_extreme["sm_grid"], 
        levels=[1.0], colors=['#e65100'], linewidths=3.0
    )

    # Shade the Equatorial Choked Region for Extremal Spin
    ax.fill_between([0.8, 3.5], 0.0, 0.6, color='gray', alpha=0.15, label='Equatorial Blockade ($S_M < 1.0$)')

    # Polar Jet Venting Vectors for Extreme Spin
    ax.annotate(
        '', xy=(0.0, 3.2), xytext=(0.0, 2.2),
        arrowprops=dict(facecolor='#e65100', edgecolor='#e65100', width=2.5, headwidth=9.0)
    )
    ax.text(0.1, 2.7, "Collimated Polar Jet Venting\n($S_M \\ge 1.0$ at $\\theta \\to 0$)", color='#e65100', fontweight='bold', fontsize=8.5)

    # Labels and Formatting
    ax.set_xlabel('Equatorial Distance ($x / r_s$ where $\\theta = \\pi/2$)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Polar Axis Distance ($y / r_s$ where $\\theta = 0$)', fontsize=11, fontweight='bold')
    ax.set_title('Figure S8: 2D Iso-Contour Boundary $S_M(r, \\theta) = 1.0$ Across Spin $a_*$', fontsize=12, fontweight='bold')

    # Dummy lines for clean legend
    ax.plot([], [], color='#1565c0', linewidth=2.5, label='$a_* = 0.0$ (Isotropic Schwarzschild $R_d$)')
    ax.plot([], [], color='#7b1fa2', linewidth=2.5, linestyle='--', label='$a_* = 0.5$ (Torsional Oblate Distortion)')
    ax.plot([], [], color='#e65100', linewidth=3.0, label='$a_* \\to 1.0$ (Polar Venting & Hypernova Jet)')

    ax.set_xlim(0.0, 3.5)
    ax.set_ylim(0.0, 3.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', fontsize=8.5)

    # Callout Box
    ax.text(
        0.15, 0.8,
        "Kerr Parameter Sweep Dynamics:\n"
        "• $a_* = 0$: Isotropic 3D drainage ($R_d$ spherical horizon)\n"
        "• $a_* = 0.5$: Oblate deformation $\\rightarrow$ Torsional Magnetar Starquake\n"
        "• $a_* \\to 1.0$: Centrifugal blockade at equator ($S_M < 1$)\n"
        "  Forces hyper-collimated polar jet venting (GRBs/Hypernovae)\n"
        "• Movie Anchor: Movie S19",
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff3e0', edgecolor='#e65100', alpha=0.9),
        fontsize=8.5, fontweight='bold'
    )

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/FigureS8_Rotation_Sweep.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_supplementary_rotation_sweep()
