"""Tests for geometric-progression mesh generation."""
import pytest

from toughreact_concrete.geometry_trc.constrgeom import suite_geom, suite_geom2


class TestSuiteGeom:
    def test_total_length(self):
        """Sum of all elements equals dim_struct + one boundary micro-element.

        The formula places one micro-element (1e-5 m) at each end; by
        construction sum(elements) - elements[-1] == dim_struct.
        """
        elements = suite_geom(0.1, 10, 1.5)
        assert abs(sum(elements) - elements[-1] - 0.1) < 1e-6

    def test_length_including_boundaries(self):
        """Total list length equals nElem (boundary micro-elements included)."""
        elements = suite_geom(0.1, 10, 1.5)
        assert len(elements) == 10

    def test_boundary_micro_elements(self):
        """First and last elements are 1e-5 m."""
        elements = suite_geom(0.1, 10, 1.5)
        assert elements[0] == pytest.approx(0.00001)
        assert elements[-1] == pytest.approx(0.00001)

    def test_all_positive(self):
        """All element sizes are strictly positive."""
        elements = suite_geom(0.05, 8, 1.3)
        assert all(e > 0 for e in elements)


class TestSuiteGeom2:
    def test_total_length(self):
        """Sum of elements equals dim_struct."""
        elements = suite_geom2(0.1, 10, 1.5)
        assert sum(elements) == pytest.approx(0.1, rel=1e-6)

    def test_list_length(self):
        """List length equals nElem."""
        elements = suite_geom2(0.1, 10, 1.5)
        assert len(elements) == 10

    def test_decroissant_default(self):
        """Default direction: elements decrease (refinement at right)."""
        elements = suite_geom2(0.1, 10, 1.5, sens='decroissant')
        assert elements[0] > elements[-1]

    def test_croissant(self):
        """Croissant direction: elements increase (refinement at left)."""
        elements = suite_geom2(0.1, 10, 1.5, sens='croissant')
        assert elements[0] < elements[-1]

    def test_all_positive(self):
        """All element sizes are strictly positive."""
        elements = suite_geom2(0.05, 8, 1.3)
        assert all(e > 0 for e in elements)
