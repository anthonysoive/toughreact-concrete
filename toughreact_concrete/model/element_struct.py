"""
Created on Tue Sep 29 17:49:46 2015

@author: anthonysoive
"""
import math
import os
import shutil
import sys

#PyTOUGH
import t2data
import t2grids
import t2incons
from sympy import erfinv

import toughreact_concrete.materiau.mat_ciment as mat_ciment
import toughreact_concrete.model.cond_limit  #,  toughreact_concrete.model.hydration_data
import toughreact_concrete.model.data.maree as maree
import toughreact_concrete.model.data.physical_const as physical_const

#import  toughreact_concrete.model.conversion_species as conversion_species
import toughreact_concrete.model.post as post

#import  toughreact_concrete.model.t2R_chemical as t2R_chemical
import toughreact_concrete.model.t2R_savechem as t2R_savechem
import toughreact_concrete.model.toughreact as toughreact
from toughreact_concrete.model.conversion_species import *
from toughreact_concrete.model.mesh import Mesh  # noqa: F401 — re-exported for backwards compat


class Model:
    def __init__(self, mesh):
        self.mesh = mesh
        self.dat=t2data.t2data()
        self.dat.title = 'Test'
        self.dat.type = 'TOUGH2'
        self.dat.grid=t2grids.t2grid().fromgeo(self.mesh.geo)
        self.list_blk_bc = self._affect_block()
        
        self.list_blk_water = []
        self.list_material = []
        self.list_cementitious_material = []
        self.dat.incon = {}
        self.BC_struct = {'top':None, 'bottom':None, 'left':None, 'right':None}
        self.database = ''
        self.database_phreeqc = ''
        self.minerals = {}
        self.species = {}
        self.nb_especes = 0
        self.nb_mineraux = 0
        self.pitzer = False
        self.kinetics = True
        self.update_porosity = False
        self.complexation = True
        self.init_minerals = False
        self.temperature_isotherme = 0.0 #pour calcul eos9
        self.current_time = 0.0
        self.exe = ''
        self.pas_temps_calcul = 3600.
        #self._initialize_PyTOUGH(self)
    
    def _add_mesh(self):
        pass
        
    
    def _affect_block(self):
        list_block = {}
        for elem in self.mesh.CL:
            for element in self.mesh.CL[elem]:
                if float(self.mesh.num_elem['Z']) > 40:
                    if element == 'left':
                        list_block['left'] = [self.dat.grid.block[self.mesh.geo.layerlist[i].name+self.mesh.geo.columnlist[0].name]
                                      for i in range(1,len(self.mesh.geo.layerlist))]
                    if element == 'right':
                        list_block['right'] = [self.dat.grid.block[self.mesh.geo.layerlist[i].name+self.mesh.geo.columnlist[-1].name]
                                      for i in range(1,len(self.mesh.geo.layerlist))]
                    if element == 'top':
                        list_block['top'] = [self.dat.grid.block[self.mesh.geo.layerlist[1].name+self.mesh.geo.columnlist[i].name]
                                      for i in range(len(self.mesh.geo.columnlist))]
                    if element == 'bottom':
                        list_block['bottom'] = [self.dat.grid.block[self.mesh.geo.layerlist[-1].name+self.mesh.geo.columnlist[i].name]
                                      for i in range(len(self.mesh.geo.columnlist))]
                else:
                    if element == 'left':
                        list_block['left'] = [self.dat.grid.block[self.mesh.geo.columnlist[0].name+self.mesh.geo.layerlist[i].name] 
                                              for i in range(1,len(self.mesh.geo.layerlist))]
                    if element == 'right':
                        list_block['right'] = [self.dat.grid.block[self.mesh.geo.columnlist[-1].name+self.mesh.geo.layerlist[i].name] 
                                               for i in range(1,len(self.mesh.geo.layerlist))]
                    if element == 'top':
                        list_block['top'] = [self.dat.grid.block[self.mesh.geo.columnlist[i].name+self.mesh.geo.layerlist[1].name] 
                                             for i in range(len(self.mesh.geo.columnlist))]
                    if element == 'bottom':
                        list_block['bottom'] = [self.dat.grid.block[self.mesh.geo.columnlist[i].name+self.mesh.geo.layerlist[-1].name] 
                                                for i in range(len(self.mesh.geo.columnlist))]

        list_block_wo_maree = [self.mesh.CL[elem] for elem in self.mesh.CL if not elem == 'maree']
        #list_block_maree = [self.mesh.CL[elem] for elem in ]
        list_elem_block_maree = []
        if len(self.mesh.CL) > 0:
            for elem in self.mesh.CL['maree']:
                list_elem_block_maree += list_block[elem]
            if 'infini' in self.mesh.CL:
                for elem in self.mesh.CL['infini']:
                    for element in list_elem_block_maree:
                        if element in list_block[elem]:
                            list_block[elem].remove(element)
        return list_block
    
#     atmos    2 2300.    0.2000    0.0000E  30.0000E  30.0000E  3 1.660    0.1000E+31
#                         0.0000
#     1     0.2000    0.3000    0.7000    0.8000
#     1                          1.000

    def write_tough2_atmos(self, humidite_relative, temperature):
        #Writing hydraulic parameters
        self.atmos = t2grids.rocktype(name='atmos',nad=2,density=1.0e50,\
        porosity=0.999,permeability=3*[1.0e-17])
        self.atmos.relative_permeability['type']=1
        self.atmos.relative_permeability['parameters']=[0.1,0.0,1.0,0.1]
        #self.atmos.relative_permeability['type']=5
        #self.atmos.relative_permeability['parameters']=[]
#        mat_tmp.capillarity['type']=7
#        mat_tmp.capillarity['parameters']=self.pc_model['params']
        self.atmos.capillarity['type']=1
        print("Capillary pressure : ",-physical_const.rho_wl*physical_const.R*(temperature + 273.15)/\
        physical_const.M_w * math.log(humidite_relative/100.0))
        self.atmos.capillarity['parameters'] = [0.0,0.0,1.0]
        #self.atmos.capillarity['parameters'] = [-physical_const.rho_wl*physical_const.R*(temperature + 273.15)/\
        #physical_const.M_w * math.log(humidite_relative/100.0), 0.000E+00, 1.0]
        self.atmos.tortuosity = 0.0
        self.dat.grid.add_rocktype(self.atmos)
        return
    
    def write_tough2_water(self, humidite_relative, temperature):
        #Writing hydraulic parameters
        self.water = t2grids.rocktype(name='water',nad=2,density=1.0e50,\
        porosity=0.999,permeability=3*[1.0e-17])
        self.water.relative_permeability['type']=5
        self.water.relative_permeability['parameters']=[]
