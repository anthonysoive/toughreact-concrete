#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation of seawater propagation in M70-30FA concrete
under tidal exposure conditions.
"""

from toughreact_concrete.model.simulation import run_simulation

# ── Time units ────────────────────────────────────────────────────────────────
hour = 3600.
day  = 24. * hour

# ── Parameters ────────────────────────────────────────────────────────────────
run_simulation(
    # Thermodynamic database
    database            = "Thermoddem_2023.txt",
    eos                 = 'eos9',
    pitzer              = False,

    # Geometry
    ep_struct           = 0.01,     # structural thickness (m)
    hauteur             = 1.0,      # height (m)
    n_elements          = 200,      # number of elements along X
    raison_suite        = 0.999,    # geometric-progression ratio

    # Material
    nom_beton           = 'M70-30FA',
    temps_cure          = 10000.,   # curing time (h) — full hydration
    porosite            = 0.22,     # measured porosity (-)
    D_eff               = 0.25e-12, # effective diffusion coefficient (m²/s)

    # Environmental conditions
    temperature_eau     = 20.0,     # water temperature (°C)
    humidite_relative_ext = 70,     # external relative humidity (%)
    temperature_ext     = 14,       # external atmospheric temperature (°C)
    P_atm               = 1.013e5,  # atmospheric pressure (Pa)
    Pp_co2              = 0.0,      # CO2 partial pressure (Pa)

    # Exposure geometry
    boundary_side       = 'right',  # exposed face: 'left' or 'right'
    ep_couche_limite    = 2e-5,     # boundary-layer element thickness (m)

    # Simulation duration
    temps_exposure      = 1 * hour,
    time_output         = [1 * hour],

    # Solver options
    kinetics            = True,
    update_porosity     = False,
    complexation        = True,
    dt_max              = 600.,     # maximum time step (s)
)
