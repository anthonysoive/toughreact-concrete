"""
Cementitious material class with hydration, transport, and thermodynamic properties.
"""
import math
import sys

import t2grids

#from  materiau.hydration.floculation import *
import toughreact_concrete.materiau.mat_poreux as mat_poreux
import toughreact_concrete.model.data.bd_materiau_hydrat as bd_materiau_hydrat
import toughreact_concrete.model.data.bd_materiaux as bd_materiaux

#from data.model_parametres import *
#import  toughreact_concrete.model.hydration_data
import toughreact_concrete.model.data.physical_const as physical_const

#import  toughreact_concrete.model.conversion_species
#from  toughreact_concrete.model.data.bd_materiaux import params_model
# sys.path.append('/Users/anthonysoive/Documents/CR_Nantes_2014_11/02-Modelisation/workspace/concrete_durab/hydrationDIM_CTOA')
# import hydrationDIM_CTOA.src.hydrationDIM_CTOA as hydrationDIM_CTOA
from toughreact_concrete.materiau.hydration.calcul_hydratation import calcul_hydratation
from toughreact_concrete.model import toughreact

#import  toughreact_concrete.model.outils_math
from toughreact_concrete.model.conversion_species import (
    hydrat_thermoddem,
    mineral_database,
)

#PHREEQC

if sys.platform == 'darwin':
    MODE = 'dll'  # 'dll' or 'com'
else:
    MODE = 'com'  # 'dll' or 'com'


# if MODE == 'com':
#     import phreeqpy.iphreeqc.phreeqc_com as phreeqc_mod
# elif MODE == 'dll':
#     import phreeqpy.iphreeqc.phreeqc_dll as phreeqc_mod
# else:
#     raise Exception('Mode "%s" is not defined use "com" or "dll".' % MODE)