#        mat_tmp.capillarity['type']=7
#        mat_tmp.capillarity['parameters']=self.pc_model['params']
        self.water.capillarity['type']=1
        self.water.capillarity['parameters'] = [-physical_const.rho_wl*physical_const.R*(temperature + 273.15)/\
        physical_const.M_w * math.log(humidite_relative/100.0), 0.000E+00, 0.9999E+00]
        self.water.tortuosity = 1.0
        self.dat.grid.add_rocktype(self.water)
        return

    def add_material(self, material, complexation):
        '''Adds an object of type MateriauCimentaire.
        If the hydration degree of the material is greater than 0.9, it is considered
        that the material no longer evolves. Otherwise, each mesh element
        is associated with a material initially identical to all others.
        The evolution of each material's properties is then specific to each element.

        Also adds the atmos material with the same properties but with
        a porosity on the order of 1'''
        self.complexation = complexation
        print("degré d'hydratation du matériau : ",material.degre_hydratation)
        if material.degre_hydratation > 0.2:
            self.dat = material.write_toughreact(self.dat, complexation)
            for blk in self.dat.grid.blocklist:
                blk.rocktype = material
                self.list_material.append(material)
                self.list_cementitious_material.append(material)
        else:
            for i, blk in enumerate(self.dat.grid.blocklist, start=1):
                nom_mat = 'B%4d'%i
                tmp_beton = mat_ciment.MateriauCimentaire(nom_mat)
                tmp_beton.formulation = material.formulation
                tmp_beton.porosite = material.porosite
                tmp_beton.indicateurs_deduits = material.indicateurs_deduits
                cs = 0.546 #concentration en surface (eau de mer)
                hydration_stop_date = (blk.centre[0]/(2*erfinv(1-0.001/cs)))**2 / material.indicateurs_deduits['D_eff']
                print("Position de l'élément [m] : ",blk.centre[0])
                print("Arrêt de l'hydratation [jours] : ",hydration_stop_date/3600/24)
                tmp_beton.hydratation(hydration_stop_date)
                print("degré d'hydratation : ",tmp_beton.degre_hydratation)
                self.dat = tmp_beton.write_toughreact(self.dat, complexation)
                blk.rocktype=tmp_beton
                self.list_material.append(tmp_beton)
                self.list_cementitious_material.append(material)
        return
        
    def add_bc(self, BC, location):
        for elem in location:
            if self.BC_struct[elem]:
                print("Cet endroit contient déjà une condition limite !")
                print("Arrêt de la simulation.")
            else:
                #partie tough2
                self.BC_struct[elem] = BC
#                 for blk in self.list_blk_bc[elem]:
#                     blk.volume = 1.0  # Volumes "infinis" dans la colonne limite
                if BC.type_cond != 'infini':
                    if BC.type_cond == 'maree':
                        for blk in self.list_blk_bc[elem]:
                            blk.volume = 1.0e52
                        #Addition of the "materials" atmos and water
                        self.write_tough2_atmos(BC.humidite_relative_ext[0], BC.temperature_ext[0])
                        self.write_tough2_water(BC.humidite_relative_ext[0], BC.temperature_ext[0])
                        #Addition of the "material" REFCO for eos9
    #                 self.atmos.humidite_relative = BC.humidite_relative_ext[0]
    #                 self.atmos.temperature = BC.temperature_ext[0]
    #                 self.atmos.P_atm = BC.P_atm[0]
                    for blk in self.list_blk_bc[elem]:
                        if BC.hauteur_maree[0] < 1e-3:
                            blk.rocktype = self.atmos
                        else:
                            blk.rocktype = self.water
                        #blk.rocktype = self.water #self.dat.grid.blocklist[new_index].rocktype #
                        self.dat.incon[str(blk)] = [None, self.input_BC_maree(self.eos,BC.P_atm[0],BC.temperature_eau[0])]
        for blk in self.dat.grid.blocklist:
            if blk.centre[0] < abs(self.mesh.len_eau)+self.mesh.ep_couche_limite:
                if BC.hauteur_maree[0] < 1e-3:
                    blk.rocktype = self.atmos
                else:
                    blk.rocktype = self.water
                self.list_blk_water.append(blk)
                #partie react...

    def add_ic(self):
        pass
    
    def _init_file(self):
        '''Defines the results directory and deletes any existing toughreact files
        if applicable'''
        self.rep_out = "OUTPUT"
        if os.path.exists(self.rep_out):
            shutil.rmtree(self.rep_out)
        os.mkdir(self.rep_out)
        if os.path.isfile("INCON") :
            os.remove("INCON")
        if os.path.isfile("SAVE") :
            os.remove("SAVE")
        if os.path.isfile("inchem") :
            os.remove("inchem")
        if os.path.isfile("savechem") :
            os.remove("savechem")
    
    def _initialize_PyTOUGH(self):
        self.tough_params()
        self.solve_method()
  

    def solve_method(self):
        _EOS_MULTI = {
            'eos3':  {'num_components':2,'num_equations':3,'num_phases':2,'num_secondary_parameters':8},
            'eos4':  {'num_components':2,'num_equations':3,'num_phases':2,'num_secondary_parameters':8},
            'eco2n': {'num_components':3,'num_equations':4,'num_phases':3,'num_secondary_parameters':8},
            'eos7':  {'num_components':3,'num_equations':4,'num_phases':2,'num_secondary_parameters':8},
            'eos9':  {'num_components':1,'num_equations':1,'num_phases':1,'num_secondary_parameters':6},
        }
        self.dat.multi = _EOS_MULTI[self.eos]

    
    def tough_params(self):
        self.dat.start=True
        self.dat.diffusion=3*[[physical_const.D_air_gaz,physical_const.D_air_eau]]
