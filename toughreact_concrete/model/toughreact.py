'''
Created on 9 févr. 2016

@author: anthonysoive
'''


import os
import shutil
import sys

import t2data

import toughreact_concrete.model.post as post
from toughreact_concrete.model.conversion_species import *

# jennite = 'JENNITE'
# tobermorite = 'TOBERMORITE'
# feoh3 = 'Ferrihydrite(2L)'
# monosulfoaluminate = 'MONOSULFOALUMINATE'
# ettringite = 'ETTRINGITE'
# hydrotalcite = 'HYDROTALCITE'
# portlandite = 'PORTLANDITE'
# friedel_salt = 'FRIEDEL_SALT'
# brucite = 'BRUCITE'
# calcite = 'CALCITE'
# monocarboaluminate = 'MONOCARBOALUMINATE'
# c3as084h432 = 'C3AS0.84H4.32'
# kuzel_salt = 'KUZEL_SALT'
# c3ah6 = 'C3AH6'
# gypsum = 'GYPSUM'
##Removing dolomite, magnesite, gibbsite, chrysotile, anhydrite
##Removing 'gypsum' in the presence of seawater
list_minerals_kinetics = ['JENNITE', 'TOBERMORITE', 'MONOSULFOALUMINATE',
                          'ETTRINGITE', 'HYDROTALCITE', 'PORTLANDITE', 'FRIEDEL_SALT', 'BRUCITE',
                          'CALCITE', 'MONOCARBOALUMINATE', 'ARAGONITE',
                          'ANHYDRITE',
                          'C3AH6', 'GYPSUM', 'KUZEL_SALT', 'CHRYSOTILE']#,'GIBBSITE', 'C3AFS0.84H4.32'] # 'C3FS1.34H3.32', #'Ferrihydrite(2L)', , 'C3AS0.84H4.32'
list_minerals = list_minerals_kinetics #+ ['PERICLASE', 'SEPIOLITE']

list_complexes = ['tobermorite','jennite']#,'C3AS0.84H4.32','monosulfoaluminate','portlandite' #For monosulfoaluminate, this is a way to account for a transformation of monosulfoaluminate into Kuzel salts by anionic exchange SO4 => Cl
name_complexe_database = {
    'jennite': 'CSH_OH',
    'tobermorite': 'CSH_OH1',
    'C3AS0.84H4.32': 'CAS_OH',
    'portlandite': 'POR_OH',
    'monosulfoaluminate': 'MON'
}

#Tobermorite => C/S = 0.83
#Jennite => C/S = 1.67
specific_surface_area = {#in cm2/g
    #'tobermorite': 300 * 1e4,#Yoshida et al. 2021 from figures 3 and 5
    #'jennite': 225 * 1e4,#Yoshida et al. 2021 from figures 3 and 5
    'tobermorite': 500 * 1e4,# Soive et al., 2017
    'jennite': 500 * 1e4,#Soive et al., 2017
    'C3AS0.84H4.32': 275 * 1e4,#Yoshida et al. 2021 from figures 3 and 5
    'portlandite': 14.31 * 1e4,#Elakneswaran et al.,2009
    'monosulfoaluminate': 600 * 1e4,
    'msh': 300 * 1e4
}
Avogadro = 6.0221408e+23
surface_site_density = {#mol/m2 of solid = nm-2 * 1e18 /avogadro
    'tobermorite': 4.3 * 1e18 / Avogadro,#Yoshida et al. 2021 from figure 5
    'jennite': 7 * 1e18 / Avogadro,#Yoshida et al. 2021 from figure 5
    'C3AS0.84H4.32': 4.25 * 1e18 / Avogadro,#Yoshida et al. 2021 from figure 5
    'portlandite': 2.31 * 1e18 / Avogadro,#Payne et al., 2013 in Almendros-Ginesta et al., 2023
    'monosulfoaluminate': 4.25 * 1e18 / Avogadro,
    'msh': 4.25 * 1e18 / Avogadro
}

num_complexes_by_mineral = {
    "Thermoddem_2023.txt": {
        'tobermorite': 6,
        'jennite': 6,
        'C3AS0.84H4.32': 7,
        'portlandite': 7,
        'monosulfoaluminate': 2
    },
    "cemdata18_2022.out": {
        'tobermorite': 7,
        'jennite': 7,
        'C3AS0.84H4.32': 7,
        'portlandite': 7,
        'monosulfoaluminate': 2
    },
    "Th_Yoshida2021.txt": {
        'tobermorite': 3,
        'jennite': 3,
        'C3AS0.84H4.32': 3,
        'portlandite': 3,
        'monosulfoaluminate': 2
    },
    "cemdata.out": {
        'tobermorite': 7,
        'jennite': 7,
        'C3AS0.84H4.32': 7,
        'portlandite': 7,
        'monosulfoaluminate': 2
    }
}
####

RCOUR = 0.5
DIFF_COEFF_WATER = 1.710e-09
LIQUID_PRESSURE = 101300.0

TORTUOSITY = 0

MSH = False


def lecture_database(database):
    masse_volumique, volume_molaire = {}, {}
    dict_minerals = {}
    minerals_name = ''
    number_null = 0
    #with open(rep_result_cerema+"thermodatabase.out","r") as fichier:
    chemin_database = '..\\Calcul\\' + database
    with open(chemin_database) as fichier:
        for line in fichier:
            if number_null == 2:
                if len(line.split()) > 2:
                    if not (minerals_name == line.split()[0]):
                        reaction = {}
                        minerals_name = line.split()[0][1:-1].upper()
                        dict_minerals[minerals_name] = {}
                        for i in range(int(line.split()[3])):
                            reaction[line.split()[4+i*2+1][1:-1]] = float(line.split()[4+i*2])
                        #print(dict_minerals)
                        dict_minerals[minerals_name]['density'] = float(line.split()[1])/1000. #dm3/mol
                        dict_minerals[minerals_name]['molar_volume'] = float(line.split()[2])/1000.
                        dict_minerals[minerals_name]['reaction'] = reaction
                    minerals_name = line.split()[0]
            if "'null'" in line:
                number_null += 1
    return dict_minerals

def species2toughreact(species):
    '''return a dictionnary of species with the toughreact format from a dictionnary of species'''
    dict_species = {}
    for spec in species:
        dict_species[spec] = {
            'guess': species[spec],
            'ctotal': species[spec]
        }
    return dict_species

