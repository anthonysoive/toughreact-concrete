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
    chemin_database = os.path.join('..', 'Calcul', database)
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

def ecriture_flow(temp, porosity, tortuosity=TORTUOSITY, liquid_pressure=LIQUID_PRESSURE):
    with open("trame_flow.inp") as f:
        tmp_result = f.read().replace("TITRE\n", "")
    result = tmp_result.replace("TEMP", f"{temp:>4}")
    result = result.replace("POROSITY", f"{porosity:>8}")
    result = result.replace("TORTUOSITY", f"{tortuosity:>10}")
    result = result.replace("PRESSURELIQ", f"{liquid_pressure:>11}")
    with open("flow.inp", "w") as f:
        f.write(result)

def ecriture_solute(nb_species, nb_minerals, database, type_eq, complexation=True, update_porosity=True, D_eff=DIFF_COEFF_WATER, porosite=1.0, rcour=RCOUR):
    if complexation:
        nb_complexes = 0
        for comp in list_complexes:
            nb_complexes += num_complexes_by_mineral[database][comp]
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
    with open("trame_solute.inp") as f:
        result = f.read().replace("NB_SPECIES", str(nb_species))
    if update_porosity:
        result=result.replace("UPDATE_PORO", str(1))
    else:
        result=result.replace("UPDATE_PORO", str(0))
    result=result.replace("NB_MINERALS", str(nb_minerals))
    result=result.replace("NB_COMPLEXES", str(nb_complexes))
    result=result.replace("NUM_SPECIES", num_species)
    result=result.replace("NUM_MINERALS", num_minerals)
    result=result.replace("DATABASE", database)
    result=result.replace("RCOUR", str(rcour))
    tortuosite = porosite**0.33 #Millington and Quirk, 1961
    result=result.replace("DIFF_COEFF", str(D_eff/tortuosite/porosite))
    result=result.replace("DEFAULT_CHEM_PROP", default_chem_prop)
    result=result.replace("BND_CHEM_PROP", bnd_chem_prop)
    result=result.replace("NUM_COMPLEXES", num_complexes)
    with open("solute.inp", "w") as f:
        f.write(result)


def _build_species_declaration_txt(list_ordonnee, species, complexation, database, extra_species=None, msh=MSH):
    '''Build SPECIES_0_TXT block (species declaration + surface complexes).

    extra_species: optional list of additional species names not covered by list_ordonnee
                   (used in reactive transport to include species outside the ordered list).
    '''
    species_upper = {k.upper() for k in species}
    txt = ''
    for elem in list_ordonnee:
        if elem.upper() in species_upper:
            txt += f"'{elem}'      0\n"
    if extra_species:
        for elem in extra_species:
            if elem.lower() not in list_ordonnee:
                txt += f"'{elem}'      0\n"
    if complexation:
        for complexe in list_complexes:
            db_mineral = mineral_database[database][complexe.upper()]
            density = surface_site_density[complexe]
            txt += f"'{name_complexe_database[complexe]}'       2  '{db_mineral}' {density}  3 \n"
        if msh:
            db_mineral = mineral_database[database]['HYDROTALCITE']
            txt += f"'MSH'           2  '{db_mineral}' {surface_site_density['msh']}  3 \n"
    txt += "'*'"
    return txt


def _build_species_values_txt(species_dict, complexation, missing_complexe_init='1.0E-20 1.0E-20', msh=MSH):
    '''Build SPECIES_TXT block (guess/ctotal values per species + surface complexes).

    missing_complexe_init: "guess ctotal" string used when a surface complex is absent
                           from species_dict. Defaults to near-zero for equilibrium runs;
                           use '0.6416E-01  0.7477E+00' for reactive transport runs.
    '''
    existing_upper = {k.upper() for k in species_dict}
    txt = ''
    for elem, val in species_dict.items():
        txt += f"'{elem}'    1    {val['guess']}    {val['ctotal']}  '*'   0.0 \n"
    if complexation:
        for complexe in list_complexes:
            if name_complexe_database[complexe].upper() not in existing_upper:
                txt += f"'{name_complexe_database[complexe]}     ' 1   {missing_complexe_init}  '*'   0.0\n"
        if msh:
            txt += "'MSH'           1   0.6416E-01  0.7477E+00  '*'   0.0\n"
    txt += "'*'"
    return txt


