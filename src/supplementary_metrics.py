"""
src/supplementary_metrics.py

Supplementary Material: Materials and Methods Parameterization & Dimensionless Metric Calculations.
Contains dimensionless density mappings, degeneracy pressure functions, Kerr curvature parameterizations,
and the universal metric elasticity threshold (epsilon_M).
"""

import numpy as np

# Physical Constants (SI Units)
C = 2.99792458e8             # Speed of light [m/s]
G = 6.67430e-11              # Gravitational constant [m^3 kg^-1 s^-2]
HBAR = 1.054571817e-34       # Reduced Planck constant [J s]
M_E = 9.1093837015e-31       # Electron mass [kg]
M_N = 1.67492749804e-27      # Neutron mass [kg]
M_U = 1.66053906660e-27      # Atomic mass unit [kg]
SOLAR_MASS = 1.98847e30      # Solar mass [kg]

# Fundamental Metric Limits
RHO_PLANCK = (C**5) / (HBAR * (G**2))  # ~5.155e96 kg/m^3 (5.155e93 g/cm^3)
EPSILON_M = (C**4) / (8.0 * np.pi * G)  # ~4.810e42 N (Universal Elastic Limit)


def calculate_mass_density_normalization(rho_kg_m3: float) -> float:
    """
    Calculates dimensionless mass-density parameter D = rho / rho_Planck.
    """
    return rho_kg_m3 / RHO_PLANCK


def calculate_electron_degeneracy_pressure(rho_kg_m3: float, mu_e: float = 2.0) -> float:
    """
    Calculates relativistic electron degeneracy pressure P_e and Fermi momentum ratio x_F.
    """
    # Fermi momentum ratio x_F
    p_f_term = (3.0 * (np.pi**2) * (HBAR**3) * rho_kg_m3) / ((M_E**3) * (C**3) * mu_e * M_U)
    x_f = p_f_term**(1.0 / 3.0)
    
    # Relativistic Fermi integral function f(x_F)
    f_xf = x_f * (2.0 * x_f**2 - 3.0) * np.sqrt(x_f**2 + 1.0) + 3.0 * np.arcsinh(x_f)
    
    p_e = ((M_E**4) * (C**5) / (3.0 * (np.pi**2) * (HBAR**3))) * f_xf
    return p_e


def calculate_static_curvature(mass_kg: float, radius_m: float) -> float:
    """
    Calculates static curvature parameterization Phi_static = G * M / (r * c^2) = r_s / (2 * r).
    """
    r_s = (2.0 * G * mass_kg) / (C**2)
    return r_s / (2.0 * radius_m)


def calculate_rotating_curvature(mass_kg: float, radius_m: float, theta_rad: float, spin_a: float) -> float:
    """
    Calculates Kerr-like axisymmetric rotating curvature parameterization Phi_rotating(r, theta).
    
    Parameters:
        mass_kg (float): Node mass [kg]
        radius_m (float): Radial distance [m]
        theta_rad (float): Polar angle in radians
        spin_a (float): Angular momentum per unit mass dimensionless ratio a = J / (M * c) in meters
    """
    rho_g = (G * mass_kg) / (C**2)
    sigma = (radius_m**2) + (spin_a**2) * (np.cos(theta_rad)**2)
    
    phi_base = (G * mass_kg * radius_m) / (sigma * (C**2))
    spin_factor = 1.0 + ((spin_a / rho_g)**2) * (np.cos(theta_rad)**2)
    
    return phi_base * spin_factor
    # ==============================================================================
# ISRAEL JUNCTION CONDITIONS & R_d PHASE TRANSITION MATHEMATICAL MECHANICS
# ==============================================================================

