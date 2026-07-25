"""
scripts/generate_fig11_kilonova_splicing.py

Generates publication figure for Section:
"Kilonovae: Manifold Splicing in Compact Binary Mergers"
Figure 11: Geometric Dynamics of Manifold Splicing in a Compact Binary Merger Event.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import calculate_manifold_splicing_metrics, SOLAR_MASS


def plot_kilonova_splicing():
    # Model GW170817 binary neutron star collision (1.4 M_sun + 1.3 M_sun)
    m1 = 1.4 * SOLAR_MASS
    m2 = 1.3 * SOLAR_MASS
    
    splicing_res = calculate_manifold_splicing_metrics(m1, m2, ejecta_velocity_c=0.2)

    # Time array for kilonova light curve evolution (0.1 to 15 days)
    days = np.linspace(0.1, 15.0, 500)
    
    # Model multi-band optical/infrared bolometric luminosity curve [ergs/s]
    # Blue kilonova (lanthanide-poor) + Red kilonova (lanthanide-rich r-process)
    l_blue = 1.0e42 * (days / 1.0)**(-1.2) * np.exp(-days / 2.0)
    l_red = 3.0e41 * (days / 3.0)**(-1.1) * np.exp(-days / 8.0)
    l_total = l_blue + l_red

    # Setup Plotting (2 Panels)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Composite Saturation Spike & Relaxation Profile
    time_sec = np.linspace(0, 120, 500)
    sm_profile = 0.98 + (splicing_res["s_m_composite"] - 0.98) * np.exp(-((time_sec - 10.0)**2) / 50.0)
    sm_profile[time_sec > 10.0] = 1.0 + (splicing_res["s_m_composite"] - 1.0) * np.exp(-(time_sec[time_sec > 10.0] - 10.0) / splicing_res["relaxation_timescale_s"])

    ax1.plot(time_sec, sm_profile, color='#1565c0', linewidth=2.5, label='Composite Saturation $S_M^{\\text{composite}}$')
    ax1.axhline(1.0, color='red', linestyle='--', linewidth=1.5, label='Critical Threshold ($S_M = 1.0$)')
    ax1.axvspan(5, 20, color='orange', alpha=0.2, label='Dynamic Splicing Phase')

    ax1.set_xlabel('Time Post-Contact [Seconds]', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Composite Metric Saturation $S_M$', fontsize=11, fontweight='bold')
    ax1.set_title('A: Metric Curvature Fusion & Relaxation', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right', fontsize=8.5)

    # Panel B: Electromagnetic Kilonova Light Curve (GW170817 / AT2017gfo Anchor)
    ax2.plot(days, l_total, color='#d32f2f', linewidth=2.2, label='Bolometric Luminosity (Total)')
    ax2.plot(days, l_blue, color='#1e88e5', linestyle='--', label='Blue Component (Fast Ejecta)')
    ax2.plot(days, l_red, color='#8e24aa', linestyle=':', label='Red Component ($r$-Process Heavy Elements)')

    ax2.set_yscale('log')
    ax2.set_xlabel('Time Since Merger [Days]', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Luminosity [erg / s]', fontsize=11, fontweight='bold')
    ax2.set_title('B: $r$-Process Kilonova Transient (GW170817 Anchor)', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', fontsize=8.5)

    # Ingestion Data Box
    ax2.text(5.0, 1.0e40,
             "Splicing Mechanics:\n"
             f"• Peak $S_M^{{\\text{{comp}}}}$: {splicing_res['s_m_composite']:.2f}\n"
             f"• Un-stented Ejecta: ~{splicing_res['ejecta_mass_msun']:.3f} $M_\\odot$\n"
             f"• $r$-Process Yield (Au/Pt): Enabled\n"
             f"• Anchor: GW170817 / AT2017gfo",
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#e3f2fd', edgecolor='#1565c0', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure 11: Manifold Splicing in Compact Binary Mergers ($S_M^{\\text{composite}} > 1$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output figure
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/Figure11_Kilonova_Splicing.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_kilonova_splicing()
