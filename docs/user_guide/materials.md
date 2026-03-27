# Materials

## Class hierarchy

```
t2grids.rocktype  (PyTOUGH)
    └── MateriauPoreux        mat_poreux.py
            └── MateriauCimentaire   mat_ciment.py
```

## MateriauPoreux

Base class for any porous material. Provides:

- Van Genuchten relative permeability and capillary pressure models
- `HR(S_l, T)` — relative humidity from saturation via Kelvin equation
- `input_IC(eos)` — initial conditions vector for the TOUGHREACT flow file
- `write_toughreact(dat, complexation)` — write rock type to PyTOUGH data object

```python
from toughreact_concrete.materiau.mat_poreux import MateriauPoreux

mat = MateriauPoreux('ROCK1')
hr = mat.HR(S_l=0.85, T=20)   # relative humidity in %
ic = mat.input_IC('eos9')      # [P_atm]
```

## MateriauCimentaire

Extends `MateriauPoreux` with cement-specific properties. The typical usage pattern is:

```python
from toughreact_concrete.materiau.mat_ciment import MateriauCimentaire

mat = MateriauCimentaire('M25FA')
mat.lecture_database()          # load formulation and measured properties
mat.hydratation(temps_cure=28)  # compute hydration state at 28 days
```

After `hydratation()`, the following attributes are populated:

| Attribute | Description |
|-----------|-------------|
| `porosite` | Capillary porosity |
| `densite` | Dry bulk density (kg/m³) |
| `permeabilite` | Intrinsic water permeability (m²) |
| `result_hydration` | Full hydration result dict |
| `minerals` | Mineral volume fractions |