#        #mop=[1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,3,0,0,0,0,3,0,0,0]#Debug
        if self.pitzer:
            #self.dat.mop=[0,0,0,0,0,0,0,0,0,0,0,2,0,1,1,3,0,0,0,0,3,0,0,0]
            self.dat.mop=[0,0,0,0,0,0,0,0,0,0,0,2,2,0,2,0,4,0,1,0,0,5,0,0,0]
        else:
            if self.eos == 'eos4':
                self.dat.mop=[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,3,0,0,0,0,0,0,0,0]
            else:
                self.dat.mop=[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,3,0,0,0,0,0,0,0,0]
        #EO3-like intialization
        #self.dat.mop=[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,3,0,0,2,0,3,0,0,0]#Debug
        #self.dat.mop=[1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,3,0,0,0,0,3,0,0,0]
        #'max_timestep':500.,
        self.dat.parameter={'print_level':0,'max_timesteps':9999,'max_iterations':20,
        'print_interval':9999,'option':self.dat.mop,\
        'tstart':0.0,'tstop':3.6e+03,'const_timestep':0.0,\
        'print_block':'  a 1','gravity':9.81,'timestep_reduction':4.0,'scale':1.0,\
        'relative_error':1e-5,'absolute_error':1.0,'upstream_weight':1.0,'newton_weight':1.0,\
        'default_incons':self.list_material[0].input_IC(self.eos)}
        self.dat.parameter['max_timestep'] = self.pas_temps_calcul
        self.dat.solver={'type':3,'z_precond':'Z1','o_precond':'O0','relative_max_iterations':0.1,\
        'closure':1e-6}
    
    def _save_mesh(self):
        '''Saves the abscissa file to the results directory'''
        if  os.path.isfile("OUTPUT/Pos_x.txt"):
            os.remove("OUTPUT/Pos_x.txt")
        self.mesh.write_mesh_x()
    
    def calcul_equilibre_hydratation(self):
        '''Equilibrium calculation of mineral phases from the hydration calculation
        to obtain the concentration of ionic species in solution,
        at the desired temperature.
        The calculation is performed only once on the initial cementitious material.'''
        #Hydration calculation
        compo_hydrat = self.list_material[0].compo_mat_hydrat(self.list_material[0].degre_hydratation)
        #Conversion of mineral species names to match the database
        #used in Toughreact
        init_minerals_hydrat = self.list_material[0].convert_hydrat_thermoddem(compo_hydrat)
    
    def calcul_seawater(self, temperature):
        '''Calculates the ionic composition of seawater as a function of temperature.
        This calculation is based on an ionic composition at 20°C in the Atlantic Ocean'''
        pass

    def _initialize_solve(self, echeance, time_output): 
        '''Initial calculation from initial conditions and boundary conditions.
        Returns one (or more) result file(s) that can be used as
        initial conditions for a new calculation'''
        self._init_file()        
        self._initialize_PyTOUGH()
        
        dict_minerals_database = toughreact.lecture_database(self.database)
        
        ###############################################################################
        #Equilibrium calculation of mineral phases from the hydration calculation
        #to obtain the concentration of ionic species in solution,
        #at the desired temperature
        if self.list_material[0].minerals:
            #On enlève les espèces solides suivantes :
            list_minerals_del = [#'ANHYDRITE','CHRYSOTILE','GIBBSITE',
                                 'MAGNESITE','DOLOMITE(ORDERED)','FE(OH)3', 'C3AFS0.84H4.32'
                                 ]#,'MONOCARBOALUMINATE','CALCITE','ARAGONITE']#,,'GYPSUM','BRUCITE','KUZEL_SALT',,'C3AS0.84H4.32' 'C3FS1.34H3.32','FE(OH)3'
            tmp_del_minerals = []
            material_species = []
            tmp_del_species = []
            tmp_no_del_species = []
            for elem in self.list_material[0].minerals.keys():
                convert_mineral = mineral_database[self.database][elem].upper()
                if elem.upper() in list_minerals_del:#list of minerals and ions (by comparison with ions from remaining minerals) to remove
                    tmp_del_minerals.append(elem)
                    tmp_del_species += list(dict_minerals_database[convert_mineral]['reaction'])#list of ions contained in the minerals to remove
                else:
                    tmp_no_del_species += list(dict_minerals_database[convert_mineral]['reaction'])#list of ions contained in the minerals to keep
                if convert_mineral.upper() in dict_minerals_database:
                    material_species += list(dict_minerals_database[convert_mineral]['reaction'])
            
            material_species = list(set(material_species + ['H+', 'H2O']))
            list_species_del = list(set(tmp_del_species) - set(tmp_no_del_species) - set(['H+', 'H2O']))
            for elem in material_species:
                if elem not in self.list_material[0].species:
                    self.list_material[0].species[elem] = {'guess':1e-20,'ctotal':1e-20}
            # list_species_del = [x for x in self.list_material[0].species if x not in set(material_species)]
            # list_species_del.remove('Na+')
            # list_species_del.remove('K+')
            # for elem in list(set(material_species)):
            #     self.list_material[0].species[elem] = 0.0
            #Removing minerals and ions
            for elem in tmp_del_minerals:
                del self.list_material[0].minerals[elem]
            #     if elem.upper() in dict_minerals_database:
            #         tmp_species += list(dict_minerals_database[elem]['reaction'])
            # tmp_species = list(set(material_species))
            # tmp_species += ['H+', 'H2O']
            #Removing the following elements
            list_species_del += []#'FE+3'
            # tmp_species = []
            # for elem in self.list_material[0].species.keys():
            #     if elem.upper() in list_species_del:
            #         tmp_species.append(elem)
            for elem in list_species_del:
                if elem in self.list_material[0].species.keys():
                    del self.list_material[0].species[elem]
            #self.list_material[0].species, self.list_material[0].minerals = toughreact.calcul_equilibre_toughreact_minerals(self.list_material[0].minerals,self.list_material[0].species)
            # First pass: no complexation, to initialise species
            init_species_inter, init_minerals = toughreact.calcul_equilibre_mineraux(
                self.list_material[0], self.database, False, True, False)
            self._apply_equilibre_species(init_species_inter)
            # Two iterative passes with full settings (convergence)
            for _ in range(2):
                init_species_inter, init_minerals = toughreact.calcul_equilibre_mineraux(
                    self.list_material[0], self.database, self.complexation, self.kinetics, False)
                self._apply_equilibre_species(init_species_inter)
        else:
            init_species_inter, init_minerals = self.list_material[0].hydration_equilibrium()
        
        #Retrieving tidal height and water temperature information
        list_BC_struct_maree = [[],[]]
        for location in self.BC_struct:
            if (self.BC_struct[location] and self.BC_struct[location].type_cond != 'infini'):
                if self.BC_struct[location].type_cond == 'maree':
                    h = int(round(self.BC_struct[location].hauteur_maree[0] * \
                    self.mesh.num_elem['Z']/(self.mesh.hauteur),0))
                    #self.mesh.num_elem['Z']/(self.mesh.dims['Z']),0))
                    #List of submerged blocks
                    list_BC_struct_maree[0] += self.list_blk_bc[location][-h:]#[:]#
                    #List of emerged blocks
                    list_BC_struct_maree[1] += self.list_blk_bc[location][:-h]#[]#
                    temperature_eau = float(self.BC_struct[location].temperature_eau[0])
                    #self.BC_struct[location].seawater_species = toughreact.calcul_equilibre_bnd_solution(temperature_eau,len(init_species_inter))
                    self.BC_struct[location].bnd_solution[0]['temperature'] = temperature_eau
                    bnd_species = toughreact.calcul_equilibre_bnd_solution(self.BC_struct[location].bnd_solution[0],
                                                                           self.list_material[0].porosite,
                                                                           self.database)
                    tmp_convert_species = {}
                    for elem in bnd_species['composition']:
                        elem_database = convert_ionic_species(elem, self.database)
                        tmp_convert_species[elem_database] = {'guess':bnd_species['composition'][elem]['guess'],
                                                              'ctotal':bnd_species['composition'][elem]['ctotal']
                                                              }
                    bnd_species['composition'] = tmp_convert_species
                    Pp_co2 = self.BC_struct[location].Pp_co2
                    #bnd_species = self.BC_struct[location].species#self.BC_struct[location].seawater_species
                else:
                    bnd_species = {}
                    Pp_co2 = self.BC_struct[location].Pp_co2
        
        if self.pitzer:
            del init_minerals['Jennite']
            del init_minerals['C3AH6']
            del init_species_inter["HSiO3-"]
            if 'HSiO3-' in bnd_species['composition']:
                del bnd_species['composition']["HSiO3-"]
        
        #liste_especes=list(init_species_inter.keys()) + list(set(bnd_species['composition'].keys()) - set(init_species_inter.keys()))
        liste_especes=list(set(list(self.list_material[0].species.keys()) + list(bnd_species['composition'].keys())))
        for elem in liste_especes:
            print(elem)
            if elem not in self.list_material[0].species.keys():
                self.list_material[0].species[elem] = {'guess':0.1247E-16,'ctotal':0.8863E-16}
            if elem not in bnd_species['composition'].keys():
                bnd_species['composition'][elem] = {'guess':1E-20,'ctotal':1E-20}
                