def _build_adsorption_txt(complexation, msh=MSH):
    '''Build ADSORPTION_TXT block (surface complexation zones).'''
    txt = ''
    if complexation:
        txt += "1               !ndtype= number of sorption zones \n"
        txt += "# zone       ad.surf.(cm2/g)  total ad.sites (mol/m2)\n"
        txt += "1  1    ! zone index, equilibration flag\n"
        for complexe in list_complexes:
            txt += f"'{name_complexe_database[complexe]}'           0    {specific_surface_area[complexe]} \n"
        if msh:
            txt += f"'MSH'          0    {specific_surface_area['msh']} \n"
    txt += '*'
    return txt


def ecriture_chemical_equilibre(database, minerals_list, species, temperature, complexation, kinetics):
    minerals, list_ordonnee = conversion_database(database, minerals_list)
    txt_minerals_0 = declare_minerals(database, minerals, kinetics)
    txt_minerals = declare_minerals_init(database, minerals, kinetics)
    txt_species_0 = _build_species_declaration_txt(list_ordonnee, species, complexation, database)
    txt_species = _build_species_values_txt(species, complexation)
    txt_adsorption = _build_adsorption_txt(complexation)
    with open("trame_chemical.inp") as f:
        result = f.read().replace("MINERALS_0_TXT", txt_minerals_0)
    result = result.replace("MINERALS_TXT", txt_minerals)
    result = result.replace("SPECIES_0_TXT", txt_species_0)
    result = result.replace("SPECIES_TXT", txt_species)
    result = result.replace("TEMP", str(temperature))
    result = result.replace("ADSORPTION_TXT", txt_adsorption)
    with open("chemical.inp", "w") as f:
        f.write(result)

def ecriture_chemical_transport_reactif(database, material, bnd_solution, complexation, kinetics):
    minerals, list_ordonnee = conversion_database(database, material.minerals)
    species = material.species
    temperature = material.temperature
    temperature_solution = bnd_solution['temperature']
    txt_minerals_0 = declare_minerals(database, minerals, kinetics)
    txt_minerals = declare_minerals_init(database, minerals, kinetics)

    complex_names_lower = {name_complexe_database[c].lower() for c in name_complexe_database}
    extra_species = [x for x in material.species if x not in complex_names_lower]
    txt_species_0 = _build_species_declaration_txt(
        list_ordonnee, species, complexation, database, extra_species=extra_species
    )

    txt_Kd_0 = ''
    if not complexation:
        txt_Kd_0 += "'Cl-'                0.0d0        0.0  0.0     ! with only Kd\n"
    txt_Kd_0 += "'*'"

    txt_species = _build_species_values_txt(
        species, complexation, missing_complexe_init='0.6416E-01  0.7477E+00'
    )
    bnd_composition = {elem: bnd_solution['composition'][elem] for elem in species}
    txt_species_bnd = _build_species_values_txt(
        bnd_composition, complexation, missing_complexe_init='0.6416E-01  0.7477E+00'
    )
    txt_adsorption = _build_adsorption_txt(complexation)

    txt_Kd = ''
    if not complexation:
        txt_Kd += "1                    !kdtpye=number of Kd zones \n"
        txt_Kd += "1                    !idtype \n"
        txt_Kd += "#'species   solid-density(Sden,kg/dm**3)  Kd(l/kg=mass/kg solid / mass/l' #0.1124 \n"
        txt_Kd += f"'cl-'    2.4166666666666665    {material.indicateurs_deduits['cl_adsorption_csh']} \n"
    txt_Kd += '*'

    with open("trame_chemical_reactive_transport.inp") as f:
        result = f.read().replace("MINERALS_0_TXT", txt_minerals_0)
    result = result.replace("MINERALS_TXT", txt_minerals)
    result = result.replace("SPECIES_0_TXT", txt_species_0)
    result = result.replace("ADSORPTION_KD_0_TXT", txt_Kd_0)
    result = result.replace("SPECIES_TXT", txt_species)
    result = result.replace("TEMP_EXT", str(temperature_solution))
    result = result.replace("TEMP", str(temperature))
    result = result.replace("ADSORPTION_TXT", txt_adsorption)
    result = result.replace("ADSORPTION_KD_TXT", txt_Kd)
    result = result.replace("SPECIES_BND_TXT", txt_species_bnd)
    with open("chemical.inp", "w") as f:
        f.write(result)

