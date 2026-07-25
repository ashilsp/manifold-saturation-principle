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

# ==============================================================================
# PULSARS & NEUTRON STARS: PRE-CRITICAL BOTTLENECK (S_M -> 1^-)
# ==============================================================================

def calculate_pulsar_bottleneck_metric(rho_core: float, mass_ns: float, radius_ns: float, spin_freq_hz: float) -> float:
    """
    Calculates the pre-critical bottleneck Saturation Metric S_M -> 1^- for a neutron star.

    Parameters:
        rho_core (float): Central nuclear mass density in kg/m^3 (~1e17 to 1e18 kg/m^3).
        mass_ns (float): Neutron star mass in kg (~1.4 to 2.1 M_sun).
        radius_ns (float): Radius of neutron star in meters (~10,000 to 12,000 m).
        spin_freq_hz (float): Rotation frequency omega_rot / (2*pi) in Hertz.

    Returns:
        float: Saturation Metric S_M (pinned just below 1.0, e.g., 0.95 - 0.99).
    """
    d_density = calculate_normalized_density(rho_core)
    
    # Calculate Kerr angular momentum J = I * omega
    inertia_moment = 0.35 * mass_ns * (radius_ns**2)  # Standard NS moment of inertia
    omega_rot = 2.0 * np.pi * spin_freq_hz
    ang_momentum = inertia_moment * omega_rot
    
    phi_curv = calculate_curvature_intensity(mass_ns, radius_ns, ang_momentum)
    s_m_raw = (d_density * phi_curv * (RHO_PLANCK * (C**2))) / (EPSILON_M / (radius_ns**2))
    
    # Pinned sub-critical asymptote S_M -> 1^- due to nuclear degeneracy pressure
    return min(s_m_raw, 0.995)


def calculate_metric_grinding_power(s_m: float, mass_ns: float, radius_ns: float, spin_freq_hz: float) -> dict:
    """
    Computes rotational kinetic energy conversion via metric grinding against the 
    stressed 3D spacetime canvas when S_M -> 1^- with zero higher-dimensional flux.

    Parameters:
        s_m (float): Local saturation metric (must be < 1.0).
        mass_ns (float): Mass in kg.
        radius_ns (float): Radius in meters.
        spin_freq_hz (float): Spin frequency in Hz.

    Returns:
        dict: Grinding torque, radiated power, magnetic surface field B, and flux status.
    """
    omega_rot = 2.0 * np.pi * spin_freq_hz
    inertia_moment = 0.35 * mass_ns * (radius_ns**2)
    e_rot = 0.5 * inertia_moment * (omega_rot**2)
    
    # Spacetime strain factor amplifies metric drag as S_M approaches 1.0
    strain_factor = 1.0 / (1.0 - min(s_m, 0.99))
    
    # Radiated spin-down power via metric grinding [Watts]
    p_grind = 1.0e24 * strain_factor * (spin_freq_hz / 30.0)**4
    
    # Effective surface magnetic field B generated by frame dragging [Tesla]
    b_effective = np.sqrt(p_grind) * 1.0e4
    
    return {
        "s_m": s_m,
        "kappa_flux": 0.0,  # Unpunctured elastic bottleneck (kappa_flux = 0)
        "rotational_e_kin_joules": e_rot,
        "grinding_power_watts": p_grind,
        "effective_b_field_tesla": b_effective,
        "regime": "Pre-Critical Metric Bottleneck (Crab Pulsar / PSR J0740+6620)"
    }
# ==============================================================================
# MAGNETARS: TORSIONAL CRISIS & TOPOLOGICAL KNOTTING (S_M ~ 1 with Extreme J)
# ==============================================================================

def calculate_magnetar_curvature_with_spin(mass_kg: float, radius_m: float, ang_momentum_j: float, alpha: float = 1.0) -> float:
    """
    Calculates the spin-enhanced curvature intensity component:
        Phi_curvature = Phi_mass + alpha * (J / (M * c))^2
    
    Parameters:
        mass_kg (float): Magnetar mass in kg.
        radius_m (float): Magnetar radius in meters.
        ang_momentum_j (float): Angular momentum J (kg m^2 / s).
        alpha (float): Coupling constant for rotational metric deformation.

    Returns:
        float: Enhanced curvature scalar Phi_curvature.
    """
    r_s = (2.0 * G * mass_kg) / (C**2)
    phi_mass = r_s / (2.0 * radius_m)
    phi_spin = alpha * ((ang_momentum_j / (mass_kg * C))**2) / (radius_m**2)
    return phi_mass + phi_spin


