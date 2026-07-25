"""
scripts/generate_fig_supp1_parameterization.py

Generates Supplementary Figure S1:
Parameterization and Dimensionless Variables across Metric Regimes.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.supplementary_metrics import (
    calculate_mass_density_normalization,
    calculate_electron_degeneracy_pressure,
    calculate_static_curvature,
    calculate_rotating_curvature,
    EPSILON_M,
    SOLAR_MASS,
    G,
    C
)


def plot_supplementary_parameterization():
    # Setup Figure with 2 Panels
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Degeneracy Pressure Pe vs. Dimensionless Density D
    rho_arr = np.logspace(6, 18, 300)  # Density from 10^6 to 10^18 kg/m^3
    d_arr = [calculate_mass_density_normalization(r) for r in rho_arr]
    pe_arr = [calculate_electron_degeneracy_pressure(r) for r in rho_arr]

    ax1.loglog(d_arr, pe_arr, color='#00838f', linewidth=2.2, label='Relativistic $P_e(x_F)$')
    ax1.set_xlabel('Dimensionless Mass Density $D = \\rho / \\rho_{\\text{Planck}}$', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Degeneracy Pressure $P_e$ [Pa]', fontsize=11, fontweight='bold')
    ax1.set_title('A: Degeneracy Pressure & Planck Normalization', fontsize=11, fontweight='bold')
    ax1.grid(True, which='both', linestyle=':', alpha=0.5)
    ax1.legend(loc='upper left', fontsize=8.5)

    # Panel B: Kerr Rotating Curvature Distortion Phi_rotating(theta) vs Polar Angle
    theta_deg = np.linspace(0, 180, 360)
    theta_rad = np.radians(theta_deg)
    
    m_test = 10.0 * SOLAR_MASS
    r_test = (2.0 * G * m_test) / (C**2) * 1.5  # 1.5 r_s
    rho_g = (G * m_test) / (C**2)
    
    # Compare non-rotating (a = 0) vs fast rotating (a = 0.9 * rho_g)
    phi_static_line = [calculate_static_curvature(m_test, r_test) for _ in theta_deg]
    phi_kerr_line = [calculate_rotating_curvature(m_test, r_test, t, spin_a=0.9 * rho_g) for t in theta_rad]

    ax2.plot(theta_deg, phi_kerr_line, color='#d32f2f', linewidth=2.2, label='Rotating Kerr $\\Phi_{\\text{rotating}}(\\theta)$ ($a = 0.9 r_g$)')
    ax2.plot(theta_deg, phi_static_line, color='black', linestyle='--', label='Static Schwarzschild $\\Phi_{\\text{static}}$')
    ax2.axvline(90, color='gray', linestyle=':', label='Equator ($\\theta = 90^\\circ$)')

    ax2.set_xlabel('Polar Angle $\\theta$ [Degrees]', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Curvature Parameter $\\Phi_{\\text{curvature}}$', fontsize=11, fontweight='bold')
    ax2.set_title('B: Axisymmetric Curvature Distortion', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', fontsize=8.5)

    # Data Annotation Box
    ax2.text(10, min(phi_kerr_line) * 1.05,
             f"Universal Elastic Limit:\n"
             f"• $\\epsilon_M = c^4 / (8\\pi G) \\approx {EPSILON_M:.3e}$ N\n"
             f"• Polar Curvature Enhancement at $\\theta=0^\\circ, 180^\\circ$",
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#e0f7fa', edgecolor='#00838f', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure S1: Dimensionless Metric Parameterization & Elastic Bounds', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/FigureS1_Parameterization.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_supplementary_parameterization()
