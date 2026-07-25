"""
scripts/generate_fig_supp6_chandrasekhar_sensitivity.py

Generates Supplementary Figure S6:
Radial Parameter Profiles of the Manifold Saturation Metric (S_M)
across Core Compositions (M -> M_Ch) (Figure 17 / Movie S17).
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.supplementary_metrics import (
    calculate_global_chandrasekhar_sm
)


def plot_supplementary_chandrasekhar_sensitivity():
    # Radial coordinate normalized to R_core
    r_norm_arr = np.linspace(0.0, 1.0, 300)
    
    # Calculate radial S_M profiles at M -> M_Ch (mass_ratio = 0.995)
    mass_ratio = 0.995
    
    # High-Carbon Kernel (X_C = 0.6)
    sm_high_carbon = [
        calculate_global_chandrasekhar_sm(mass_ratio, x_carbon=0.6, r_norm=r)
        for r in r_norm_arr
    ]
    
    # Oxygen-Rich Kernel (X_C = 0.2)
    sm_oxygen_rich = [
        calculate_global_chandrasekhar_sm(mass_ratio, x_carbon=0.2, r_norm=r)
        for r in r_norm_arr
    ]

    # Setup Plot
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

    # Criticality Threshold Line S_M = 1.0
    ax.axhline(1.0, color='#d32f2f', linestyle='--', linewidth=2.0, label='Criticality Limit ($S_M = 1.0$)')

    # Curve 1: High-Carbon Kernel
    ax.plot(r_norm_arr, sm_high_carbon, color='#1565c0', linewidth=2.5, label='High-Carbon Kernel ($X_C = 0.6 \\ge 0.5$)')
    
    # Curve 2: Oxygen-Rich Kernel
    ax.plot(r_norm_arr, sm_oxygen_rich, color='#e65100', linewidth=2.5, label='Oxygen-Rich Kernel ($X_C = 0.2 < 0.3$)')

    # Highlight 85% Core Volume Uniform Breach for Carbon Core
    ax.axvspan(0.0, 0.85, color='blue', alpha=0.08, label='Uniform Breach Zone ($85\\%$ Core Volume)')

    ax.set_xlabel('Normalized Core Radius ($r / R_{\\text{core}}$)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Manifold Saturation Metric ($S_M$)', fontsize=11, fontweight='bold')
    ax.set_title('Figure S6: $S_M$ Radial Profiles across Chandrasekhar Boundary ($M \\to M_{\\text{Ch}}$)', fontsize=12, fontweight='bold')
    
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.2, 1.6)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', fontsize=9)

    # Annotation Callout Box
    ax.text(0.05, 0.35,
             "Bifurcation Mechanics:\n"
             "• High-Carbon ($X_C \\ge 0.5$): Global uniform breach across $85\\%$ radius\n"
             "  $\\rightarrow$ Synchronized 3D metric snap-back (No remnant)\n"
             "• Oxygen-Rich ($X_C < 0.3$): Central density spike gradient\n"
             "  $\\rightarrow$ Favors electron-capture collapse pathway\n"
             "• Movie Anchor: Movie S17",
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#e0f7fa', edgecolor='#00838f', alpha=0.9),
             fontsize=9, fontweight='bold')

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/FigureS6_Chandrasekhar_Sensitivity.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_supplementary_chandrasekhar_sensitivity()
