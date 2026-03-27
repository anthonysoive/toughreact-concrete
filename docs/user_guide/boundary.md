# Boundary conditions

The `CondLimit` class defines the exposure conditions applied at the concrete surface. The type is selected at instantiation and dispatched to a dedicated sub-initialiser.

## Atmospheric drying

```python
from toughreact_concrete.model.cond_limit import CondLimit

bc = CondLimit(
    'sechage',
    HR_ext=[65],        # relative humidity (%)
    T_ext=[20],         # temperature (°C)
    Patm=[1.013e5],     # atmospheric pressure (Pa)
)
```

Optional: `Pp_co2` (CO₂ partial pressure in Pa) for carbonation simulations.

## Full immersion

```python
bc = CondLimit(
    'mouillage',
    T_eau=[15],
    Bnd_solution={'composition': {'ca+2': 0.001, 'cl-': 0.5}},
)
```

## Tidal cycling

```python
from toughreact_concrete.model.data.maree import lecture_maree

nb_jours = 30
increments, heights = lecture_maree(nb_jours)

bc = CondLimit(
    'maree',
    [increments, heights],
    HR_ext=[65],
    T_ext=[20],
    T_eau=[15],
    Patm=[1.013e5],
    Bnd_solution=[{'composition': {}}],
)
```

Single-value lists are broadcast to the length of the tidal time series.

## Infinite reservoir

```python
bc = CondLimit('infini')
```

No boundary flux — used for symmetric or semi-infinite problems.
