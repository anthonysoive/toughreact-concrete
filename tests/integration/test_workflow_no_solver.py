"""Integration test: full pre-solver workflow without calling TOUGHREACT binary."""

import pytest

from toughreact_concrete.geometry_trc.constrgeom import suite_geom2
from toughreact_concrete.model.cond_limit import CondLimit
from toughreact_concrete.model.data.physical_const import Psat


@pytest.mark.skip(reason="Requires PyTOUGH t2data object; run manually")
def test_full_workflow_geometry_to_bc():
    """Verify that geometry + boundary condition objects are constructed correctly."""
    # Geometry
    elements = suite_geom2(0.05, 20, 1.3)
    assert len(elements) == 20
    assert sum(elements) == pytest.approx(0.05, rel=1e-5)

    # Boundary condition
    cl = CondLimit('sechage', HR_ext=[65], T_ext=[20], Patm=[1.013e5])
    assert cl.type_cond == 'sechage'

    # Physical consistency: Psat at boundary temperature
    psat = Psat(cl.temperature_ext[0] + 273.15)
    assert psat > 0


def test_geometry_and_bc_independent():
    """Geometry and boundary conditions can be created independently."""
    elements = suite_geom2(0.10, 15, 1.5)
    cl = CondLimit('sechage', HR_ext=[50], T_ext=[25], Patm=[1.013e5])
    assert len(elements) == 15
    assert cl.humidite_relative_ext == [50]
