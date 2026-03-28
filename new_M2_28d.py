#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation de propagation d'eau de mer dans le béton M70-30FA
sous conditions de marnage.
"""

from toughreact_concrete.model.simulation import run_simulation

# ── Unités ───────────────────────────────────────────────────────────────────
heure = 3600.
jour  = 24. * heure

# ── Paramètres ───────────────────────────────────────────────────────────────
run_simulation(
    # Base de données thermodynamique
    database            = "Thermoddem_2023.txt",
    eos                 = 'eos9',
    pitzer              = False,

    # Géométrie
    ep_struct           = 0.01,     # épaisseur de la structure (m)
    hauteur             = 1.0,      # hauteur (m)
    n_elements          = 200,      # nombre d'éléments selon X
    raison_suite        = 0.999,    # raison de la suite géométrique

    # Matériau
    nom_beton           = 'M70-30FA',
    temps_cure          = 10000.,   # temps de cure (h) — hydratation complète
    porosite            = 0.22,     # porosité mesurée (-)
    D_eff               = 0.25e-12, # coefficient de diffusion effectif (m²/s)

    # Conditions environnementales
    temperature_eau     = 20.0,     # température de l'eau (°C)
    humidite_relative_ext = 70,     # humidité relative extérieure (%)
    temperature_ext     = 14,       # température atmosphérique (°C)
    P_atm               = 1.013e5,  # pression atmosphérique (Pa)
    Pp_co2              = 0.0,      # pression partielle CO₂ (Pa)

    # Géométrie d'exposition
    boundary_side       = 'right',  # face exposée : 'left' ou 'right'
    ep_couche_limite    = 2e-5,     # épaisseur de la couche limite (m)

    # Durée de simulation
    temps_exposure      = 1 * heure,
    time_output         = [1 * heure],

    # Options solveur
    kinetics            = True,
    update_porosity     = False,
    complexation        = True,
    dt_max              = 600.,     # pas de temps maximum (s)
)
