"""Tests for species name conversion dictionaries."""
from toughreact_concrete.model.conversion_species import (
    convert_ionic_species,
    hydrat_thermoddem,
    thermoddem_JFB,
)


class TestHydratThermoddem:
    def test_portlandite(self):
        assert hydrat_thermoddem['CH'] == 'Portlandite'

    def test_ettringite(self):
        assert hydrat_thermoddem['C6ASb3H32'] == 'Ettringite'

    def test_gypsum(self):
        assert hydrat_thermoddem['CSbH2'] == 'Gypsum'

    def test_all_values_are_strings(self):
        for key, val in hydrat_thermoddem.items():
            assert isinstance(val, str), f"Value for '{key}' is not a string"


class TestThermoddemJFB:
    """Reverse mapping: THERMODDEM names → JFB notation."""

    def test_portlandite_reverse(self):
        assert thermoddem_JFB['Portlandite'] == 'CH'

    def test_ettringite_reverse(self):
        assert thermoddem_JFB['Ettringite'] == 'C6ASb3H32'

    def test_roundtrip(self):
        """JFB → Thermoddem → JFB roundtrip for unambiguous entries only.

        Some Thermoddem names map to multiple JFB keys (e.g. 'Jennite' maps to
        both 'CSH' and 'CSHHD'), so the reverse dict only preserves one of them.
        We only check that entries where the mapping is unambiguous round-trip.
        """
        # Build the set of Thermoddem names that appear more than once
        from collections import Counter
        counts = Counter(hydrat_thermoddem.values())
        for jfb_key, thermoddem_name in hydrat_thermoddem.items():
            if counts[thermoddem_name] == 1 and thermoddem_name in thermoddem_JFB:
                assert thermoddem_JFB[thermoddem_name] == jfb_key


class TestConvertIonicSpecies:
    def test_lowercase_ca(self):
        result = convert_ionic_species('ca+2', 'Thermoddem.txt')
        assert result == 'Ca+2'

    def test_uppercase_ca(self):
        result = convert_ionic_species('CA+2', 'Thermoddem.txt')
        assert result == 'Ca+2'

    def test_h2o(self):
        result = convert_ionic_species('h2o', 'Thermoddem.txt')
        assert result == 'H2O'

    def test_chloride(self):
        result = convert_ionic_species('cl-', 'Thermoddem.txt')
        assert result == 'Cl-'

    def test_cemdata_database(self):
        result = convert_ionic_species('ca+2', 'cemdata18_2022.out')
        assert result == 'Ca+2'