class MateriauCimentaire(mat_poreux.MateriauPoreux):
    """Cementitious material with hydration-derived properties.

    Extends :class:`~toughreact_concrete.materiau.mat_poreux.MateriauPoreux`
    with cement-specific attributes: mix design, hydration degree, mineral
    volume fractions, and methods to compute density, permeability, and the
    full hydration state from a curing time.

    Parameters
    ----------
    nom_mat : str
        Material name, used as a key in ``bd_materiaux`` databases and as the
        TOUGH2 rock-type identifier (truncated/padded to 5 characters).
    """

    def __init__(self, nom_mat: str) -> None:
        self.nom_mat = nom_mat
        self.name = self.modif_name(nom_mat)
        self.P_atm = 101500. #in Pascals
        self.age_cure = 10000. #fully hydrated by default
        self.degre_hydratation = 99.0
        self.result_hydration = {}
        self.Sl_init = 0.99
        self.temperature = 20.0
        self.minerals = {}
        # for elem in  toughreact_concrete.model.toughreact.list_minerals:
        #     self.minerals[elem] = 0.
        self.species = {}
        self.surface_complexes = ['CSH_OH','CSH_OH1']
        self.formulation = None
        self.parametres_materiau = None
        self.porosite = 0.
        self.D_eff = 0.
        self.database = ''
    
    def lecture_database(self):
        self.formulation = bd_materiaux.formulation_beton[self.nom_mat]
        #self.binder = self.formulation['binder']
        self.densite = self.densite(self.formulation)
        self.mesures_expe = bd_materiaux.mesures_expe[self.nom_mat]
        self.indicateurs_deduits = bd_materiaux.indicateurs_deduits[self.nom_mat]
        self.params_model = bd_materiaux.params_model_default
        
        
        if self.nom_mat in bd_materiau_hydrat.minerals_in.keys():
            self.minerals = bd_materiau_hydrat.minerals_in[self.nom_mat]
            self.species = bd_materiau_hydrat.species_in[self.nom_mat]
        else:
            print('Le matériau cimentaire ne se trouve pas dans la base de données !')
        
        self.porosite = self.mesures_expe['P_eau']
        self.permeabilite = self.permeabilite()
    
    def hydratation(self, temps_cure):
        """Compute hydration state and derived material properties for a given curing time.

        Calls :func:`~toughreact_concrete.materiau.hydration.calcul_hydratation.calcul_hydratation`
        with the mix design stored in ``self.formulation``, then populates
        ``self.result_hydration`` with volume fractions, compositions, and
        hydration degree.  Also sets ``self.porosite``, ``self.densite``,
        ``self.permeabilite``, and the van Genuchten model parameters.

        Parameters
        ----------
        temps_cure : float
            Curing time (days).

        Returns
        -------
        dict
            Hydration results dictionary with keys ``'fracvol'``, ``'compo'``,
            ``'alpha'`` (hydration degree), and others.
        """
        self.densite = self.densite(self.formulation)
        self.permeabilite = self.permeabilite()
        #Parametres de calcul
        krl_model = {'type':'genuchten','params':[4.396e-01,0.0,1.0,0.01]}
        pc_model = {'type':'genuchten','params':[4.396e-01,0.0,5.369e-08,9.381e7,1.0]}
        modele_adsorb_desorb = {'krl':krl_model, 'pc':pc_model}
        klinkenberg_default = 1.e5
        self.params_model = {'adsorb_desorb':modele_adsorb_desorb, 'klinkenberg':klinkenberg_default}
        
        self.age_cure = temps_cure #fully hydrated by default
        
        #----------------------------------------------------------------------
        def Bogues_revisited(composition):
            M_SiO2=60.08;M_Al2O3=101.96;M_CaO=56.08;M_Fe2O3=159.69;M_SO3=80.06;M_O=18.02;M_CO2=44.01
            n_SiO2 = composition['SiO2']/M_SiO2
            n_Al2O3 = composition['Al2O3']/M_Al2O3
            n_CaO = composition['CaO']/M_CaO
            n_Fe2O3 = composition['Fe2O3']/M_Fe2O3
            n_SO3 = composition['SO3']/M_SO3
            n_CO2 = composition['CO2']/M_CO2
            
            #!!!AS
            n_CaO_consomme = min(n_CaO,n_CO2)
            n_CaO = n_CaO - n_CaO_consomme
            n_CaCO3 = n_CaO_consomme
            #!!!AS
            
            #Gypse
            n_gypse = n_SO3
            n_CaO_gypse = n_gypse
            n_CaO_consomme = min(n_CaO,n_CaO_gypse)
            n_CaO = n_CaO - n_CaO_consomme
            n_gypse = n_CaO_consomme
            m_gypse = n_gypse * (M_CaO+M_SO3)
            
            #C4AF
            n_C4AF = n_Fe2O3
            n_CaO_C4AF = 4*n_C4AF
            n_CaO_consomme = min(n_CaO_C4AF,min(n_CaO,4*n_Al2O3))
            n_CaO = n_CaO - n_CaO_consomme
            n_C4AF = n_CaO_consomme/4.
            m_C4AF = n_C4AF*(4*M_CaO+M_Al2O3+M_Fe2O3)
            n_Al2O3 = n_Al2O3 - n_C4AF
            n_Fe2O3 = n_Fe2O3 - n_C4AF
            
            #C3A
            n_C3A = n_Al2O3
            n_CaO_C3A = 3*n_C3A
            n_CaO_consomme = min(n_CaO,n_CaO_C3A)
            n_CaO = n_CaO - n_CaO_consomme
            n_C3A = n_CaO_consomme/3.
            m_C3A = n_C3A*(3*M_CaO+M_Al2O3)
            n_Al2O3 = n_Al2O3 - n_C3A
            
            #reste
            if n_SiO2 > 0:
                C_S = n_CaO / n_SiO2
            else:
                C_S = 0.
            
            if n_SiO2 > 0:
                if C_S > 2:
                    n_C3S = n_CaO - 2 * n_SiO2
                    n_C2S = 3 * n_SiO2 - n_CaO
                else:
                    n_C3S = 0.
                    n_C2S = n_CaO/2.
            else:
                n_C3S = 0.
                n_C2S = 0.
            
            if n_SiO2 > 0:
                if C_S < 2:
                    n_S = n_SiO2 - n_CaO/2.
                else:
                    n_S = 0.
            else:
                n_S = 0.
            
            n_SiO2 = n_SiO2 - n_C3S - n_C2S - n_S
            n_CaO = n_CaO - 3*n_C3S - 2*n_C2S
            
            m_C3S = n_C3S*(3*M_CaO+M_SiO2)
            m_C2S = n_C2S*(2*M_CaO+M_SiO2)
            m_S = n_S*M_SiO2
            m_Al2O3 = n_Al2O3 * M_Al2O3
            m_Fe2O3 = n_Fe2O3 * M_Fe2O3
            m_gypse_hydrate = m_gypse/(M_CaO+M_SO3)*(M_CaO+M_SO3+2*M_O)
            m_CaO_libre = n_CaO * M_CaO
            m_SO3_libre = n_SO3 * M_SO3
            m_CaCO3 = n_CaCO3 * (M_CaO+M_CO2)
            
            composition_Bogues = {'C3S':m_C3S,'C2S':m_C2S, 'C3A':m_C3A, 
                                  'C4AF':m_C4AF,'CSbH2':m_gypse_hydrate,
                                  'SS':m_S,'A':m_Al2O3,'CCb':m_CaCO3}
            return composition_Bogues
        #----------------------------------------------------------------------
        
        #Conversion of cement composition into C3S, C3A, C4AF... (input data for the hydration model)
        masse_totale_binder = 0
        for elem in self.formulation['binder']:
            self.formulation['binder'][elem]['compo']['composition_Bogues'] = {}
            if ("C3S" and "C3A") in self.formulation['binder'][elem]['compo']['composition']:
                self.formulation['binder'][elem]['compo']['composition_Bogues']['C3S'] = self.formulation['binder'][elem]['compo']['composition']['C3S']
                self.formulation['binder'][elem]['compo']['composition_Bogues']['C3A'] = self.formulation['binder'][elem]['compo']['composition']['C3A']
                self.formulation['binder'][elem]['compo']['composition_Bogues']['C2S'] = self.formulation['binder'][elem]['compo']['composition']['C2S']
                self.formulation['binder'][elem]['compo']['composition_Bogues']['C4AF'] = self.formulation['binder'][elem]['compo']['composition']['C4AF']
                if 'CSbH2' in self.formulation['binder'][elem]['compo']['composition']:
                    self.formulation['binder'][elem]['compo']['composition_Bogues']['CSbH2'] = self.formulation['binder'][elem]['compo']['composition']['CSbH2']
                if 'SS' in self.formulation['binder'][elem]['compo']['composition']:
                    self.formulation['binder'][elem]['compo']['composition_Bogues']['SS'] = self.formulation['binder'][elem]['compo']['composition']['SS']
                if 'A' in self.formulation['binder'][elem]['compo']['composition']:
                    self.formulation['binder'][elem]['compo']['composition_Bogues']['A'] = self.formulation['binder'][elem]['compo']['composition']['A']
                if 'CCb' in self.formulation['binder'][elem]['compo']['composition']:
                    self.formulation['binder'][elem]['compo']['composition_Bogues']['CCb'] = self.formulation['binder'][elem]['compo']['composition']['CCb']
            else:
                self.formulation['binder'][elem]['compo']['composition_Bogues'] = Bogues_revisited(self.formulation['binder'][elem]['compo']['composition'])
            print("Composition de Bogue pour ",elem,": ", self.formulation['binder'][elem]['compo']['composition_Bogues'])
            masse_totale_binder += self.formulation['binder'][elem]['kg']
        #retrieval of the hydration calculation result
        #-fracvol is expressed in cm3/cm3 of material (concrete)
        output_hydration = calcul_hydratation(self.formulation,temps_cure)
        for elem in output_hydration['fracvol']:
            if elem not in ['bigcapillaryvoids','anhydre','A','C3AFSH4','SS','C4AF','C3A','C3S','C2S','CSHLP']:#,'CSHHD','CSHLD'
                #volume fraction of solid in the cement paste
                if output_hydration['fracvol'][elem] > 0:
                    self.minerals[hydrat_thermoddem[elem].upper()] = output_hydration['fracvol'][elem] #/(1-output_hydration['phic'])
                else:
                    self.minerals[hydrat_thermoddem[elem].upper()] = 0.
            else:
                print(elem,output_hydration['fracvol'][elem])#/(1-output_hydration['phic']))

        #Conversion to volume fraction of solid in the cementitious material
        #g : volume fraction of aggregates
        #g = sum([self.formulation['granulats'][elem]['kg'] / (self.formulation['granulats'][elem]['nature']['densite']*1000.) for elem in self.formulation['granulats']])
        for elem in self.minerals:
            self.minerals[elem] = self.minerals[elem] / (1-self.porosite)# * (1-g)
        
        q_C3A = output_hydration['fracvol']['C3A'] * 3.03 / 270.3# * (1-g) #mol/cm3 of material
        print("Amount of C3A (mol/cm3 of material): ",q_C3A)
        q_C3S = output_hydration['fracvol']['C3S'] * 3.15 / 228.4 # * (1-g) #mol/cm3 of material
        print("Amount of C3S (mol/cm3 of material): ",q_C3S)
        print("Potential amount of chlorides bound from C3A (g/100g of material): ",min([q_C3A,q_C3S])*35.5*2/2.4*100)
        #print("Amount of C2S (mol/cm3 of material): ",output_hydration['fracvol']['C2S'] * (1-g) *3.28 / ...)
        #print("Amount of C4AF (mol/cm3 of material): ",output_hydration['fracvol']['C4AF'] * (1-g) *3.73 / ...)

        self.degre_hydratation = output_hydration["alpha"]
        print("average hydration degree: ",self.degre_hydratation)
        #nb_mol_Jennite = elem,output_hydration['fracvol']["CSHHD"]/(1-output_hydration['phic'])/78.
        #nb_mol_Tobermorite = elem,output_hydration['fracvol']["CSHLD"]/(1-output_hydration['phic'])/59.
        #print("nb mol/cm3 de Jennite :",nb_mol_Jennite)
        #print("nb mol/cm3 de Tobermorite :",nb_mol_Tobermorite)

        #Calculation of porosity and effective diffusion coefficient by "homogenisation"
        #from the paste porosity and the aggregate volume fraction
        #For the effective diffusion coefficient of the paste, it is assumed
        #to be equal to 5.e-13
        #self.porosite = output_hydration['phic'] * (1-g)
        #self.indicateurs_deduits['D_eff'] = 1.e-12 / (1+g/2.)/(1-g)
        #print("calculated porosity: ",self.porosite)
        #print("calculated effective diffusion coefficient: ",self.indicateurs_deduits['D_eff'])
        
        dict_minerals_database = toughreact.lecture_database(self.database)
        material_species = []
        for elem in self.minerals.keys():
            convert_mineral = mineral_database[self.database][elem].upper()
            if convert_mineral.upper() in dict_minerals_database:
                material_species += list(dict_minerals_database[convert_mineral]['reaction'])
                # tmp = list(dict_minerals_database[convert_mineral]['reaction'])
                # for ion in tmp:
                #     material_species.append(convert_ionic_species(ion, self.database))
                # #

        material_species = list(set(material_species))
        material_species += ['H+', 'H2O']
        for elem in material_species:
            if elem not in self.species:
                self.species[elem] = {'guess':1e-20,'ctotal':1e-20}
        
        # self.species = toughreact.species2toughreact(tmp_species)
        
        #species_in_trame = species_database[self.database]

        #Species
        q_Na_solution = 0
        q_K_solution = 0
        for elem in self.formulation['binder']:#g/g de liant
            proportion_elem = self.formulation['binder'][elem]['kg']/masse_totale_binder
            q_Na_solution += self.formulation['binder'][elem]['compo']['composition']['Na2O'] / 100. * self.formulation['binder'][elem]['kg']
            q_K_solution += self.formulation['binder'][elem]['compo']['composition']['K2O'] / 100. * self.formulation['binder'][elem]['kg']
        MK = 39.1
        MNa = 22.99
        q_Na_solution_moll = q_Na_solution / MNa / (self.formulation['e'] / 1000) 
        q_K_solution_moll = q_K_solution / MK / (self.formulation['e'] / 1000)
        self.species['K+'] = {'guess':q_K_solution_moll,'ctotal':q_K_solution_moll}
        self.species['Na+'] = {'guess':q_Na_solution_moll,'ctotal':q_Na_solution_moll}
        self.species['H2O'] = {'guess':1.0,'ctotal':1.0}
        self.species['H+'] = {'guess':1.0E-13,'ctotal': -0.4070E-01}
        
        #print("volume fraction of solid species: ",self.minerals)
        #print("molar concentration of ionic species: ",self.species)
        
        fracvol_minerals_total = sum([self.minerals[elem] for elem in self.minerals])
        #print("Volume fraction of reactive minerals: ",fracvol_minerals_total)
        # fracvol_minerals_prisencompte = fracvol_minerals_total - self.minerals['C3FS1.34H3.32'] - self.minerals['C3AS0.84H4.32'] - self.minerals['C3AH6']
        fracvol_minerals_prisencompte = fracvol_minerals_total - self.minerals['C3AFS0.84H4.32'] - self.minerals['C3AH6']
        #print("Volume fraction of reactive minerals taken into account: ",fracvol_minerals_prisencompte)
    
    def calcul_Na_K_solution(self,species):
        Na2O = sum([self.formulation['binder'][elem]['compo']['composition']['Na2O'] for elem in self.formulation['binder']])
        K2O = sum([self.formulation['binder'][elem]['compo']['composition']['K2O'] for elem in self.formulation['binder']])
        Cl = sum([self.formulation['binder'][elem]['compo']['composition']['Cl'] for elem in self.formulation['binder']])
        e_c = sum([self.formulation['binder'][elem]['kg'] for elem in self.formulation['binder']])
        M_Na2O = 61.98
        M_K2O = 94.2
        M_Cl = 35.45
        species['na+'] = 2 * Na2O / e_c / M_Na2O * 1000.
        species['k+'] = 2 * K2O / e_c / M_K2O * 1000.
        species['cl-'] = 1 * Cl / e_c / M_Cl * 1000.
        return species

    
    def modif_name(self, nom_mat):
        name = ''
        if len(nom_mat) >= 5:
            name = nom_mat[0:5]
        else:
            name = nom_mat + ' '*(5 - len(nom_mat))
        return name
    
    def densite(self, formulation):
        """Compute the total dry mass per unit volume from the mix design.

        Parameters
        ----------
        formulation : dict
            Mix design dictionary with keys ``'binder'`` and ``'granulats'``,
            each containing mass quantities in kg.

        Returns
        -------
        float
            Total mass of solid constituents per unit volume (kg/m³).
        """
        densite = formulation['binder']["c"]['kg']
        for elem in formulation['granulats'].keys():
            densite += formulation['granulats'][elem]['kg']
        return densite
    
    def temperature_cure(self, temperature: float) -> float:
        temperature_cure = 0
        if temperature > 273.15:
            temperature_cure = temperature - 273.15
        else:
            temperature_cure = temperature
        return temperature_cure
    
    def permeabilite(self):
        """Return the intrinsic water permeability from the material database.

        Returns
        -------
        float
            Intrinsic permeability (m²), read from ``indicateurs_deduits['K_eau']``.
        """
        permeabilite = self.indicateurs_deduits['K_eau']
        self.permeabilite_ref = permeabilite
        return permeabilite
    
    def HR(self, S_l: float, T: float) -> float:
        m = bd_materiaux.pc_model['params'][0]
        alpha = bd_materiaux.pc_model['params'][2]
        n = 1/(1-m)
        Pc_new = 1/alpha * (S_l**(-1/m))**(1/n)
        return 100 * math.exp(-(Pc_new*physical_const.M_w)/(physical_const.rho_wl*physical_const.R*(T + 273.15)))
    
    def convert_hydrat_thermoddem(self, compo_hydrat):
        '''Converts the dictionary produced by the hydration calculation into a dictionary
        of species known in the BRGM thermoddem thermodynamic database'''
        dict_thermoddem = {}
        for elem in compo_hydrat.keys():
            dict_thermoddem[hydrat_thermoddem[elem]] = compo_hydrat[elem]
        return dict_thermoddem
            
