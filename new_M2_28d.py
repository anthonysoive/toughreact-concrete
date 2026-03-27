#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:29:20 2019

@author: anthonysoive
"""

import numpy as np

###########################################################################################################
#   Parametres de modélisation
###########################################################################################################
database = "Thermoddem_2023.txt" #"Th_Yoshida2021.txt" #"kswitch.out" #"Thermoddem.txt" #"thermoddem_hsio3.out"# "cemdata18_2022_al3_hco3_fe2_e_nh3_hsio3.out"# 'cemdata18_2022.out' #'thermodatabase.out' #
pitzer = False#True#


###########################################################################################################
#   Initialisation
###########################################################################################################
import  toughreact_concrete.model.pre #module AS

eos = 'eos9'#type de module utilisé dans toughreact (Richards)
toughreact_exe =  toughreact_concrete.model.pre.initialize(eos, database, pitzer)

###########################################################################################################
#   GEOMETRY
###########################################################################################################
ep_eau = 0.0001
ep_struct = 0.01
hauteur = 1.0
P1 = [-ep_eau,0.0,0.0]
P2 = [0.0,0.0,0.0]
P3 = [ep_struct,0.0,0.0]
points_struct = [P2,P3]
points_eau = [P1,P2]

###########################################################################################################
#   MESH
###########################################################################################################
from  toughreact_concrete.geometry_trc.constrgeom import suite_geom2
#Construction du maillage et affectation de numéros par zone et pour les conditions aux limites
points_struct = [P2,P3]
nElem={'X':200,'Y':1,'Z':1}
raison_suite = 0.999
points_elem_struct = {'Y':[1.0]}
points_elem_struct['X'] =  suite_geom2(ep_struct, nElem['X'], raison_suite, sens='croissant')
points_elem_struct['Z'] = [i/float(nElem['Z'])*hauteur for i in range(1,nElem['Z']+1)]

#Eau en contact
points_eau = [P1,P2]
nElem_eau={'X':1,'Y':nElem['Y'],'Z':nElem['Z']}
points_elem_eau = {'Y':points_elem_struct['Y'],'Z':points_elem_struct['Z']}
points_elem_eau['X'] = [i/float(nElem_eau['X'])*ep_eau for i in range(1,nElem_eau['X']+1)]

geom = [{'name':'struct','points':[P2,P3],'elements':points_elem_struct}]

###########################################################################################################
#   MATERIAL COMPOSITION AND MIX-DESIGN
###########################################################################################################
import toughreact_concrete.materiau.mat_ciment
nom_beton = 'M70-30FA'
cement_type = 'CEM I' # 
nature_granulat = {}
nature_granulat['ISO'] = {'densite':2.64,'capa':0.84}

compo_ciment = {}
compo_ciment['CEM I'] = {"SiO2":20.00,"Al2O3":4.60,"TiO2":0.0,"Fe2O3":3.20,
                          "CaO":64.00,"MgO":1.30,"Na2O":0.07,"K2O":1.30,
                         "SO3":3.40,"Mn2O3":0.0,"P2O5":0.48,"Cl":0.006,"CO2":0,"Cr2O3":0.00}

ciment = {'composition':compo_ciment[cement_type],'surface_specific':490.}

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
                               "binder":{"c":{"kg":864.00,"compo":ciment},
                                          "fly_ash":{"kg":283.50,"compo":fly_ash['BHP2000']},
                                         "silica_fume":{"kg":202.50,"compo":silica_fume['BHP2000']}},
                               "e":607.50, "phiair":0.0}

###########################################################################################################
#   MATERIAL DEFINITION AND HYDRATION
###########################################################################################################
temps_cure = 10000.
# Toujours mettre un temps de cure trés long pour considérer que le matériaux est complètement hydraté vue que on peux pas faire la compétition entre hydratation et transport en meme temps
porosite_mesuree = 0.22 #0.23#

materiau =  toughreact_concrete.materiau.mat_ciment.MateriauCimentaire(nom_beton)
materiau.formulation = formulation_beton
#######################################
#   MATERIAL COEFFICIENT
# Dapp = 7.84565532e-11 # 1.18e-12 # analyse inverse sur données expérimentales à 6 mois
# coeff_isotherme = 0.33   # issue de l'isotherme de fixation calculée
# coeff_effet_maree = 1   # pas de marée
# # idée : faire un premier calcul avec un coefficient de diffusion quelconque puis déduire l'isotherme de fixation des Cl- (coeff_isotherme)
# # Refaire le calcul avec la nouvelle valeur de D_eff
# Dbound_s_Deff = porosite_mesuree+coeff_isotherme #4 issue de l'isotherme de fixation calculée Dapp = Deff/(phi+dcb/dcf)
D_eff = 0.25e-12 #Dapp*Dbound_s_Deff # #  8.7e-12 #* coeff_isotherme #50.e-12# Dapp*(porosite_mesuree+coeff_isotherme)*coeff_effet_maree
materiau.porosite = porosite_mesuree
materiau.D_eff = D_eff
materiau.indicateurs_deduits = {'K_eau':8.0e-21,'cl_adsorption_csh':0.0001}#A determiner! 'D_eff':D_eff,
print("Coefficient de diffusion effectif : ",D_eff)
#######################################
#   HYDRATION
materiau.database = database
materiau.hydratation(temps_cure)
print(materiau.minerals)


###############################################################################
humidite_relative_ext = [70] #humidité relative extérieure
temperature_ext = [14] #température extérieure
P_atm = [1.013e5] #pression atmosphérique
Pp_co2 = 0.0#3.549e-4

#######################################
#   NATURE OF THE SOLUTION IN CONTACT WITH THE MATERIAL 
#   !!!! Il faut adapter les ions à la base de données utilisées !
q_NaCl = 35 #g/l
q_NaOH = 4 #g/l
M_NaCl = 58.44 #g/mol
M_NaOH = 39.997 #g/mol
bnd_solution = {
    'Thermoddem_2023.txt': [
        {
        'composition' : {
            'h2o': 0.1700E+01,'H+': 1.7e-7,'Ca+2': 1e-30,
            'SO4-2': 0.0357,'h4sio4': 1.000e-30,
            'K+': 1e-30,'Mg+2': 1e-30,'Na+': 0.0714,
            'Al+3': 1.000e-30,'Cl-': 1e-30},
        'temperature' : 20.0}],
    'Th_Yoshida2021.txt': [
        {
        'composition' : {
            'h2o': 0.1000E+01, 'H+': 1.11E-10,
            'Na+': 0.679, 'Cl-': 0.599,
            'Ca+2': 1e-20, 'SO4-2': 1e-20, 'h4sio4': 1e-20,'K+': 1e-20,'Mg+2': 1e-20, 'Al+3': 1e-20,
            'HCO3-': 2.029e-3},
        'temperature' : 15.1}]
}
print("Concentration Na+ et Cl- (en mol/l) : ", q_NaCl/M_NaCl + q_NaOH/M_NaOH, " et ", q_NaCl/M_NaCl)

bnd_solution['kswitch.out'] = bnd_solution['Th_Yoshida2021.txt']

boundary_solution = bnd_solution[database]

#Evolution dans le temps de la température de la solution (liste de valeurs)
temperature_eau = [20.0]

#######################################
#   DURATION EXPOSURE 
heure = 3600.
jour = 24.*heure
annee = 365.25*jour

temps_mouillage = 1*heure#62*mosis#19*annee#2*jour#10*annee #5*annee #726*jour#100*annee #6*heure#2*annee#
time_output = [[1*heure]]#[[2.5*mois,11*mois,11.5*mois,24*mois,45*mois,62*mois,9*annee]]#[[i*annee for i in range(1,int(temps_mouillage/annee)+1)]]#[[2*jour]]#*annee,4*annee,10*annee]]#,20*annee]]

#######################################
#   NATURE OF EXPOSURE (immerged, wetting/drying cycles...)
chargement_marnage = [[temps_mouillage],[10]]

cond_enviro = {'HR_ext':humidite_relative_ext, 'T_ext':temperature_ext,'T_eau':temperature_eau,
               'Patm':P_atm, 'Bnd_solution':boundary_solution, 'Pp_co2':Pp_co2}

#Conditions aux limites
CL = {'maree':['right']}

ep_couche_limite = 2e-5#20e-2

###########################################################################################################
#   MODEL OPTIONS
###########################################################################################################

#Options de calcul
kinetics = True#False#
update_porosity = False#True# 
complexation = True#False#

dt_max = 600.

###############################################################################
#import  toughreact_concrete.model.mat_ciment
import  toughreact_concrete.model.cond_limit
import  toughreact_concrete.model.element_struct #modules AS
import  toughreact_concrete.model.pre #module AS

m =  toughreact_concrete.model.element_struct.Mesh(geom, CL, ep_couche_limite)
m.construct_mesh(geom)
struct =  toughreact_concrete.model.element_struct.Model(m)

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
    struct.database = database

struct.database_phreeqc = 'thermoddem.dat'

# toughreact_exe =  toughreact_concrete.model.pre.initialize(eos, struct.database, pitzer)

struct.add_material(materiau, complexation)
CL_maree =  toughreact_concrete.model.cond_limit.CondLimit('maree', chargement_marnage, **cond_enviro)
struct.add_bc(CL_maree, CL['maree'])

frequence = 1.
struct.solve(chargement_marnage, time_output, frequence, toughreact_exe)
