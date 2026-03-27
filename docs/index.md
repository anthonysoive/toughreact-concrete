# toughreact-concrete

Python package for simulating **reactive transport and chemical durability** in concrete structures using TOUGHREACT.

## Overview

`toughreact-concrete` automates the construction of TOUGHREACT input files for concrete durability simulations. It covers the full workflow:

```
pre.py          → initialize working directory (binary + templates)
constrgeom.py   → 1D mesh generation (geometric progression)
calcul_hydratation.py → cement hydration (DIM-CTOA4 model)
mat_ciment.py / mat_poreux.py → material properties
cond_limit.py   → boundary conditions
toughreact.py   → run TOUGHREACT solver
post.py         → parse results to DataFrames
```

## Physical models

| Module | Model |
|--------|-------|
| Hydration kinetics | DIM-CTOA4 (Baroghel-Bouny et al.) |
| Relative permeability | van Genuchten |
| Capillary pressure | van Genuchten |
| Relative humidity | Kelvin equation |
| Species activity | TOUGHREACT built-in (Pitzer optional) |

## Supported exposure conditions

- Atmospheric drying (`sechage`)
- Full immersion (`mouillage`)
- Tidal cycling (`maree`)
- Infinite reservoir (`infini`)

## Thermodynamic databases

- THERMODDEM 2023 (BRGM)
- CEMDATA18
