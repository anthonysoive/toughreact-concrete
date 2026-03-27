"""
Physical and thermodynamic constants used throughout toughreact_concrete.

Constants
---------
rho_wl : float
    Density of liquid water, 1000 kg/m³.
R : float
    Ideal gas constant, 8.314 J/mol/K.
M_w : float
    Molar mass of water, 0.01802 kg/mol.
D_cl_water : float
    Diffusion coefficient of chloride ions in water, 1.710e-9 m²/s.
D_water : float
    Average diffusion coefficient of ions in water, 4.500e-9 m²/s.
D_air_gaz : float
    Diffusion coefficient of air in gas phase, 0.217e-4 m²/s.
D_air_eau : float
    Diffusion coefficient of air in liquid water, 1.71e-9 m²/s.
Psat : callable
    Saturated vapour pressure as a function of temperature (K); see function below.
rho_C : float
    Density of cement, 2950 kg/m³.
Dv : float
    Water vapour diffusion coefficient in air, 2.2e-5 m²/s.
C_L_v : float
    Latent heat of vaporisation, 2.4e6 J/kg.
min_spec_cement : dict
    Molar masses (g/mol), densities (g/cm³), and molar volumes (cm³/mol)
    for the main cement mineral phases.
"""
import math

# Density of liquid water (kg/m³)
rho_wl = 1000
# Ideal gas constant (J/mol/K)
R = 8.314
# Molar mass of water (kg/mol)
M_w = 0.01802
# Diffusion coefficient of chloride ions in water (m²/s)
D_cl_water = 1.710e-09
# Average diffusion coefficient of ions in water (m²/s)
D_water = 4.50017e-09
# Diffusion coefficients of air in gas phase and liquid water, respectively (m²/s)
D_air_gaz, D_air_eau = 0.217e-4, 1.71e-9
# Density of cement (kg/m³)
rho_C = 2950.
# Water vapour diffusion coefficient in air (m²/s)
Dv = 2.2e-5
# Latent heat of vaporisation (J/kg)
C_L_v = 2.4e6

# Molar masses (g/mol), densities (g/cm³), and molar volumes (cm³/mol)
# for main cement mineral phases
min_spec_cement = {}
min_spec_cement['C3S'] = {'M':236.33,'rho':3.13,'v':75.51}
min_spec_cement['C2S'] = {'M':176.25,'rho':3.28,'v':53.73}
min_spec_cement['C3A'] = {'M':270.20,'rho':3.03,'v':89.17}
min_spec_cement['C4AF'] = {'M':485.97,'rho':3.73,'v':130.29}
min_spec_cement['Hemihydrate'] = {'M':173.16,'rho':2.74,'v':63.20}
min_spec_cement['Gypsum'] = {'M':200.26,'rho':2.32,'v':86.28}
min_spec_cement['Portlandite'] = {'M':74.08,'rho':2.23,'v':33.21}
min_spec_cement['C3S2H3'] = {'M':342.40,'rho':2.63,'v':130.19}
min_spec_cement['Ettringite'] = {'M':1338.69,'rho':1.78,'v':752.07}
min_spec_cement['Monosulfoaluminate'] = {'M':650.36,'rho':2.02,'v':321.96}
min_spec_cement['FH3'] = {'M':213.69,'rho':2.20,'v':97.13}
min_spec_cement['C3AH6'] = {'M':378.19,'rho':2.52,'v':150.10}
min_spec_cement['CSH_1.6'] = {'M':196.50,'rho':2.23,'v':88.10}


def Psat(T: float) -> float:
    """Compute the saturated vapour pressure at temperature T.

    Uses the Clausius-Clapeyron equation referenced to the boiling point
    of water at 1 atm.

    Parameters
    ----------
    T : float
        Absolute temperature (K).

    Returns
    -------
    float
        Saturated vapour pressure (Pa).

    Examples
    --------
    >>> abs(Psat(373.15) - 101325) < 500   # ~1 atm at boiling point
    True
    >>> abs(Psat(273.15) - 611) < 50       # ~triple point
    True
    """
    Psat_0 = 101500.
    T_0 = 373.
    return Psat_0 * math.exp(C_L_v * M_w/R*(1/T_0 - 1/T))