def ecriture_flow(temp,porosity):
#    if boundary:
#        tmp_result=open("trame_flow_boundary.inp","r").read().replace("TITRE\n", "")
#    else:
#        tmp_result=open("trame_flow.inp","r").read().replace("TITRE\n", "")
    tmp_result=open("trame_flow.inp").read().replace("TITRE\n", "")
    temperature = (4 - len(str(temp))) * ' ' + str(temp)
    result=tmp_result.replace("TEMP", temperature)
    porosity = (8 - len(str(porosity))) * ' ' + str(porosity)
    result=result.replace("POROSITY", porosity)
    tortuosity = (10 - len(str(TORTUOSITY))) * ' ' + str(TORTUOSITY)
    result=result.replace("TORTUOSITY", tortuosity)
    liquid_pressure = (11 - len(str(LIQUID_PRESSURE))) * ' ' + str(LIQUID_PRESSURE)
    result=result.replace("PRESSURELIQ", liquid_pressure)
    open("flow.inp","w").write(result)

def ecriture_solute(nb_species, nb_minerals, database, type_eq, complexation=True,update_porosity=True, D_eff=DIFF_COEFF_WATER, porosite=1.0):
    if complexation:
        nb_complexes = 0
        for comp in list_complexes:
            nb_complexes += num_complexes_by_mineral[database][comp]
        # if 'monosulfoaluminate' in list_complexes:
        #     nb_complexes -= 5 #-7+2
    else:
        nb_complexes = 0
    if nb_minerals == 0:
        nb_minerals = 1
    if type_eq == 'reactive_transport':
        default_chem_prop = '    1    0    1    0    1    0    0    0    0'
        bnd_chem_prop = '  a 1    0    0    2    0    0    0    0    0    0    0   0'
    else:
        default_chem_prop = '    0    0    0    0    0    0    0    0    0'
        if type_eq == 'boundary':
            bnd_chem_prop = '  a 1    0    0    1    0    0    0    0    0    0    0    0'
        else:
            bnd_chem_prop = '  a 1    0    0    1    0    1    0    1    0    0    0    0'
    num_species = ''
    for i in range(nb_species):
        num_species += str(i+1) + "    "
    num_minerals = ''
    for i in range(nb_minerals):
        num_minerals += str(i+1) + "    "
    num_complexes = ''
    if complexation:
        for i in range(nb_complexes):
            num_complexes += str(i+1) + "    "
#    if boundary:
#        result=open(trame_file,"r").read().replace("NB_SPECIES", str(nb_species))
#        result=result.replace("NUM_SPECIES", num_species)
#    else:
    result=open("trame_solute.inp").read().replace("NB_SPECIES", str(nb_species))
    if update_porosity:
        result=result.replace("UPDATE_PORO", str(1))
    else:
        result=result.replace("UPDATE_PORO", str(0))
    result=result.replace("NB_MINERALS", str(nb_minerals))
    result=result.replace("NB_COMPLEXES", str(nb_complexes))
    result=result.replace("NUM_SPECIES", num_species)
    result=result.replace("NUM_MINERALS", num_minerals)
    result=result.replace("DATABASE", database)
    result=result.replace("RCOUR", str(RCOUR))
    #result=result.replace("DIFF_COEFF_WATER", str(DIFF_COEFF_WATER))
    tortuosite = porosite**0.33 #Millington and Quirk, 1961
    result=result.replace("DIFF_COEFF", str(D_eff/tortuosite/porosite))
    result=result.replace("DEFAULT_CHEM_PROP", default_chem_prop)
    result=result.replace("BND_CHEM_PROP", bnd_chem_prop)
    result=result.replace("NUM_COMPLEXES", num_complexes)
    open("solute.inp","w").write(result)


#def ecriture_chemical_sol_inter(minerals,species,temperature):
#    new_species = {}
#    for elem in species:
#        new_species[elem] = {'guess':species[elem],'ctotal':species[elem]}
#    ecriture_chemical_equilibre(minerals,new_species,temperature)

def ecriture_chemical_equilibre(database,minerals_list,species,temperature,complexation,kinetics):
    minerals, list_ordonnee = conversion_database(database, minerals_list)
    txt_minerals_0 = declare_minerals(database,minerals,kinetics)
    txt_minerals = declare_minerals_init(database,minerals,kinetics)
    #Declaration of ionic species
    txt_species_0 = ''
    #for elem in self.init_species.keys():
    #choice of the ordered list based on the database
    for elem in list_ordonnee:
        if elem.upper() in [tmp.upper() for tmp in species.keys()]:
            txt_species_0 += "'" + elem + "'      0\n"
    if complexation:
        for complexe in list_complexes:
            txt_species_0 += "'"+name_complexe_database[complexe]+"'       2  '"+mineral_database[database][complexe.upper()]+"' "+str(surface_site_density[complexe])+"  3 \n"
        # txt_species_0 += "'CSH_OH'       2  '"+mineral_database[database]['JENNITE']+"' "+str(surface_site_density["jennite"])+"  0 \n"
        # txt_species_0 += "'CSH_OH1'      2  '"+mineral_database[database]['TOBERMORITE']+"' "+str(surface_site_density["tobermorite"])+"  0 \n"
        # txt_species_0 += "'POR_OH'       2  '"+mineral_database[database]['PORTLANDITE']+"' "+str(surface_site_density["portlandite"])+"  0 \n"
        # txt_species_0 += "'MON'       2  '"+mineral_database[database]['MONOSULFOALUMINATE']+"' "+str(surface_site_density["monosulfoaluminate"])+"  0 \n"
        if MSH:
            txt_species_0 += "'MSH'           2  '"+mineral_database[database]['HYDROTALCITE']+"' "+str(surface_site_density["msh"])+"  3 \n"
    
    txt_species_0 += "'*'"
    txt_species = ''
    for elem in species.keys():
        if elem.upper() == 'H+':
