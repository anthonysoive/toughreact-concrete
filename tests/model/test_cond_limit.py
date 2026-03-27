"""Tests for CondLimit boundary condition class."""
import pytest

from toughreact_concrete.model.cond_limit import CondLimit


@pytest.fixture
def tidal_kwargs():
    return {
        'HR_ext': [65],
        'T_ext': [20],
        'T_eau': [15],
        'Patm': [1.013e5],
        'Bnd_solution': [{'composition': {}}],
    }


@pytest.fixture
def tidal_heights():
    # [time_increments, tidal_heights] — 4 half-tides
    return [[6, 6, 6, 6], [10, 0, 10, 0]]


class TestCondLimitSechage:
    def test_attributes_set(self):
        cl = CondLimit('sechage', HR_ext=[65], T_ext=[20], Patm=[1.013e5])
        assert cl.humidite_relative_ext == [65]
        assert cl.temperature_ext == [20]
        assert cl.P_atm == [1.013e5]

    def test_type_stored(self):
        cl = CondLimit('sechage', HR_ext=[65], T_ext=[20], Patm=[1.013e5])
        assert cl.type_cond == 'sechage'

    def test_pp_co2_optional(self):
        cl = CondLimit('sechage', HR_ext=[65], T_ext=[20], Patm=[1.013e5],
                       Pp_co2=0.04e5)
        assert cl.Pp_co2 == pytest.approx(0.04e5)


class TestCondLimitMouillage:
    def test_relative_humidity_100(self):
        cl = CondLimit('mouillage', T_eau=[20],
                       Bnd_solution={'composition': {'ca+2': 0.01}})
        assert cl.humidite_relative_ext == [100]

    def test_species_set(self):
        comp = {'ca+2': 0.01}
        cl = CondLimit('mouillage', T_eau=[20],
                       Bnd_solution={'composition': comp})
        assert cl.species == comp


class TestCondLimitInfini:
    def test_instantiates(self):
        cl = CondLimit('infini')
        assert cl.type_cond == 'infini'


class TestCondLimitMaree:
    def test_broadcast_single_value(self, tidal_heights, tidal_kwargs):
        """Single-value lists are broadcast to the length of tidal_heights."""
        cl = CondLimit('maree', tidal_heights, **tidal_kwargs)
        n = len(tidal_heights[1])
        assert len(cl.humidite_relative_ext) == n
        assert len(cl.temperature_ext) == n
        assert len(cl.temperature_eau) == n
        assert len(cl.P_atm) == n
