"""
scripts/generate_fig_supp5_torsion_magnetic.py

Generates Supplementary Figure S5:
Differential Geometry Layout of Affine Torsion Frames and Electrodynamic Induction Coupling (Figure 16 / Movie S16).
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.supplementary_metrics import (
    calculate_metric_torsion_vector,
    calculate_induced_magnetic_field,
    calculate_magnetar_induction_profile,
    SOLAR_MASS
)


def plot_supplementary_torsion_magnetic():
    m_test = 1.4 * SOLAR_MASS  # Standard Neutron Star Mass
    r_test = 12.0e3             # 12 km radius

    # Spin period sweep (0.1 ms to 10 ms) -> spin_j angular momentum
    periods_ms = np.linspace(0.5, 10.0, 300)
    omega_arr = (2.0 * np.pi) / (periods_ms * 1.0e-3)
    
    # Moment of inertia I ~ 0.4 * M * R^2
    inertia = 0.4 * m_test * (r_test**2)
    spin_j_arr = inertia * omega_arr

    # Calculate Torsion and Induction B
    res_list = [calculate_magnetar_induction_profile(m_test, r_test, j) for j in spin_j_arr]
    tau_arr = [r["torsion_m1"] for r in res_list]
    b_gauss_arr = [r["b_gauss"] for r in res_list]

    # Setup Figure with 2 Panels
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Panel A: Manifold Torsion Vector |tau| vs Spin Period
    ax1.plot(periods_ms, tau_arr, color='#6a1b9a', linewidth=2.5, label='Manifold Torsion $\\boldsymbol{\\tau} = \\nabla \\times \\mathbf{e}_{\\text{metric}}$')
    ax1.set_xlabel('Rotation Period $P$ [ms]', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Metric Torsion Magnitude $|\\boldsymbol{\\tau}|$ [m$^{-1}$]', fontsize=11, fontweight='bold')
    ax1.set_title('A: Frame-Dragging Metric Torsion vs Spin', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.legend(loc='upper right', fontsize=8.5)

    # Panel B: Induced Magnetic Field B (Gauss) vs Metric Torsion |tau|
    ax2.plot(tau_arr, b_gauss_arr, color='#c2185b', linewidth=2.5, label='EMC Induction $\\mathbf{B} = \\sqrt{\\frac{c^4}{G \\mu_0}} \\boldsymbol{\\tau}$')
    ax2.axhspan(1.0e14, 1.0e15, color='magenta', alpha=0.15, label='Magnetar Field Range ($10^{14}-10^{15}$ G)')

    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Metric Torsion $|\\boldsymbol{\\tau}|$ [m$^{-1}$]', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Induced Magnetic Field $B$ [Gauss]', fontsize=11, fontweight='bold')
    ax2.set_title('B: Electrodynamic Induction Coupling ($B \\propto \\tau$)', fontsize=11, fontweight='bold')
    ax2.grid(True, which='both', linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left', fontsize=8.5)

    # Annotation Box
    ax2.text(1.0e-11, 2.0e11,
             "Einstein-Maxwell-Cartan Coupling:\n"
             "• $\\tau^{\\lambda}_{\\mu\\nu} = e^\\lambda_a(\\partial_\\mu e^a_\\nu - \\partial_\\nu e^a_\\mu) \\neq 0$\n"
             "• Off-diagonal potential $A_i = \\gamma_{0i} / \\gamma_{00}$\n"
             "• $B = \\sqrt{c^4 / (G \\mu_0)} \\cdot \\boldsymbol{\\tau}$\n"
             "• Explains magnetar fields without dynamo support\n"
             "• Movie Anchor: Movie S16",
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#f3e5f5', edgecolor='#6a1b9a', alpha=0.9),
             fontsize=8.5, fontweight='bold')

    plt.suptitle('Figure S5: Affine Torsion Frames and Electrodynamic Induction Coupling ($B \\propto \\boldsymbol{\\tau}$)', fontsize=13, fontweight='bold', y=0.98)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/FigureS5_Torsion_Magnetic_Coupling.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_supplementary_torsion_magnetic()