#         if elem == 'oh-':
            txt_species += "'" + elem + "'    1    "+str(species[elem]['guess'])+"    "+str(species[elem]['ctotal'])+"  '*'   0.0 \n"
        else:
            if species[elem] == 0:
                species[elem] = 1.0e-20
            txt_species += "'" + elem + "'    1    "+str(species[elem]['guess'])+"    "+str(species[elem]['ctotal'])+"  '*'   0.0 \n"
    if complexation:
        for complexe in list_complexes:
            if name_complexe_database[complexe].lower() not in species.keys():
                # txt_species += "'"+name_complexe_database[complexe].lower()+"     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
                txt_species += "'"+name_complexe_database[complexe].lower()+"     ' 1   1.0E-20 1.0E-20  '*'   0.0\n"
        # if not ('csh_oh' in species.keys() or 'csh_oh1' in species.keys() or 'por_oh' in species.keys() or 'mon' in species.keys()):
        #     txt_species += "'csh_oh     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        #     txt_species += "'csh_oh1    ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        #     txt_species += "'por_oh     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        #     txt_species += "'mon     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        if MSH:
            txt_species += "'MSH'           1   0.6416E-01  0.7477E+00  '*'   0.0\n"
    txt_species += "'*'"
    
    txt_adsorption = ''
    if complexation:
        txt_adsorption += "1               !ndtype= number of sorption zones \n"
        txt_adsorption += "# zone       ad.surf.(cm2/g)  total ad.sites (mol/m2)\n"
        txt_adsorption += "1  1    ! zone index, equilibration flag\n"
        for complexe in list_complexes:
            txt_adsorption += "'"+name_complexe_database[complexe]+"'           0    "+str(specific_surface_area[complexe])+" \n"
        # txt_adsorption += "'CSH_OH'           0    "+str(specific_surface_area["jennite"])+" \n"
        # txt_adsorption += "'CSH_OH1'          0    "+str(specific_surface_area["tobermorite"])+" \n"
        # txt_adsorption += "'POR_OH'           0    "+str(specific_surface_area["portlandite"])+" \n"
        # txt_adsorption += "'MON'           0    "+str(specific_surface_area["monosulfoaluminate"])+" \n"
        if MSH:
            txt_adsorption += "'MSH'          0    "+str(specific_surface_area["msh"])+" \n"
    txt_adsorption += '*'
    
    result=open("trame_chemical.inp").read().replace("MINERALS_0_TXT", txt_minerals_0)
    result=result.replace("MINERALS_TXT", txt_minerals)
    result=result.replace("SPECIES_0_TXT", txt_species_0)
    result=result.replace("SPECIES_TXT", txt_species)
    result=result.replace("TEMP", str(temperature))
    result=result.replace("ADSORPTION_TXT", txt_adsorption)
    open("chemical.inp","w").write(result)

def ecriture_chemical_transport_reactif(database, material,bnd_solution,complexation,kinetics):
    minerals, list_ordonnee = conversion_database(database, material.minerals)
    #minerals = material.minerals
    species = material.species
    temperature = material.temperature
    temperature_solution = bnd_solution['temperature']
    txt_minerals_0 = declare_minerals(database,minerals,kinetics)
    txt_minerals = declare_minerals_init(database,minerals,kinetics)
    #Declaration of ionic species
    txt_species_0 = ''
    txt_Kd_0 = ''
    #for elem in self.init_species.keys():
    key_species_upper = [tmp.upper() for tmp in species.keys()]
    for elem in list_ordonnee:
        if elem.upper() in [tmp.upper() for tmp in species.keys()]:
            txt_species_0 += "'" + elem + "'      0\n"
    #for elem in [x for x in material.species if x not in ['csh_oh', 'csh_oh1', 'por_oh', 'mon']]:
    for elem in [x for x in material.species if x not in [name_complexe_database[complexe_name].lower() for complexe_name in name_complexe_database]]:
        if elem.lower() not in list_ordonnee:
            txt_species_0 += "'" + elem + "'      0\n"
    if complexation:
        for complexe in list_complexes:
            txt_species_0 += "'"+name_complexe_database[complexe]+"'       2  '"+mineral_database[database][complexe.upper()]+"' "+str(surface_site_density["jennite"])+"  3 \n"
        # txt_species_0 += "'CSH_OH'       2  '"+mineral_database[database]['JENNITE']+"' "+str(surface_site_density["jennite"])+"  3 \n"
        # txt_species_0 += "'CSH_OH1'      2  '"+mineral_database[database]['TOBERMORITE']+"' "+str(surface_site_density["tobermorite"])+"  3 \n"
        # txt_species_0 += "'POR_OH'       2  '"+mineral_database[database]['PORTLANDITE']+"' "+str(surface_site_density["portlandite"])+"  3 \n"
        # txt_species_0 += "'MON'       2  '"+mineral_database[database]['MONOSULFOALUMINATE']+"' "+str(surface_site_density["monosulfoaluminate"])+"  3 \n"
    else:
        txt_Kd_0 += "'Cl-'                0.0d0        0.0  0.0     ! with only Kd\n"
    if MSH:
        txt_species_0 += "'MSH'           2  '"+mineral_database[database]['HYDROTALCITE']+"' "+str(surface_site_density["msh"])+"  3 \n"
    
    txt_species_0 += "'*'"
    txt_Kd_0 += "'*'"
    txt_species = ''
    for elem in species.keys():
        if elem.upper() == 'H+':
            txt_species += "'" + elem + "'    1    "+str(species[elem]['guess'])+"    "+str(species[elem]['ctotal'])+"  '*'   0.0 \n"
        else:
            if species[elem] == 0:
                species[elem] = 1.0e-20
            txt_species += "'" + elem + "'    1    "+str(species[elem]['guess'])+"    "+str(species[elem]['ctotal'])+"  '*'   0.0 \n"
    if complexation:
        for complexe in list_complexes:
            if name_complexe_database[complexe] not in key_species_upper:
                txt_species += "'"+name_complexe_database[complexe]+"     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        # if not ('csh_oh'.upper() in key_species_upper or 'csh_oh1'.upper() in key_species_upper or 'por_oh'.upper() in key_species_upper or 'mon'.upper() in key_species_upper):
        #     txt_species += "'csh_oh     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        #     txt_species += "'csh_oh1    ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        #     txt_species += "'por_oh     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        #     txt_species += "'mon     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        if MSH:
            txt_species += "'MSH'           1   0.6416E-01  0.7477E+00  '*'   0.0\n"
    txt_species += "'*'"
    
    txt_species_bnd = ''
    for elem in species.keys():
        if elem.upper() == 'H+':
            txt_species_bnd += "'" + elem + "'    1    "+str(bnd_solution['composition'][elem]['guess'])+"    "+str(bnd_solution['composition'][elem]['ctotal'])+"  '*'   0.0 \n"
        else:
            if species[elem] == 0:
                species[elem] = 1.0e-20
            txt_species_bnd += "'" + elem + "'    1    "+str(bnd_solution['composition'][elem]['guess'])+"    "+str(bnd_solution['composition'][elem]['ctotal'])+"  '*'   0.0 \n"
    if complexation:
        for complexe in list_complexes:
            if name_complexe_database[complexe] not in key_species_upper:
                txt_species_bnd += "'"+name_complexe_database[complexe]+"     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        # if not ('csh_oh'.upper() in key_species_upper or 'csh_oh1'.upper() in key_species_upper or 'por_oh'.upper() in key_species_upper or 'mon'.upper() in key_species_upper):
        #     txt_species_bnd += "'csh_oh     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        #     txt_species_bnd += "'csh_oh1    ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        #     txt_species_bnd += "'por_oh     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        #     txt_species_bnd += "'mon     ' 1   0.6416E-01  0.7477E+00  '*'   0.0\n"
        if MSH:
            txt_species_bnd += "'MSH'           1   0.6416E-01  0.7477E+00  '*'   0.0\n"
    txt_species_bnd += "'*'"
    
    txt_adsorption = ''
    if complexation:
        txt_adsorption += "1               !ndtype= number of sorption zones \n"
        txt_adsorption += "# zone       ad.surf.(cm2/g)  total ad.sites (mol/m2)\n"
        txt_adsorption += "1  1    ! zone index, equilibration flag\n"
        for complexe in list_complexes:
            txt_adsorption += "'"+name_complexe_database[complexe]+"'           0    "+str(specific_surface_area[complexe])+" \n"
        # txt_adsorption += "'CSH_OH'           0    "+str(specific_surface_area["jennite"])+" \n"
        # txt_adsorption += "'CSH_OH1'          0    "+str(specific_surface_area["tobermorite"])+" \n"
        # txt_adsorption += "'POR_OH'           0    "+str(specific_surface_area["portlandite"])+" \n"
        # txt_adsorption += "'MON'           0    "+str(specific_surface_area["monosulfoaluminate"])+" \n"
        if MSH:
            txt_adsorption += "'MSH'          0    "+str(specific_surface_area["msh"])+" \n"
    txt_adsorption += '*'
    
    txt_Kd = ''
    if not complexation:
        txt_Kd += "1                    !kdtpye=number of Kd zones \n"
        txt_Kd += "1                    !idtype \n"
        txt_Kd += "#'species   solid-density(Sden,kg/dm**3)  Kd(l/kg=mass/kg solid / mass/l' #0.1124 \n"
        txt_Kd += "'cl-'    2.4166666666666665    "+str(material.indicateurs_deduits['cl_adsorption_csh'])+" \n"
    txt_Kd += '*'
    
    result=open("trame_chemical_reactive_transport.inp").read().replace("MINERALS_0_TXT", txt_minerals_0)
    result=result.replace("MINERALS_TXT", txt_minerals)
    result=result.replace("SPECIES_0_TXT", txt_species_0)
    result=result.replace("ADSORPTION_KD_0_TXT", txt_Kd_0)
    result=result.replace("SPECIES_TXT", txt_species)
    result=result.replace("TEMP_EXT", str(temperature_solution))
    result=result.replace("TEMP", str(temperature))
    result=result.replace("ADSORPTION_TXT", txt_adsorption)
    result=result.replace("ADSORPTION_KD_TXT", txt_Kd)
    result=result.replace("SPECIES_BND_TXT", txt_species_bnd)
    open("chemical.inp","w").write(result)

