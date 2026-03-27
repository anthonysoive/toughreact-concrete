# Cement hydration

The hydration module computes the **degree of hydration** and resulting phase assemblage (volume fractions, mineral compositions) as a function of curing time, using the **DIM-CTOA4** kinetic model.

## Supported binder types

- Portland cement (CEM I) — Bogue clinker phases: C₃S, C₂S, C₃A, C₄AF
- CEM I + fly ash
- CEM I + silica fume

## Usage

```python
import toughreact_concrete.model.data.bd_materiaux as bd_materiaux
from toughreact_concrete.materiau.hydration.calcul_hydratation import calcul_hydratation

formulation = bd_materiaux.formulation_beton['M25FA']
result = calcul_hydratation(formulation, temps_cure=28)
```

## Result dictionary

| Key | Description |
|-----|-------------|
| `alpha` | Overall hydration degree (0–1) |
| `phic` | Capillary porosity (cm³/cm³ of material) |
| `fracvol` | Volume fractions of hydration products |
| `compo` | Molar concentrations of phases (mol/cm³ of material) |

## Available mix designs

Mix designs are stored in `bd_materiaux.formulation_beton`. Keys include:
`M25`, `M25FA`, `M30FA`, `M50`, `M50FA`, `M75`, `M75SF`, `M100SF`, `M120SF`, etc.

## Side effects

`calcul_hydratation` writes two Excel files to the current working directory:
- `hydrationDIM_CTOA_in.xls` — model inputs
- `hydrationDIM_CTOA.xls` — full time series results

When using in tests or scripts, ensure the working directory is writable.
