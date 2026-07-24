"""
scripts/generate_fig9_type_ii_rejection.py

Generates publication figure for Section:
"Failure Modes at Metric Criticality: Rebound and Topological Rejection"
Figure 9: Geometric Dynamics of a Core-Collapse Rejection Failure Mode in a Type II Supernova Event.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import check_core_collapse_rejection, get_topological_rejection_taxonomy


def plot_type_ii_rejection():
    # Setup turbulence vs saturation grid
    entropy_arr = np.linspace(1.0, 10.0, 200)
    sm_arr = np.linspace(0.8, 1.0, 200)
    
    SM, ENTROPY = np.meshgrid(sm_arr, entropy_arr)
    
    # Calculate rebound shock energy across parameter space
    rebound_energy = np.zeros_like(SM)
    for i in range(ENTROPY.shape[0]):
        for j in range(SM.shape[1]):
            res = check_core_collapse_rejection(
                s_m_core=SM[i, j], 
                entropy_per_baryon=ENTROPY[i, j], 
                asymmetry_factor=0.5
            )
            rebound_energy[i, j] = res["shock_rebound_kinetic_energy_joules"] / 1e44

    # Setup Plotting (2 Panels)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Phase Transition Map (Successful OCM vs Topological Rejection)
    cp = ax1.contourf(SM, ENTROPY, rebound_energy, levels=20, cmap='YlOrRd')
    cbar = fig.colorbar(cp, ax=ax1)
    cbar.set_label('Rebound Shock Energy [$10^{44}$ Joules]', fontsize=9, fontweight='bold')

    ax1.set_xlabel('Core Metric Saturation $S_M^{\\text{core}}$', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Entropic Turbulence ($S / k_B$)', fontsize=11, fontweight='bold')
    ax1.set_title('A: Topological Rejection Boundary Phase Diagram', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.5)

    ax1.text(0.82, 2.0, "Successful 4D Ignition Zone\n(Clean Black Hole)", 
             fontsize=8.5, fontweight='bold', color='black', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax1.text(0.92, 8.0, "Core Rejection Zone\n(Type II Supernova)", 
             fontsize=8.5, fontweight='bold', color='darkred', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Panel B: Filamentary Asymmetry Simulation (Cassiopeia A Remnant Anchor)
    np.random.seed(42)
    theta = np.linspace(0, 2 * np.pi, 300)
    # Chaotic, asymmetric shockwave radius
    r_shock = 1.0 + 0.3 * np.sin(3 * theta) + 0.2 * np.cos(7 * theta) + 0.1 * np.random.normal(0, 0.2, 300)
    
    x_shock = r_shock * np.cos(theta)
    y_shock = r_shock * np.sin(theta)

    ax2.plot(x_shock, y_shock, color='#d62728', linewidth=1.5, label='Asymmetric Filamentary Shell')
    ax2.fill(x_shock, y_shock, color='#ff7f0e', alpha=0.2)
    ax2.scatter([0], [0], color='blue', s=60, zorder=5, label='Neutron Star Remnant')

    ax2.set_xlabel('Spatial Dimension $X$ [Arbitrary Units]', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Spatial Dimension $Y$ [Arbitrary Units]', fontsize=11, fontweight='bold')
    ax2.set_title('B: Filamentary Ejecta Geometry (Cas A Anchor)', fontsize=11, fontweight='bold')
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', fontsize=8.0)

    # Summary Text Box
    ax2.text(-1.6, -1.5,
             "Rejection Mechanics:\n"
             "• Reflected 3D kinetic shockwave\n"
             "• Disordered high-entropy exhaust\n"
             "• Empirical Anchor: Cassiopeia A Shell",
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff5f5', edgecolor='#d62728', alpha=0.9),
             fontsize=8.0, fontweight='bold')

    plt.suptitle('Figure 9: Topological Rejection & Metric Rebound Dynamics ($S_M^{\\text{core}} \\to 1$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/Figure9_Type_II_Rejection.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_type_ii_rejection()