#def ecriture_chemical_equilibre_seawater():
#    result=open("trame_chemical_atl_seawater.inp","r").read()
#    open("chemical.inp","w").write(result)

def ecriture_chemical_equilibre_boundary_solution(database,species,temperature):
    result=open("trame_chemical_bnd_solution.inp").read()
    #Declaration of ionic species
    txt_species_0 = ''
    #for elem in self.init_species.keys():
    minerals, list_ordonnee = conversion_database(database, {})
    for elem in species.keys():
        # if elem.lower() in list_ordonnee:
        #     txt_species_0 += "'" + elem + "'      0\n"
        txt_species_0 += "'" + elem + "'      0\n"
    txt_species_0 += "'*'"
    txt_species = ''
    for elem in species.keys():
        if elem.upper() == 'H+':
        #if elem.upper() == 'OH-':
            txt_species += "'" + elem + "'    3    "+str(species[elem])+"    "+str(species[elem])+"  '*'   0.0 \n"
        else:
            if species[elem] == 0:
                species[elem] = 1.0e-20
            txt_species += "'" + elem + "'    1    "+str(species[elem])+"    "+str(species[elem])+"  '*'   0.0 \n"
    txt_species += "'*'"
    result=result.replace("SPECIES_0_TXT", txt_species_0)
    result=result.replace("SPECIES_TXT", txt_species)
    result=result.replace("TEMP", str(temperature))
    open("chemical.inp","w").write(result)

def recup_txt_species(nb_lines = 13):
    '''read chdump -> retrieve ionic species (guess and ctotal)'''
    txt_species=open("chdump.out").readlines()
    nb_lines = 0
    while '# component  flag    guess' not in txt_species[-nb_lines-1]:
           # component  flag    guess
        nb_lines += 1
    txt_species = txt_species[-nb_lines:][-nb_lines:-1]
    species = {}
    for elem in txt_species:
        elem_list = elem.split()
        if elem_list[3][-4] == '-':
            tmp_elem_guess = float(elem_list[3][:-4]+'e'+elem_list[3][-4:])
        else:
            tmp_elem_guess = float(elem_list[3])
        if elem_list[4][-4] == '-':
            tmp_elem_ctotal = float(elem_list[4][:-4]+'e'+elem_list[4][-4:])
        else:
            tmp_elem_ctotal = float(elem_list[4])
        species[elem_list[0][1:]] = {'guess':tmp_elem_guess,'ctotal':tmp_elem_ctotal}
    #print(species)
    return species#new_txt_species