#        list_minerals_add = ['friedel_salt','kuzel_salt','Hydrotalcite','Ettringite','Monosulfoaluminate','Gibbsite',
#                                  'Chrysotile','Brucite','Jennite','Tobermorite',
#                                  'Anhydrite','Gypsum','Portlandite','Sepiolite']
#        for elem in list_minerals_add:
#            if not elem.upper() in [tmp.upper() for tmp in init_minerals.keys()]:
#                init_minerals[elem] = 0.0
        
        #list_blk_limit = [blk for blk in self.dat.grid.blocklist if blk.rocktype == self.atmos]
        
        ###############################################################################
        #Writing the flow.inp file for the Toughreact calculation
        self.dat.parameter['tstop'] = echeance
        self.dat.output_times = {'num_times_specified':len(time_output),'time':time_output}
        #self.dat.incon[str(blk)] = [None, self.input_BC_maree(self.eos,BC.P_atm[0],BC.temperature_eau[0])]
        self.dat.write('flow.inp')
        self._patch_flow_inp()

        ###############################################################################
        self._save_mesh()
        
        init_species_inter,init_minerals=toughreact.calcul_transport_reactif(self.list_material[0],
                                                                             bnd_species,
                                                                             self.database,
                                                                             self.complexation,
                                                                             self.kinetics,
                                                                             self.update_porosity,
                                                                             self.exe)

        self.minerals = init_minerals
        self.species = init_species_inter
        self.nb_especes = len(self.species)
        self.nb_mineraux = len(self.minerals)
        
    def _delete_ic(self):
        '''Removes initial conditions from the flow and solute files
        in order to continue a previously performed calculation (restart).'''
        #######################For the flow part
        #Removal of default values for initial and boundary conditions
        self.dat.parameter['default_incons'] = None
        self.dat.incon = {}
    
    def ClausiusClapeyron(self,temperature):
        '''Function to calculate the saturating vapour pressure as a function of temperature'''
        #reference pressure
        p0 = 1.01e5#Pascal
        #reference temperature
        T0 = 373#Kelvin
        #universal ideal gas constant
        R = 8.314#J/mol K
        #latent heat of vaporisation
        Hvap = 40.7e3#J/mol
        return p0*math.exp(-Hvap/R*(1/temperature - 1/T0))
    
    def Flux_evaporation(self,temperature, humidite_relative):
        '''Calculates the evaporation flux as a function of the vapour pressure difference between the atmosphere and the liquid'''
        ######evaporation flux
        #wind speed
        V = 0#m/s
        #water evaporation coefficient
        E = 2.188e-8+1.859e-8*V#kg.m2/s/Pa
        return E *self.ClausiusClapeyron(temperature)*(1-humidite_relative/100)

    def input_BC(self, eos, temperature_ext, humidite_relative_ext, P_atm):
        #calcul de la pression partiel d'air
        Pa = P_atm - humidite_relative_ext/100.0*physical_const.Psat(temperature_ext + 273.15)
        result = {}
        result['eos3'] = [P_atm, 1.0, temperature_ext]#[P_atm, 10.99, temperature_ext]
        result['eos4'] = [P_atm, temperature_ext, Pa]#[P_atm, 0.000015, temperature_ext]#S_g, Pa]
        #Fraction massique d'air dans l'air
        air_gas = 1-0.0035
        result['eco2n'] = [P_atm, 0., 1., temperature_ext]#0.991, self.temperature]
        result['eos7'] = [P_atm, 0., air_gas, temperature_ext]
        result['eos9'] = [0.00001]
        return result[eos]

    def input_BC_maree(self, eos, P_atm, temperature_eau):
        #############################
        #WARNING IC and BC must be distinguished (temperatures and RH are not the same)
        #############################
        result = {}
        result['eos3'] = [P_atm, 10.01, temperature_eau]#[P_atm, 0.99, temperature_eau]
        result['eos4'] = [P_atm, temperature_eau, 1.0e4]#[P_atm, 0.000015, temperature_eau]#S_g, Pa]
        result['eco2n'] = [P_atm, 0.0355, 5.e-4, temperature_eau]#0.0355, 1.e-5, T - 273.15]#10.+S_g, T - 273.15]#10., 0.00001, T - 273.15]
        #result['eos7'] = [self.P_atm, 0.0355, 10.+S_g, temperature_eau]#0.0355, 1.e-5, T - 273.15]#10.+S_g, T - 273.15]#10., 0.00001, T - 273.15]
        result['eos9'] = [101300.0]#[0.999, temperature_eau]
        return result[eos]

    def _update_bc(self, i, time_input, time_output):
        '''Modifies the boundary conditions in the flow and solute files'''
        self.dat.clear_generators()
        self.dat.incon = {}
        inc=t2incons.t2incon("SAVE")
        for location in self.BC_struct:
            if (self.BC_struct[location] and self.BC_struct[location].type_cond != 'infini'):
                self.atmos.humidite_relative = self.BC_struct[location].humidite_relative_ext[i]
                self.atmos.temperature = self.BC_struct[location].temperature_ext[i]
                self.atmos.P_atm = self.BC_struct[location].P_atm[i]
                if self.BC_struct[location].type_cond == 'maree':
                    inc = self._update_bc_maree(location, i, inc)
                else:
                    for blk in self.list_blk_bc[location]:
                        #calcul de la pression partiel d'air
                        T = self.atmos.temperature + 273.15
                        Pa = self.atmos.P_atm - self.atmos.humidite_relative/100.0*self.atmos.Psat(T)
                        inc[str(blk)] = [self.atmos.P_atm, self.atmos.temperature, Pa]
                        #print inc[str(blk)]
        #inc.timing['tstart'] = time_input[-1]
        #inc.timing['sumtim'] = time_input[-1]
        inc.write("INCON",reset=False)
        
        self.dat.grid.rocktype['atmos'].capillarity['parameters'] = [-physical_const.rho_wl*physical_const.R*(self.atmos.temperature + 273.15)/\
        physical_const.M_w * math.log(self.atmos.humidite_relative/100.0), 0.000E+00, 0.999E+00]
        self.dat.output_times = {'num_times_specified':len(time_output),'time':time_output}
        #self.dat.parameter['tstart'] = time_input[-1]#0.0#self.dat.parameter['tstop']
        self.dat.parameter['max_timestep'] = 3600.0
        self.dat.parameter['tstop'] = time_output[-1]-time_input[-1]#time_output[-1]#86400#time_output[-1]-self.dat.parameter['tstop']#
        #print(self.dat.parameter['tstop'])
        self.dat.write('flow.inp')
        self._patch_flow_inp()

    def _update_bc_maree(self, location, incr, inc):
        #########Calculation of submerged elements
        #discretised height below which elements are submerged
        BC = self.BC_struct[location]
        
        BC.bnd_solution[incr]['temperature'] = BC.temperature_eau[incr]
        bnd_species = toughreact.calcul_equilibre_bnd_solution(BC.bnd_solution[incr],
                                                               self.list_material[0].porosite,
                                                               self.database)#self.list_material[0].mesures_expe['P_eau']
        
        h = int(round(BC.hauteur_maree[incr]*self.mesh.num_elem['Z']/(self.mesh.hauteur),0))
