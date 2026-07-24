"""
src/metrics.py

Manifold Saturation Principle (MSP) - Core Metrics Engine
Section 1: Foundational Framework & Saturation Metric (S_M) definitions.
"""

import numpy as np

# ==============================================================================
# PHYSICAL AND FUNDAMENTAL CONSTANTS (SI / Planck Units)
# ==============================================================================
C = 2.99792458e8             # Speed of light in vacuum [m/s]
G = 6.67430e-11              # Universal Gravitational Constant [m^3 kg^-1 s^-2]
HBAR = 1.054571817e-34       # Reduced Planck Constant [J s]
SOLAR_MASS = 1.98840e30      # Standard Solar Mass M_sun [kg]

# Elasticity threshold of 3D spacetime canvas (epsilon_M = c^4 / (8 * pi * G))
EPSILON_M = (C**4) / (8.0 * np.pi * G)  # ~4.810e42 [N]

# Fundamental Planck Density (rho_Planck = c^5 / (hbar * G^2))
RHO_PLANCK = (C**5) / (HBAR * (G**2))   # ~5.155e96 [kg/m^3]


# ==============================================================================
# CORE SATURATION FORMULAS (SECTION 1)
# ==============================================================================

def calculate_normalized_density(rho: float) -> float:
    """
    Calculates the dimensionless normalized mass density D = rho / rho_Planck.
    
    Parameters:
        rho (float): Core baryonic mass density in kg/m^3.
        
    Returns:
        float: Dimensionless density D.
    """
    return rho / RHO_PLANCK


def calculate_curvature_intensity(mass: float, radius: float, angular_momentum: float = 0.0) -> float:
    """
    Computes the localized curvature intensity parameter Phi_curvature.
    
    In general relativity, geometric curvature scales as GM/(r c^2) with 
    a spin correction term for angular momentum J (Kerr contribution).
    
    Parameters:
        mass (float): Rest mass of stellar core in kg.
        radius (float): Core radial distance in meters.
        angular_momentum (float): Dynamic angular momentum J in kg m^2 / s.
        
    Returns:
        float: Dimensionless curvature intensity scalar Phi_curvature.
    """
    r_s = (2.0 * G * mass) / (C**2)  # Schwarzschild radius
    base_curvature = r_s / (2.0 * radius)
    
    # Spin-coupling factor (a_* = c J / G M^2)
    if mass > 0:
        a_star = (C * angular_momentum) / (G * (mass**2))
        spin_factor = 1.0 + (a_star**2)
    else:
        spin_factor = 1.0
        
    return base_curvature * spin_factor


def calculate_manifold_saturation(rho: float, mass: float, radius: float, angular_momentum: float = 0.0) -> float:
    """
    Computes Equation (1) from Section 1 of the paper:
        S_M = (D * Phi_curvature) / epsilon_M
        
    Evaluates the proximity of a stellar core configuration to the TOV elastic limit
    and higher-dimensional Nodal Interface (R_d) materialization.
    
    Parameters:
        rho (float): Local core mass density in kg/m^3.
        mass (float): Core mass in kg.
        radius (float): Radial distance in meters.
        angular_momentum (float): Dynamic spin J in kg m^2 / s.
        
    Returns:
        float: Manifold Saturation Metric (S_M).
    """
    d_density = calculate_normalized_density(rho)
    phi_curv = calculate_curvature_intensity(mass, radius, angular_momentum)
    
    # Dimensionless scaling factor for S_M metric response
    # Normalized against Planck energy-density elasticity threshold
    s_m = (d_density * phi_curv * (RHO_PLANCK * (C**2))) / (EPSILON_M / (radius**2))
    return s_m


def get_sm_regime(s_m: float) -> str:
    """
    Maps an S_M value to its physical regime as defined in Section 1 (Figure 3).
    
    Parameters:
        s_m (float): Computed Saturation Metric.
        
    Returns:
        str: Classification regime label.
    """
    if s_m < 0.90:
        return "Sub-Critical (S_M << 1): Stable 3D Degenerate Remnant (White Dwarf / Sub-stellar)"
    elif 0.90 <= s_m < 1.0:
        return "Pre-Critical Bottleneck (S_M -> 1^-): Active Pulsar / Magnetar Stress State"
    elif 1.0 <= s_m <= 1.1:
        return "Critical Nodal Transition (S_M = 1): R_d Interface Materialization (Black Hole)"
    else:
        return "Super-Critical Over-Saturation (S_M >> 1): Venting Jet Dynamics (Hypernova / Kilonova)"
# ==============================================================================
# SUB-CRITICAL STATES (S_M < 1) - WHITE DWARF METRIC CONTAINERS
# ==============================================================================

def calculate_wd_subcritical_metric(d_deg: float, phi_local: float) -> float:
    """
    Calculates Equation (2) for a White Dwarf sub-critical metric container:
        S_M_WD = (D_deg * Phi_local) / epsilon_M << 1
        
    Parameters:
        d_deg (float): Degenerate electron mass-density parameter (rho_deg / rho_Planck).
        phi_local (float): Localized curvature scalar for degenerate core.
        
    Returns:
        float: S_M value (strictly << 1).
    """
    s_m_wd = (d_deg * phi_local * (RHO_PLANCK * (C**2))) / EPSILON_M
    return s_m_wd


