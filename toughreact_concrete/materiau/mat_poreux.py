"""
Base porous material class for TOUGHREACT simulations.
"""
import math
import os

import t2grids

import toughreact_concrete.model.data.physical_const as physical_const


class MateriauPoreux(t2grids.rocktype):
    """Base class for porous materials in TOUGHREACT simulations.

    Extends PyTOUGH's :class:`t2grids.rocktype` with hydraulic and transport
    properties relevant to cementitious porous media: van Genuchten relative
    permeability and capillary pressure models, initial species concentrations,
    and methods to compute relative humidity and write TOUGHREACT input blocks.

    Parameters
    ----------
    nom_mat : str
        Material name (used as-is if ≤ 5 characters; truncated or padded
        otherwise to match the 5-character TOUGH2 rock-type format).
    """

    def __init__(self, nom_mat):
        self.nom_mat = nom_mat
        self.name = self.modif_name(nom_mat)
        self.P_atm = 101500.  # en Pascals
        self.Sl_init = 0.99
        self.temperature = 20.0
        self.surface_complexes = []
        self.parametres_materiau = None
        self.porosite = 0.

        #Parametres de calcul
        krl_model = {'type':'genuchten','params':[4.396e-01,0.0,1.0,0.01]}
        pc_model = {'type':'genuchten','params':[4.396e-01,0.0,5.369e-08,9.381e7,1.0]}
        modele_adsorb_desorb = {'krl':krl_model, 'pc':pc_model}
        klinkenberg_default = 1.e5
        self.params_model = {'adsorb_desorb':modele_adsorb_desorb, 'klinkenberg':klinkenberg_default}#, 'cl_adsorption_csh':cl_adsorption_csh_default}

        # Thermoddem
        species_in_trame = {'h2o': {'guess': 1.0, 'ctotal': 1.0},
                            'h+': {'guess': 1.0E-13, 'ctotal': -0.4070E-01},
                            'ca+2': {'guess': 1.0e-30, 'ctotal': 1.0e-30},
                            'so4-2': {'guess': 1.0e-30, 'ctotal': 1.0e-30},
                            'h4sio4': {'guess': 1.0e-30, 'ctotal': 1.0e-30},
                            'mg+2': {'guess': 1.0e-30, 'ctotal': 1.0e-30},
                            'al+3': {'guess': 1.0e-30, 'ctotal': 1.0e-30},
                            'cl-': {'guess': 1.0e-30, 'ctotal': 1.0e-30},
                            'hco3-': {'guess': 1.0e-30, 'ctotal': 1.0e-30},
                            'fe+2': {'guess': 1.0e-30, 'ctotal': 1.0e-30},
                            'o2(aq)': {'guess': 1.56e-4, 'ctotal': 1.56e-4}}
        # #Eau de mer (pour Geocorail)
        # species_in_trame = {'h2o': {'guess': 1.0, 'ctotal': 1.0},
        #                     'h+': {'guess': 1.223e-08, 'ctotal': -0.0001041},
        #                     'ca+2': {'guess': 0.008437, 'ctotal': 0.00997},
        #                     'so4-2': {'guess': 0.01245, 'ctotal': 0.0276},
        #                     'h4sio4': {'guess': 9.771e-21, 'ctotal': 1e-20},
        #                     'k+': {'guess': 0.008889, 'ctotal': 0.00971},
        #                     'mg+2': {'guess': 0.03806, 'ctotal': 0.0522},
        #                     'na+': {'guess': 0.4484, 'ctotal': 0.459},
        #                     'al+3': {'guess': 1.993e-28, 'ctotal': 1e-20},
        #                     'cl-': {'guess': 0.5344, 'ctotal': 0.546},
        #                     'hco3-': {'guess': 0.001549, 'ctotal': 0.002029},
        #                     'fe+2': {'guess': 1.011e-40, 'ctotal': 1e-30},
        #                     'o2(aq)': {'guess': 0.000156, 'ctotal': 0.000156}}

        # #Cemdata
        # species_in_trame = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal': -0.4070E-01},
        #                         'ca+2':{'guess':1.0e-30,'ctotal':1.0e-30},'so4-2':{'guess':1.0e-30,'ctotal':1.0e-30},
        #                         'sio2(aq)':{'guess':1.0e-30,'ctotal':1.0e-30},'mg+2':{'guess':1.0e-30,'ctotal':1.0e-30},
        #                         'alo2-':{'guess':1.0e-30,'ctotal':1.0e-30},'cl-':{'guess':1.0e-30,'ctotal':1.0e-30},
        #                         'co3-2':{'guess':1.0e-30,'ctotal':1.0e-30},'feo2-':{'guess':1.0e-30,'ctotal':1.0e-30},
        #                         'e-':{'guess':1.e-10,'ctotal':1.e-10}}
        self.species = species_in_trame


    def modif_name(self, nom_mat):
        name = ''
        if len(nom_mat) >= 5:
            name = nom_mat[0:5]
        else:
            name = nom_mat + ' '*(5 - len(nom_mat))
        return name

    def physical_properties(self,mineral,database):
        """Read database file"""
        database_path = os.getcwd()+'/'+database
        with open(database_path) as f:
            found = False
            for line in f:
                if not found:
                    if line.startswith("'"+str(mineral)+"'"):
                        print(line)
                        density,molar_mass = float(line.split()[1]),float(line.split()[2])
                        found = True
        return density,molar_mass

    def input_IC(self, eos: str) -> list[float]:
        """Return the initial conditions vector for the given EOS module.

        Parameters
        ----------
        eos : str
            EOS module identifier: ``'eos3'``, ``'eos4'``, ``'eos9'``,
            ``'eco2n'``, or ``'eos7'``.

        Returns
        -------
        list of float
            Primary variable values for the initial condition block in
            the TOUGHREACT flow input file. Length depends on the EOS.
        """
        #############################
        #ATTENTION Il faut dissocier IC de BC (on ne parle pas des mêmes températures et HR)
        #############################
        result = {}
        #calcul de la pression partiel d'air
        #S_l = #self.result_hydration['moisture']#(1+(alpha*Pc)**n)**(-m)
        S_g = 1-self.Sl_init
        HR = self.HR(self.Sl_init, self.temperature)
        Pa = self.P_atm - HR / 100.0 * physical_const.Psat(self.temperature + 273.15)
        #Fraction massique d'air dans l'eau
        air_liquid = 26./1000.
        result['eos3'] = [self.P_atm, 10.01, self.temperature]#[self.P_atm, 10+(1-self.Sl_init), self.temperature]#[self.P_atm, 0.015, self.temperature]
        result['eos4'] = [self.P_atm, self.temperature, 1.0e4]#[self.P_atm, self.temperature, Pa]#[self.P_atm, S_g, Pa]#[self.P_atm, 10+S_g, self.temperature]#[self.P_atm, self.temperature, self.P_atm]#[self.P_atm, self.temperature, 1.0e4]#
        result['eco2n'] = [self.P_atm, 10., 1.e-5, self.temperature]#[self.P_atm, 0.0, 10.+S_g, T - 273.15]#air_liquid/100.
        result['eos7'] = [self.P_atm, 0., 10.+air_liquid, self.temperature]#[self.P_atm, 0.0, 10.+S_g, T - 273.15]
        result['eos9'] = [self.P_atm]
        return result[eos]

    def write_toughreact(self, dat, complexation: bool):
        """Write material properties into a TOUGHREACT data object.

        Delegates to :meth:`write_tough2` for hydraulic properties.

        Parameters
        ----------
        dat : t2data
            PyTOUGH data object to which the rock type will be added.
        complexation : bool
            If ``True``, surface complexation is active (no chloride
            adsorption correction applied to tortuosity).

        Returns
        -------
        t2data
            The updated ``dat`` object.
        """
        self.write_tough2(dat, complexation)
        return dat

    def write_tough2(self, dat, complexation):
        #Ecriture des paramètres hydriques
        mat_tmp = t2grids.rocktype(name=self.name,nad=2,density=self.densite,
                                   porosity=self.porosite,permeability=3*[self.permeabilite])
        mat_tmp.relative_permeability['type']=7
        mat_tmp.relative_permeability['parameters']=self.params_model['adsorb_desorb']['krl']['params']
        mat_tmp.capillarity['type']=7
        mat_tmp.capillarity['parameters']=self.params_model['adsorb_desorb']['pc']['params']
        ponderation = 1.0
        if not complexation:
            ponderation = 1 + self.indicateurs_deduits['cl_adsorption_csh']#bd_materiaux.cl_adsorption_csh_default
        self.tortuosite = self.indicateurs_deduits['D_eff'] / physical_const.D_water / self.porosite * ponderation
        mat_tmp.tortuosity = self.tortuosite
        mat_tmp.klinkenberg = self.params_model['klinkenberg']
        dat.grid.add_rocktype(mat_tmp)
        return dat

    def write_react(self, dat):
        pass

    def permeabilite(self):
        permeabilite = self.indicateurs_deduits['K_eau']
        self.permeabilite_ref = permeabilite
        return permeabilite

    def HR(self, S_l: float, T: float) -> float:
        """Compute relative humidity from liquid saturation via van Genuchten model.

        Uses the van Genuchten capillary pressure model and the Kelvin equation
        to convert liquid saturation to relative humidity.

        Parameters
        ----------
        S_l : float
            Liquid saturation (0–1).
        T : float
            Temperature (°C).

        Returns
        -------
        float
            Relative humidity (%).
        """
        m = self.params_model['adsorb_desorb']['pc']['params'][0]
        alpha = self.params_model['adsorb_desorb']['pc']['params'][2]
        n = 1/(1-m)
        Pc_new = 1/alpha * (S_l**(-1/m))**(1/n)
        return 100 * math.exp(-(Pc_new * physical_const.M_w) / (
                    physical_const.rho_wl * physical_const.R * (T + 273.15)))
