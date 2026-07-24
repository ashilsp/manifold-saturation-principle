"""
scripts/generate_fig4_white_dwarf.py

Generates publication figure for Section:
"Sub-Critical States (S_M < 1): Metric Retentiveness and Localized Rejections"
Figure 4: Geometric Dynamics of a Sub-Critical White Dwarf Metric Container.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import calculate_manifold_saturation, get_higher_dimensional_flux, SOLAR_MASS


def plot_white_dwarf_container():
    # Radial array from core outward (in km)
    r_km = np.linspace(0.1, 20000, 500)
    r_m = r_km * 1000.0

    # Typical White Dwarf Parameters (M = 1.0 M_sun, R = 6000 km)
    mass_wd = 1.0 * SOLAR_MASS
    rho_wd_core = 1e9  # kg/m^3

    # Calculate S_M potential profile across radial metric well
    sm_profile = [
        calculate_manifold_saturation(rho=rho_wd_core * np.exp(-r / 6e6), 
                                     mass=mass_wd, 
                                     radius=r)
        for r in r_m
    ]
    
    # Calculate higher-dimensional flux kappa_flux across profile
    flux_profile = [get_higher_dimensional_flux(sm) for sm in sm_profile]

    # Plotting setup
    fig, ax1 = plt.subplots(figsize=(8, 5), dpi=300)

    # Plot S_M Curve
    color = '#1f77b4'
    ax1.set_xlabel('Radial Distance $r$ [km]', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Manifold Saturation Metric $S_M(r)$', color=color, fontsize=11, fontweight='bold')
    ax1.plot(r_km, sm_profile, color=color, linewidth=2.5, label='White Dwarf Metric Well ($S_M \\ll 1$)')
    ax1.axhline(1.0, color='red', linestyle='--', linewidth=1.5, label='Spacetime Elastic Threshold ($S_M = 1.0$)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 1.2)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Plot Higher-Dimensional Flux Boundary (Secondary Axis)
    ax2 = ax1.twinx()
    color = '#d62728'
    ax2.set_ylabel('Higher-Dimensional Flux $\\kappa_{\\text{flux}}$ [J s$^{-1}$ m$^{-2}$]', color=color, fontsize=11, fontweight='bold')
    ax2.plot(r_km, flux_profile, color=color, linewidth=2, linestyle=':', label='Orthogonal Flux $\\kappa_{\\text{flux}}$')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(-0.1e38, 1e38)

    # Annotations
    ax1.text(10000, 0.4, 'Metric Container Regime\n3D Trapped Thermal Exhaust\n$\\kappa_{\\text{flux}} = 0$ (BLOCKED)', 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='orange', alpha=0.8),
             fontsize=9, fontweight='bold')

    plt.title('Figure 4: White Dwarf Sub-Critical Metric Container ($S_M \\ll 1$)', fontsize=12, fontweight='bold', pad=12)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/Figure4_White_Dwarf_Container.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_white_dwarf_container()