def recup_minerals(exe_ini, minerals, database):
    '''read solid.out -> retrieve volume fractions of mineral species'''
    file = "solid.out"
    result = open(file).readlines()[-1:]
    list_val = result[0].split()
    header_out = post.recup_entete_solid(file, exe_ini)[0]
    i = 0
    porosity = 0.0
    for elem in header_out:
        if elem.lower() == 'porosity':
            porosity = float(list_val[i])
        i += 1
    i = 0
    dico = {}
    minerals_tronques = {}
    key_list_minerals = [mineral_database[database][k]  for k in minerals]
    for element in minerals.keys():
        if len(element) > 11:
            minerals_tronques[element[0:11]] = element.lower()
    key_list_minerals = [mineral_database[database][k].lower()  for k in minerals]
    for elem in header_out:#mineral_database[database]['HYDROTALCITE']
        if elem.lower() in key_list_minerals or elem.upper() in minerals_tronques:# minerals:#mineral_database[database] 
            dico[elem] = float(list_val[i])/(1-porosity)
        elif elem.upper() in minerals_tronques: #minerals_tronques:
            dico[minerals_tronques[elem.upper()]] = float(list_val[i])/(1-porosity)
        # if elem == 'monosulfoal' or elem == 'monosulphat':
        #     dico['Monosulfoaluminate'] = float(list_val[i])/(1-porosity)
        # if elem == 'monocarboal' or elem == 'monocarbona':
        #     dico['Monocarboaluminate'] = float(list_val[i])/(1-porosity)
        # if elem == 'fe_ettringi':
        #     dico['Fe_Ettringite'] = float(list_val[i])/(1-porosity)
        # if elem == 'hydrotalcit':
        #     dico['Hydrotalcite'] = float(list_val[i])/(1-porosity)
        # if elem == 'fe(oh)3(am)':
        #     dico['FE(OH)3'] = float(list_val[i])/(1-porosity)
        # if elem.lower() in ['tob-i', 'c0.8sh']:
        #     dico['TOBERMORITE'] = float(list_val[i])/(1-porosity)
        # if elem.lower() in ['c1.6sh']:
        #     dico['JENNITE'] = float(list_val[i])/(1-porosity)
        # if elem.lower() == 'c3afs0.84h4':
        #     dico['C3AFS0.84H4.32'] = float(list_val[i])/(1-porosity)
        i += 1
    return dico

#def calcul_solution_interstitielle(minerals,species,database,temperature):
#    ecriture_flow(temperature)
#    ecriture_solute_equilibre(len(species),len(minerals),database)
#    #ecriture_chemical_equilibre(minerals,species,temperature)
#    ecriture_chemical_sol_inter(minerals,species,temperature)
#    titi=t2data.t2data("flow.inp")
#    if sys.platform == 'darwin':
#        exe_ini = './treactv3omp_eos9_macosx_intel'
#    else:
#        exe_ini = 'tr3.0-omp_eos9_PC64.exe'
#    titi.run(simulator=exe_ini)
#    return recup_txt_species(), recup_minerals(exe_ini, minerals)

