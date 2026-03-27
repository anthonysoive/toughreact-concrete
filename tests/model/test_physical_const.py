"""Tests for physical constants and Psat function."""
import pytest

from toughreact_concrete.model.data.physical_const import (
    D_cl_water,
    D_water,
    M_w,
    Psat,
    R,
    min_spec_cement,
    rho_wl,
)


class TestConstants:
    def test_rho_wl(self):
        assert rho_wl == 1000

    def test_R(self):
        assert R == pytest.approx(8.314)

    def test_M_w(self):
        assert M_w == pytest.approx(0.01802)

    def test_D_cl_water(self):
        assert D_cl_water == pytest.approx(1.710e-9)

    def test_D_water(self):
        assert D_water == pytest.approx(4.50017e-9)

    def test_min_spec_cement_keys(self):
        expected = {'C3S', 'C2S', 'C3A', 'C4AF', 'Portlandite', 'Ettringite', 'Gypsum'}
        assert expected.issubset(min_spec_cement.keys())

    def test_min_spec_cement_structure(self):
        """Each mineral entry has M, rho, and v keys."""
        for mineral, data in min_spec_cement.items():
            assert 'M' in data, f"{mineral} missing 'M'"
            assert 'rho' in data, f"{mineral} missing 'rho'"
            assert 'v' in data, f"{mineral} missing 'v'"


class TestPsat:
    def test_boiling_point(self):
        """Psat at 373.15 K ≈ 101 325 Pa (1 atm)."""
        assert Psat(373.15) == pytest.approx(101325, rel=0.01)

    def test_triple_point(self):
        """Psat at 273.15 K ≈ 611 Pa (triple point of water)."""
        assert Psat(273.15) == pytest.approx(611, rel=0.1)

    def test_monotonically_increasing(self):
        """Psat increases with temperature."""
        temps = [273.15, 293.15, 323.15, 353.15, 373.15]
        values = [Psat(T) for T in temps]
        assert all(values[i] < values[i + 1] for i in range(len(values) - 1))

    def test_positive(self):
        """Psat is always positive."""
        for T in [250, 300, 350, 400]:
            assert Psat(T) > 0
