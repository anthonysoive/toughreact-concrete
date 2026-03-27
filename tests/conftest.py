"""Shared pytest fixtures."""
import pytest

import toughreact_concrete.model.data.bd_materiaux as bd_materiaux


@pytest.fixture
def formulation_m25fa():
    """Mix design for M25FA concrete (CEM I + 30% fly ash)."""
    return bd_materiaux.formulation_beton['M25FA']


@pytest.fixture
def porous_material():
    """Instantiated MateriauPoreux with default parameters."""
    from toughreact_concrete.materiau.mat_poreux import MateriauPoreux
    return MateriauPoreux('TEST')