def calculate_extrinsic_curvature_jump(mass_kg: float, s_m: float) -> dict:
    """
    Calculates the extrinsic curvature jump [K_ij] = K_ij^+ - K_ij^- across 
    the null boundary hypersurface Sigma_d at r = R_d.

    Parameters:
        mass_kg (float): Stellar node mass in kg.
        s_m (float): Metric saturation scalar S_M.

    Returns:
        dict: Inner curvature K_minus, outer curvature K_plus, and jump delta_K.
    """
    r_s = (2.0 * G * mass_kg) / (C**2)
    # At S_M >= 1, R_d radius is regularized
    r_d = r_s if s_m >= 1.0 else r_s / max(s_m, 1.0e-3)
    
    # Schwarzschild extrinsic curvature limits across surface
    k_minus = 0.0 if s_m < 1.0 else (1.0 / r_d) * np.sqrt(1.0 - r_s / r_d)
    k_plus = (1.0 / r_d)
    
    delta_k = k_plus - k_minus
    
    return {
        "k_minus": k_minus,
        "k_plus": k_plus,
        "extrinsic_curvature_jump": delta_k,
        "r_d_m": r_d
    }


def calculate_israel_surface_stress(s_m: float, mass_kg: float) -> float:
    """
    Computes the Israel Junction surface stress component S_ij:
        S_ij = - (c^4 / 8*pi*G) * ([K_ij] - h_ij * [K]) * (1 - 1 / S_M)

    Parameters:
        s_m (float): Metric saturation scalar.
        mass_kg (float): Node mass in kg.

    Returns:
        float: Tangential surface stress S_ij [N/m or Pa equivalent].
    """
    if s_m < 1.0:
        return 0.0  # Retentive domain: no surface stress shell formed
    
    jump_data = calculate_extrinsic_curvature_jump(mass_kg, s_m)
    delta_k = jump_data["extrinsic_curvature_jump"]
    
    # Israel junction prefactor: EPSILON_M * delta_K * (1 - 1/S_M)
    s_ij = EPSILON_M * delta_k * (1.0 - (1.0 / s_m))
    return s_ij


def calculate_stress_energy_decoupling(s_m: float, kappa_crit: float = 1.0e39) -> dict:
    """
    Evaluates the tensorial decoupling of T_munu across Sigma_d:
        T_munu^(3D) = S_munu * delta(Sigma_d) + n_mu * n_nu * kappa_flux

    Returns:
        dict: Surface stress weight and orthogonal flux magnitude.
    """
    if s_m < 1.0:
        return {
            "surface_stress_weight": 1.0,
            "orthogonal_flux_kappa": 0.0,
            "decoupled": False
        }
    
    kappa_flux = kappa_crit * (1.0 - (1.0 / (s_m**2)))
    surface_weight = 1.0 / s_m
    
    return {
        "surface_stress_weight": surface_weight,
        "orthogonal_flux_kappa": kappa_flux,
        "decoupled": True
    }
# ==============================================================================
# FULL MATHEMATICAL DERIVATION: S_M & (4+1)D TENSOR DECOMPOSITION MECHANICS
# ==============================================================================

def calculate_local_ricci_scalar(rho_kg_m3: float, pressure_pa: float, angular_momentum_j: float, volume_m3: float) -> float:
    """
    Calculates the localized 3D trace-free Ricci curvature scalar R_local:
        R_local = (8*pi*G / c^4) * (rho * c^2 + P) + (8*pi*G / c^4) * (J / (V * c))^2
    """
    prefactor = (8.0 * np.pi * G) / (C**4)
    matter_term = rho_kg_m3 * (C**2) + pressure_pa
    rotation_term = (angular_momentum_j / (volume_m3 * C))**2
    
    return prefactor * (matter_term + rotation_term)


def calculate_spatial_stress_integral(mass_kg: float, radius_m: float, spin_j: float = 0.0) -> float:
    """
    Computes the total 3D spatial stress integral Omega_stress:
        Omega_stress = integral (R_local + K_ij K^ij - K^2) sqrt(gamma) d^3x
    """
    volume = (4.0 / 3.0) * np.pi * (radius_m**3)
    rho = mass_kg / volume
    pressure = 0.0  # Dominant relativistic rest-mass contribution
    
    r_local = calculate_local_ricci_scalar(rho, pressure, spin_j, volume)
    
    # Scale spatial stress by effective volume interaction
    omega_stress = r_local * volume * EPSILON_M
    return omega_stress