def ecriture_chemical_equilibre_boundary_solution(database,species,temperature):
    with open("trame_chemical_bnd_solution.inp") as f:
        result = f.read()
    txt_species_0 = ''
    minerals, list_ordonnee = conversion_database(database, {})
    for elem in species.keys():
        txt_species_0 += "'" + elem + "'      0\n"
    txt_species_0 += "'*'"
    txt_species = ''
    for elem in species.keys():
        if elem.upper() == 'H+':
            txt_species += "'" + elem + "'    3    "+str(species[elem])+"    "+str(species[elem])+"  '*'   0.0 \n"
        else:
            if species[elem] == 0:
                species[elem] = 1.0e-20
            txt_species += "'" + elem + "'    1    "+str(species[elem])+"    "+str(species[elem])+"  '*'   0.0 \n"
    txt_species += "'*'"
    result=result.replace("SPECIES_0_TXT", txt_species_0)
    result=result.replace("SPECIES_TXT", txt_species)
    result=result.replace("TEMP", str(temperature))
    with open("chemical.inp", "w") as f:
        f.write(result)

def recup_txt_species():
    '''read chdump -> retrieve ionic species (guess and ctotal)'''
    with open("chdump.out") as f:
        txt_species = f.readlines()
    nb_lines = 0
    while '# component  flag    guess' not in txt_species[-nb_lines-1]:
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
    return species

def recup_minerals(exe_ini, minerals, database):
    '''read solid.out -> retrieve volume fractions of mineral species'''
    file = "solid.out"
    with open(file) as f:
        result = f.readlines()[-1:]
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
        elif elem.upper() in minerals_tronques:
            dico[minerals_tronques[elem.upper()]] = float(list_val[i])/(1-porosity)
        i += 1
    return dico

