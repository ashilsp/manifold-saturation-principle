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