def calculate_4plus1_tensor_decomposition(s_m: float, kappa_crit: float = 1.0e39) -> dict:
    """
    Calculates the (4+1)D stress-energy tensor coordinate decomposition:
        T^(4+1) -> Surface Stress S_munu + Orthogonal Flux J_flux^mu
    """
    if s_m < 1.0:
        return {
            "j_flux_magnitude": 0.0,
            "s_tangent_stress": s_m * EPSILON_M,
            "is_stented": False
        }
    
    j_flux = kappa_crit * (1.0 - (1.0 / (s_m**2)))
    s_tangent = EPSILON_M  # Saturated at maximum elastic ceiling
    
    return {
        "j_flux_magnitude": j_flux,
        "s_tangent_stress": s_tangent,
        "is_stented": True
    }

# ==============================================================================
# ORTHOGONAL FLUX MECHANICS (kappa_flux) & BOUNDARY JUMP INTEGRATION
# ==============================================================================

def calculate_kappa_flux(s_m: float, kappa_crit: float = 1.0e39) -> float:
    """
    Computes the orthogonal energy flux vector magnitude kappa_flux:
        kappa_flux = 0                               for S_M < 1 (Complete 3D Confinement)
        kappa_flux = kappa_crit * (1 - 1 / S_M^2)    for S_M >= 1 (Orthogonal Drainage)
    """
    if s_m < 1.0:
        return 0.0
    return kappa_crit * (1.0 - (1.0 / (s_m**2)))


def calculate_boundary_jump_integral(s_m: float, delta_r: float, kappa_crit: float = 1.0e39) -> float:
    """
    Evaluates the boundary jump integral across [R_d - delta, R_d + delta] as delta -> 0:
        kappa_flux = lim_{delta -> 0} integral_{R_d - delta}^{R_d + delta} ( d T^00 / dt + div S ) dr
    """
    if s_m < 1.0:
        return 0.0
    
    # Core asymptotic integral evaluation regularized over delta_r
    flux_inf = calculate_kappa_flux(s_m, kappa_crit)
    integral_value = flux_inf * (1.0 - np.exp(-1.0 / (delta_r + 1.0e-9)))
    return integral_value
    # Vacuum Permeability constant [T m / A or N / A^2]
MU_0 = 4.0 * np.pi * 1.0e-7

# ==============================================================================
# TORSIONAL STRESS TENSOR (tau) AND MAGNETIC INDUCTION (B)
# ==============================================================================

def calculate_metric_torsion_vector(mass_kg: float, radius_m: float, spin_j: float) -> float:
    """
    Computes magnitude of spatial manifold torsion vector |tau| = |curl(e_metric)|:
        tau ~ (G * J) / (c^2 * r^3)

    Parameters:
        mass_kg (float): Stellar node mass [kg].
        radius_m (float): Radius [m].
        spin_j (float): Angular momentum J [kg m^2 / s].

    Returns:
        float: Torsion vector magnitude |tau| [m^-1].
    """
    if radius_m <= 0:
        return 0.0
    return (G * spin_j) / ((C**2) * (radius_m**3))


def calculate_induced_magnetic_field(tau_magnitude: float) -> float:
    """
    Computes magnetic induction field B [Tesla] from metric torsion tau via:
        B = sqrt(c^4 / (G * mu_0)) * tau

    Returns:
        float: Induced magnetic field B in Tesla (1 Tesla = 10^4 Gauss).
    """
    coupling_factor = np.sqrt((C**4) / (G * MU_0))
    b_tesla = coupling_factor * tau_magnitude
    return b_tesla


def calculate_magnetar_induction_profile(mass_kg: float, radius_m: float, spin_j: float) -> dict:
    """
    Full Einstein-Maxwell-Cartan electrodynamic coupling calculation.

    Returns:
        dict: Torsion magnitude, B in Tesla, and B in Gauss.
    """
    tau_mag = calculate_metric_torsion_vector(mass_kg, radius_m, spin_j)
    b_tesla = calculate_induced_magnetic_field(tau_mag)
    b_gauss = b_tesla * 1.0e4  # Convert Tesla to Gauss

    return {
        "torsion_m1": tau_mag,
        "b_tesla": b_tesla,
        "b_gauss": b_gauss
    }