# Kinetics parameters per canonical mineral key.
# 'flag'         : 4th column in the header line (1 for C-S-H phases, 0 otherwise)
# 'body'         : all lines after the header, including the closing "0.0   0.    000.00" line
# 'surface_area' : initial reactive surface area (cm²/g) used in declare_minerals_init
_MINERAL_KINETICS = {
    'JENNITE': {
        'flag': 1,
        'body': (
            "              2.75E-12    0   1.0  1.0  0.0  0.0  0.0  0.0  \n"
            "              2.75E-12    0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00    \n"
        ),
        'surface_area': '41e4',
    },
    'TOBERMORITE': {
        'flag': 1,
        'body': (
            "              2.75E-12    0   1.0  1.0  0.0  0.0  0.0  0.0  \n"
            "              2.75E-12    0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00    \n"
        ),
        'surface_area': '41e4',
    },
    'MONOSULFOALUMINATE': {
        'flag': 0,
        'body': (
            "              6.76E-12    0   1.0  1.0  0.0  0.0  0.0  0.0\n"
            "              6.76E-12    0   1.0  1.0  0.0  0.0  0.0  0.0     1.e-6   0\n"
            "0.0   0.    000.00    \n"
        ),
        'surface_area': '5.7e4',
    },
    'MONOCARBOALUMINATE': {
        'flag': 0,
        'body': (
            "              6.76E-12    0   1.0  1.0  0.0  0.0  0.0  0.0\n"
            "              6.76E-12    0   1.0  1.0  0.0  0.0  0.0  0.0     1.e-6   0\n"
            "0.0   0.    000.00    \n"
        ),
        'surface_area': '5.7e4',
    },
    'ETTRINGITE': {
        'flag': 0,
        'body': (
            "               7.08E-13  0   1.0  1.0  0.0  0.0  0.0  0.0\n"
            "               7.08E-13  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00    \n"
        ),
        'surface_area': '9.8e4',
    },
    'HYDROTALCITE': {
        'flag': 0,
        'body': (
            "               1.00e-9  0   1.0  1.0  0  0.0  0.0  0.0\n"
            "               1.00e-9  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00            \n"
        ),
        'surface_area': '9.8e4',
    },
    'PORTLANDITE': {
        'flag': 0,
        'body': (
            "               2.24e-8  0   1.0  1.0  0  0.0  0.0  0.0\n"
            "               2.24e-8  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00        \n"
        ),
        'surface_area': '16.5e4',
    },
    'FRIEDEL_SALT': {
        'flag': 0,
        'body': (
            "               6.76e-12  0   1.0  1.0  0.0  0.0  0.0  0.0    0.0   0\n"
            "               6.76e-12  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00        \n"
        ),
        'surface_area': '5.7e4',
    },
    'BRUCITE': {
        'flag': 0,
        'body': (
            "              5.7544E-09    2   1.0  1.0  42.0  0.0  0.0  0.0    \n"
            "                          1\n"
            "                          1.86209E-05    59.0    1   'h+'   0.5  ! acid mechanism                      \n"
            "              5.7544E-09    2   1.0  1.0  42.0  0.0  0.0  0.0         1.e-6   0    \n"
            "                          1\n"
            "                          1.86209E-05    59.0    1   'h+'   0.5  ! acid mechanism    \n"
            "0.0   0.    000.00                              \n"
        ),
        'surface_area': '9.8e4',
    },
    'CALCITE': {
        'flag': 0,
        'body': (
            "              1.55e-6    2   1.0  1.0  23.5  0.0  0.0  0.0    \n"
            "                          2\n"
            "                          5e-1    14.4    1   'h+'   1  ! acid mechanism\n"
            "                          3.31e-4 35.4    1   'h+'   1      ! base mechanism     \n"
            "\n"
            "              0.0    1   1.0  1.0  0.0  0.0  0.0  0.0  1.e-6   0        \n"
            "                          1\n"
            "                          1.55e-6  23.5    1    'mg+2'   -0.5      ! base mechanism     \n"
            "0.0   0.    000.00    \n"
        ),
        'surface_area': '9.8e4',
    },
    'ARAGONITE': {  # Palandri and Kharaka, 2004
        'flag': 0,
        'body': (
            "              4.5709e-10     2   1.0  1.0  23.5  0.0  0.0  0.0\n"
            "                          1\n"
            "                          4.1687e-7   14.4    1   'h+'   1.0  ! acid mechanism\n"
            "              4.5709e-10     2   1.0  1.0  23.5  0.0  0.0  0.0  1.e-15   0    \n"
            "                          1\n"
            "                          4.1687e-7   14.4    1   'h+'   1.0  ! acid mechanism\n"
            "0.0   0.    000.00    \n"
        ),
        'surface_area': '9.1e4',
    },
    'ANHYDRITE': {
        'flag': 0,
        'body': (
            "               0.000645654  0   1.0  1.0  14.3  0.0  0.0  0.0\n"
            "               0.000645654  0   1.0  1.0  14.3  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00        \n"
        ),
        'surface_area': '9.8e4',
    },
    'C3AH6': {
        'flag': 0,
        'body': (
            "               2.24e-10  0   1.0  1.0  0  0.0  0.0  0.0\n"
            "               2.24e-10  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00        \n"
        ),
        'surface_area': '16.5e4',
    },
    'GYPSUM': {
        'flag': 0,
        'body': (
            "               0.00162181  0   1.0  1.0  0.0  0.0  0.0  0.0\n"
            "               0.00162181  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00        \n"
        ),
        'surface_area': '9.8e4',
    },
    'KUZEL_SALT': {
        'flag': 0,
        'body': (
            "               2.24e-08  0   1.0  1.0  0  0.0  0.0  0.0\n"
            "               2.24e-08  0   1.0  1.0  0.0  0.0  0.0  0.0    1.e-6   0\n"
            "0.0   0.    000.00        \n"
        ),
        'surface_area': '16.5e4',
    },
    'CHRYSOTILE': {
        'flag': 0,
        'body': (
            "              10e-12    2   1.0  1.0  73.5  0.0  0.0  0.0\n"
            "                          2\n"
            "                          0   73.5    1   'h+'   -0.230      ! acid mechanism         \n"
            "                          2.63e-14   73.5    1   'h+'   -0.230      ! base mechanism           \n"
            "              10e-12    2   1.0  1.0  73.5  0.0  0.0  0.0     1.e-6\n"
            "                          0   73.5    1   'h+'   -0.230      ! acid mechanism     \n"
            "                          2.63e-14   73.5    1   'h+'   -0.230      ! base mechanism     \n"
            "0.0   0.    000.00                      \n"
        ),
        'surface_area': '9.8e4',
    },
}

