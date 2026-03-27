"""
Species name conversion dictionaries between thermodynamic databases.

Three conversion mappings are provided:

- ``hydrat_thermoddem`` : hydration model notation (JFB) → THERMODDEM mineral names
- ``thermoddem_JFB`` : THERMODDEM mineral names → JFB notation (reverse of above)
- ``phreeqc_thermoddem`` : PHREEQC element symbols → THERMODDEM species names
- ``mineral_database`` : canonical internal keys → per-database mineral names,
  for each supported thermodynamic database file
- ``species_database`` : canonical ionic species keys → per-database name variants,
  used to normalise species names read from TOUGHREACT output
- ``ordered_list_species_database`` : ordered list of primary species per database
"""
hydrat_thermoddem = {}
hydrat_thermoddem['C3AH6'] = 'C3AH6'
hydrat_thermoddem['C4ASbH12'] = 'Monosulfoaluminate'
hydrat_thermoddem['C4ACb11H'] = 'Monocarboaluminate'
hydrat_thermoddem['C6ASb3H32'] = 'Ettringite'
hydrat_thermoddem['CH'] = 'Portlandite'
hydrat_thermoddem['CSH'] = 'Jennite'
hydrat_thermoddem['CSHp'] = 'Tobermorite' #A corriger CSHp => C/S = 1.1, Tobermorite => C/S = 0.83 !
hydrat_thermoddem['CSHLP'] = 'Tobermorite' #A corriger CSHp => C/S = 1.1, Tobermorite => C/S = 0.83 !
hydrat_thermoddem['CSHHD'] = 'Jennite'
hydrat_thermoddem['CSHLD'] = 'Tobermorite'
hydrat_thermoddem['CSbH2'] = 'Gypsum'
hydrat_thermoddem['SS'] = 'Quartz'
hydrat_thermoddem['FH3'] = 'Fe(OH)3'
hydrat_thermoddem['CCb'] = 'Calcite'
hydrat_thermoddem['C2S'] = 'C2S'
hydrat_thermoddem['C3A'] = 'C3A'
hydrat_thermoddem['C3S'] = 'C3S'
hydrat_thermoddem['C4AF'] = 'C4AF'
hydrat_thermoddem['C4AH13'] = 'C4AH13'
hydrat_thermoddem['C6AFS2H19'] = 'Fe_Ettringite' #Erreur à corriger !
hydrat_thermoddem['C3AFS0.84H4.32'] = 'C3AFS0.84H4.32'
hydrat_thermoddem['C3AS0.84H'] = 'C3AS0.84H4.32'
hydrat_thermoddem['C3FS0.95H'] = 'C3FS0.95H'
hydrat_thermoddem['C3FS1.34H'] = 'C3FS1.34H3.32'
hydrat_thermoddem['Magnesite'] = 'Magnesite'
hydrat_thermoddem['Monocarboaluminate'] = 'Monocarboaluminate'
hydrat_thermoddem['Dolomite(ordered)'] = 'Dolomite(ordered)'
hydrat_thermoddem['calcite'] = 'calcite'
hydrat_thermoddem['Aragonite'] = 'Aragonite'
hydrat_thermoddem['hydrotalcite'] = 'hydrotalcite'
hydrat_thermoddem['Si_Hydrogarnet'] = 'Si_Hydrogarnet'
hydrat_thermoddem['Jennite'] = 'Jennite'
hydrat_thermoddem['Tobermorite'] = 'Tobermorite'
hydrat_thermoddem['portlandite'] = 'portlandite'
hydrat_thermoddem['kuzel_salt'] = 'kuzel_salt'
hydrat_thermoddem['Friedel_salt'] = 'Friedel_salt'
hydrat_thermoddem['ettringite'] = 'ettringite13'


thermoddem_JFB = {}
thermoddem_JFB['C3AH6'] = 'C3AH6'
thermoddem_JFB['Monosulfoaluminate'] = 'C4ASbH12'
thermoddem_JFB['Monocarboaluminate'] = 'C4ACb11H'
thermoddem_JFB['Ettringite'] = 'C6ASb3H32'
thermoddem_JFB['Portlandite'] = 'CH'
#thermoddem_JFB['CSH(1.6)'] = 'CSH'
thermoddem_JFB['Jennite'] = 'CSH'
thermoddem_JFB['Gypsum'] = 'CSbH2'

