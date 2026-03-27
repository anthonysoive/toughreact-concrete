"""
Geometric-progression mesh generation for 1D TOUGHREACT grids.

Meshes are typically refined near boundaries (small elements) and coarser
in the interior, achieved via a geometric sequence of element sizes.
"""


def suite_geom(dim_struct: float, nElem: int, raison: float) -> list[float]:
    """Generate a geometric-progression element sequence, refined at both ends.

    Produces ``nElem`` elements whose sizes follow a geometric sequence.
    Two boundary micro-elements (1e-5 m) are prepended and appended so that
    TOUGHREACT boundary conditions can be applied at fixed nodes.

    Parameters
    ----------
    dim_struct : float
        Total length of the domain (metres).
    nElem : int
        Number of interior elements (excluding the two boundary micro-elements).
    raison : float
        Common ratio of the geometric sequence (> 1 for refinement at the
        left boundary, i.e. elements grow from left to right).

    Returns
    -------
    list of float
        Element sizes, length ``nElem + 2`` (including boundary micro-elements).
    """
    prem_terme = dim_struct*(raison-1)/(raison**(nElem-1-1) -1)
    elements_dr = [prem_terme]
    for i in range(nElem-1-2):
        elements_dr.append(elements_dr[-1]*raison)
    elements_dr[0] = dim_struct - sum(elements_dr) + prem_terme - 0.00001
    elements_dr.reverse()
    elements_dr.insert(0, 0.00001)
    elements_dr.append(0.00001)

    return elements_dr


def suite_geom2(
    dim_struct: float, nElem: int, raison: float, sens: str = 'decroissant'
) -> list[float]:
    """Generate a geometric-progression element sequence without boundary micro-elements.

    Parameters
    ----------
    dim_struct : float
        Total length of the domain (metres).
    nElem : int
        Number of elements.
    raison : float
        Common ratio of the geometric sequence.
    sens : {'decroissant', 'croissant'}, optional
        Direction of progression. ``'decroissant'`` (default): elements
        decrease from left to right (refinement at the right boundary).
        ``'croissant'``: elements increase from left to right (refinement at
        the left boundary).

    Returns
    -------
    list of float
        Element sizes, length ``nElem``.
    """
    prem_terme = dim_struct*(raison-1)/(raison**(nElem+1) -1)
    elements_dr = [prem_terme]
    for i in range(nElem-1):
        elements_dr.append(elements_dr[-1]*raison)
    elements_dr[0] = dim_struct - sum(elements_dr) + prem_terme
    if sens == 'croissant':
        elements_dr.reverse()

    return elements_dr