#     def __init__(self, nom_mat, formulation, densite, compo_ciment, age_cure, 
#                  temperature, mesures_ref, modeles_mat, tortuosite, klinkenberg=0.0):
#         if len(nom_mat) >= 5:
#             self.name = nom_mat[0:5]
#         else:
#             self.name = nom_mat + ' '*(5 - len(nom_mat))
#         self.formulation = formulation
#         self.densite = densite
#         if 'CaO' in compo_ciment:
#             self.compo_ciment_oxy = compo_ciment
#             self.compo_ciment = self.bogue(compo_ciment)
#         else:
#             self.compo_ciment = compo_ciment
#         self.result_hydrat = hydration_data.hydration_content(self.compo_ciment, formulation)
#         self.age_cure = age_cure #en jours
#         self.degre_hydratation = self.result_hydrat(3600.*24.*self.age_cure)["deghyd"]
#         if self.degre_hydratation < 0.4:
#             print "Warning! An initial hydration degree below 0.4"
#             print "is not taken into account in this model"
#         self.porosite_ref = mesures_ref['porosite']
#         if self.degre_hydratation > 0.94:
#             self.porosite = self.porosite_ref
#         else:
#             self.porosite = self._porosite()(self.degre_hydratation)
#         if temperature > 273.15:
#             self.temperature = temperature - 273.15
#         else:
#             self.temperature = temperature
#         self.permeabilite_ref = mesures_ref['permeabilite']
#         self.permeabilite = self.calcul_Kl(self.porosite)
#         self.krl_model = modeles_mat['krl']
#         self.pc_model = modeles_mat['pc']
#         self.P_atm = 101500. #in Pascals
#         self.humidite_relative = 99
#         self.tortuosite = tortuosite
#         self.cl_adsorption_csh = modeles_mat['cl_adsorption_csh']
#         self.klinkenberg = klinkenberg
    