def get_higher_dimensional_flux(s_m: float) -> float:
    """
    Evaluates orthogonal higher-dimensional metric energy flux (kappa_flux).
    
    For sub-critical states (S_M < 1), no topological puncture occurs at R_d,
    resulting in zero higher-dimensional flux (kappa_flux = 0). All energy is 
    trapped within 3D spatial constraints (Metric Retentiveness).
    
    Parameters:
        s_m (float): Local saturation metric.
        
    Returns:
        float: Orthogonal energy flux vector magnitude kappa_flux [J s^-1 m^-2].
    """
    if s_m < 1.0:
        return 0.0  # Denied orthogonal flux paths (kappa_flux = 0)
    else:
        # Puncture active (S_M >= 1): Non-zero flux branch
        kappa_crit = 1e38  # Reference critical flux capacity
        return kappa_crit * (s_m - 1.0)
        # ==============================================================================
# CLASSICAL NOVAE & SURFACE SHRUGS (S_M_surface -> 1)
# ==============================================================================

def calculate_surface_shrug_metric(d_core: float, delta_d_acc: float, phi_surface: float) -> float:
    """
    Calculates Equation (3) for a Pseudo-Critical Surface Shrug in a Classical Nova:
        S_M_surface = ((D_core + delta_D_acc) * Phi_surface) / epsilon_M -> 1_surface
        
    Parameters:
        d_core (float): Base mass-density parameter of underlying WD core.
        delta_d_acc (float): Accreted surface layer density contribution.
        phi_surface (float): Curvature intensity parameter evaluated at the surface.
        
    Returns:
        float: Surface Saturation Metric (S_M_surface).
    """
    d_total = d_core + delta_d_acc
    s_m_surface = (d_total * phi_surface * (RHO_PLANCK * (C**2))) / EPSILON_M
    return s_m_surface


def check_surface_shrug_trigger(s_m_surface: float, s_m_core: float) -> dict:
    """
    Evaluates whether an accreted surface shell triggers a Surface Shrug explosion 
    while preserving underlying core structural integrity.
    
    Parameters:
        s_m_surface (float): Computed surface metric.
        s_m_core (float): Computed core metric.
        
    Returns:
        dict: Shrug status, core status, and higher-dimensional flux state.
    """
    shrug_triggered = s_m_surface >= 0.98
    core_intact = s_m_core < 0.90
    
    return {
        "shrug_triggered": shrug_triggered,
        "core_intact": core_intact,
        "kappa_flux": 0.0,  # 3D spatial container limits intact (kappa_flux = 0)
        "regime": "Pseudo-Critical Surface Shrug (RS Oph / U Sco type)" if (shrug_triggered and core_intact) else "Stable Accretion / Sub-threshold"
    }
# ==============================================================================
# TYPE IA SUPERNOVAE & GLOBAL METRIC SNAP-BACK (S_M_global -> 1)
# ==============================================================================

def calculate_type_ia_global_metric(d_uniform: float, mass_core: float, radius_core: float) -> float:
    """
    Calculates the global saturation metric S_M_global for a degenerate C-O White Dwarf
    approaching the Chandrasekhar limit (M ~ 1.44 M_sun) with a nearly uniform density profile.

    Parameters:
        d_uniform (float): Average uniform mass-density ratio (rho_avg / rho_Planck).
        mass_core (float): Stellar core mass in kg (~1.44 M_sun).
        radius_core (float): Radius of the core in meters.

    Returns:
        float: Global Saturation Metric S_M_global.
    """
    r_s = (2.0 * G * mass_core) / (C**2)
    phi_global = r_s / (2.0 * radius_core)
    s_m_global = (d_uniform * phi_global * (RHO_PLANCK * (C**2))) / (EPSILON_M / (radius_core**2))
    return s_m_global


def check_rd_stent_organization(density_gradient_scale: float) -> dict:
    """
    Evaluates whether a collapsing core can organize a localized 2D laminar boundary (R_d).

    Without a steep core-density gradient (e.g., in isotropic degenerate C-O cores),
    the core reaches S_M ~ 1 simultaneously across its volume, preventing localized
    stenting (R_d fails to organize) and forcing total 3D metric snap-back.

    Parameters:
        density_gradient_scale (float): Core density gradient scale height (d(rho)/dr).

    Returns:
        dict: Stent status, snap-back trigger state, and total energy release.
    """
    # Threshold for steep density gradient necessary to localize R_d
    steep_gradient_threshold = 1.0e-3

    if density_gradient_scale < steep_gradient_threshold:
        return {
            "rd_stent_formed": False,
            "snapback_triggered": True,
            "kappa_flux": 0.0,  # Denied 4D flux stent
            "energy_release_joules": 1.0e44,  # Total thermonuclear binding energy liberated
            "central_remnant": None,  # No core remnant left behind
            "regime": "Global Metric Snap-Back (Type Ia Supernova / SN 2011fe)"
        }
    else:
        return {
            "rd_stent_formed": True,
            "snapback_triggered": False,
            "kappa_flux": 1.0e38,
            "energy_release_joules": 0.0,
            "central_remnant": "Compact Core",
            "regime": "Localized Core Puncture"
        }

