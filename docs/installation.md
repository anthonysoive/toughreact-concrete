# Installation

## Requirements

- Python 3.11+
- [PyTOUGH](https://github.com/acroucher/PyTOUGH) v1.6.5+

## Install the package

```bash
pip install PyTOUGH
pip install toughreact-concrete
```

## Install for development

```bash
git clone https://github.com/anthonysoive/toughreact-concrete.git
cd toughreact-concrete
pip install -e ".[dev]"
```

## TOUGHREACT solver binaries

The TOUGHREACT binaries are **not redistributed** with this package due to licence restrictions. You must obtain them separately from the [TOUGH portal](https://tough.lbl.gov/software/toughreact/).

Once obtained, place them in `toughreact_concrete/exe/` following this naming convention:

| Platform | EOS | Filename |
|----------|-----|----------|
| Windows 64-bit | EOS9 | `tr3.0-omp_eos9_PC64.exe` |
| Windows 64-bit | EOS4 | `tr3.0-omp_eos4_PC64.exe` |
| macOS Intel | EOS9 | `treactv3omp_eos9_macosx_intel` |
| Linux Intel | EOS9 | `treactv3omp_eos9_linux_intel` |

Also copy the required Intel Fortran runtime DLLs (Windows only):
`libifcoremd.dll`, `libiomp5md.dll`, `libmmd.dll`, `svml_dispmd.dll`.

## Verify installation

```python
from toughreact_concrete.geometry_trc.constrgeom import suite_geom2
from toughreact_concrete.model.data.physical_const import Psat

elements = suite_geom2(0.05, 10, 1.3)
print(f"Mesh: {len(elements)} elements, total length = {sum(elements):.4f} m")
print(f"Psat at 20°C: {Psat(293.15):.1f} Pa")
```