phreeqc_thermoddem = {}
phreeqc_thermoddem['S'] = 'SO4--'
phreeqc_thermoddem['Si'] = 'HSiO3-'
phreeqc_thermoddem['Ca'] = 'Ca++'
phreeqc_thermoddem['Al'] = 'Al+++'
phreeqc_thermoddem['Na'] = 'Na+'
phreeqc_thermoddem['K'] = 'K+'
phreeqc_thermoddem['CSH(1.6)'] = 'CSH_1.6'
phreeqc_thermoddem['C3AH6'] = 'C3AH6'
phreeqc_thermoddem['Monosulfoaluminate'] = 'Monosulfoaluminate'
phreeqc_thermoddem['Ettringite'] = 'Ettringite'
phreeqc_thermoddem['Portlandite'] = 'Portlandite'
phreeqc_thermoddem['Gypsum'] = 'Gypsum'
phreeqc_thermoddem['Jennite'] = 'Jennite'

mineral_database = {
    'Thermoddem.txt':{
        'C3AH6': 'C3AH6',
        'MONOSULFOALUMINATE': 'Monosulfoaluminate',
        'MONOCARBOALUMINATE': 'Monocarboaluminate',
        'ETTRINGITE': 'Ettringite',
        'PORTLANDITE': 'Portlandite',
        'JENNITE': 'C1.6SH',#'Jennite', #
        'TOBERMORITE': 'C0.8SH',#'Tobermorite(11A)', #'Tobermorite', # #A corriger CSHp => C/S = 1.1, Tobermorite => C/S = 0.83 !
        'GYPSUM': 'Gypsum',
        'C2S': 'C2S',
        'C3A': 'C3A',
        'C3S': 'C3S',
        'C4AF': 'C4AF',
        'C4AH13': 'C4AH13',
        'C3AS0.84H4.32': 'C3AS0.84H4.32',#'C0.7A0.01SH',#'C3AS0.84H4.32',#'C1.6A0.01SH',#
        'C3AFS0.84H4.32': 'C3AFS0.84H4.32',
        'C3FS0.95H': 'C3FS0.95H',
        'C3FS1.34H3.32': 'C3FS1.34H3.32',
        'Magnesite': 'Magnesite',
        'DOLOMITE(ORDERED)': 'Dolomite(ordered)',
        'CALCITE': 'Calcite',
        'ARAGONITE': 'Aragonite',
        'HYDROTALCITE': 'Hydrotalcite',
        'SI_HYDROGARNET': 'Si_Hydrogarnet',
        'KUZEL_SALT': 'kuzel_salt',
        'FRIEDEL_SALT': 'Friedel_salt',
        'BRUCITE': 'Brucite',
        'FERRIHYDRITE(2L)': 'Ferrihydrite(2L)',
        'THAUMASITE': 'Thaumasite',
        'ANHYDRITE': 'Anhydrite',
        'MAGNESITE': 'Magnesite(Natur)',
        'PERICLASE': 'Periclase',
        'SEPIOLITE': 'Sepiolite',
        'CHRYSOTILE': 'Chrysotile',
        'GIBBSITE': 'Gibbsite',
        'FE(OH)3': 'Fe(OH)2'
    },
    'thermodatabase.out':{
        'C3AH6': 'C3AH6',
        'C4ASbH12': 'Monosulfoaluminate',
        'C4ACb11H': 'Monocarboaluminate',
        'C6ASb3H32': 'Ettringite',
        'CH': 'Portlandite',
        'CSH': 'Jennite',
        'CSHp': 'Tobermorite', #A corriger CSHp => C/S = 1.1, Tobermorite => C/S = 0.83 !
        'CSHLP': 'Tobermorite', #A corriger CSHp => C/S = 1.1, Tobermorite => C/S = 0.83 !
        'CSHHD': 'Jennite',
        'CSHLD': 'Tobermorite',
        'CSbH2': 'Gypsum',
        'C2S': 'C2S',
        'C3A': 'C3A',
        'C3S': 'C3S',
        'C4AF': 'C4AF',
        'C4AH13': 'C4AH13',
        'C3AS0.84H4.32': 'C3AS0.84H4.32',
        'C3FS0.95H': 'C3FS0.95H',
        'C3FS1.34H3.32': 'C3FS1.34H3.32',
        'MAGNESITE': 'Magnesite',
        'MONOCARBOALUMINATE': 'Monocarboaluminate',
        'MONOSULFOALUMINATE': 'Monosulfoaluminate',
        'DOLOMITE(ORDERED)': 'Dolomite(ordered)',
        'CALCITE': 'calcite',
        'HYDROTALCITE': 'hydrotalcite',
        'SI_HYDROGARNET': 'Si_Hydrogarnet',
        'JENNITE': 'Jennite',
        'TOBERMORITE': 'Tobermorite',
        'PORTLANDITE': 'portlandite',
        'KUZEL_SALT': 'kuzel_salt',
        'FRIEDEL_SALT': 'Friedel_salt',
        'ETTRINGITE': 'ettringite',
        'BRUCITE': 'Brucite',
        'GYPSUM': 'Gypsum',
        'THAUMASITE': 'Thaumasite',
        'ANHYDRITE': 'Anhydrite',
        'MAGNESITE': 'Magnesite(Natur)',
        'PERICLASE': 'Periclase',
        'SEPIOLITE': 'Sepiolite',
        'CHRYSOTILE': 'Chrysotile',
    },
    'cemdata18_2022.out':{
        'C3AH6': 'C3AH6',
        'MONOSULFOALUMINATE': 'monosulphate9',
        'MONOCARBOALUMINATE': 'monocarbonate9',
        'ETTRINGITE': 'ettringite',
        'PORTLANDITE': 'Portlandite',
        'JENNITE': 'Jennite',#'CSHQ-JenD',# 
        'TOBERMORITE': 'Tob-I', #'CSHQ-TobH',# A corriger CSHp => C/S = 1.1, Tobermorite => C/S = 0.83 !
        'GYPSUM': 'Gp',
        'C2S': 'C2S',
        'C3A': 'C3A',
        'C3S': 'C3S',
        'C4AF': 'C4AF',
        'C4AH13': 'C4AH13',
        'C3AS0.84H4.32': 'C3AS0.84H4.32',
        'C3AFS0.84H4.32': 'C3AFS0.84H4.32',
        'C3FS0.95H': 'C3FS0.84H4.32',
        'C3FS1.34H3.32': 'C3FS1.34H3.32',
        'DOLOMITE(ORDERED)': 'Ord-Dol',
        'CALCITE': 'Cal',
        'ARAGONITE': 'Arg',
        'HYDROTALCITE': 'hydrotalcite',
        #'SI_HYDROGARNET': None,
        'KUZEL_SALT': 'C4AsClH12',
        'FRIEDEL_SALT': 'C4AClH10',
        'BRUCITE': 'Brc',
        'THAUMASITE': 'thaumasite',
        'ANHYDRITE': 'Anh',
        'MAGNESITE': 'Mgs',
        #'PERICLASE': None,
        'SEPIOLITE': 'M075SH',
        'CHRYSOTILE': 'M15SH',
        'GIBBSITE': 'AlOHam',
        'FE(OH)3': 'Fe(OH)3(am)'
    },
}
mineral_database['thermoddem_hsio3.out'] = mineral_database['Thermoddem.txt']
mineral_database['Th_Yoshida2021.txt'] = mineral_database['Thermoddem.txt']
mineral_database['Thermoddem_2023.txt'] = mineral_database['Thermoddem.txt']
mineral_database['kswitch.out'] = mineral_database['cemdata18_2022.out']
mineral_database['cemdata.out'] = mineral_database['cemdata18_2022.out']


