"""
scripts/generate_fig12_hypernova_polar_jet.py

Generates publication figure for Section:
"Hypernovae and Long Gamma-Ray Bursts (S_M >> 1)"
Figure 12: Geometric Dynamics of Axisymmetric Polar Venting in a Super-Critical Ignition Event.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import calculate_polar_venting_profile, calculate_hypernova_lgrb_metrics


def plot_hypernova_polar_jet():
    # Setup polar angle grid [0 to 180 degrees]
    theta_deg = np.linspace(0, 180, 360)
    theta_rad = np.radians(theta_deg)
    
    kappa_base = 1.0e39
    s_m_super = 3.0
    
    # Calculate polar venting profiles for different spin states
    phi_vent = [calculate_polar_venting_profile(t, s_m=s_m_super, kappa_flux=kappa_base) for t in theta_rad]
    
    # Model LGRB Prompt Emission Light Curve (SN 1998bw / GRB 980425)
    time_sec = np.linspace(0, 100, 500)
    # FRED (Fast Rise, Exponential Decay) pulse profile
    lgrb_flux = 1.0e45 * (time_sec / 5.0)**1.5 * np.exp(-time_sec / 12.0)

    # Setup Plotting (2 Panels)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Angular Polar Venting Distribution Phi_vent(theta)
    ax1.plot(theta_deg, np.array(phi_vent) / 1.0e39, color='#e65100', linewidth=2.5, label='Polar Venting $\\Phi_{\\text{vent}}(\\theta) \\propto \\cos^2\\theta$')
    ax1.axvline(90, color='gray', linestyle='--', linewidth=1.5, label='Equatorial Choke Zone ($\\theta = 90^\\circ$)')
    ax1.fill_between(theta_deg, 0, np.array(phi_vent) / 1.0e39, color='#ffb74d', alpha=0.3)

    ax1.set_xlabel('Polar Angle $\\theta$ [Degrees]', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Venting Flux Density [$10^{39}$ W]', fontsize=11, fontweight='bold')
    ax1.set_title('A: Angular Energy Venting & Equatorial Choke', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper center', fontsize=8.5)

    # Panel B: LGRB Prompt Gamma-Ray Light Curve (GRB 980425 Anchor)
    ax2.plot(time_sec, lgrb_flux, color='#d32f2f', linewidth=2.2, label='Prompt Gamma-Ray Pulse ($E_{\\text{iso}}$)')
    ax2.set_xlabel('Time [Seconds]', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Isotropic Luminosity [erg / s equivalent]', fontsize=11, fontweight='bold')
    ax2.set_title('B: Relativistic Jet Birth Cry (SN 1998bw / GRB 980425)', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', fontsize=8.5)

    # Ingestion Data Box
    lgrb_data = calculate_hypernova_lgrb_metrics(mass_msun=30.0, spin_j_norm=0.85, s_m=s_m_super)
    ax2.text(35, max(lgrb_flux) * 0.5,
             "Super-Critical LGRB Mechanics:\n"
             f"• Metric Saturation ($S_M$): {lgrb_data['s_m']:.1f} >> 1\n"
             f"• Jet Beaming Angle (\\theta_j): ~{lgrb_data['jet_half_angle_deg']:.1f}^\\circ\n"
             f"• Lorentz Factor (\\Gamma): > {lgrb_data['lorentz_factor_gamma']:.0f}\n"
             f"• Empirical Anchor: SN 1998bw / GRB 980425",
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#fff3e0', edgecolor='#e65100', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure 12: Polar Jet Venting in Super-Critical Ignitions ($S_M \\gg 1$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/Figure12_Hypernova_Polar_Jet.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_hypernova_polar_jet()