#     def ecriture_class(self):
#         print "formulation: ",self.formulation
#         print "cement composition: ",self.compo_ciment
#         print "curing duration (in days): ",self.age_cure
#         print "hydration degree: ",self.degre_hydratation
#         print "composition of hydrated material (after curing): ",self.result_hydration(3600.*24.*self.age_cure)
#         print "porosity: ",self.porosite
#         print "temperature: ",self.temperature
#         print "reference permeability: ",self.permeabilite_ref, " for a reference porosity of: ",self.porosite_ref
#         print "permeability: ",self.permeabilite
#         print "relative permeability model: ",self.params_model['adsorb_desorb']['krl']
#         print "capillary pressure model: ",self.params_model['adsorb_desorb']['pc']
    
#     def _porosite(self):
#         '''Returns a function that computes the porosity as a function
#         of the hydration degree of the cementitious material'''
#         def content(degre_hydratation):
#             return self.result_hydrat(0.)["phi"]*(1-param_hydrat['mu']*\
#             self.formulation['c']/self.formulation['e']*degre_hydratation) #these Nguyen (3.76)
#         return content
#             
#     def _rho_app(self):
#         def content(degre_hydratation):
#             return  (1+degre_hydratation*param_hydrat['lambda_'])/\
#                    (1/physical_const.rho_C + self.formulation['e']/\
#                    (self.formulation['c']*physical_const.rho_wl))
#         return content
#     
#     def _psi(self):
#         def content(degre_hydratation):
#             return (1+degre_hydratation*param_hydrat['lambda_'])/\
#             (degre_hydratation*param_hydrat['gamma_etoile']) #these nguyen (6.9)
#         return content
#         
#     def theta_RH(self,x):
#         #fonction teneur en eau en fonction de RH
#         c = params_beton['van_genuchten']['c']
#         m = params_beton['van_genuchten']['m']
#         n = params_beton['van_genuchten']['n']
#         return (1+(-c*math.log(x))**n)**(-m) #f(RH), fprime(RH)
# 
#     def param_pc_RH(self):
#         '''Computes the coefficients of the polynomial equation (cf. Nguyen/Thierry)'''
#         def content(degre_hydratation):
#             x = param_hydrat['rh_lim_theta']
#             by = misc.derivative(self.theta_RH,x, dx=1e-6)
#             bx = self.theta_RH(x)
#             porosite = self._porosite()(degre_hydratation)
#             rho_app = self._rho_app()(degre_hydratation)
#             psi = self._psi()(degre_hydratation)
#             bz = psi*physical_const.rho_wl/rho_app*porosite
#             b = np.array([bx, by, bz])
#             A = np.array([[x**2, x, 1],[2*x, 1, 0], [1, 1, 1]])
#             A_inverse = np.linalg.inv(A)
#             x = np.dot(A_inverse , b)
#             return x
#         return content
# 
#     def slpc_RH(self,rh):
#         '''Computes the liquid saturation and capillary pressure as a
#         function of RH'''
#         def content(degre_hydratation):
#             porosite = self._porosite()(degre_hydratation)
#             rho_app = self._rho_app()(degre_hydratation)
#             psi = self._psi()(degre_hydratation)
#             theta_max = porosite*physical_const.rho_wl/rho_app
#             rho_E = physical_const.rho_wl
#             T = self.temperature + 273.15
#             Mv = physical_const.M_w
#             R = 8.32
#             #Sl = np.zeros(len(rh))
#             #pc = np.zeros(len(rh))
#             w_etoile = []
#             A,B,C = self.param_pc_RH()(degre_hydratation)
#             #psi = self.params_hyd_sech['psi'] #this parameter appears in Nguyen's thesis (p.184)
#             #in order to remove the dependency on CSH content
#             if rh < 0.44:
#                 tmp_w_etoile = self.theta_RH(rh)
#                 pc = -rho_E*R*T/Mv*math.log(rh)
#             else:
#                 tmp_w_etoile = A*rh**2+B*rh+C
#                 delta = B**2 - 4*A*(C-tmp_w_etoile)
#                 pc = -rho_E*R*T/Mv * math.log((-B+math.sqrt(delta))/(2*A))
#             w_etoile.append(tmp_w_etoile)
#             Sl = tmp_w_etoile/psi/theta_max
#             return Sl,pc
#         return content
# 
#     def H(self,porosity,Sl,sl_rh_70):
#         theta_l = porosity * Sl
#         theta_l_crit = porosity * sl_rh_70
#         beta=2.
#         if theta_l > theta_l_crit:
#             result = ((theta_l - theta_l_crit)/(porosity - theta_l_crit))**beta
#         else:
#             result = 0.
#         return result
# 
#     def cinetique_hydratation(self,degre_hydrat,t,porosity,Sl,sl_rh_70):
#         tau = param_hydrat['R_ciment']**2./(3.*param_hydrat['D'])
#         A = (1-degre_hydrat)**(2./3.)/((1.-param_hydrat['degre_hydrat_D'])**(1./3.)\
#         -(1-degre_hydrat)**(1./3.))
#         d_alpha_dt = 1./tau * A * self.H(porosity,Sl,sl_rh_70)
#         #print tau, A, d_alpha_dt
#         return d_alpha_dt
# 
#     def eau_consom_hydrat(self,d_degre_hydrat):
#         '''Water consumed by the hydration of concrete'''
#         w_ult = param_hydrat['lambda_'] * self.formulation['c'] / physical_const.rho_wl
#         #print 'Sl ',Sl 
#         return w_ult*d_degre_hydrat
# 
#     def hydration(self,liquid_saturation,duree):
#         '''Returns the effective liquid saturation and the volume of water consumed
#         by hydration from a liquid saturation and a duration'''
#         tmp_porosity = self._porosite()(self.degre_hydratation)
#         sl_lim_hydrat, tutu = self.slpc_RH(param_hydrat['rh_lim_hydrat'])(self.degre_hydratation)
#         
#         # Times at which the solution is to be computed.
#         t = np.linspace(0, duree, 2)
#         #iterative loop to find the hydration degree and the other
#         #parameters such as porosity, rh_70_Sl...
#         list_degre_hydrat = [0,self.degre_hydratation]
#         while (list_degre_hydrat[-1]-list_degre_hydrat[-2]) > 1.0e-7:
#             degre_hydrat = integrate.odeint(self.cinetique_hydratation, 
#                                             list_degre_hydrat[1], t, 
#                                            args=(tmp_porosity,liquid_saturation,
#                                                  sl_lim_hydrat,))
#             #print tmp_rh_70_Sl,liquid_saturation,degre_hydrat
#             list_degre_hydrat.append(degre_hydrat[-1][0])
#             #tmp_porosity = self._porosite()(degre_hydrat[-1][0])
#             sl_lim_hydrat, tutu = self.slpc_RH(param_hydrat['rh_lim_hydrat'])(self.degre_hydratation)
#             #print tmp_porosity,tmp_rho_app,tmp_psi,tmp_rh_70_Sl
#             #list_degre_hydrat.append(degre_hydrat[-1])
#         
#         d_degre_hydrat = (list_degre_hydrat[-1] - list_degre_hydrat[1])/duree
#         self.porosite = self._porosite()(degre_hydrat[-1][0])
#         eau_consom = self.eau_consom_hydrat(d_degre_hydrat)/self.porosite
#         #print eau_consom
#         Sl = liquid_saturation - eau_consom/self.porosite
#         
#         self.update_materiau(degre_hydrat[-1][0])
# #        print self.name
# #        print 'Porosity :',self.porosity
# #        print 'Sl_70 : ',self.rh_70_Sl
# #        print 'Hydration degree: ',self.degre_hydrat
# #        print 'Saturation effective :',Sl
# #        print '**************************'
#         return Sl, eau_consom
# 
#     def calcul_Kl(self, porosite):
#         return self.permeabilite_ref * (porosite / self.porosite_ref)**2 * \
#         ((1-self.porosite_ref)/(1-porosite))**2
#     
#     def calcul_krl_pc(self):
#         '''Computes the relative permeability and capillary pressure parameters'''
#         tab_rh = np.arange(0.1, 1, 0.01)
#         x_plot, y_plot = np.zeros(len(tab_rh)),np.zeros(len(tab_rh))
#         i = 0
#         for rh in tab_rh:
#             x_plot[i], y_plot[i]  = self.slpc_RH(rh)(self.degre_hydratation)
#             i += 1
#         plt.xlabel('RH')
#         plt.ylabel('Liquid saturation')
#         plt.plot(tab_rh,x_plot)
#         plt.show()
#         #*******************fit Van Genuchten
#         p_0 = -5.369e-08
#         p_1 = 4.396e-01
#         p_2 = 0
#         p0 = [p_0 , p_1, p_2]
#         fit = outils_math.Levenberg_Marquardt(outils_math.fit_function_VG, p0, 
#                                               y_plot, x_plot)
#         fit = np.array(fit)
#         #*******************fit Van Genuchten
#         #relative_permeability['parameters'][0] = fit[0][1]
#         #capillarity['parameters'] = [fit[0][1],0.0,fit[0][0],9.381e7,1.0]
#         return fit[0][1], [fit[0][1],0.0,fit[0][0],9.381e7,1.0]
# 
# 
#     def update_materiau(self, degre_hydrat):
#         '''Updates the material properties as a function of the hydration
#         degree'''
#         self.degre_hydratation = degre_hydrat
#         self.porosite = self._porosite()(degre_hydrat)
#         self.permeability = self.calcul_Kl(self.porosite)
#         params_krl, params_pc = self.calcul_krl_pc()
#         self.params_model['adsorb_desorb']['krl']['params'][0] = params_krl
#         self.params_model['adsorb_desorb']['pc']['params'] = params_pc
#         
#         #######################
#         #+ Minerals and ions...
#     
#     def compo_mat_hydrat(self,degre_hydrat):
#         '''Returns the composition of the hydrated cementitious material as a function of
#         the hydration degree. This includes mineral and ionic species.'''
#         #Duration in days beyond which hydration is assumed complete
#         duree_initiale = 100.
#         duree = duree_initiale
#         tmp_degre_hydrat = self.result_hydrat(3600.*24.*duree)["deghyd"]
#         #print degre_hydrat, tmp_degre_hydrat
#         if degre_hydrat < tmp_degre_hydrat:
#             diff = tmp_degre_hydrat - degre_hydrat
#             while np.abs(diff) > 1e-3:
#                 if diff > 0:
#                     duree = duree/2.
#                 else:
#                     duree = 1.5 * duree
#                 tmp_degre_hydrat = self.result_hydrat(3600.*24.*duree)["deghyd"]
#                 #print tmp_degre_hydrat
#                 diff = tmp_degre_hydrat - degre_hydrat
#         return self.result_hydrat(3600.*24.*duree)

    def input_IC(self, eos: str) -> list[float]:
        #############################
        #WARNING: IC and BC must be distinguished (they do not refer to the same temperatures and RH)
        #############################
        result = {}
        #calculation of the partial air pressure
        #S_l = #self.result_hydration['moisture']#(1+(alpha*Pc)**n)**(-m)
        S_g = 1-self.Sl_init
        HR = self.HR(self.Sl_init, self.temperature)
        Pa = self.P_atm - HR/100.0*physical_const.Psat(self.temperature + 273.15)
        #Mass fraction of air in water
        air_liquid = 26./1000.
        result['eos3'] = [self.P_atm, 10.01, self.temperature]#[self.P_atm, 10+(1-self.Sl_init), self.temperature]#[self.P_atm, 0.015, self.temperature]
        result['eos4'] = [self.P_atm, S_g, Pa]#[self.P_atm, self.temperature, Pa]#[self.P_atm, 10+S_g, self.temperature]#[self.P_atm, self.temperature, self.P_atm]#[self.P_atm, self.temperature, 1.0e4]#
        result['eco2n'] = [self.P_atm, 10., 1.e-5, self.temperature]#[self.P_atm, 0.0, 10.+S_g, T - 273.15]#air_liquid/100.
        result['eos7'] = [self.P_atm, 0., 10.+air_liquid, self.temperature]#[self.P_atm, 0.0, 10.+S_g, T - 273.15]
        result['eos9'] = [self.Sl_init]
        return result[eos]

    def write_toughreact(self, dat, complexation: bool):
        '''Write in TOUGHREACT format.
        The function calls 'write_tough2' for the hydraulic part and 'write_react'
        for the reactive part'''
        self.write_tough2(dat, complexation)
        return dat
    
    def write_tough2(self, dat, complexation):
        #Writing of hydraulic parameters
        mat_tmp = t2grids.rocktype(name=self.name,nad=2,density=self.densite,\
        porosity=self.porosite,permeability=3*[self.permeabilite])
        mat_tmp.relative_permeability['type']=7
        mat_tmp.relative_permeability['parameters']=self.params_model['adsorb_desorb']['krl']['params']
        mat_tmp.capillarity['type']=7
        mat_tmp.capillarity['parameters']=self.params_model['adsorb_desorb']['pc']['params']
        ponderation = 1.0
        if not complexation:
            ponderation = 1 + self.indicateurs_deduits['cl_adsorption_csh']#bd_materiaux.cl_adsorption_csh_default
        self.tortuosite = 0.0 #self.indicateurs_deduits['D_eff'] / physical_const.D_water / self.porosite * ponderation
        mat_tmp.tortuosity = self.tortuosite
        mat_tmp.klinkenberg = self.params_model['klinkenberg']
        dat.grid.add_rocktype(mat_tmp)
        return dat
    
    def write_react(self, dat):
        pass
    
