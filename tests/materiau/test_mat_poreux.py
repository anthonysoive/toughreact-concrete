"""Tests for MateriauPoreux base class."""
import pytest

from toughreact_concrete.materiau.mat_poreux import MateriauPoreux


@pytest.fixture
def mat():
    return MateriauPoreux('TEST')


class TestMateriauPoreuxInit:
    def test_name_short(self):
        """Names shorter than 5 chars are padded with spaces."""
        m = MateriauPoreux('AB')
        assert m.name == 'AB   '

    def test_name_exact(self):
        m = MateriauPoreux('ABCDE')
        assert m.name == 'ABCDE'

    def test_name_truncated(self):
        """Names longer than 5 chars are truncated."""
        m = MateriauPoreux('ABCDEFGH')
        assert m.name == 'ABCDE'

    def test_default_saturation(self, mat):
        assert mat.Sl_init == pytest.approx(0.99)

    def test_default_temperature(self, mat):
        assert mat.temperature == pytest.approx(20.0)

    def test_default_porosity(self, mat):
        assert mat.porosite == pytest.approx(0.0)


class TestHR:
    def test_high_saturation_near_100(self, mat):
        """At Sl=0.99 the result is between 80 and 100 %."""
        hr = mat.HR(0.99, 20)
        assert 80 <= hr <= 100

    def test_medium_saturation_range(self, mat):
        """At Sl=0.5 the result is between 0 and 100 %."""
        hr = mat.HR(0.5, 20)
        assert 0 < hr < 100

    def test_increases_with_saturation(self, mat):
        """Higher saturation → higher relative humidity."""
        hr_low = mat.HR(0.4, 20)
        hr_high = mat.HR(0.9, 20)
        assert hr_low < hr_high

    def test_float_output(self, mat):
        assert isinstance(mat.HR(0.8, 20), float)


class TestInputIC:
    def test_eos9_length_1(self, mat):
        """EOS9 initial conditions vector has length 1."""
        ic = mat.input_IC('eos9')
        assert len(ic) == 1

    def test_eos9_pressure(self, mat):
        """EOS9 first variable is atmospheric pressure."""
        ic = mat.input_IC('eos9')
        assert ic[0] == pytest.approx(mat.P_atm)

    def test_eos3_length_3(self, mat):
        ic = mat.input_IC('eos3')
        assert len(ic) == 3

    def test_eos4_length_3(self, mat):
        ic = mat.input_IC('eos4')
        assert len(ic) == 3