def declare_minerals(database,minerals,kinetics):
    #Declaration of mineral species
    list_minerals = [mineral_database[database][mineral].upper() for mineral in list_minerals_kinetics]
    txt_minerals_0 = ''
    txt_tmp = ''
    for elem in minerals.keys():
        if kinetics:
            if elem.upper() in list_minerals:
                if elem.upper() == mineral_database[database]['JENNITE'].upper():
                    txt_tmp += "'"+mineral_database[database]['JENNITE']+"'                         1      3      1      0\n"
                    txt_tmp += "              2.75E-12    0   1.0  1.0  0.0  0.0  0.0  0.0  \n"
                    txt_tmp += "              2.75E-12    0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == mineral_database[database]['TOBERMORITE'].upper():
                    txt_tmp += "'"+mineral_database[database]['TOBERMORITE']+"'                         1      3      1      0\n"
                    txt_tmp += "              2.75E-12    0   1.0  1.0  0.0  0.0  0.0  0.0  \n"
                    txt_tmp += "              2.75E-12    0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == 'C2S':
                    txt_tmp += "'C2S'                    1      3      0      0\n"
                    txt_tmp += "               2.24e-6  0   1.0  1.0  0  0.0  0.0  0.0\n"
                    txt_tmp += "               2.24e-6    0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == 'C3A':
                    txt_tmp += "'C3A'                    1      3      0      0\n"
                    txt_tmp += "               2.24e-6  0   1.0  1.0  0  0.0  0.0  0.0\n"
                    txt_tmp += "               2.24e-6    0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == 'C3S':
                    txt_tmp += "'C3S'                    1      3      0      0\n"
                    txt_tmp += "               2.24e-6  0   1.0  1.0  0  0.0  0.0  0.0\n"
                    txt_tmp += "               2.24e-6    0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == 'C4AF':
                    txt_tmp += "'C4AF'                    1      3      0      0\n"
                    txt_tmp += "               2.24e-6  0   1.0  1.0  0  0.0  0.0  0.0\n"
                    txt_tmp += "               2.24e-6    0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == mineral_database[database]['MONOSULFOALUMINATE'].upper():
                    txt_tmp += "'"+mineral_database[database]['MONOSULFOALUMINATE']+"'                   1      3      0      0\n"
                    txt_tmp += "              6.76E-12    0   1.0  1.0  0.0  0.0  0.0  0.0\n"
                    txt_tmp += "              6.76E-12    0   1.0  1.0  0.0  0.0  0.0  0.0     1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == mineral_database[database]['MONOCARBOALUMINATE'].upper():
                    txt_tmp += "'"+mineral_database[database]['MONOCARBOALUMINATE']+"'                   1      3      0      0\n"
                    txt_tmp += "              6.76E-12    0   1.0  1.0  0.0  0.0  0.0  0.0\n"
                    txt_tmp += "              6.76E-12    0   1.0  1.0  0.0  0.0  0.0  0.0     1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == mineral_database[database]['ETTRINGITE'].upper():
                    txt_tmp += "'"+mineral_database[database]['ETTRINGITE']+"'                   1      3      0      0\n"
                    txt_tmp += "               7.08E-13  0   1.0  1.0  0.0  0.0  0.0  0.0\n"
                    txt_tmp += "               7.08E-13  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == mineral_database[database]['C3AS0.84H4.32'].upper():
                    txt_tmp += "'"+mineral_database[database]['C3AS0.84H4.32']+"'                   1      3      0      0\n"
                    txt_tmp += "               7.08E-13  0   1.0  1.0  0.0  0.0  0.0  0.0\n"
                    txt_tmp += "               7.08E-13  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == mineral_database[database]['C3AFS0.84H4.32'].upper():
                    txt_tmp += "'"+mineral_database[database]['C3AFS0.84H4.32']+"'                   1      3      0      0\n"
                    txt_tmp += "               7.08E-14  0   1.0  1.0  0.0  0.0  0.0  0.0\n"
                    txt_tmp += "               7.08E-14  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == 'C3FS1.34H3.32':
                    txt_tmp += "'C3FS1.34H3.32'                   1      3      0      0\n"
                    txt_tmp += "               7.08E-13  0   1.0  1.0  0.0  0.0  0.0  0.0\n"
                    txt_tmp += "               7.08E-13  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == 'DOLOMITE(ORDERED)':
                    txt_tmp += "'Dolomite(ordered)'          1      3     0    0             \n"
                    txt_tmp += "              2.95e-8     2   1.0  1.0  52.2  0.0  0.0  0.0\n"
                    txt_tmp += "                          2\n"
                    txt_tmp += "                          6.46e-4   36.1    1   'h+'   0.5  ! acid mechanism\n"
                    txt_tmp += "                          7.76e-6   34.8    1   'h+'   0.5     ! base mechanism     \n"
                    txt_tmp += "\n"
                    txt_tmp += "              9.5e-15     0   1.0  1.0  103.0  0.0  0.0  0.0  1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == mineral_database[database]['ARAGONITE'].upper():#Palandri and Kharaka,2004
                    txt_tmp += "'"+mineral_database[database]['ARAGONITE']+"'          1      3     0    0             \n"
                    txt_tmp += "              4.5709e-10     2   1.0  1.0  23.5  0.0  0.0  0.0\n"
                    txt_tmp += "                          1\n"
                    txt_tmp += "                          4.1687e-7   14.4    1   'h+'   1.0  ! acid mechanism\n"
                    txt_tmp += "              4.5709e-10     2   1.0  1.0  23.5  0.0  0.0  0.0  1.e-15   0    \n"
                    txt_tmp += "                          1\n"
                    txt_tmp += "                          4.1687e-7   14.4    1   'h+'   1.0  ! acid mechanism\n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == mineral_database[database]['CALCITE'].upper():
                    txt_tmp += "'"+mineral_database[database]['CALCITE']+"'          1      3     0    0             \n"
                    txt_tmp += "              1.55e-6    2   1.0  1.0  23.5  0.0  0.0  0.0    \n"
                    txt_tmp += "                          2\n"
                    txt_tmp += "                          5e-1    14.4    1   'h+'   1  ! acid mechanism\n"
                    txt_tmp += "                          3.31e-4 35.4    1   'h+'   1      ! base mechanism     \n"
                    txt_tmp += "\n"
                    # txt_tmp += "              1.8e-7    2   2.0  0.5  66.0  0.0  0.0  0.0  1.e-6   0    \n"
                    # txt_tmp += "                          1\n"
                    # txt_tmp += "                          1.9e-3  67.0    1   'CO3-2'   1.6      ! base mechanism \n\n"
                    txt_tmp += "              0.0    1   1.0  1.0  0.0  0.0  0.0  0.0  1.e-6   0        \n"
                    txt_tmp += "                          1\n"
                    txt_tmp += "                          1.55e-6  23.5    1    'mg+2'   -0.5      ! base mechanism     \n"
                    txt_tmp += "0.0   0.    000.00    \n"
                if elem.upper() == mineral_database[database]['CHRYSOTILE'].upper():
                    txt_tmp += "'"+mineral_database[database]['CHRYSOTILE']+"'                    1      3      0      0\n"
                    txt_tmp += "              10e-12    2   1.0  1.0  73.5  0.0  0.0  0.0\n"
                    txt_tmp += "                          2\n"
                    txt_tmp += "                          0   73.5    1   'h+'   -0.230      ! acid mechanism         \n"
                    txt_tmp += "                          2.63e-14   73.5    1   'h+'   -0.230      ! base mechanism           \n"                
                    txt_tmp += "              10e-12    2   1.0  1.0  73.5  0.0  0.0  0.0     1.e-6\n"
                    txt_tmp += "                          0   73.5    1   'h+'   -0.230      ! acid mechanism     \n"
                    txt_tmp += "                          2.63e-14   73.5    1   'h+'   -0.230      ! base mechanism     \n"
                    txt_tmp += "0.0   0.    000.00                      \n"
                if elem.upper() == mineral_database[database]['HYDROTALCITE'].upper():
                    txt_tmp += "'"+mineral_database[database]['HYDROTALCITE']+"'                  1      3      0      0\n"#1      3      0      0\n"
                    txt_tmp += "               1.00e-9  0   1.0  1.0  0  0.0  0.0  0.0\n"
                    txt_tmp += "               1.00e-9  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00            \n"
                if elem.upper() == 'THAUMASITE':
                    txt_tmp += "'Thaumasite'                  1      3      0      0\n"#1      3      0      0\n"
                    txt_tmp += "               1.00e-13  0   1.0  1.0  0  0.0  0.0  0.0\n"
                    txt_tmp += "               1.00e-13  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00            \n"
                if elem.upper() == mineral_database[database]['GIBBSITE'].upper():
                    txt_tmp += "'"+mineral_database[database]['GIBBSITE']+"'                    1      3      0      0\n"
                    txt_tmp += "              3.16e-12    2   1.0  1.0  61.2  0.0  0.0  0.0\n"
                    txt_tmp += "                          2\n"
                    txt_tmp += "                          2.24e-8   47.5    1   'h+'   0.992  ! acid mechanism\n"
                    txt_tmp += "                          2.24e-17   80.1    1   'h+'   -0.784      ! base mechanism                 \n\n"          
                    txt_tmp += "              3.16e-12    2   1.0  1.0  61.2  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "                          2\n"
                    txt_tmp += "                          2.24e-8   47.5    1   'h+'   0.992  ! acid mechanism\n"
                    txt_tmp += "                          2.24e-17   80.1    1   'h+'   -0.784      ! base mechanism     \n"
                    txt_tmp += "0.0   0.    000.00                      \n"
                if elem.upper() == mineral_database[database]['ANHYDRITE'].upper():
                    txt_tmp += "'"+mineral_database[database]['ANHYDRITE']+"'                    1      3      0      0\n"
                    txt_tmp += "               0.000645654  0   1.0  1.0  14.3  0.0  0.0  0.0\n"
                    txt_tmp += "               0.000645654  0   1.0  1.0  14.3  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00        \n"
                if elem.upper() == mineral_database[database]['GYPSUM'].upper():
                    txt_tmp += "'"+mineral_database[database]['GYPSUM']+"'                    1      3      0      0\n"
                    txt_tmp += "               0.00162181  0   1.0  1.0  0.0  0.0  0.0  0.0\n"
                    txt_tmp += "               0.00162181  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00        \n"
                if elem.upper() == 'MAGNESITE':
                    txt_tmp += "'Magnesite'              1      3     0    0             \n"
                    txt_tmp += "              4.57088E-10    2   1.0  1.0  23.5  0.0  0.0  0.0    \n"
                    txt_tmp += "                          2\n"
                    txt_tmp += "                          4.16869E-07    14.4    1   'h+'   1  ! acid mechanism\n"
                    txt_tmp += "                          6.0256E-06     62.8    1   'co3-2'   1      ! base mechanism           \n\n"                
                    txt_tmp += "              4.57088E-10    2   1.0  1.0  23.5  0.0  0.0  0.0     1.e-6   0    \n"
                    txt_tmp += "                          2\n"
                    txt_tmp += "                          4.16869E-07    14.4    1   'h+'   1  ! acid mechanism\n"
                    txt_tmp += "                          6.0256E-06     62.8    1   'co3-2'   1      ! base mechanism         \n"
                    txt_tmp += "0.0   0.    000.00                              \n"
                if elem.upper() == mineral_database[database]['BRUCITE'].upper():
                    txt_tmp += "'"+mineral_database[database]['BRUCITE']+"'                1      3     0    0             \n"
                    txt_tmp += "              5.7544E-09    2   1.0  1.0  42.0  0.0  0.0  0.0    \n"
                    txt_tmp += "                          1\n"
                    txt_tmp += "                          1.86209E-05    59.0    1   'h+'   0.5  ! acid mechanism                      \n"
                    txt_tmp += "              5.7544E-09    2   1.0  1.0  42.0  0.0  0.0  0.0         1.e-6   0    \n"
                    txt_tmp += "                          1\n"
                    txt_tmp += "                          1.86209E-05    59.0    1   'h+'   0.5  ! acid mechanism    \n"
                    txt_tmp += "0.0   0.    000.00                              \n"
                if elem.upper() == mineral_database[database]['C3AH6'].upper():
                    txt_tmp += "'"+mineral_database[database]['C3AH6']+"'                    1      3      0      0\n"
                    txt_tmp += "               2.24e-10  0   1.0  1.0  0  0.0  0.0  0.0\n"
                    txt_tmp += "               2.24e-10  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00        \n"
                if elem.upper() == mineral_database[database]['PORTLANDITE'].upper():
                    txt_tmp += "'"+mineral_database[database]['PORTLANDITE']+"'                    1      3      0      0\n"
                    txt_tmp += "               2.24e-8  0   1.0  1.0  0  0.0  0.0  0.0\n"
                    txt_tmp += "               2.24e-8  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00        \n"
                if elem.upper() == mineral_database[database]['KUZEL_SALT'].upper():
                    txt_tmp += "'"+mineral_database[database]['KUZEL_SALT']+"'                    1      3      0      0\n"
                    txt_tmp += "               2.24e-08  0   1.0  1.0  0  0.0  0.0  0.0\n"
                    txt_tmp += "               2.24e-08  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    txt_tmp += "0.0   0.    000.00        \n"
                if elem.upper() == mineral_database[database]['FRIEDEL_SALT'].upper():
                    txt_tmp += "'"+mineral_database[database]['FRIEDEL_SALT']+"'                    1      3      0      0\n"
                    txt_tmp += "               6.76e-12  0   1.0  1.0  0.0  0.0  0.0  0.0    0.0   0\n"
                    txt_tmp += "               6.76e-12  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
                    #txt_tmp += "0.0   0.    000.00        \n"
                    txt_tmp += "0.0   0.    000.00        \n"
            else:
                txt_minerals_0 += "'" + elem + "'           0      0      0      0\n"
                txt_minerals_0 += "0.0 0.0 0.0\n"
        else:
            txt_minerals_0 += "'" + elem + "'           0      0      0      0\n"
            txt_minerals_0 += "0.0 0.0 0.0\n"
    txt_minerals_0 += txt_tmp
    txt_minerals_0 += "'*'"
    return txt_minerals_0