#         self.dat.parameter['tstart'] = 0.0#self.dat.parameter['tstop']
#         self.dat.parameter['tstop'] = BC.increment_maree[incr]#self.dat.parameter['tstop'] + BC.increment_maree[incr]
        #print "hauteur :", h
        self.pip = 0
        if h < self.mesh.num_elem['Z']:
            self.pip= self.mesh.num_elem['Z']-h
        
        for elem in self.list_blk_bc[location][self.pip:]:#list_blk_moul:
            #print "mouillage..."
            #Updating the moisture transfer part (flow.inp and INCON
            self.dat.grid.block[elem.name].rocktype = self.water
            inc[str(elem)] = self.input_BC_maree(self.eos, BC.P_atm[incr], BC.temperature_eau[incr])
            print("Données d'entrée des conditions limites : ", inc)
            print('imbibition')
            if bnd_species['composition']['cl-']['ctotal'] > 0.01:
                print('Chlorures...')
#----------------------------------
#         bnd_species_in = BC.bnd_solution[incr]
#         
#         for elem in bnd_species_in['composition']:
#             if not elem.lower() in ['cl-','na+']:
#                 bnd_species_in['composition'][elem] = self.chemical.init_species[elem.lower()]['ctotal']
#         bnd_species = toughreact.calcul_equilibre_bnd_solution(bnd_species_in,
#                                                                self.list_material[0].mesures_expe['P_eau'],
#                                                                self.database)
#----------------------------------
#         bnd_species_in = {'composition':{},'temperature':BC.temperature_eau[incr]}
#         for elem in bnd_species.keys():
#             bnd_species_in['composition'][elem] = bnd_species[elem]['ctotal']
        
