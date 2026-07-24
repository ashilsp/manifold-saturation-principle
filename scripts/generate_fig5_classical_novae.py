"""
scripts/generate_fig5_classical_novae.py

Generates publication figure for Section:
"Classical Novae: Surface Shrugging (S_M_surface -> 1)"
Figure 5: Geometric Dynamics of a Pseudo-Critical Surface Shrug.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root directory to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import calculate_surface_shrug_metric, check_surface_shrug_trigger, SOLAR_MASS


def plot_classical_nova_shrug():
    # Time steps for binary accretion cycle (in years)
    time_years = np.linspace(0, 20, 500)
    
    # White Dwarf Core Baseline Parameters (M = 1.35 M_sun, near Chandrasekhar limit)
    d_core = 1.5e-87     # Deeply sub-critical core density ratio
    phi_surface = 1.2e-4  # Surface curvature scalar
    
    # Accretion rate simulation driving delta_D_acc over time
    accretion_rate = 1.8e-88  # Density accumulation per year
    
    s_m_surface_list = []
    s_m_core_list = []
    shrug_events = []
    
    # Simulate cyclic accretion and surface shrug resets
    current_acc = 0.0
    for t in time_years:
        current_acc += accretion_rate * (20.0 / 500.0)
        s_m_surf = calculate_surface_shrug_metric(d_core, current_acc, phi_surface)
        s_m_c = calculate_surface_shrug_metric(d_core, 0.0, phi_surface)
        
        status = check_surface_shrug_trigger(s_m_surf, s_m_c)
        
        if status["shrug_triggered"]:
            shrug_events.append((t, s_m_surf))
            current_acc = 0.0  # Thermonuclear ejection resets accreted shell
            
        s_m_surface_list.append(s_m_surf)
        s_m_core_list.append(s_m_c)

    # Plotting setup
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    
    ax.plot(time_years, s_m_surface_list, color='#d62728', linewidth=2.2, label='Surface Metric $S_M^{\\text{surface}}(t)$')
    ax.plot(time_years, s_m_core_list, color='#1f77b4', linewidth=2.0, linestyle='--', label='Core Metric $S_M^{\\text{core}} \\ll 1$ (Intact)')
    
    # Draw Critical Surface Limit
    ax.axhline(1.0, color='black', linestyle=':', linewidth=1.5, label='Pseudo-Critical Threshold ($S_M^{\\text{surface}} = 1.0$)')
    
    # Highlight Surface Shrug Ejection Events
    for t_event, sm_val in shrug_events:
        ax.plot(t_event, sm_val, 'ro', markersize=8)
        ax.annotate('Surface Shrug Blast\n(Ejecta Shell Released)', 
                    xy=(t_event, sm_val), 
                    xytext=(t_event - 3.5, sm_val + 0.12),
                    arrowprops=dict(facecolor='red', shrink=0.08, width=1.5, headwidth=6),
                    fontsize=8, fontweight='bold', color='red')

    ax.set_xlabel('Binary Accretion Time [Years]', fontsize=11, fontweight='bold')
    ax.set_ylabel('Manifold Saturation Metric $S_M$', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 1.3)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Annotations for empirical anchors
    ax.text(1.0, 0.25, 
            'Empirical Anchors: RS Ophiuchi & U Scorpii\n'
            '• Core preserves sub-critical state ($S_M^{\\text{core}} \\ll 1$)\n'
            '• Elastic 3D Rebound drives periodic shell ejection\n'
            '• Zero higher-dimensional leakage ($\\kappa_{\\text{flux}} = 0$)', 
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#fff2cc', edgecolor='#d62728', alpha=0.85),
            fontsize=8.5, fontweight='bold')

    plt.title('Figure 5: Classical Nova Surface Shrug Mechanics ($S_M^{\\text{surface}} \\to 1$)', fontsize=12, fontweight='bold', pad=12)
    fig.tight_layout()

    # Save output plot
    os.makedirs('figures_output', exist_ok=True)
    output_path = 'figures_output/Figure5_Classical_Novae_Shrug.png'
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated and saved figure to: {output_path}")


if __name__ == '__main__':
    plot_classical_nova_shrug()