def calculate_manifold_torsion_and_bfield(s_m_surface: float, phi_spin: float) -> dict:
    """
    Evaluates whether extreme angular momentum prevents clean 2D R_d boundary formation,
    trapping structural shear into manifold torsion tau and generating ultra-strong 
    induction fields B proportional to tau.

    Parameters:
        s_m_surface (float): Local saturation metric at the surface.
        phi_spin (float): Rotational contribution to curvature intensity.

    Returns:
        dict: Torsion magnitude, induction B-field, R_d status, and QPO frequency modes.
    """
    # High rotational shear threshold that obstructs axisymmetric R_d formation
    torsion_threshold = 0.05

    if phi_spin >= torsion_threshold and s_m_surface >= 0.92:
        # Torsion tensor magnitude tau = |curl(e_metric)|
        tau_magnitude = phi_spin * 1.0e14  # Arbitrary unit scale for geometric twist
        b_gauss = tau_magnitude * 1.0e1    # B-field scaled to Gauss (10^14 - 10^15 Gauss)
        
        # Primary manifold viscosity reaction QPOs (e.g., 18 Hz, 29 Hz, 92.5 Hz, 625 Hz for SGR 1806-20)
        qpo_modes_hz = [18.0, 29.0, 92.5, 625.0]
        
        return {
            "rd_formed": False,
            "torsional_crisis": True,
            "manifold_torsion_tau": tau_magnitude,
            "magnetic_field_gauss": b_gauss,
            "qpo_frequencies_hz": qpo_modes_hz,
            "starquake_flare_energy_joules": 1.0e39,
            "regime": "Torsional Crisis / Topological Knotting (SGR 1806-20)"
        }
    else:
        return {
            "rd_formed": True,
            "torsional_crisis": False,
            "manifold_torsion_tau": 0.0,
            "magnetic_field_gauss": 1.0e12,
            "qpo_frequencies_hz": [],
            "starquake_flare_energy_joules": 0.0,
            "regime": "Standard Sub-Critical Remnant"
        }
        # ==============================================================================
# CORE-COLLAPSE REJECTION & TOPOLOGICAL FAILURE MODES (Type II Supernovae)
# ==============================================================================

def check_core_collapse_rejection(s_m_core: float, entropy_per_baryon: float, asymmetry_factor: float) -> dict:
    """
    Evaluates whether a collapsing massive star core (S_M_core -> 1) achieves a coherent 
    2D laminar boundary (R_d) or suffers an entropic/turbulent topological rejection.

    Parameters:
        s_m_core (float): Local core metric saturation value.
        entropy_per_baryon (float): Entropy scale S/k_B (high entropy drives turbulence).
        asymmetry_factor (float): Hydrodynamic/rotational asymmetry index [0.0 to 1.0].

    Returns:
        dict: Phase transition outcome, shock rebound energy, and remnant classification.
    """
    # Threshold for turbulence/entropy preventing coherent R_d stenting
    turbulence_index = entropy_per_baryon * (1.0 + asymmetry_factor)
    critical_turbulence_limit = 4.0

    if s_m_core >= 0.95 and turbulence_index > critical_turbulence_limit:
        return {
            "rd_stent_formed": False,
            "topological_rejection": True,
            "kappa_flux": 0.0,  # 4D conduit denied
            "shock_rebound_kinetic_energy_joules": 1.5e44,  # Rebound kinetic shock in 3D
            "ejecta_asymmetry_index": asymmetry_factor * 2.5,
            "remnant_type": "Neutron Star / Pulsar",
            "regime": "Core-Collapse Rejection (Type II Supernova / Cassiopeia A)"
        }
    else:
        return {
            "rd_stent_formed": True,
            "topological_rejection": False,
            "kappa_flux": 1.0e39,
            "shock_rebound_kinetic_energy_joules": 0.0,
            "ejecta_asymmetry_index": 0.1,
            "remnant_type": "Stellar Mass Black Hole",
            "regime": "Successful 4D OCM Ignition"
        }


def get_topological_rejection_taxonomy() -> list:
    """
    Returns the comprehensive taxonomy table of topological rejections at the metric boundary.
    
    Returns:
        list of dicts: Metric failure regimes, initial states, mechanisms, and remnants.
    """
    return [
        {
            "event_type": "Recurrent Nova",
            "initial_state": "S_M^core << 1, S_M^surf -> 1",
            "mechanism": "Localized Surface Shrug",
            "remnant": "Intact Degenerate Core"
        },
        {
            "event_type": "Type Ia Supernova",
            "initial_state": "S_M^global -> 1",
            "mechanism": "Uniform Volume Snap-Back",
            "remnant": "Total Progenitor Disruption"
        },
        {
            "event_type": "Type II Supernova",
            "initial_state": "S_M^core -> 1",
            "mechanism": "Turbulent Core Rejection",
            "remnant": "Neutron Star / Pulsar"
        },
        {
            "event_type": "Magnetar Starquake",
            "initial_state": "S_M ~ 1",
            "mechanism": "Torsional Metric Knotting",
            "remnant": "Highly Magnetized Remnant"
        }
    ]