def declare_minerals(database, minerals, kinetics):
    #Declaration of mineral species
    db_to_canonical = {mineral_database[database][k].upper(): k for k in mineral_database[database]}
    kinetics_names = {mineral_database[database][k].upper() for k in list_minerals_kinetics
                      if k in mineral_database[database]}
    txt_equilibrium = ''
    txt_kinetic = ''
    for elem in minerals:
        if kinetics and elem.upper() in kinetics_names:
            canonical = db_to_canonical.get(elem.upper())
            params = _MINERAL_KINETICS.get(canonical) if canonical else None
            if params:
                txt_kinetic += f"'{elem}'    1      3      {params['flag']}      0\n"
                txt_kinetic += params['body']
            else:
                txt_equilibrium += f"'{elem}'           0      0      0      0\n"
                txt_equilibrium += "0.0 0.0 0.0\n"
        else:
            txt_equilibrium += f"'{elem}'           0      0      0      0\n"
            txt_equilibrium += "0.0 0.0 0.0\n"
    return txt_equilibrium + txt_kinetic + "'*'"

def declare_minerals_init(database, minerals, kinetics):
    db_to_canonical = {mineral_database[database][k].upper(): k for k in mineral_database[database]}
    kinetics_names = {mineral_database[database][k].upper() for k in list_minerals_kinetics
                      if k in mineral_database[database]}
    txt = ''
    for elem, vol_frac in minerals.items():
        if kinetics and elem.upper() in kinetics_names:
            canonical = db_to_canonical.get(elem.upper())
            params = _MINERAL_KINETICS.get(canonical) if canonical else None
            if params:
                txt += f"'{elem}'     {vol_frac}    1\n"
                txt += f"              0.0e0                                {params['surface_area']}     0\n"
            else:
                txt += f"'{elem}'    {vol_frac}    0.\n"
        else:
            txt += f"'{elem}'    {vol_frac}    0.\n"
    txt += "'*'                0.0      0 \n"
    return txt

def calcul_equilibre_bnd_solution(boundary_solution,porosity,database):
    os.chdir('Boundary')
    ecriture_flow(boundary_solution['temperature'],porosity)
    ecriture_solute(len(boundary_solution['composition']),0,database,'boundary')
    ecriture_chemical_equilibre_boundary_solution(database,boundary_solution['composition'],boundary_solution['temperature'])
    titi=t2data.t2data("flow.inp")
    if sys.platform == 'darwin':
        exe_ini = './treactv3omp_eos9_macosx_intel'
    else:
        exe_ini = 'tr3.0-omp_eos9_PC64.exe'
    titi.run(simulator=exe_ini)
    shutil.copy2("plot.dat","eq_init.dat")
    species = recup_txt_species()
    os.chdir('..')
    eq_bnd_solution = {'temperature':boundary_solution['temperature'],'composition':species}
    return eq_bnd_solution

def calcul_equilibre_mineraux(material,database,complexation,kinetics,update_porosity):
    os.chdir('Material_equilibrium')
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
    list_minerals_TR = [x for x in list_minerals if x not in set(material.minerals)]
    for elem in list_minerals_TR:
        material.minerals[elem] = 0.0
    ecriture_solute(len(material.species),len(material.minerals),database,"reactive_transport",complexation,update_porosity,
                    D_eff=material.D_eff, porosite=material.porosite)
    ecriture_chemical_transport_reactif(database,material,bnd_solution,complexation,kinetics)
    titi=t2data.t2data("flow.inp")
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