#        for elem in bnd_species['composition'].keys():
#            self.chemical.bnd_species[elem] = bnd_species['composition'][elem]
#        self.chemical.temperature_env = BC.temperature_eau[incr]
#        #print "Ecriture du fichier chemical.inp"
#        self.chemical.write_chemical("chemical.inp", self.pitzer, self.kinetics, self.complexation)
                
        self.correction_boundary_solution(location,bnd_species['composition'])#BC.bnd_solution[incr])
            
        for elem in self.list_blk_bc[location][:self.pip]:#list_blk_sech:
            #print "drying..."
            #print elem.name
            self.dat.grid.block[elem.name].rocktype = self.atmos
            inc[str(elem)] = self.input_BC(self.eos, BC.temperature_ext[incr], BC.humidite_relative_ext[incr], BC.P_atm[incr])
        
        
#         for layer in self.mesh.geo.layerlist[1:]:
#             blockname=self.mesh.geo.block_name(layer.name,self.mesh.geo.columnlist[1].name)
#             gen=t2data.t2generator(name='INF'+layer.name,block=blockname,type='COM1',gx=self.Flux_evaporation((BC.temperature_ext[incr]+273), BC.humidite_relative_ext[incr]))
#             self.dat.add_generator(gen)
        
        #List of submerged blocks
        list_BC_struct_maree = [[],[]]
        list_BC_struct_maree[0] += self.list_blk_bc[location][self.pip:]
        #List of emerged blocks
        list_BC_struct_maree[1] += self.list_blk_bc[location][:self.pip]

        return inc
    
    def correction_concentration(self,previous_savechem):
        detail = False
        savechem = t2R_savechem.t2rsavechem(self.mesh.num_elem['X'],self.nb_especes, self.nb_mineraux,
                                 self.exe,self.pitzer,self.kinetics,
                                 self.complexation,'savechem')
#        pH_derive = savechem.contenu['pH'][-1] - previous_savechem.contenu['pH'][-1]
#        for i in range(len(savechem.contenu['concentration_primary'][0])):
#            gap = savechem.contenu['concentration_primary'][-1][i] - previous_savechem.contenu['concentration_primary'][-1][i]
#            savechem.contenu['pH'][i] = savechem.contenu['pH'][i] - pH_derive
#            if detail == True:
#                print(savechem.contenu['concentration_primary'][-1][i],previous_savechem.contenu['concentration_primary'][-1][i])
#            for j in range(1,len(savechem.contenu['concentration_primary'])):
#                savechem.contenu['concentration_primary'][j][i] = savechem.contenu['concentration_primary'][j][i] - gap#conc_H_derive
#
##         for i in range(len(savechem.contenu['concentration_secondary'][0])):
##             gap = savechem.contenu['concentration_secondary'][-1][i] - previous_savechem.contenu['concentration_secondary'][-1][i]
##             if detail == true:
##                 print(savechem.contenu['concentration_secondary'][-1][i],previous_savechem.contenu['concentration_secondary'][-1][i])
##             for j in range(1,len(savechem.contenu['concentration_secondary'])):
##                 savechem.contenu['concentration_secondary'][j][i] = savechem.contenu['concentration_secondary'][j][i] - gap#conc_H_derive
##         #conc_H_derive = savechem.contenu['concentration_primary'][-1][1] - previous_savechem.contenu['concentration_primary'][-1][1]
        if self.complexation == False:
            complexation_derive_oh = savechem.contenu['concentration_primary'][-1][-2] - previous_savechem.contenu['concentration_primary'][-1][-1]
            complexation_derive_oh1 = savechem.contenu['concentration_primary'][-1][-1] - previous_savechem.contenu['concentration_primary'][-1][-2]
            complexation_derive_UT_oh = savechem.contenu['UT_species'][-1][-2] - previous_savechem.contenu['UT_species'][-1][-1]
            complexation_derive_UT_oh1 = savechem.contenu['UT_species'][-1][-1] - previous_savechem.contenu['UT_species'][-1][-2]
            for elem in range(0, len(savechem.contenu['concentration_primary'])):
                savechem.contenu['concentration_primary'][elem][-1] = 1e-20 # 0.7477E+00#savechem.contenu['concentration_primary'][-1][-2]# -= complexation_derive_oh
                savechem.contenu['concentration_primary'][elem][-2] = 1e-20 #0.7477E+00#savechem.contenu['concentration_primary'][-1][-1]# -= complexation_derive_oh1
                savechem.contenu['UT_species'][elem][-1] = 1e-20 #0.6416E-01#savechem.contenu['UT_species'][-1][-2]# -= complexation_derive_UT_oh
                savechem.contenu['UT_species'][elem][-2] = 1e-20 #0.6416E-01#savechem.contenu['UT_species'][-1][-1]# -= complexation_derive_UT_oh1
        savechem.write_savechem('savechem')
    
    def correction_boundary_solution(self,location,bnd_solution):
        #print(bnd_solution)
        savechem = t2R_savechem.t2rsavechem(self.mesh.num_elem['X'],self.nb_especes, self.nb_mineraux,
                                 self.exe,self.pitzer,self.kinetics,
                                 self.complexation,'savechem')
        list_ordonnee = ['h2o','h+','ca+2','so4-2','hsio3-','co3-2','k+','na+','mg+2','al+3','cl-','fe+3','csh_oh','csh_oh1']
        composition_solution_lower = {}
        for elem in bnd_solution.keys():
            composition_solution_lower[elem.lower()] = bnd_solution[elem]
        indice = {'left': 0, 'right': -1}[location]
        i = 0
        for elem in list_ordonnee:
            if elem in self.species.keys():
                if elem in composition_solution_lower:
                    if elem == 'h2o':
                        savechem.contenu['concentration_primary'][indice][i] = 55.481536
                        savechem.contenu['UT_species'][indice][i] = 55.481536
                    else:
                        savechem.contenu['concentration_primary'][indice][i] = composition_solution_lower[elem]['guess']
                        savechem.contenu['UT_species'][indice][i] = composition_solution_lower[elem]['ctotal']
                else:
                    savechem.contenu['concentration_primary'][indice][i] = 1.0e-20
                    savechem.contenu['UT_species'][indice][i] = 1.0e-20
                i += 1
        if self.complexation == True:
            savechem.contenu['concentration_primary'][0][-1] = 0.56504758E-03
            savechem.contenu['concentration_primary'][0][-2] = 0.56333140E-02
            savechem.contenu['UT_species'][0][-1] = 0.64364915E-03
            savechem.contenu['UT_species'][0][-2] = 0.64169060E-02
        savechem.write_savechem('inchem')

    def _patch_flow_inp(self):
        '''Appends the REACT block to flow.inp and optionally inserts the REFCO section for eos9'''
        mopr = "00021000200201" if self.pitzer else "00021004"
        txt_react = ("REACT----1MOPR(20)-2----*----3----*----4----*----5----*----6----*----7----*----8\n"
                     + mopr + "\nENDCY")
        content = open("flow.inp").read().replace("ENDCY", txt_react)
        open("flow.inp", "w").write(content)
        if self.eos == 'eos9':
            txt_refco = f"REFCO       101300.0      {self.temperature_isotherme:>4}\t\n\nPARAM"
            content = open("flow.inp").read().replace("\nPARAM", txt_refco)
            open("flow.inp", "w").write(content)

    def _apply_equilibre_species(self, init_species_inter):
        '''Updates the species of the first material from an equilibrium result,
        excluding H2O, Na+ and K+.'''
        for elem, value in init_species_inter.items():
            elem_database = convert_ionic_species(elem, self.database)
            if elem_database not in ['H2O', 'Na+', 'K+']:
                self.list_material[0].species[elem_database] = value

    def _initialize_restart(self):
        '''Transforms the result files from a first calculation into initial
        conditions for a second one'''
        # The results of the previous calculation serve as IC for the next calculation
        # Rewriting initial conditions in INCON and inchem
        if os.path.isfile("inchem"):
            os.remove("inchem")
        #os.rename("savechem","inchem")
        if os.path.isfile("INCON"):
            os.remove("INCON")
        #os.rename("SAVE","INCON")
        shutil.copyfile('savechem','inchem')

    
    def solve(self, chargement_marnage, time_output, frequence, toughreact_exe, pas=3600.):
        if sys.platform == 'win32':
            self.exe = toughreact_exe
        else:
            self.exe = './'+toughreact_exe
        #Check for the presence of IC, BC, mesh, solution method...
        #self.duree = duree
        #duree_sec = self.duree * 3600. * 24.
        self._initialize_solve(chargement_marnage[0][0], time_output[0])
        #self.dat.run(simulator=self.exe)
        t = chargement_marnage[0][0]#pas
        self._sauvegarde(t/3600.0/24.0, toughreact_exe, time_output[0])
        i = 1
        self.frequence_sauv = frequence #save frequency (in hours)
        print("Calcul en cours...")
        #while t <= duree_sec:
        if len(chargement_marnage[0]) > 1:
            for elem in chargement_marnage[0][1:]:
                t = elem
                print(t/3600.0/24.0, "jours")
    #            print "numero de pas :", i
                if self.complexation:
                   previous_savechem = t2R_savechem.t2rsavechem(self.mesh.num_elem['X'],
                                                       self.nb_especes, self.nb_mineraux,
                                                       self.exe,self.pitzer,self.kinetics,
                                                       self.complexation)
                self._initialize_restart()
                self._update_bc(i,time_output[i-1],time_output[i])
    #            self._update_material()
                self.dat.run(simulator=self.exe)
                if self.complexation:
                   self.correction_concentration(previous_savechem)
                i += 1
                ##########################################################################
                #####Sauvegarde des resultats (toutes les x heures)
                if ((i)/self.frequence_sauv)%1 == 0 :
                    #print('jour '+str(t/24.0/3600.0)+'\n')
                    self._sauvegarde(t/24.0/3600.0, toughreact_exe, time_output[i-1], init=False)
                #t += pas
        print("Fin du calcul. Veuillez trouver les résultats dans le répertoire OUTPUT.")

    def _sauvegarde(self, jours, toughreact_exe, time_output, init=True):
        txt_jours = "%.2f"%jours
        #----Coordinates
        fich = "MESH"
        post.recup_coord(self.mesh)
        #----Species
        fich = "plot.dat"
        fich_res = "OUTPUT/plot_"+txt_jours+".dat"
        os.rename(fich,fich_res)
        post.convert_to_pandas(fich_res,toughreact_exe,self.pitzer,self.complexation, time_output, init, self.mesh)
        #----Minerals
        if "solid.out":
            fich_res_out = "OUTPUT/solid_"+txt_jours+".out"
            shutil.copy2("solid.out",fich_res_out)
            post.convert_to_pandas_out(fich_res_out,toughreact_exe,self.pitzer, time_output, init, self.mesh)
