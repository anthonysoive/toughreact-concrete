"""
Boundary condition classes for TOUGHREACT concrete simulations.

The main class :class:`CondLimit` dispatches to sub-initialisers depending on
the exposure scenario (tidal cycling, drying, wetting, infinite reservoir).
"""


class CondLimit2:
    """Boundary condition class (simplified version, immersion only)."""

    def __init__(self):
        pass

    @classmethod
    def immersion(cls, composition, temperature):
        cls.composition = composition
        cls.temperature = temperature


class CondLimit:
    """Boundary conditions applied to the concrete structure surface.

    Instantiation dispatches to a sub-initialiser named ``init_<type_cond>``,
    forwarding all positional and keyword arguments.

    Parameters
    ----------
    type_cond : str
        Exposure scenario. Supported values:

        - ``'maree'`` — tidal cycling (alternating submersion / atmospheric
          drying); requires ``args[0]`` = ``[increment, heights]`` and kwargs
          ``HR_ext``, ``T_ext``, ``T_eau``, ``Patm``, optionally ``Pp_co2``
          and ``Bnd_solution``.
        - ``'sechage'`` — atmospheric drying; kwargs ``HR_ext``, ``T_ext``,
          ``Patm``, optionally ``Pp_co2``.
        - ``'mouillage'`` — full immersion; kwargs ``T_eau``,
          ``Bnd_solution``.
        - ``'infini'`` — infinite reservoir (no boundary flux).

    *args
        Positional arguments forwarded to the sub-initialiser.
    **kargs
        Keyword arguments forwarded to the sub-initialiser.
    """

    def __init__(self, type_cond, *args, **kargs):
        self.type_cond = type_cond
        method_name = 'init_' + str(type_cond)
        method = getattr(self, method_name, lambda: "nothing")
        return method(*args, **kargs)
        for elem in args:
            print(elem)

    def init_maree(self, *args, **kargs):
        """Initialise tidal cycling boundary condition.

        Parameters
        ----------
        args[0] : list of two lists
            ``[time_increments, tidal_heights]`` — lists of the same length
            giving the time step (hours) and tidal height (cm) for each
            half-tide.
        HR_ext : list of float
            Relative humidity of the atmosphere (%) for each tidal step.
            Length 1 (broadcast) or same length as ``tidal_heights``.
        T_ext : list of float
            Atmospheric temperature (°C) for each tidal step.
        T_eau : list of float
            Water temperature (°C) for each tidal step.
        Patm : list of float
            Atmospheric pressure (Pa) for each tidal step.
        Pp_co2 : float, optional
            CO₂ partial pressure (Pa).
        Bnd_solution : list of dict, optional
            Boundary solution composition for each tidal step.
        """
        print("on va être mouillé !")
        self.hauteur_maree = args[0][1]
        self.increment_maree = args[0][0]
        self.humidite_relative_ext = kargs['HR_ext']
        self.temperature_ext = kargs['T_ext']
        self.humidite_relative_eau = [1.0]
        self.temperature_eau = kargs['T_eau']
        self.P_atm = kargs['Patm']
        if 'Pp_co2' in kargs.keys():
            self.Pp_co2 = kargs['Pp_co2']
        if 'Bnd_solution' in kargs:
            self.bnd_solution = kargs['Bnd_solution']
        if len(self.humidite_relative_ext) == 1:
            self.humidite_relative_ext = self.humidite_relative_ext*len(self.hauteur_maree)
        if len(self.temperature_ext) == 1:
            self.temperature_ext = self.temperature_ext*len(self.hauteur_maree)
        if len(self.humidite_relative_eau) == 1:
            self.humidite_relative_eau = self.humidite_relative_eau*len(self.hauteur_maree)
        if len(self.temperature_eau) == 1:
            self.temperature_eau = self.temperature_eau*len(self.hauteur_maree)
        if len(self.P_atm) == 1:
            self.P_atm = self.P_atm*len(self.hauteur_maree)
        if len(self.bnd_solution) == 1:
            self.bnd_solution = self.bnd_solution*len(self.hauteur_maree)
        l_HR = len(self.humidite_relative_ext)
        l_Ta = len(self.temperature_ext)
        l_Tw = len(self.temperature_eau)
        l_Pg = len(self.P_atm)
        l_maree = len(self.hauteur_maree)
        if ((l_HR * l_Ta * l_Tw * l_Pg) != 1) and (l_HR != l_maree or
        l_Ta != l_maree or l_Tw != l_maree or l_Pg != l_maree):
            print("Données d'entrée erronnées : les listes doivent être de")
            print("longueur 1 ou égale à la longueur de 'la marée'")

    def init_sechage(self, *args, **kargs):
        """Initialise atmospheric drying boundary condition.

        Parameters
        ----------
        HR_ext : list of float
            External relative humidity (%).
        T_ext : list of float
            External temperature (°C).
        Patm : list of float
            Atmospheric pressure (Pa).
        Pp_co2 : float, optional
            CO₂ partial pressure (Pa).
        """
        print("sous le soleil ?")
        self.humidite_relative_ext = kargs['HR_ext']
        self.temperature_ext = kargs['T_ext']
        self.P_atm = kargs['Patm']
        if 'Pp_co2' in kargs.keys():
            self.Pp_co2 = kargs['Pp_co2']

    def init_mouillage(self, *args, **kargs):
        """Initialise full immersion boundary condition.

        Parameters
        ----------
        T_eau : list of float
            Water temperature (°C).
        Bnd_solution : dict
            Boundary solution with key ``'composition'``.
        """
        print("masques et tubas de rigueur...")
        self.humidite_relative_ext = [100]
        self.temperature_ext = kargs['T_eau']
        self.species = kargs['Bnd_solution']['composition']
        self.P_atm = 1.013e5

    def init_infini(self, *args, **kargs):
        """Initialise infinite-reservoir boundary condition (no boundary flux)."""
        print("quel grand volume !")
        pass


if __name__ == '__main__':
    nb_jours = 1
    hauteur_marnage = nb_jours*2*12*[10]
    humidite_relative_ext = [65]
    temperature_ext = [20]
    temperature_eau = [15]
    P_atm = [1.013e5]
    CL_maree = {'HR_ext':humidite_relative_ext, 'T_ext':temperature_ext,
    'T_eau':temperature_eau, 'Patm':P_atm}
    CL_sechage = {'HR_ext':humidite_relative_ext, 'T_ext':temperature_ext,
                  'Patm':P_atm}
    CL_mouillage = {'T_eau':temperature_eau}

    titi = CondLimit('maree', hauteur_marnage, **CL_maree)
    tutu = CondLimit('sechage', **CL_sechage)
    toto = CondLimit('mouillage', **CL_mouillage)
    toto = CondLimit('infini')