ordered_list_species_database = {
    'Thermoddem.txt': ['h2o','h+','ca+2','so4-2','h4sio4','hco3-','k+','na+','mg+2','al+3','fe+2','o2(aq)'],#,'fe+3','cl-'
    'kswitch.out': ['h2o','h+','ca+2','so4-2','h4sio4','hco3-','k+','na+','mg+2','al+3'],#,'fe+3','fe+2','cl-'
    'thermoddem_hsio3.out': ['h2o','h+','ca+2','so4-2','hsio3-','hco3-','k+','na+','mg+2','al+3'],#,'fe+3','fe+2','cl-'
    'thermodatabase.out': ['h2o','h+','ca+2','so4-2', 'hsio3-','k+','na+','mg+2','al+3','cl-','fe+2'],#,'co3-2'
    'cemdata18_2022.out': ['h2o','h+','alo2-','co3-2','ca+2','cl-','feo2-','k+','na+','mg+2','so4-2', 'sio2(aq)'],#,'co3-2'
    'cemdata.out': ['h2o','h+','ca+2','so4-2','hsio3-','hco3-','k+','na+','mg+2','al+3','fe+2','o2(aq)']#,'fe+3','fe+2','cl-'
#['h2o','h+','ca+2','so4-2','sio2(aq)','co3-2','k+','na+','mg+2','alo2-','cl-','fe+3','fe+2']
}
ordered_list_species_database['Th_Yoshida2021.txt'] = ordered_list_species_database['Thermoddem.txt']
ordered_list_species_database['Thermoddem_2023.txt'] = ordered_list_species_database['Thermoddem.txt']

