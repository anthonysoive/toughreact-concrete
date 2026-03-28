#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:29:20 2019

@author: anthonysoive
"""

###########################################################################################################
#   Parametres de modélisation
###########################################################################################################
database = "Thermoddem_2023.txt"
pitzer = False

###########################################################################################################
#   Initialisation
###########################################################################################################
import toughreact_concrete.model.pre

eos = 'eos9'  # type de module utilisé dans toughreact (Richards)
toughreact_exe = toughreact_concrete.model.pre.initialize(eos, database, pitzer)

###########################################################################################################
#   GEOMETRY
###########################################################################################################
ep_eau = 0.0001
ep_struct = 0.01
hauteur = 1.0
P1 = [-ep_eau, 0.0, 0.0]
P2 = [0.0, 0.0, 0.0]
P3 = [ep_struct, 0.0, 0.0]

###########################################################################################################
#   MESH
###########################################################################################################
from toughreact_concrete.geometry_trc.constrgeom import suite_geom2

nElem = {'X': 200, 'Y': 1, 'Z': 1}
raison_suite = 0.999
points_elem_struct = {'Y': [1.0]}
points_elem_struct['X'] = suite_geom2(ep_struct, nElem['X'], raison_suite, sens='croissant')
points_elem_struct['Z'] = [i / float(nElem['Z']) * hauteur for i in range(1, nElem['Z'] + 1)]

nElem_eau = {'X': 1, 'Y': nElem['Y'], 'Z': nElem['Z']}
points_elem_eau = {'Y': points_elem_struct['Y'], 'Z': points_elem_struct['Z']}
points_elem_eau['X'] = [i / float(nElem_eau['X']) * ep_eau for i in range(1, nElem_eau['X'] + 1)]

geom = [{'name': 'struct', 'points': [P2, P3], 'elements': points_elem_struct}]

###########################################################################################################
#   MATERIAL DEFINITION AND HYDRATION
###########################################################################################################
import toughreact_concrete.materiau.mat_ciment
from toughreact_concrete.model.data.bd_materiaux import formulation_beton, indicateurs_deduits

nom_beton = 'M70-30FA'
temps_cure = 10000.
# Temps de cure long pour considérer une hydratation complète
porosite_mesuree = 0.22
D_eff = 0.25e-12

materiau = toughreact_concrete.materiau.mat_ciment.MateriauCimentaire(nom_beton)
materiau.formulation = formulation_beton[nom_beton]
materiau.porosite = porosite_mesuree
materiau.D_eff = D_eff
materiau.indicateurs_deduits = indicateurs_deduits[nom_beton]
print("Coefficient de diffusion effectif : ", D_eff)

materiau.database = database
materiau.hydratation(temps_cure)
print(materiau.minerals)

###########################################################################################################
#   CONDITIONS D'EXPOSITION
###########################################################################################################
from toughreact_concrete.model.data.bd_solutions import bnd_solution

humidite_relative_ext = [70]
temperature_ext = [14]
P_atm = [1.013e5]
Pp_co2 = 0.0

q_NaCl = 35   # g/l
q_NaOH = 4    # g/l
M_NaCl = 58.44
M_NaOH = 39.997
print("Concentration Na+ et Cl- (en mol/l) : ", q_NaCl / M_NaCl + q_NaOH / M_NaOH, " et ", q_NaCl / M_NaCl)

boundary_solution = bnd_solution[database]
temperature_eau = [20.0]

###########################################################################################################
#   DURÉE ET TYPE D'EXPOSITION
###########################################################################################################
heure = 3600.
jour = 24. * heure
annee = 365.25 * jour

temps_mouillage = 1 * heure
time_output = [[1 * heure]]
chargement_marnage = [[temps_mouillage], [10]]

cond_enviro = {
    'HR_ext': humidite_relative_ext, 'T_ext': temperature_ext, 'T_eau': temperature_eau,
    'Patm': P_atm, 'Bnd_solution': boundary_solution, 'Pp_co2': Pp_co2,
}
CL = {'maree': ['right']}
ep_couche_limite = 2e-5

###########################################################################################################
#   OPTIONS DE CALCUL
###########################################################################################################
kinetics = True
update_porosity = False
complexation = True
dt_max = 600.

###########################################################################################################
#   MODÈLE ET RÉSOLUTION
###########################################################################################################
import toughreact_concrete.model.cond_limit
import toughreact_concrete.model.element_struct

m = toughreact_concrete.model.element_struct.Mesh(geom, CL, ep_couche_limite)
m.construct_mesh(geom)
struct = toughreact_concrete.model.element_struct.Model(m)

struct.eos = eos
if struct.eos == 'eos9':
    print('calcul isotherme')
    struct.temperature_isotherme = temperature_eau[0]

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

struct.add_material(materiau, complexation)
CL_maree = toughreact_concrete.model.cond_limit.CondLimit('maree', chargement_marnage, **cond_enviro)
struct.add_bc(CL_maree, CL['maree'])

frequence = 1.
struct.solve(chargement_marnage, time_output, frequence, toughreact_exe)