#     def calcul_especes_ioniques_phreeqc(self, dbase):
#         '''Computes the ionic species in equilibrium with the mineral species'''
#         titi_brgm = self.convert_hydrat_thermoddem(self.compo_mat_hydrat(self.degre_hydratation))
#         # Reaction configuration
#         input_string = "SOLUTION 1 Pure water\n"
#         input_string += "\tpH      12.\n"
#         input_string += "\ttemp    "+str(self.temperature)+"\n"
# #        input_string += "\tK    0.121\n"
# #        input_string += "\tNa    0.121\n"
#         input_string += "\t-water\t"+str(self.porosite)+"\n"
#         input_string += "EQUILIBRIUM_PHASES"
#         for elem in titi_brgm.keys():
#             if titi_brgm[elem] > 0:
#                 input_string += "\n\t" + elem + "    0    " + str(titi_brgm[elem]*1000.)
#             else:
#                 input_string += "\n\t" + elem + "    0     0"
#         input_string += "\n\tNa2O\t0     0.2"
#         input_string += "\n\tK2O\t0     0.3"
#         #!!!!!!!!!!! + NA2O + K2O
#         phreeqc = phreeqc_mod.IPhreeqc()
#         phreeqc.load_database(dbase)
#         #input_string += "\nUSE SOLUTION\t1\nSELECTED_OUTPUT\n\t-file   ex2.sel"
#         #input_string += "\n\t-total\tAl\tCa"
#         #print input_string
#         phreeqc.run_string(input_string)
#         #print input_string
#         components = phreeqc.get_component_list()
#         headings = "\n\t-total\t"#\tAl\tCa"
#         for i in range(len(components)):
#             headings += components[i] + "\t"
#         if not "K" in components:
#             components.append("K")
#             headings += components[-1] + "\t"
#         if not "Na" in components:
#             components.append("Na")
#             headings += components[-1] + "\t"
#         headings += "\n\t-equilibrium_phases\t"#\tAl\tCa"
#         for elem in titi_brgm.keys():
#             headings += elem + "\t"
# #        headings += "Katoitesi1"
#         selected_output = input_string+"\nSELECTED_OUTPUT\n\t-file   ex2.sel"#\nUSE SOLUTION\t1
#         selected_output += headings + "\nEND\n"
#         print selected_output
#         phreeqc.run_string(selected_output)
#         
#         def get_selected_output(phreeqc):
#             """Return calculation result as dict.
#             Header entries are the keys and the columns are the values as lists of numbers.
#             """
#             output = phreeqc.get_selected_output_array()
#             header = output[0]
#             conc = {}
#             for head in header:
#                 conc[head] = []
#             for row in output[1:]:
#                 for col, head in enumerate(header):
#                     conc[head].append(row[col])
#             return conc
#         conc = get_selected_output(phreeqc)
#         mineral_species = {}
#         ionic_species = {}
#         for elem in titi_brgm.keys():
#             mineral_species[elem] = conc[elem][1]
# #        mineral_species['KatoiteSi1'] = conc['Katoitesi1'][1]
#         elem_ionic = [elem for elem in conc if 'mol/kgw' in elem]
#         for elem in elem_ionic:
#             ionic_species[str(elem[:-9])] = conc[elem][1]
#         toto = phreeqc.get_selected_output_array()
#         def test_ecart(titi_brgm, conc):
#             for elem in titi_brgm.keys():
#                 if titi_brgm[elem] > 0:
#                     if np.abs(((titi_brgm[elem]*1000.)-conc[elem][1])/(titi_brgm[elem]*1000.)) > 0.1:
#                         print "Warning! The relative error with respect to the concentrations"
#                         print "is greater than 10% for: "+elem
#                         print str(titi_brgm[elem]*1000.)+" "+str(conc[elem][1])
#                         print np.abs(((titi_brgm[elem]*1000.)-conc[elem][1])/(titi_brgm[elem]*1000.))
#                 elif conc[elem][1] > 0:
#                     if np.abs(((titi_brgm[elem]*1000.)-conc[elem][1])/conc[elem][1]) > 0.1:
#                         print "Warning! The relative error with respect to the concentrations"
#                         print "is greater than 10% for: "+elem
#                         print str(titi_brgm[elem]*1000.)+" "+str(conc[elem][1])
#                         print np.abs(((titi_brgm[elem]*1000.)-conc[elem][1])/conc[elem][1])
# #        test_ecart(titi_brgm, conc)
#         return mineral_species, ionic_species
    
    def fracvolsolid(self,result_hydration):
        fracvol_solid = {}
        for elem in result_hydration:
            if elem not in ['bigcapillaryvoids','anhydre','A','SS','CCb']:
                fracvol_solid[elem] = result_hydration[elem] / (1-self.porosite)
        return fracvol_solid
    
    def hydration_equilibrium(self):
        #compo_hydrat = self.compo_mat_hydrat(self.degre_hydratation)
        #init_minerals_hydrat = self.convert_hydrat_thermoddem(compo_hydrat)
        #fracvol_solid = self.fracvolsolid(self.result_hydration['fracvol'])
        init_minerals = bd_materiau_hydrat.minerals_in[self.nom_mat]#self.convert_hydrat_thermoddem(fracvol_solid)
        print(init_minerals)
        
        def calcul_Na_K_solution(species):
            Na2O = sum([self.formulation['binder'][elem]['compo']['composition']['Na2O'] for elem in self.formulation['binder']])
            K2O = sum([self.formulation['binder'][elem]['compo']['composition']['K2O'] for elem in self.formulation['binder']])
            Cl = sum([self.formulation['binder'][elem]['compo']['composition']['Cl'] for elem in self.formulation['binder']])
            e_c = sum([self.formulation['binder'][elem]['kg'] for elem in self.formulation['binder']])
            M_Na2O = 61.98
            M_K2O = 94.2
            M_Cl = 35.45
            species['na+'] = 2 * Na2O / e_c / M_Na2O * 1000.
            species['k+'] = 2 * K2O / e_c / M_K2O * 1000.
            species['cl-'] = 1 * Cl / e_c / M_Cl * 1000.
            return species
        