#        fich_inchem = "OUTPUT/inchem_"+txt_jours+".out"
#        shutil.copy2("inchem",fich_inchem)
        
if __name__ == '__main__':
    import pre
    eos = 'eco2n'
    rep_outil = '/Users/anthonysoive/Documents/CR_Nantes_2014_11/02-Modelisation/durabilite_marnage/'
    rep_travail = '/Users/anthonysoive/Documents/CR_Nantes_2014_11/02-Modelisation/Calcul/'
#    if not os.path.exists(rep_travail):
#        os.mkdir(rep_travail)
#    else:
#        shutil.rmtree(rep_travail)
#        os.mkdir(rep_travail)
#    if sys.platform == 'darwin':
#        exe = 'treactv3omp_'+eos+'_macosx_intel'
#        shutil.copyfile(rep_outil+'exe/'+exe,rep_travail+exe)
#        toughreact_exe = rep_travail+exe
#    else:
#        exe = 'tr3.0-omp_'+eos+'_PC64.exe'
#        shutil.copyfile(rep_outil+'exe/'+exe,rep_travail+exe)
#        toughreact_exe = rep_travail+exe
#    if eos == 'eco2n':
#        shutil.copyfile(rep_outil+'data/CO2TAB',rep_travail+'CO2TAB')
#    
#    os.chdir(rep_travail)
#    os.chmod(toughreact_exe,100)
    
    ######Construction d'un maillage
    dim_struct = {'X':0.1,'Y':1., 'Z':10.}
    nElem={'X':100,'Y':1,'Z':10}
    if (nElem['X'] * nElem['Y'] + 2 * (nElem['X'] + nElem['Y'])) > 120:
        print('Attention ! Le nombre de materiaux ne doit pas dépasser 120 !')
    #m = Mesh({'name':'geometric_prog', 'common_ratio':0.9}, dim_struct, nElem)
    m = Mesh({'name':'regular'}, dim_struct, nElem)
    #m.geo.write_vtk('titi.vtk')
    
    ###########################################################################
    #Material input data
    compo_ciment = {}
    #compo_ciment={"C3S":67.8/100.,"C2S":16.6/100.,"C3A":4./100.,
    #"C4AF":7.2/100.,"CSbH2":2.8/100.}
    #Compo Van-Quan
    compo_ciment={"C3S":64.2178/100.,"C2S":12.33449168/100.,"C3A":1.4918/100.,"C4AF":13.9978/100.,"CSbH2":2./100.}
    
    nom_beton = 'BO'
    # Formulations de beton
    formulation = {}
    #formulation[nom_beton]={"g12.5/20":733.,"g5/12.5":459.,"g0/5":0.,"s0/4":744.,"c":353.,"e":172.,\
    # "e/ctot":0.5,"e/c":0.49,"g/c":5.48,"phiair":0.012}
    # Formulation Van-Quan Carcasses
    formulation[nom_beton] = {"g12.5/20":0.,"g5/12.5":0.,"g0/5":0.,"s0/4":1365.,"c":617.7,"e":264.,\
         "e/ctot":0.44,"e/c":0.43,"g/c":2.21,"phiair":0.012}
    densite = formulation[nom_beton]["g12.5/20"] +\
                 formulation[nom_beton]["g5/12.5"] +\
                 formulation[nom_beton]["g0/5"] +\
                 formulation[nom_beton]["s0/4"] +\
                 formulation[nom_beton]["c"]
    temperature = 25. #material temperature in degrees Celsius
    age_cure = 200. #en jours
    mesures_ref = {'permeabilite':4.00e-20,'porosite':0.122}
    krl_model = {'type':'genuchten','params':[4.396e-01,0.0,1.0,0.01]}
    pc_model = {'type':'genuchten','params':[4.396e-01,0.0,5.369e-08,9.381e7,1.0]}
    tortuosite = 1.342e-2
    modele_mat = {}
    modele_mat[nom_beton]={'krl':krl_model,'pc':pc_model, 'cl_adsorption_csh':1.386e-2}
    beton = mat_ciment.MateriauCimentaire(nom_beton, formulation[nom_beton], 
                                          densite, compo_ciment, 
                                          age_cure, temperature, mesures_ref, 
                                          modele_mat[nom_beton], tortuosite)
    ######Construction du model
    model = Model(m)
    toughreact_concrete.model.add_material(beton)
    ###########################################################################
    toughreact_concrete.model.eos = eos
    toughreact_concrete.model.database = 'tk-ddem25aug09.dat'
    toughreact_concrete.model.database_phreeqc = 'thermoddem.dat'#'concrete_3T_V07_02.dat'
    #database_toughreact = 'tk-ddem25aug09.dat'
    #dir_dbase = '/Users/anthonysoive/Documents/CR_Nantes_2014_11/02-Modelisation/durabilite_marnage/model/'
    #dbase = dir_dbase+database_phreeqc
    ###########################################################################
    ###########################Initial conditions##########################
    ######Creation of initial conditions
    toughreact_concrete.model.add_ic()
    ###########################################################################
    
    ###########################Boundary conditions##########################
    ######Creation of boundary conditions
    nb_jours = 1./6.
    hauteur_marnage = maree.lecture_maree(nb_jours)#[5,5]#,10]#nb_jours*2*12*[10]#[0,0,0,0,0,0,10,10,10,10,10,10] #nb_jours*2*[0,0,0,0,0,0,10,10,10,10,10,10] #
    humidite_relative_ext = [65] #external relative humidity
    temperature_ext = [25] #external temperature
    temperature_eau = [15] #water temperature
    P_atm = [1.013e5] #atmospheric pressure
