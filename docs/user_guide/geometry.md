# Geometry

The `constrgeom` module generates 1D mesh element sequences using a **geometric progression**, allowing fine discretisation near boundaries where concentration gradients are steepest.

## Functions

### `suite_geom` — mesh with boundary micro-elements

```python
from toughreact_concrete.geometry_trc.constrgeom import suite_geom

elements = suite_geom(dim_struct=0.05, nElem=10, raison=1.5)
```

Produces `nElem + 2` elements. The first and last are micro-elements of 1×10⁻⁵ m used as TOUGHREACT boundary nodes. Interior elements follow a geometric sequence.

### `suite_geom2` — plain geometric sequence

```python
from toughreact_concrete.geometry_trc.constrgeom import suite_geom2

# Refinement at exposed surface (right side, sens='decroissant')
elements = suite_geom2(dim_struct=0.05, nElem=20, raison=1.3)

# Refinement at left surface
elements = suite_geom2(dim_struct=0.05, nElem=20, raison=1.3, sens='croissant')
```

## Choosing the ratio

| `raison` | Effect |
|----------|--------|
| 1.0 | Uniform mesh |
| 1.2–1.4 | Moderate grading |
| 1.5–2.0 | Strong grading (few elements) |

A ratio of **1.3** with 20 elements gives a good balance for most durability simulations over 0–10 cm slabs.
