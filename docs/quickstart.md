# Quick start

This example reproduces a typical drying simulation for a 5 cm concrete slab with a CEM I + 30% fly ash mix design (M25FA).

## 1. Initialize the working directory

```python
from toughreact_concrete.model.pre import initialize

exe = initialize(eos='eos9', database='Thermoddem_2023.txt')
```

This creates `../Calcul/`, copies the solver binary and all input templates.

## 2. Build the mesh

```python
from toughreact_concrete.geometry_trc.constrgeom import suite_geom2

# 50 mm slab, 20 elements, geometric ratio 1.3 (refined at exposed surface)
elements = suite_geom2(dim_struct=0.05, nElem=20, raison=1.3, sens='decroissant')
```

## 3. Compute cement hydration

```python
import toughreact_concrete.model.data.bd_materiaux as bd_materiaux
from toughreact_concrete.materiau.hydration.calcul_hydratation import calcul_hydratation

formulation = bd_materiaux.formulation_beton['M25FA']
hydration = calcul_hydratation(formulation, temps_cure=28)

print(f"Porosity at 28 days: {hydration['phic']:.3f}")
print(f"Hydration degree:    {hydration['alpha']:.2f}")
```

## 4. Create the material

```python
from toughreact_concrete.materiau.mat_ciment import MateriauCimentaire

mat = MateriauCimentaire('M25FA')
mat.lecture_database()
mat.hydratation(temps_cure=28)
```

## 5. Define the boundary condition

```python
from toughreact_concrete.model.cond_limit import CondLimit

bc = CondLimit(
    'sechage',
    HR_ext=[65],    # 65% relative humidity
    T_ext=[20],     # 20°C
    Patm=[1.013e5], # 1 atm
)
```

## 6. Run the solver and post-process

```python
# (requires TOUGHREACT binary — see Installation)
from toughreact_concrete.model import toughreact
from toughreact_concrete.model.post import read_results

# toughreact.run(exe, ...)
# df = read_results('output_file.out')
```

!!! note
    Steps 1 and 6 require the TOUGHREACT binary. Steps 2–5 work without it
    and can be used to inspect hydration and material properties independently.