#         def volume_fraction_minerals(init_minerals_tmp):
#             '''Computes the volume of each mineral species per unit solid volume from
#              the mineral species quantities calculated by the hydration model
#              '''
#         
#             init_minerals = {}
#             for elem in init_minerals_tmp.keys():
#                 #print elem, conversion_species.thermoddem_JFB[elem]
#                 molar_volume = hydrationDIM_CTOA.d_hydrate[conversion_species.thermoddem_JFB[elem]]['v']
#                 init_minerals[elem] = init_minerals_tmp[elem]*molar_volume
# #                 if tmp_value > 0:
# #                     init_minerals[conversion_species.phreeqc_thermoddem[elem]] = tmp_value#init_minerals_tmp[elem]#tmp_value#
# #                 else:
# #                     init_minerals[conversion_species.phreeqc_thermoddem[elem]] = 0.0
#             print init_minerals
#             volume_granulats = sum([self.formulation['granulats'][elem]['kg']/self.formulation['granulats'][elem]['nature']['densite']
#                                      for elem in self.formulation['granulats']])
#             total_volume_solid = volume_granulats +\
#             sum([self.result_hydration['compo'][el]*1000.*hydrationDIM_CTOA.d_anhyd[el]['v'] for el in hydrationDIM_CTOA.d_anhyd.keys()]) +\
#             sum([self.result_hydration['compo'][el]*1000.*hydrationDIM_CTOA.d_gypsum[el]['v'] for el in hydrationDIM_CTOA.d_gypsum.keys()]) +\
#             sum([self.result_hydration['compo'][el]*1000.*hydrationDIM_CTOA.d_hydrate[el]['v'] for el in hydrationDIM_CTOA.d_hydrate.keys()])
#             #print "Total solid volume: ",total_volume_solid
#             for elem in init_minerals.keys():
#                 #print init_minerals[elem]
#                 if elem == 'Monosulfoaluminate':
#                     init_minerals[elem] = init_minerals[elem] / total_volume_solid #* 0.75
#                 else:
#                     init_minerals[elem] = init_minerals[elem] / total_volume_solid
#             return init_minerals
#         
#         init_minerals = volume_fraction_minerals(init_minerals_hydrat)
        default_value = 0.8856e-16
        default_pH = 13.37
        species = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':0.3790E-13,'ctotal':-0.4295E+00},
              'ca+2':{'guess':0.3931E-03,'ctotal':0.9171E-03},'so4-2':{'guess':0.3191E-03,'ctotal':0.4763E-02},
              'co3-2':{'guess':0.6823E-18,'ctotal':0.2480E-17}, 'hsio3-':{'guess':0.4787E-04,'ctotal':0.4787E-05},
              'k+':{'guess':0.1282E+00,'ctotal':0.1572E+00},'na+':{'guess':0.2429E-00,'ctotal':0.2721E-00},
              'mg+2':{'guess':0.1925E-10,'ctotal':0.6865E-09},'al+3':{'guess':0.9037E-33,'ctotal':0.4965E-03},
              'cl-':{'guess':0.2496E-13,'ctotal':0.2840E-13}}
