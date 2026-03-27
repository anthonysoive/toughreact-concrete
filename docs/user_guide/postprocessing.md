# Post-processing

The `post` module parses TOUGHREACT output files into pandas DataFrames for analysis and plotting.

## Reading results

```python
from toughreact_concrete.model.post import post_toughreact

# Parse output after a completed simulation
results = post_toughreact(...)
```

Output DataFrames typically contain:

- Time steps
- Spatial profiles of saturation, pressure, temperature
- Mineral volume fractions at each time step
- Aqueous species concentrations

## Typical analysis workflow

```python
import matplotlib.pyplot as plt

# Plot chloride profile at final time step
cl_profile = results['Cl-'].iloc[-1]
plt.plot(cl_profile)
plt.xlabel('Distance from surface (m)')
plt.ylabel('[Cl⁻] (mol/L)')
plt.title('Chloride profile')
plt.show()
```

!!! note
    The exact API of `post.py` depends on the EOS mode and output file format.
    Refer to the [API reference](../api/model.md) for full details.
