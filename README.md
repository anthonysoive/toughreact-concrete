# toughreact-concrete

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Python package for simulating reactive transport and chemical durability in concrete structures using [TOUGHREACT](https://tough.lbl.gov/software/toughreact/). Includes a module for computing cement hydration (Portland cement with optional fly ash or silica fume) based on the DIM-CTOA4 kinetic model.

## Features

- **Cement hydration** — Bogue clinker calculation, fly ash and silica fume support, DIM-CTOA4 kinetics
- **Material properties** — Porosity, permeability, relative humidity (van Genuchten model), tortuosity
- **Reactive transport** — Full TOUGHREACT input generation (EOS3, EOS4, EOS9, ECO2N)
- **Boundary conditions** — Immersion, drying, tidal cycling, infinite reservoir
- **Post-processing** — TOUGHREACT output parsing to pandas DataFrames

## Installation

```bash
pip install PyTOUGH
pip install toughreact-concrete
```

### TOUGHREACT solver binaries

The TOUGHREACT solver binaries are **not included** in this package (licence restrictions). Download them from the [TOUGH portal](https://tough.lbl.gov/software/toughreact/) and place them in `toughreact_concrete/exe/` following the naming convention used in `pre.py`.

Pre-compiled binaries for Windows, macOS (Intel), and Linux are available separately upon request.

## Quick example

```python
import toughreact_concrete.model.data.bd_materiaux as bd_materiaux
from toughreact_concrete.materiau.hydration.calcul_hydratation import calcul_hydratation
from toughreact_concrete.materiau.mat_ciment import MateriauCimentaire
from toughreact_concrete.model.cond_limit import CondLimit
from toughreact_concrete.geometry_trc.constrgeom import suite_geom2

# 1. Mesh (50 mm slab, 20 elements, ratio 1.3)
elements = suite_geom2(0.05, 20, 1.3)

# 2. Cement hydration at 28 days
formulation = bd_materiaux.formulation_beton['M25FA']
result = calcul_hydratation(formulation, temps_cure=28)
print(f"Porosity: {result['phic']:.3f}  |  Hydration degree: {result['alpha']:.2f}")

# 3. Boundary condition (atmospheric drying)
bc = CondLimit('sechage', HR_ext=[65], T_ext=[20], Patm=[1.013e5])
```

## Documentation

Full documentation is available at [docs/](docs/index.md) (build locally with `mkdocs serve`).

## Citation

If you use this package in your research, please cite:

> Soive, A. (2025). *toughreact-concrete: A Python package for reactive transport
> simulation in concrete structures*. [thesis/article reference to be added]

## License

MIT — see [LICENSE](LICENSE).