#    seawater_species = {'H2O':1.0,'H+':6.31e-9,'Cl-':5.350e-1,'Ca++':9.980e-3,\
#    'SO4--':2.760e-2,'H4SiO4(aq)':1.0e-20,'K+':0.972e-2,'Mg++':0.5222e-01,\
#    'Na+':0.459,'Al+++':1.0e-20,'O2(aq)':1.0e-10,'Fe++':1.0e-10,'HCO3-':1.0e-10}
    seawater_species = {'H2O':1.0,'H+':6.31e-9,'Cl-':5.350e-1,'Ca++':9.980e-3,\
    'SO4--':2.760e-2,'H4SiO4(aq)':1.0e-20,'K+':0.972e-2,'Mg++':0.5222e-01,\
    'Na+':0.459,'Al+++':1.0e-20}

    maree = {'HR_ext':humidite_relative_ext, 'T_ext':temperature_ext,
    'T_eau':temperature_eau, 'Patm':P_atm, 'ionic_species':seawater_species}
    CL_maree = cond_limit.CondLimit('maree', hauteur_marnage, **maree)
    CL_infini = cond_limit.CondLimit('infini')
    ######Ajout des conditions limites
    toughreact_concrete.model.add_bc(CL_maree, 'left')
    toughreact_concrete.model.add_bc(CL_infini, 'right')
    ###########################################################################
    
    ###########################################################################
    #problem resolution
    #save frequency
    frequence = 6
    toughreact_exe = pre.initialize(rep_outil, rep_travail, eos, toughreact_concrete.model.database,
                                    toughreact_concrete.model.database_phreeqc)
    toughreact_concrete.model.solve(nb_jours, frequence, toughreact_exe)    
    
#    taille_elem_z = dim_struct['Z']/nElem['Z']
#    list_node_b = [t2grids.node('n_'+str(i), \
#    np.array([0.1+1e-5,0.5,taille_elem_z*(i+0.5)])) for i in range(nElem['Z'])]
#    col = t2grids.column('x', list_node_b)
#    m.geo.add_column('x')
#    m.geo.boundary_columns

#    m.geo.add_column()
#    m.geo.add_connection()
#    #test de la connexion entre les colonnes limites et le reste du maillage
#    m.geo.connects()
#    ######Ajout d'une couche pour les conditions limites
#    m.geo.add_layer()
#    #test de la connexion entre la couche limite et le reste du maillage
#    m.geo.connects()
#    toughreact_concrete.model.dat.write("flow.inp")