# ==============================================================================
# CRITICAL & SUPER-CRITICAL IGNITIONS (S_M >= 1): NODAL MATURITY & SINGULARITY REGULARIZATION
# ==============================================================================

def calculate_regularized_laminar_radius(mass_kg: float, kappa_flux: float, kappa_crit: float = 1.0e39) -> float:
    """
    Calculates the finite, regularized 2D laminar boundary radius R_d:
        R_d = (2 * G * M / c^2) * [1 + sqrt(1 - kappa_flux / kappa_crit)]

    Parameters:
        mass_kg (float): Node mass in kg.
        kappa_flux (float): Higher-dimensional energy flux rate (W or kg/s equivalent).
        kappa_crit (float): Critical flux capacity threshold.

    Returns:
        float: Regularized radius R_d in meters (prevents non-physical r -> 0 singularity).
    """
    r_s = (2.0 * G * mass_kg) / (C**2)
    flux_ratio = min(max(kappa_flux / kappa_crit, 0.0), 1.0)
    r_d = r_s * (1.0 + np.sqrt(1.0 - flux_ratio))
    return r_d


def calculate_stellar_birth_cry_luminosity(mass_kg: float, kappa_flux: float) -> dict:
    """
    Computes the hard X-ray / Gamma-ray 'Stellar Birth Cry' energy yield upon 
    initial materialization and activation of the 4D orthogonal conduit.

    Parameters:
        mass_kg (float): Stellar-mass node mass in kg (~3 to 20 M_sun).
        kappa_flux (float): Orthogonal flux rate.

    Returns:
        dict: Birth Cry peak luminosity, regularized radius, and empirical status.
    """
    m_sun_units = mass_kg / SOLAR_MASS
    r_d = calculate_regularized_laminar_radius(mass_kg, kappa_flux)
    
    # Peak hard X-ray / Gamma-ray burst power [Watts]
    p_birth_cry = 1.0e38 * (m_sun_units / 10.0) * (kappa_flux / 1.0e39)
    
    return {
        "s_m": 1.0,
        "singularity_regularized": True,
        "regularized_radius_m": r_d,
        "kappa_flux": kappa_flux,
        "birth_cry_luminosity_watts": p_birth_cry,
        "regime": "Super-Critical Nodal Maturity (Cygnus X-1 / M33 X-7)"
    }
# ==============================================================================
# KILONOVAE & COMPACT BINARY MERGERS: MANIFOLD SPLICING (S_M^composite > 1)
# ==============================================================================

def calculate_manifold_splicing_metrics(mass1_ns: float, mass2_ns: float, ejecta_velocity_c: float = 0.2) -> dict:
    """
    Computes curvature fusion, lateral un-stented ejecta mass, and r-process 
    heavy element yield during binary neutron star manifold splicing.

    Parameters:
        mass1_ns (float): Primary NS mass in kg (~1.3 to 1.6 M_sun).
        mass2_ns (float): Secondary NS mass in kg (~1.2 to 1.4 M_sun).
        ejecta_velocity_c (float): Ejecta velocity as a fraction of c (~0.1c to 0.3c).

    Returns:
        dict: Composite S_M, dynamic ejecta mass, r-process yield, and relaxation timescale.
    """
    total_mass_kg = mass1_ns + mass2_ns
    total_m_sun = total_mass_kg / SOLAR_MASS
    
    # Composite saturation spikes super-critically upon contact
    s_m_composite = 1.05 + 0.1 * (total_m_sun - 2.7)
    
    # Lateral un-stented dynamic ejecta mass [Solar Masses]
    m_ejecta_msun = 0.01 + 0.03 * (ejecta_velocity_c / 0.2) * (total_m_sun / 2.7)
    m_ejecta_kg = m_ejecta_msun * SOLAR_MASS
    
    # Heavy element r-process yield (Gold, Platinum, Uranium) [kg]
    r_process_yield_kg = m_ejecta_kg * 0.05
    
    # Manifold relaxation timescale into single R_d node [seconds]
    relaxation_time_s = 50.0 * (2.7 / total_m_sun)

    return {
        "s_m_composite": s_m_composite,
        "manifold_spliced": True,
        "ejecta_mass_msun": m_ejecta_msun,
        "r_process_yield_kg": r_process_yield_kg,
        "relaxation_timescale_s": relaxation_time_s,
        "regime": "Manifold Splicing Kilonova (GW170817 / AT2017gfo)"
    }