#         species = {'h2o':1.0,'h+':10**(-default_pH),'ca+2':default_value,'so4-2':default_value,'hsio3-':default_value,
#                    'mg+2':default_value,'al+3':default_value,'co3-2':default_value,'fe+3':default_value}
        init_species = calcul_Na_K_solution(species)
        species_out, minerals_out = toughreact.calcul_equilibre_toughreact_minerals(init_minerals,init_species,self.temperature)
        #Conversion to solid volume fraction of the mineral quantities (toughreact returns a total volume fraction)
        for elem in minerals_out:
            minerals_out[elem] = minerals_out[elem]/(1-self.porosite)
        return species_out, minerals_out

# class Expe:
#     def __init__(self,formulation,duree,compo,tps_cure,temp,HR,Patm,hauteur_maree,tps_expo):
#         self.formulation = formulation
#         self.duree = duree
#         self.compo = compo
#         self.tps_cure = tps_cure
#         self.temp = temp
#         self.HR = HR
#         self.Patm = Patm
#         self.hauteur_maree = hauteur_maree
#         self.tps_expo = tps_expo
if __name__ == '__main__':
    ###########################################################################
    #Input data
    compo_ciment = {}
    #compo_ciment['Maissa']={"C3S":67.8/100.,"C2S":16.6/100.,"C3A":4./100.,
    #"C4AF":7.2/100.,"CSbH2":2.8/100.}
    compo_ciment['Maissa']={"C3S":64.2178/100.,"C2S":12.33/100.,"C3A":1.49/100.,"C4AF":14./100.,"CSbH2":2.8/100.}
    #Van-Quan : {"C3S":64.2178/100.,"C2S":12.33/100.,"C3A":1.49/100.,"C4AF":14./100.,"CSbH2":2.8/100.}
    #
    
    nom_beton = 'BO'
    # Concrete mix designs
    formulation = {}
    #formulation[nom_beton]={"g12.5/20":733.,"g5/12.5":459.,"g0/5":0.,"s0/4":744.,"c":353.,"e":172.,\
    # "e/ctot":0.5,"e/c":0.49,"g/c":5.48,"phiair":0.012}
    formulation[nom_beton]={"g12.5/20":0.,"g5/12.5":0.,"g0/5":0.,"s0/4":1365.,"c":676.,"e":264.,"e/ctot":0.4,"e/c":0.39,"g/c":2.019,"phiair":0.}
    #Van-Quan : {"g12.5/20":0.,"g5/12.5":0.,"g0/5":0.,"s0/4":1365.,"c":676.,"e":264.,\
    # "e/ctot":0.4,"e/c":0.39,"g/c":2.019,"phiair":0.}
    #
    densite = formulation[nom_beton]["g12.5/20"] +\
                 formulation[nom_beton]["g5/12.5"] +\
                 formulation[nom_beton]["g0/5"] +\
                 formulation[nom_beton]["s0/4"] +\
                 formulation[nom_beton]["c"]
    
    temperature = 20 #material temperature in degrees Celsius
    age_cure = 365. #in days
    mesures_ref = {'permeabilite':4.00e-20,'porosite':0.16}
    krl_model = {'type':'genuchten','params':[4.396e-01,0.0,1.0,0.0]}
    pc_model = {'type':'genuchten','params':[4.396e-01,0.0,5.369e-08,9.381e7,1.0]}
    modele_mat = {}
    modele_mat[nom_beton]={'krl':krl_model,'pc':pc_model, 'cl_adsorption_csh':1.386e-2}
    tortuosite = 1.342e-2
    ###########################################################################
    
    ###########################################################################
    #Test constructeur
    beton = MateriauCimentaire(nom_beton, formulation[nom_beton], densite, 
                               compo_ciment['Maissa'], age_cure, temperature,
                                mesures_ref, modele_mat[nom_beton], tortuosite)
    ###########################################################################
    #Test fonction hydratation
    tutu1, tutu2 = beton.hydration(0.1,3600*24)
    
    ###########################################################################
    #Test class display
    beton.ecriture_class()
    
    ###########################################################################
    #Test: return of mineral quantities as a function of hydration degree
    titi = beton.compo_mat_hydrat(1)
    
    dbase = '/Users/anthonysoive/Documents/CR_Nantes_2014_11/02-Modelisation/durabilite_marnage/durability/thermoddem.dat'
    conc_minerals, conc_species = beton.calcul_especes_ioniques_phreeqc(dbase)
    ###########################################################################
    
    #Test of the write to tough2