species_database = {
    'Thermoddem.txt': {
        # 'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal': -0.4070E-01},
        # 'ca+2':{'guess':1.0e-30,'ctotal':1.0e-30},'so4-2':{'guess':1.0e-30,'ctotal':1.0e-30},
        # 'h4sio4':{'guess':1.0e-30,'ctotal':1.0e-30},'mg+2':{'guess':1.0e-30,'ctotal':1.0e-30},
        # 'al+3':{'guess':1.0e-30,'ctotal':1.0e-30},'cl-':{'guess':1.0e-30,'ctotal':1.0e-30},
        # 'hco3-':{'guess':1.0e-30,'ctotal':1.0e-30}#,'fe+2':{'guess':1.0e-30,'ctotal':1.0e-30}
        'H2O': ['h2o', 'H2o', 'H2O'],
        'H+': ['h+', 'H+'],
        'Ca+2': ['ca+2', 'CA+2', 'Ca+2'],
        'SO4-2': ['so4-2', 'SO4-2', 'So4-2'],
        'H4SiO4': ['h4sio4', 'H4SIO4', 'H4SiO4', 'H4Sio4'],
        'HCO3-': ['hco3-', 'HCO3-'],
        'K+': ['k+', 'K+'],
        'Na+': ['na+', 'Na+', 'NA+'],
        'Mg+2': ['mg+2', 'MG+2', 'Mg+2'],
        'Al+3': ['al+3', 'AL+3', 'Al+3'],
        'Cl-': ['cl-', 'CL-', 'Cl-'],
        'Fe+2': ['fe+2', 'Fe+2', 'FE+2'],
        'O2(aq)': ['o2(aq)', 'O2(aq)'],
        'csh_oh': ['csh_oh'],
        'csh_oh1': ['csh_oh1'],
        'por_oh': ['por_oh'],
        'cas_oh': ['cas_oh'],
        'mon': ['mon']
        },
    'thermoddem_hsio3.out': {
        'H2O': ['h2o', 'H2o', 'H2O'],
        'H+': ['h+', 'H+'],
        'Ca+2': ['ca+2', 'CA+2', 'Ca+2'],
        'SO4-2': ['so4-2', 'SO4-2', 'So4-2'],
        'HSiO3-': ['hsio3-', 'HSIO3-', 'HSiO3-'],
        'HCO3-': ['hco3-', 'HCO3-'],
        'K+': ['k+', 'K+'],
        'Na+': ['na+', 'Na+', 'NA+'],
        'Mg+2': ['mg+2', 'MG+2', 'Mg+2'],
        'Al+3': ['al+3', 'AL+3', 'Al+3'],
        'Cl-': ['cl-', 'CL-', 'Cl-'],
        'Fe+2': ['fe+2', 'Fe+2', 'FE+2'],
        'O2(aq)': ['o2(aq)', 'O2(aq)'],
        'csh_oh': ['csh_oh'],
        'csh_oh1': ['csh_oh1']
        },
    'cemdata18_2022.out': {
        'H2O': ['h2o', 'H2o', 'H2O'],
        'H+': ['h+', 'H+'],
        'AlO2-': ['alo2-', 'ALO2-', 'AlO2-'],
        'CO3-2': ['co3-2', 'CO3-2'],
        'Ca+2': ['ca+2', 'CA+2', 'Ca+2'],
        'Cl-': ['cl-', 'CL-', 'Cl-'],
        'FeO2-': ['feo2-', 'FEO2-', 'FeO2-'],
        'K+': ['k+', 'K+'],
        'Na+': ['na+', 'Na+', 'NA+'],
        'Mg+2': ['mg+2', 'MG+2', 'Mg+2'],
        'SO4-2': ['so4-2', 'SO4-2', 'So4-2'],
        'SiO2(aq)': ['sio2(aq)', 'SIO2(AQ)', 'SiO2(aq)'],
        'csh_oh': ['csh_oh'],
        'csh_oh1': ['csh_oh1']
        },
    'cemdata.out': {
        'H2O': ['h2o', 'H2o', 'H2O'],
        'H+': ['h+', 'H+'],
        'Al+3': ['al+3', 'AL+3', 'Al+3'],
        'HCO3-': ['hco3-', 'HCO3-'],
        'Ca+2': ['ca+2', 'CA+2', 'Ca+2'],
        'Cl-': ['cl-', 'CL-', 'Cl-'],
        'Fe+2': ['fe+2', 'FE+2', 'Fe+2'],
        'K+': ['k+', 'K+'],
        'Na+': ['na+', 'Na+', 'NA+'],
        'Mg+2': ['mg+2', 'MG+2', 'Mg+2'],
        'SO4-2': ['so4-2', 'SO4-2', 'So4-2'],
        'HSiO3-': ['hsio3-', 'HSIO3-', 'HSiO3-'],
        'O2(aq)': ['o2(aq)', 'O2(aq)', 'O2(AQ)'],
        'csh_oh': ['csh_oh'],
        'csh_oh1': ['csh_oh1']
        },
    'thermodatabase.out':{
        'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal': -0.4070E-01},
        'ca+2':{'guess':1.0e-30,'ctotal':1.0e-30},'so4-2':{'guess':1.0e-30,'ctotal':1.0e-30},
        'hsio3-':{'guess':1.0e-30,'ctotal':1.0e-30},'mg+2':{'guess':1.0e-30,'ctotal':1.0e-30},
        'al+3':{'guess':1.0e-30,'ctotal':1.0e-30},'cl-':{'guess':1.0e-30,'ctotal':1.0e-30},
        #'fe+3':{'guess':1.0e-30,'ctotal':1.0e-30}}#'co3-2':{'guess':1.0e-30,'ctotal':1.0e-30},
        }
    # {
    #     'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal': -0.4070E-01},
    #     'ca+2':{'guess':1.0e-30,'ctotal':1.0e-30},'so4-2':{'guess':1.0e-30,'ctotal':1.0e-30},
    #     'sio2(aq)':{'guess':1.0e-30,'ctotal':1.0e-30},'mg+2':{'guess':1.0e-30,'ctotal':1.0e-30},
    #     'alo2-':{'guess':1.0e-30,'ctotal':1.0e-30},'cl-':{'guess':1.0e-30,'ctotal':1.0e-30},
    #     'co3-2':{'guess':1.0e-30,'ctotal':1.0e-30},'fe+3':{'guess':1.0e-30,'ctotal':1.0e-30}
    #     }
}
species_database['kswitch.out'] = species_database['Thermoddem.txt']
species_database['Th_Yoshida2021.txt'] = species_database['Thermoddem.txt']
species_database['Thermoddem_2023.txt'] = species_database['Thermoddem.txt']

def convert_ionic_species(species: str, database: str) -> str | None:
    """Return the canonical species key for a raw species name from a given database.

    Searches ``species_database[database]`` for a canonical key whose list of
    known variants contains ``species``, and returns that key.

    Parameters
    ----------
    species : str
        Raw species name as it appears in TOUGHREACT output (e.g. ``'ca+2'``,
        ``'CA+2'``).
    database : str
        Thermodynamic database filename key (e.g. ``'Thermoddem.txt'``,
        ``'cemdata18_2022.out'``).

    Returns
    -------
    str or None
        Canonical species key (e.g. ``'Ca+2'``), or ``None`` if not found
        (a message is also printed to stdout).
    """
    trouvee = False
    for elem in species_database[database]:
        if species in species_database[database][elem]:
            tourvee = True
            return elem
    if not trouvee:
        print('species ' + elem + ' not in database!')