def declare_minerals_init(database,minerals,kinetics):
    list_minerals = [mineral_database[database][mineral].upper() for mineral in list_minerals_kinetics]
    txt_minerals = ''
    for elem in minerals.keys():
        if kinetics:
            if elem.upper() in list_minerals:
                if elem.upper() == mineral_database[database]['JENNITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['JENNITE']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "              0.0e0                                41e4     0  \n"
                if elem.upper() == mineral_database[database]['TOBERMORITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['TOBERMORITE']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "              0.0e0                                41e4     0  \n"
                if elem.upper() == 'C2S':
                    txt_minerals += "'C2S'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "              0.0e0                                9.8e4     0  \n"
                if elem.upper() == 'C3A':
                    txt_minerals += "'C3A'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "              0.0e0                                9.8e4     0  \n"
                if elem.upper() == 'C3S':
                    txt_minerals += "'C3S'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "              0.0e0                                9.8e4     0  \n"
                if elem.upper() == 'C4AF':
                    txt_minerals += "'C4AF'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "              0.0e0                                9.8e4     0  \n"
        #                         if elem.upper() == 'MONOCARBOALUMINATE':
        #                             txt_minerals += "'Monocarboaluminate'     " + str(minerals[elem]) + "    1\n"
        #                             txt_minerals += "0.0e0                                9.8e4   0\n"
                if elem.upper() == mineral_database[database]['DOLOMITE(ORDERED)'].upper():
                    txt_minerals += "'"+mineral_database[database]['DOLOMITE(ORDERED)']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['CALCITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['CALCITE']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['ARAGONITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['ARAGONITE']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "0.0e0                                9.1e4     0\n"
                if elem.upper() == mineral_database[database]['ETTRINGITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['ETTRINGITE']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['C3AS0.84H4.32'].upper():
                    txt_minerals += "'"+mineral_database[database]['C3AS0.84H4.32']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['C3AFS0.84H4.32'].upper():
                    txt_minerals += "'"+mineral_database[database]['C3AFS0.84H4.32']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['C3FS1.34H3.32'].upper():
                    txt_minerals += "'"+mineral_database[database]['C3FS1.34H3.32']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['MONOSULFOALUMINATE'].upper():
                    txt_minerals += "'"+mineral_database[database]['MONOSULFOALUMINATE']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "0.0e0                                5.7e4     0 \n"
                if elem.upper() == mineral_database[database]['MONOCARBOALUMINATE'].upper():
                    txt_minerals += "'"+mineral_database[database]['MONOCARBOALUMINATE']+"'     " + str(minerals[elem]) + "    1\n"
                    txt_minerals += "0.0e0                                5.7e4     0 \n"
                if elem.upper() == mineral_database[database]['HYDROTALCITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['HYDROTALCITE']+"'      " + str(minerals[elem]) + "   1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['THAUMASITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['THAUMASITE']+"'      " + str(minerals[elem]) + "   1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['ANHYDRITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['ANHYDRITE']+"'            " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['GYPSUM'].upper():
                    txt_minerals += "'"+mineral_database[database]['GYPSUM']+"'           " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['MAGNESITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['MAGNESITE']+"'            " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['BRUCITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['BRUCITE']+"'              " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['C3AH6'].upper():
                    txt_minerals += "'"+mineral_database[database]['C3AH6']+"'              " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                16.5e4     0\n"
                if elem.upper() == mineral_database[database]['GIBBSITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['GIBBSITE']+"'              " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
                if elem.upper() == mineral_database[database]['PORTLANDITE'].upper():
                    txt_minerals += "'"+mineral_database[database]['PORTLANDITE']+"'              " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                16.5e4     0\n"
                if elem.upper() == mineral_database[database]['KUZEL_SALT'].upper():
                    txt_minerals += "'"+mineral_database[database]['KUZEL_SALT']+"'              " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                16.5e4     0\n"
                if elem.upper() == mineral_database[database]['FRIEDEL_SALT'].upper():
                    txt_minerals += "'"+mineral_database[database]['FRIEDEL_SALT']+"'              " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                5.7e4     0\n"
                if elem.upper() == mineral_database[database]['CHRYSOTILE'].upper():
                    txt_minerals += "'"+mineral_database[database]['CHRYSOTILE']+"'              " + str(minerals[elem]) + "       1\n"
                    txt_minerals += "0.0e0                                9.8e4     0\n"
            else:
                txt_minerals += "'" + elem + "'    " + str(minerals[elem]) + "    0.\n"
        else:
            txt_minerals += "'" + elem + "'    " + str(minerals[elem]) + "    0.\n"
#         else:
#             txt_minerals += "'" + elem + "'    " + str(minerals[elem]) + "    0.\n"
    txt_minerals += "'*'                0.0      0 \n"
    return txt_minerals

def calcul_equilibre_bnd_solution(boundary_solution,porosity,database):
    os.chdir('Boundary')
    ecriture_flow(boundary_solution['temperature'],porosity)
    ecriture_solute(len(boundary_solution['composition']),0,database,'boundary')
    #ecriture_chemical_equilibre_seawater()
    ecriture_chemical_equilibre_boundary_solution(database,boundary_solution['composition'],boundary_solution['temperature'])
    titi=t2data.t2data("flow.inp")
    if sys.platform == 'darwin':
        exe_ini = './treactv3omp_eos9_macosx_intel'
    else:
        exe_ini = 'tr3.0-omp_eos9_PC64.exe'
    titi.run(simulator=exe_ini)
    shutil.copy2("plot.dat","eq_init.dat")
    species = recup_txt_species(nb_lines = len(boundary_solution['composition'])+1)
    os.chdir('..')
    eq_bnd_solution = {'temperature':boundary_solution['temperature'],'composition':species}
    return eq_bnd_solution

def calcul_equilibre_mineraux(material,database,complexation,kinetics,update_porosity):
    os.chdir('Material_equilibrium')
    #dict_minerals_database = lecture_database(database)
    ecriture_flow(material.temperature,material.porosite)#mesures_expe['P_eau'])
    ecriture_solute(len(material.species),len(material.minerals),database,'eq_materiau',complexation,update_porosity)
    ecriture_chemical_equilibre(database,material.minerals,material.species,material.temperature,
                                complexation,kinetics)
    titi=t2data.t2data("flow.inp")
    if sys.platform == 'darwin':
        exe_ini = './treactv3omp_eos9_macosx_intel'
    else:
        exe_ini = 'tr3.0-omp_eos9_PC64.exe'
    titi.run(simulator=exe_ini)
    species = recup_txt_species()
    minerals = recup_minerals(exe_ini, material.minerals, database)
    os.chdir('..')
    return species, minerals

def calcul_transport_reactif(material,bnd_solution,database,complexation,kinetics,update_porosity,exe):
    #ecriture_flow(material.temperature,material.mesures_expe['P_eau'])
    list_minerals_TR = [x for x in list_minerals if x not in set(material.minerals)]
    for elem in list_minerals_TR:
        material.minerals[elem] = 0.0
    ecriture_solute(len(material.species),len(material.minerals),database,"reactive_transport",complexation,update_porosity,
                    D_eff=material.D_eff, porosite=material.porosite)
    ecriture_chemical_transport_reactif(database,material,bnd_solution,complexation,kinetics)
    titi=t2data.t2data("flow.inp")
#     if sys.platform == 'darwin':
#         exe_ini = './treactv3omp_eos9_macosx_intel'
#     else:
#         exe_ini = 'tr3.0-omp_eos9_PC64.exe'
    titi.run(simulator=exe)
    return recup_txt_species(), recup_minerals(exe, material.minerals, database)

def conversion_database(database, minerals):
    '''Conversion du dictionnaire issu du calcul d'hydratation en dictionnaire
    d'espèces connues dans la base de données thermoddem du BRGM'''
    new_minerals = {}
    for elem in minerals.keys():
        new_key = mineral_database[database][elem]
        new_minerals[new_key] = minerals[elem]
    ordered_list_species = ordered_list_species_database[database]
    return new_minerals, ordered_list_species