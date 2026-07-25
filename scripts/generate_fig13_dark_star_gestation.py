"""
scripts/generate_fig13_dark_star_gestation.py

Generates publication figure for Section:
"Primordial Gestation Sites: Dark Stars as Un-Stented Nodes"
Figure 13: Geometric Dynamics of a Primordial Nodal Gestation Site in a Super-Massive Dark Star Progenitor.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import calculate_dark_star_gestation_metrics, SOLAR_MASS


def plot_dark_star_gestation():
    # Mass range for Dark Stars (10^3 to 10^6 M_sun)
    mass_arr_msun = np.logspace(3, 6, 300)
    
    # Calculate diffuse radius and infiltration power across mass range
    radius_au_list = []
    power_solar_list = []

    for m in mass_arr_msun:
        res = calculate_dark_star_gestation_metrics(mass_msun=m, redshift_z=15.0)
        radius_au_list.append(res["diffuse_radius_au"])
        # Power in solar luminosity units (L_sun ~ 3.828e26 W)
        power_solar_list.append(res["infiltration_power_watts"] / 3.828e26)

    # Redshift evolution of SMBH seed growth (z = 20 down to z = 7)
    redshifts = np.linspace(20, 7, 300)
    # Direct collapse mass growth trajectory
    seed_mass_growth = 1.0e5 * (21.0 / redshifts)**2.5

    # Setup Plotting (2 Panels)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Un-stented Diffuse Radius & Infiltration Power
    color1 = '#00838f'
    ax1.plot(mass_arr_msun, power_solar_list, color=color1, linewidth=2.5, label='$\kappa$-Flux Infiltration Power [$L_\\odot$]')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Gestation Node Mass [$M_\\odot$]', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Ambient Infiltration Power [$L_\\odot$]', fontsize=11, fontweight='bold', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax1_twin = ax1.twinx()
    color2 = '#e65100'
    ax1_twin.plot(mass_arr_msun, radius_au_list, color=color2, linestyle='--', linewidth=2.0, label='Diffuse Basin Radius [AU]')
    ax1_twin.set_yscale('log')
    ax1_twin.set_ylabel('Diffuse Basin Radius [AU]', fontsize=11, fontweight='bold', color=color2)
    ax1_twin.tick_params(axis='y', labelcolor=color2)

    ax1.set_title('A: Primordial Dark Star Infiltration Power & Basin Scale', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.5)

    # Panel B: High-Redshift Direct Collapse Seed Growth (JWST Quasar Anchor)
    ax2.plot(redshifts, seed_mass_growth, color='#6a1b9a', linewidth=2.5, label='Direct Collapse SMBH Seed Growth')
    ax2.axhline(1.0e6, color='red', linestyle=':', label='JWST Early Quasar Seed Threshold ($10^6 M_\\odot$)')
    ax2.set_gca().invert_xaxis()  # Invert redshift axis (20 -> 7)

    ax2.set_yscale('log')
    ax2.set_xlabel('Redshift ($z$)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Node Mass [$M_\\odot$]', fontsize=11, fontweight='bold')
    ax2.set_title('B: High-Redshift Quasar Seed Formation (JWST $z > 7$)', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='lower left', fontsize=8.5)

    # Ingestion Data Box
    ax2.text(18.5, 2.0e3,
             "Nodal Gestation Mechanics:\n"
             "• Incoherent Phase: Un-stented $S_M \\to 1$\n"
             "• Fueled by background $\\kappa$-flux leaking\n"
             "• Hyper-massive growth ($10^4 - 10^6 M_\\odot$)\n"
             "• Empirical Anchor: JWST Quasars ($z > 7$)",
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#f3e5f5', edgecolor='#6a1b9a', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure 13: Primordial Nodal Gestation Sites & Dark Stars ($S_M \\to 1, z > 15$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/Figure13_Dark_Star_Gestation.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_dark_star_gestation()
