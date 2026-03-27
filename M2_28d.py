#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:29:20 2019

@author: anthonysoive
"""

print("Calcul de la propagation d'eau de mer dans le béton M70-30FA...")

ep_eau = 0.0001
ep_struct = 0.03
hauteur = 0.06
P1 = [-ep_eau,0.0,0.0]
P2 = [0.0,0.0,0.0]
P3 = [ep_struct,0.0,0.0]
points_struct = [P2,P3]
points_eau = [P1,P2]

import  geometry.constrgeom
#Construction du maillage et affectation de numéros par zone et pour les conditions aux limites
points_struct = [P2,P3]
nElem={'X':500,'Y':1,'Z':1}
raison_suite = 0.999
points_elem_struct = {'Y':[1.0]}
points_elem_struct['X'] =  geometry.constrgeom.suite_geom2(ep_struct, nElem['X'], raison_suite, sens='croissant')
points_elem_struct['Z'] = [i/float(nElem['Z'])*hauteur for i in range(1,nElem['Z']+1)]

#Eau en contact
points_eau = [P1,P2]
nElem_eau={'X':1,'Y':nElem['Y'],'Z':nElem['Z']}
points_elem_eau = {'Y':points_elem_struct['Y'],'Z':points_elem_struct['Z']}
points_elem_eau['X'] = [i/float(nElem_eau['X'])*ep_eau for i in range(1,nElem_eau['X']+1)]

geom = [{'name':'struct','points':[P2,P3],'elements':points_elem_struct}]

import  materiau.mat_ciment
nom_beton = 'M70-30FA'
nature_granulat = {}
nature_granulat['ISO'] = {'densite':2.64,'capa':0.84}

compo_ciment = {}
compo_ciment['CEM I'] = {"SiO2":20.00,"Al2O3":4.60,"TiO2":0.0,"Fe2O3":3.20,
                          "CaO":64.00,"MgO":1.30,"Na2O":0.07,"K2O":1.30,
                         "SO3":3.40,"Mn2O3":0.0,"P2O5":0.48,"Cl":0.006,"CO2":0,"Cr2O3":0.00}
#compo_ciment['CEM I 52.5 PM ES CP2'] = {"SiO2":20.06,"Al2O3":5.3,"TiO2":0.18,"Fe2O3":2.11,
#                                        "CaO":66.3,"MgO":1.09,"Na2O":0.18,"K2O":0.28,
#                                        "SO3":3.3,"Cl":0.0,"CO2":0.18}

ciment = {}
ciment['CEM I'] = {'composition':compo_ciment['CEM I'],'surface_specific':413.30}


compo_fly_ash = {}
compo_fly_ash['BHP2000'] = {"SiO2":52.00,"Al2O3":27.50,"TiO2":0.00,"Fe2O3":4.80,"CaO":6.42,"MgO":1.85,
                                      "Na2O":1.01,"K2O":0.69,"SO3":1.10,"Cl":0.01,"CO2":0.0}
fly_ash = {}
fly_ash['BHP2000'] = {'composition':compo_fly_ash['BHP2000'],'surface_specific':340.}


compo_silica_fume = {}
compo_silica_fume['BHP2000'] = {"SiO2":96.00,"Al2O3":0.00,"TiO2":0.0,"Fe2O3":0.00,"CaO":0.10,"MgO":0.00,
                                      "Na2O":0.60,"K2O":0.00,"SO3":0.50,"Cl":0.02,"CO2":0.0}
silica_fume = {}
silica_fume['BHP2000'] = {'composition':compo_silica_fume['BHP2000'],'surface_specific':23200.}

#for elem in compo_ciment['CEM I 52.5 PM ES CP2']:
#    compo_ciment['CEM I 52.5 PM ES CP2'][elem] =s compo_ciment['CEM I 52.5 PM ES CP2'][elem]*223/(223.+95.) +\
#                                                compo_fly_ash['BHP2000'][elem]*95/(223.+95.)

formulation_beton = {"granulats":{"g12.5/20":{"kg":0.,'nature':nature_granulat['ISO']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['ISO']},
                                            "g0/5":{"kg":0.,'nature':nature_granulat['ISO']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['ISO']}},
                               "binder":{"c":{"kg":864.00,"compo":ciment['CEM I']},
                                          "fly_ash":{"kg":283.50,"compo":fly_ash['BHP2000']},
                                         "silica_fume":{"kg":202.50,"compo":silica_fume['BHP2000']}},
                               "e":607.50, "phiair":0.0}

temps_cure = 28.

porosite_mesuree = 0.282
# D_eff = D_eff_mesure/porosite_mesuree
# print("Valeur du coefficient de diffusion prise en compte : ",D_eff)
materiau =  materiau.mat_ciment.MateriauCimentaire(nom_beton)
materiau.formulation = formulation_beton
#Dapp = 1.18e-12
#coeff_isotherme = 0.0125   # pour passer du Dapp au   Deff 
#coeff_effet_maree = 1   
#D_eff = Dapp*(porosite_mesuree+coeff_isotherme)*coeff_effet_maree
materiau.porosite = porosite_mesuree
D_eff = 7.94e-11
materiau.indicateurs_deduits = {'K_eau':8.0e-21,'D_eff':D_eff,'cl_adsorption_csh':0.0001}#A determiner!
print("Coefficient de diffusion effectif : ",D_eff)
materiau.hydratation(temps_cure)
print(materiau.minerals)



###############################################################################
humidite_relative_ext = [70] #humidité relative extérieure
temperature_ext = [20] #température extérieure
P_atm = [1.013e5] #pression atmosphérique
Pp_co2 = 0.0#3.549e-4

boundary_solution = [{'composition' : {'h2o': 0.1000E+01,'H+': 1e-7,'Ca+2': 1e-30,'SO4-2': 0.03550,
                                      'hsio3-': 1.000e-30,'K+': 1e-30,'Mg+2': 1e-30,'Na+': 0.69435,
                                      'Al+3': 1.000e-30,'Cl-': 0.62336},
                    'temperature' : 20.0}]

#Evolution dans le temps de la température de la solution (liste de valeurs)
temperature_eau = [20.0]

heure = 3600.
jour = 24.*heure
annee = 365.25*jour

temps_mouillage = 540*jour#62*mosis#19*annee#2*jour#10*annee #5*annee #726*jour#100*annee #6*heure#2*annee#
time_output = [[1*jour,3*jour,7*jour,14*jour,28*jour,42*jour,56*jour,70*jour,84*jour,90*jour,98*jour,112*jour,126*jour,140*jour,150*jour,154*jour,160*jour,176*jour,180*jour,360*jour,540*jour]]#[[2.5*mois,11*mois,11.5*mois,24*mois,45*mois,62*mois,9*annee]]#[[i*annee for i in range(1,int(temps_mouillage/annee)+1)]]#[[2*jour]]#*annee,4*annee,10*annee]]#,20*annee]]
chargement_marnage = [[temps_mouillage],[10]]

cond_enviro = {'HR_ext':humidite_relative_ext, 'T_ext':temperature_ext,'T_eau':temperature_eau,
               'Patm':P_atm, 'Bnd_solution':boundary_solution, 'Pp_co2':Pp_co2}

#Conditions aux limites
CL = {'maree':['left']}

ep_couche_limite = 2e-5#20e-2

eos = 'eos9'#type de module utilisé dans toughreact

#Options de calcul
pitzer = False#True#
kinetics = True#False#
update_porosity = True#False# 
complexation = True#False#

dt_max = 3600.

###############################################################################
#import  model.mat_ciment
import  model.cond_limit
import  model.element_struct #modules AS
import  model.pre #module AS

m =  model.element_struct.Mesh(geom, CL, ep_couche_limite)
m.construct_mesh(geom)
struct =  model.element_struct.Model(m)

struct.eos = eos
if struct.eos == 'eos9':
    print('calcul isotherme')
    struct.temperature_isotherme = temperature_eau[0]#20.0

struct.pitzer = pitzer

struct.kinetics = kinetics

struct.update_porosity = update_porosity

struct.complexation = complexation

struct.pas_temps_calcul = dt_max

if pitzer:
    struct.database = 'baseQuan_pitzer.dat'
else:
    struct.database = 'thermodatabase.out'#'tk-ddem25aug09.dat'#'baseQuancomplete.dat'

struct.database_phreeqc = 'thermoddem.dat'

toughreact_exe =  model.pre.initialize(eos, struct.database, pitzer)

struct.add_material(materiau, complexation)
CL_maree =  model.cond_limit.CondLimit('maree', chargement_marnage, **cond_enviro)
struct.add_bc(CL_maree, CL['maree'])

frequence = 1.
struct.solve(chargement_marnage, time_output, frequence, toughreact_exe)
