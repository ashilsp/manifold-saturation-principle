"""
scripts/generate_fig10_nodal_maturity.py

Generates publication figure for Section:
"Nodal Maturity and the Resolution of Singularities (S_M = 1)"
Figure 10: Geometric Dynamics of a Successful Super-Critical Ignition and Singularity Regularization.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import calculate_regularized_laminar_radius, calculate_stellar_birth_cry_luminosity, SOLAR_MASS


def plot_nodal_maturity():
    # Mass sweep for stellar-mass nodes (3 to 20 M_sun)
    mass_msun = np.linspace(3.0, 20.0, 300)
    mass_kg = mass_msun * SOLAR_MASS

    # Calculate classical Schwarzschild radius vs regularized R_d radius
    r_classical = (2.0 * 6.67430e-11 * mass_kg) / (3.0e8**2) / 1000.0  # in km
    
    # R_d at critical flux kappa_flux = 0.5 * kappa_crit
    r_d_regularized = [
        calculate_regularized_laminar_radius(m, kappa_flux=0.5e39) / 1000.0
        for m in mass_kg
    ]

    # Empirical Anchors: Cygnus X-1 (M ~ 14.8 M_sun) & M33 X-7 (M ~ 15.65 M_sun)
    cyg_x1_data = calculate_stellar_birth_cry_luminosity(14.8 * SOLAR_MASS, kappa_flux=0.8e39)
    m33_x7_data = calculate_stellar_birth_cry_luminosity(15.65 * SOLAR_MASS, kappa_flux=0.85e39)

    # Setup Plotting (2 Panels)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Singularity Regularization (Classical Divergence vs. R_d Stent)
    ax1.plot(mass_msun, r_d_regularized, color='#00838f', linewidth=2.5, label='OCM Regularized Radius $R_d$ ($r > 0$)')
    ax1.plot(mass_msun, r_classical, color='black', linestyle='--', linewidth=1.8, label='Schwarzschild Horizon $R_s$')
    ax1.plot(mass_msun, np.zeros_like(mass_msun), color='red', linestyle=':', linewidth=1.5, label='GR Singularity ($r = 0$)')

    ax1.scatter([14.8], [cyg_x1_data["regularized_radius_m"] / 1000.0], color='#d32f2f', s=70, zorder=5, label='Cygnus X-1 Anchor')
    ax1.scatter([15.65], [m33_x7_data["regularized_radius_m"] / 1000.0], color='#7b1fa2', s=70, zorder=5, label='M33 X-7 Anchor')

    ax1.set_xlabel('Nodal Mass [$M_\\odot$]', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Core Boundary Radius [km]', fontsize=11, fontweight='bold')
    ax1.set_title('A: Singularity Regularization & $R_d$ Interface', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left', fontsize=8.5)

    # Panel B: Stellar Birth Cry Hard X-Ray / Gamma-Ray Energy Spectrum
    energy_kev = np.logspace(0, 3, 500)  # Energy spectrum 1 keV to 1 MeV
    # Model thermal + power-law Birth Cry spectral energy distribution
    flux_spectrum = (energy_kev**(-1.7)) * np.exp(-energy_kev / 150.0) * 1.0e38

    ax2.loglog(energy_kev, flux_spectrum, color='#e65100', linewidth=2.2, label='Stellar Birth Cry Transient Spectrum')
    ax2.set_xlabel('Photon Energy [keV]', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Flux Density [Watts / keV]', fontsize=11, fontweight='bold')
    ax2.set_title('B: Hard X-Ray / $\\gamma$-Ray Birth Cry Activation Profile', fontsize=11, fontweight='bold')
    ax2.grid(True, which='both', linestyle=':', alpha=0.5)

    ax2.text(2.0, 1.0e33,
             "Super-Critical Ignition Mechanics:\n"
             f"• Singularity Regularized: True (r > 0)\n"
             f"• Cygnus X-1 R_d: ~{cyg_x1_data['regularized_radius_m']/1000.0:.1f} km\n"
             f"• Orthogonal Flux (kappa_flux): > 0\n"
             f"• Empirical Anchors: Cygnus X-1, M33 X-7",
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#e0f7fa', edgecolor='#00838f', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure 10: Nodal Maturity and Singularity Regularization ($S_M = 1$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/Figure10_Nodal_Maturity.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_nodal_maturity()
