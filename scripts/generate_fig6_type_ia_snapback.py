"""
scripts/generate_fig6_type_ia_snapback.py

Generates publication figure for Section:
"Type Ia Supernovae: The Critical Metric Snap-Back (S_M_global -> 1)"
Figure 6: Geometric Dynamics of a Global Metric Snap-Back in a Type Ia Supernova Event.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import calculate_type_ia_global_metric, check_rd_stent_organization, SOLAR_MASS


def plot_type_ia_snapback():
    # Normalized radial distance across White Dwarf core (r / R_core)
    r_norm = np.linspace(0.0, 1.0, 300)
    
    # White Dwarf near Chandrasekhar Mass (M = 1.44 M_sun, R = 2000 km)
    mass_ch = 1.44 * SOLAR_MASS
    radius_wd = 2.0e6  # 2000 km in meters

    # Nearly uniform density profile D_uniform (small gradient)
    rho_center = 2.0e9  # kg/m^3
    rho_profile_uniform = rho_center * (1.0 - 0.15 * (r_norm**2))  # Flat profile
    rho_profile_steep = rho_center * np.exp(-5.0 * r_norm)         # Steep profile (for comparison)

    # Calculate radial S_M profiles
    sm_uniform = [
        calculate_type_ia_global_metric(d_uniform=rho / 5.155e96, mass_core=mass_ch, radius_core=radius_wd)
        for rho in rho_profile_uniform
    ]
    
    sm_steep = [
        calculate_type_ia_global_metric(d_uniform=rho / 5.155e96, mass_core=mass_ch, radius_core=radius_wd)
        for rho in rho_profile_steep
    ]

    # Evaluate snapback mechanics
    snapback_data = check_rd_stent_organization(density_gradient_scale=1e-5)

    # Plotting setup
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: S_M Uniformity Comparison
    ax1.plot(r_norm, sm_uniform, color='#d62728', linewidth=2.5, label='Uniform C-O Core ($S_M^{\\text{global}} \\to 1$)')
    ax1.plot(r_norm, sm_steep, color='#1f77b4', linewidth=2.0, linestyle='--', label='Steep Core Profile (Localized $R_d$)')
    ax1.axhline(1.0, color='black', linestyle=':', linewidth=1.5, label='Elastic Threshold ($S_M = 1.0$)')
    
    ax1.fill_between(r_norm, 0.95, 1.05, color='red', alpha=0.15, label='Volumetric Breach Zone')
    ax1.set_xlabel('Normalized Core Radius ($r / R_{\\text{core}}$)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Manifold Saturation Metric $S_M$', fontsize=11, fontweight='bold')
    ax1.set_title('A: Volumetric vs. Localized Saturation', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower left', fontsize=8.5)

    # Panel B: Thermonuclear Energy Release & Remnant Absence
    time_explosion = np.linspace(0, 60, 200)  # Days post-snapback
    light_curve = (time_explosion / 18.0)**2 * np.exp(-time_explosion / 18.0) * 1.5e44  # Normalized light curve

    ax2.plot(time_explosion, light_curve / 1e44, color='#ff7f0e', linewidth=2.5, label='Bolometric Yield (SN 2011fe Anchor)')
    ax2.set_xlabel('Time Post-Snapback [Days]', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Thermonuclear Yield [$10^{44}$ Joules]', fontsize=11, fontweight='bold')
    ax2.set_title('B: 3D Metric Snap-Back Energy Release', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)

    ax2.text(20, 0.35, 
             f"Snap-Back Result:\n"
             f"• R_d Stent Formed: {snapback_data['rd_stent_formed']}\n"
             f"• Higher-Dim Flux (kappa_flux): {snapback_data['kappa_flux']}\n"
             f"• Energy Released: ~{snapback_data['energy_release_joules']:.0e} J\n"
             f"• Central Remnant: NONE (Star Completely Disrupted)", 
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#fff2cc', edgecolor='#d62728', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure 6: Type Ia Supernova Metric Snap-Back Dynamics ($S_M^{\\text{global}} \\to 1$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/Figure6_Type_Ia_SnapBack.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_type_ia_snapback()
