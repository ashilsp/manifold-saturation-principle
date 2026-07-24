"""
scripts/generate_fig7_pulsar_bottleneck.py

Generates publication figure for Section:
"Pulsars and Neutron Stars: The Pre-Critical Bottleneck (S_M -> 1^-)"
Figure 7: Geometric Dynamics of a Pre-Critical Metric Bottleneck in a Neutron Star/Pulsar System.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import calculate_pulsar_bottleneck_metric, calculate_metric_grinding_power, SOLAR_MASS


def plot_pulsar_bottleneck():
    # Mass sweep for neutron stars (1.0 to 2.2 M_sun)
    mass_arr_msun = np.linspace(1.0, 2.17, 300)
    
    # Empirical Anchors: Crab Pulsar (M ~ 1.4 M_sun, f = 30 Hz) & PSR J0740+6620 (M ~ 2.08 M_sun, f = 346 Hz)
    anchors = {
        "Crab Pulsar": {"mass": 1.4 * SOLAR_MASS, "radius": 12000, "freq": 30.0, "color": "purple"},
        "PSR J0740+6620": {"mass": 2.08 * SOLAR_MASS, "radius": 12300, "freq": 346.0, "color": "blue"}
    }

    # Radial profile calculation for potential funnel depth
    r_km = np.linspace(0.1, 50, 400)
    
    sm_profiles = {}
    for name, data in anchors.items():
        sm_val = calculate_pulsar_bottleneck_metric(
            rho_core=1.5e17, mass_ns=data["mass"], radius_ns=data["radius"], spin_freq_hz=data["freq"]
        )
        # Model local spatial strain profile S_M(r)
        sm_profiles[name] = sm_val * np.exp(-r_km / (data["radius"] / 1000.0))

    # Plotting setup
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Pre-Critical Metric Funnel S_M -> 1^-
    ax1.plot(r_km, sm_profiles["Crab Pulsar"], color='purple', linewidth=2.2, label='Crab Pulsar ($S_M \\to 1^-$)')
    ax1.plot(r_km, sm_profiles["PSR J0740+6620"], color='blue', linewidth=2.2, label='PSR J0740+6620 ($S_M \\to 1^-$)')
    ax1.axhline(1.0, color='red', linestyle='--', linewidth=1.5, label='Puncture Boundary ($S_M = 1.0$)')
    ax1.axhspan(0.90, 1.0, color='orange', alpha=0.15, label='Pre-Critical Bottleneck Zone')

    ax1.set_xlabel('Radial Distance $r$ [km]', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Manifold Saturation Metric $S_M(r)$', fontsize=11, fontweight='bold')
    ax1.set_title('A: Deep Spatial Potential Funnel ($S_M \\to 1^-$)', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.set_ylim(0, 1.1)
    ax1.legend(loc='lower right', fontsize=8.5)

    # Panel B: Resonant Pulsation Emission Profile
    phase = np.linspace(0, 2.0, 500)  # Pulse phase (2 cycles)
    # Model double-peaked resonant pulse signature
    pulse_signal = (np.exp(-((phase % 1.0 - 0.25)**2) / 0.003) + 
                    0.5 * np.exp(-((phase % 1.0 - 0.55)**2) / 0.005))

    ax2.plot(phase, pulse_signal, color='purple', linewidth=2.0, label='Macro-Topological Resonant Pulse')
    ax2.set_xlabel('Pulse Phase [Cycles]', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Resonant Intensity [Arbitrary Units]', fontsize=11, fontweight='bold')
    ax2.set_title('B: Metric Grinding Resonant Emission Profile', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)

    # Calculate grinding mechanics for Crab anchor
    crab_grind = calculate_metric_grinding_power(0.98, anchors["Crab Pulsar"]["mass"], anchors["Crab Pulsar"]["radius"], 30.0)

    ax2.text(0.8, 0.45, 
             f"Bottleneck Mechanics:\n"
             f"• Higher-Dim Flux (kappa_flux): {crab_grind['kappa_flux']}\n"
             f"• Metric Grinding Power: ~{crab_grind['grinding_power_watts']:.1e} W\n"
             f"• Effective B-Field: ~{crab_grind['effective_b_field_tesla']:.1e} T\n"
             f"• Empirical Anchors: Crab, PSR J0740+6620", 
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#f0f8ff', edgecolor='purple', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure 7: Pre-Critical Metric Bottleneck Dynamics in Pulsars ($S_M \\to 1^-$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/Figure7_Pulsar_Bottleneck.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_pulsar_bottleneck()
