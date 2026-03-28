"""
High-level entry point for TOUGHREACT concrete simulations.

Typical usage::

    from toughreact_concrete.model.simulation import run_simulation

    heure = 3600.
    run_simulation(
        nom_beton='M70-30FA',
        ep_struct=0.01,
        temps_exposure=1 * heure,
        time_output=[1 * heure],
    )
"""

from toughreact_concrete.geometry_trc.constrgeom import suite_geom2
from toughreact_concrete.materiau.mat_ciment import MateriauCimentaire
from toughreact_concrete.model import cond_limit, element_struct, pre
from toughreact_concrete.model.data.bd_materiaux import (
    formulation_beton,
    indicateurs_deduits,
)
from toughreact_concrete.model.data.bd_solutions import bnd_solution


def run_simulation(
    # ── Thermodynamic database ──────────────────────────────────────────────
    database="Thermoddem_2023.txt",
    eos="eos9",
    pitzer=False,
    # ── Geometry ────────────────────────────────────────────────────────────
    ep_struct=0.01,       # structural thickness (m)
    hauteur=1.0,          # height (m)
    n_elements=200,       # number of elements along X
    raison_suite=0.999,   # geometric-progression ratio (<1 refines near exposed face)
    # ── Material ────────────────────────────────────────────────────────────
    nom_beton="M70-30FA",
    temps_cure=10000.0,   # curing time (h); large value ≈ full hydration
    porosite=0.22,        # measured capillary porosity (-)
    D_eff=0.25e-12,       # effective diffusion coefficient (m²/s)
    # ── Environmental conditions ────────────────────────────────────────────
    temperature_eau=20.0,         # water temperature (°C)
    humidite_relative_ext=70,     # external relative humidity (%)
    temperature_ext=14,           # external atmospheric temperature (°C)
    P_atm=1.013e5,                # atmospheric pressure (Pa)
    Pp_co2=0.0,                   # CO₂ partial pressure (Pa)
    boundary_solution=None,       # None → use database default from bd_solutions
    # ── Exposure geometry ───────────────────────────────────────────────────
    boundary_side="right",        # exposed face: 'left' or 'right'
    ep_couche_limite=2e-5,        # boundary-layer element thickness (m)
    hauteur_maree=10,             # tidal height (cm)
    # ── Simulation timing ───────────────────────────────────────────────────
    temps_exposure=3600.0,        # total exposure duration (s)
    time_output=None,             # output times (s); defaults to [temps_exposure]
    frequence=1.0,
    # ── Solver options ──────────────────────────────────────────────────────
    kinetics=True,
    update_porosity=False,
    complexation=True,
    dt_max=600.0,                 # maximum time step (s)
):
    """Run a TOUGHREACT tidal-exposure simulation on a concrete specimen.

    Parameters
    ----------
    database : str
        Name of the thermodynamic database file.
    eos : str
        TOUGHREACT EOS module (``'eos9'``, ``'eos3'``, ``'eos4'``, ``'eco2n'``).
    pitzer : bool
        Use Pitzer activity model.
    ep_struct : float
        Thickness of the structural domain (m).
    hauteur : float
        Height of the specimen (m).
    n_elements : int
        Number of finite elements along X.
    raison_suite : float
        Common ratio of the geometric-progression mesh.
    nom_beton : str
        Concrete mix name (must exist in ``bd_materiaux.formulation_beton``).
    temps_cure : float
        Curing time for the hydration model (h).
    porosite : float
        Measured capillary porosity (-).
    D_eff : float
        Effective diffusion coefficient (m²/s).
    temperature_eau : float
        Temperature of the boundary water (°C).
    humidite_relative_ext : float
        External relative humidity during the dry phase (%).
    temperature_ext : float
        External atmospheric temperature (°C).
    P_atm : float
        Atmospheric pressure (Pa).
    Pp_co2 : float
        CO₂ partial pressure (Pa).
    boundary_solution : list[dict] or None
        Chemical composition of the boundary solution.  ``None`` uses the
        default for *database* from ``bd_solutions``.
    boundary_side : str
        Face exposed to boundary: ``'left'`` or ``'right'``.
    ep_couche_limite : float
        Boundary-layer element thickness (m).
    hauteur_maree : int or float
        Tidal height passed to the tidal boundary condition (cm).
    temps_exposure : float
        Total simulation duration (s).
    time_output : list[float] or None
        Times at which TOUGHREACT writes output (s).  Defaults to
        ``[temps_exposure]``.
    frequence : float
        Output frequency multiplier forwarded to ``Model.solve``.
    kinetics : bool
        Activate mineral kinetics.
    update_porosity : bool
        Update porosity as minerals precipitate/dissolve.
    complexation : bool
        Activate aqueous complexation.
    dt_max : float
        Maximum time step (s).
    """

    # ── Defaults ─────────────────────────────────────────────────────────────
    if time_output is None:
        time_output = [temps_exposure]
    if boundary_solution is None:
        boundary_solution = bnd_solution[database]

    # ── Initialise solver binary ──────────────────────────────────────────────
    toughreact_exe = pre.initialize(eos, database, pitzer)

    # ── Geometry ──────────────────────────────────────────────────────────────
    P2 = [0.0, 0.0, 0.0]
    P3 = [ep_struct, 0.0, 0.0]

    points_elem_struct = {
        "Y": [1.0],
        "X": suite_geom2(ep_struct, n_elements, raison_suite, sens="croissant"),
        "Z": [hauteur],
    }
    geom = [{"name": "struct", "points": [P2, P3], "elements": points_elem_struct}]
    CL = {"maree": [boundary_side]}

    # ── Material and hydration ────────────────────────────────────────────────
    materiau = MateriauCimentaire(nom_beton)
    materiau.formulation = formulation_beton[nom_beton]
    materiau.porosite = porosite
    materiau.D_eff = D_eff
    materiau.indicateurs_deduits = indicateurs_deduits[nom_beton]
    materiau.database = database
    materiau.hydratation(temps_cure)
    print("Minerals:", materiau.minerals)

    # ── Tidal boundary condition ──────────────────────────────────────────────
    chargement_marnage = [[temps_exposure], [hauteur_maree]]

    cond_enviro = {
        "HR_ext": [humidite_relative_ext],
        "T_ext": [temperature_ext],
        "T_eau": [temperature_eau],
        "Patm": [P_atm],
        "Bnd_solution": boundary_solution,
        "Pp_co2": Pp_co2,
    }

    # ── Model assembly ────────────────────────────────────────────────────────
    m = element_struct.Mesh(geom, CL, ep_couche_limite)
    m.construct_mesh(geom)
    struct = element_struct.Model(m)

    struct.eos = eos
    if eos == "eos9":
        print("Calcul isotherme")
        struct.temperature_isotherme = temperature_eau

    struct.pitzer = pitzer
    struct.kinetics = kinetics
    struct.update_porosity = update_porosity
    struct.complexation = complexation
    struct.pas_temps_calcul = dt_max
    struct.database = "baseQuan_pitzer.dat" if pitzer else database
    struct.database_phreeqc = "thermoddem.dat"

    struct.add_material(materiau, complexation)
    CL_maree = cond_limit.CondLimit("maree", chargement_marnage, **cond_enviro)
    struct.add_bc(CL_maree, CL["maree"])

    # ── Solve ─────────────────────────────────────────────────────────────────
    struct.solve(chargement_marnage, [time_output], frequence, toughreact_exe)
