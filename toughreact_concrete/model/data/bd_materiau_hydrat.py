'''
Created on 6 juin 2016

@author: anthonysoive
'''

VolumeMolaire = {}
#                                    cm³/mol    Formule
VolumeMolaire['ettringite']          = 707      #Ca6Al2(SO4)3(OH)12.26H2O 
VolumeMolaire['Hydrotalcite']        = 220      #Mg6Al2CO3(OH)16:4(H2O)
VolumeMolaire['portlandite']         = 33       #Ca(OH)2
VolumeMolaire['Goethite']            = 23.383   #Alpha-FeOOH
VolumeMolaire['Monosulfoaluminate']  = 309      #Ca6Al2(SO4)3(OH)12:26(H2O)
VolumeMolaire['Gibbsite']            = 33.194   #Al(OH)3
VolumeMolaire['Jennite']             = 78       #Ca9Si6O18(OH)6·8H2O 
VolumeMolaire['Tobermorite']         = 59       #Ca5Si6O16(OH)2·4H2O 
VolumeMolaire['Thaumasite']          = 333.67   #Ca3Si(OH)12.12H2O 
VolumeMolaire['Monocarboaluminate']  = 0       #Ca6Al2(SO4)3(OH)12:26(H2O)
VolumeMolaire['Gypsum']              = 74      #CaSO4.2H2O
VolumeMolaire['Anhydrite']           = 46      #CaSO4
VolumeMolaire['Friedel_salt']        = 263     #C3A.CaCl2.10H2O
VolumeMolaire['Calcite']             = 36.9    #CaCO3
# Sepiolite        Mg4Si6O15(OH)2·6H2O 
# Chrysotile        Mg3Si2O5(OH)4
# Brucite        Mg(OH)2
# Periclase        MgO
# Calcite        CaCO3
# Thaumasite        Ca3Si(OH)6(CO3)(SO4):12(H2O)

minerals_in = {}
species_in = {}
species_in_trame = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20}}#'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 
# species_in_trame = {'h2o':{'guess':1.0,'ctotal':1.0},'oh-':{'guess':1.0E-1,'ctotal':1.0e-1},
#                         'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
#                         'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
#                         'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
#                         'cl-':{'guess':1.0e-20,'ctotal':1.0e-20}}

#GEMS Results
minerals_in['M25FA'] = {'ettringite':0.0,'Hydrotalcite':0.00304,
                      'portlandite':0.006627,'Monosulfoaluminate':0.02541,
                      'Gibbsite':0.0,'Jennite':0.08242,'Tobermorite':0.00916,
                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
species_in['M25FA'] = species_in_trame
species_in['M25FA']['k+'] = {'guess':0.495877177850612,'ctotal':0.495877177850612}
species_in['M25FA']['na+'] = {'guess':0.060238054165948,'ctotal':0.060238054165948}
# species_in['M25FA'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
#                         'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
#                         'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
#                         'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
#                         'cl-':{'guess':1.0e-20,'ctotal':1.0e-20},
#                         'k+':{'guess':0.495877177850612,'ctotal':0.495877177850612},
#                         'na+':{'guess':0.060238054165948,'ctotal':0.060238054165948}}

minerals_in['M25'] = {'ettringite':0.00641,'Hydrotalcite':0.00307,
                      'portlandite':0.04363,'Monosulfoaluminate':0.02194,
                      'Gibbsite':0.0,'Jennite':0.06645,'Tobermorite':0.00739,
                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
species_in['M25'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.115326759150928,'ctotal':0.115326759150928},
                        'na+':{'guess':0.046130703660371,'ctotal':0.046130703660371}}

minerals_in['M30FA'] = {'ettringite':0.02184,'Hydrotalcite':0.00381,
                      'portlandite':0.0,'Monosulfoaluminate':0.0,
                      'Gibbsite':0.0,'Jennite':0.07973,'Tobermorite':0.03462,
                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
species_in['M30FA'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':1.01059075009716,'ctotal':1.01059075009716},
                        'na+':{'guess':0.096307811892732,'ctotal':0.096307811892732}}

# minerals_in['M50FA'] = {'ettringite':0.0,'Hydrotalcite':0.00502,
#                       'portlandite':0.01169,'Monosulfoaluminate':0.04216,
#                       'Gibbsite':0.0,'Jennite':0.13619,'Tobermorite':0.01514,
#                       'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
#                       'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
#                       'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
minerals_in['M50FA'] = {'ettringite':0.0,'Hydrotalcite':0.004518,
                      'portlandite':0.010521,'Monosulfoaluminate':0.037944,
                      'Gibbsite':0.0,'Jennite':0.122571,'Tobermorite':0.013626,
                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
species_in['M50FA'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.84535733380859,'ctotal':0.84535733380859},
                        'na+':{'guess':0.10329709499198,'ctotal':0.10329709499198}}

minerals_in['M50'] = {'ettringite':0.01115,'Hydrotalcite':0.00535,
                      'portlandite':0.07625,'Monosulfoaluminate':0.03826,
                      'Gibbsite':0.0,'Jennite':0.11596,'Tobermorite':0.01289,
                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
species_in['M50'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.201408220075323,'ctotal':0.201408220075323},
                        'na+':{'guess':0.080563288030129,'ctotal':0.080563288030129}}

minerals_in['M75'] = {'ettringite':0.01206,'Hydrotalcite':0.00582,
                      'portlandite':0.08298,'Monosulfoaluminate':0.04162,
                      'Gibbsite':0.0,'Jennite':0.12611,'Tobermorite':0.01402,
                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
species_in['M75'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.305567830313743,'ctotal':0.305567830313743},
                        'na+':{'guess':0.122227132125497,'ctotal':0.122227132125497}}

#minerals_in['M75SF'] = {'ettringite':0.00945,'Hydrotalcite':0.004564,
#                      'portlandite':0.043931,'Monosulfoaluminate':0.03182,
#                      'Gibbsite':0.0,'Jennite':0.12305,'Tobermorite':0.01368,
#                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
#                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
#                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
minerals_in['M75SF'] = {'portlandite': 0.04146633333333333, 'Monosulfoaluminate': 0.0,
           'ettringite': 0.02127991444444444, 'Jennite': 0.08046046666666667,
           'kuzel_salt':0.0,'Friedel_salt':0.,
           'Tobermorite': 0.01120672222222222, 'C3AH6': 0.0, 'Gypsum': 0.0037759114555555554, 
           'C3AS0.84H': 0.012491798666666663}#, 'C3FS1.34H': 0.01302051633333333}
#minerals_in['M75SF'] = {'ettringite':0.05,'Hydrotalcite':0.02,
#                      'portlandite':0.0,'Monosulfoaluminate':0.0,
#                      'Gibbsite':0.0,'Jennite':0.21,'Tobermorite':0.0,
#                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
#                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
#                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
species_in['M75SF'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        #'fe+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.2926944971537,'ctotal':0.2926944971537},
                        'na+':{'guess':0.114990512333966,'ctotal':0.114990512333966}}
#'h+':{'guess':1.0E-13,'ctotal':1.0e-13},0.4789E-13 -0.1844E+00

minerals_in['M100SF'] = {'ettringite':0.0098,'Hydrotalcite':0.004755,
                      'portlandite':0.03201,'Monosulfoaluminate':0.03262,
                      'Gibbsite':0.0,'Jennite':0.14413,'Tobermorite':0.01603,
                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
species_in['M100SF'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.363423517169615,'ctotal':0.363423517169615},
                        'na+':{'guess':0.141415192507804,'ctotal':0.141415192507804}}

#Attention : convergence non assurée !
minerals_in['M120SF'] = {'ettringite':0.0,'Hydrotalcite':0.0,
                      'portlandite':0.04809,'Monosulfoaluminate':0.0,
                      'Gibbsite':0.0,'Jennite':0.1876,'Tobermorite':0.01067,
                      'kuzel_salt':0.0,'Friedel_salt':0.,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,
                      'Magnesite':0.0,'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                      'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Dolomite(ordered)':0.0}
species_in['M120SF'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.47060353798127,'ctotal':0.47060353798127},
                        'na+':{'guess':0.182310093652445,'ctotal':0.182310093652445}}
#---------------


minerals_in['BO'] = {'kuzel_salt':0.0,'portlandite':0.7180E-01,'hydrotalcite':0.4471E-02,
                     'Monosulfoaluminate':0.2967E-01,'ettringite':0.4360E-02,'Jennite':0.1150E-00,
                     'Tobermorite':0.1224E-01,'Periclase':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Gibbsite':0.0,'Gypsum':0.0,
                    'Anhydrite':0.0,'Magnesite':0.0,'Brucite':0.0,'thaumasite':0.0,'Monocarboaluminate':0.0,
                    'Dolomite(ordered)':0.0,'calcite':0.0,'friedel_salt':0.0}
species_in['BO'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':0.3790E-13,'ctotal':-0.4295E+00},
                    'ca+2':{'guess':0.3931E-03,'ctotal':0.9171E-03},'so4-2':{'guess':0.3191E-03,'ctotal':0.4763E-03},
                    'co3-2':{'guess':0.1055E-17,'ctotal':0.2480E-17}, 'hsio3-':{'guess':0.4787E-04,'ctotal':0.4787E-04},
                    'k+':{'guess':0.1282E+00,'ctotal':0.1572E+00},'na+':{'guess':0.2429E-00,'ctotal':0.2721E-00},
                    'mg+2':{'guess':0.2354E-10,'ctotal':0.2354E-10},'al+3':{'guess':0.9037E-33,'ctotal':0.4965E-03},
                    'cl-':{'guess':0.2496E-13,'ctotal':0.2840E-13}}#'hco3-':{'guess':0.1055E-17,'ctotal':0.2480E-17}
minerals_in['BO-III'] = {'kuzel_salt':0.0,'Friedel_salt':0.,'portlandite':0.5900E-01,
                         'Monosulfoaluminate':0.3269E-01,'ettringite':0.1925E-01,'Jennite':0.1020E-00,
                         'Tobermorite':0.1086E-01,'Periclase':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Gibbsite':0.0,'Gypsum':0.0,
                      'Anhydrite':0.0,'Magnesite':0.0,'Brucite':0.0,'thaumasite':0.0,'Monocarboaluminate':0.0,
                      'Dolomite(ordered)':0.0,'calcite':0.0}
species_in['BO-III'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':0.2755E-12,'ctotal':-0.4077E-01},
                        'ca+2':{'guess':0.1588E-01,'ctotal':0.1969E-01},'so4-2':{'guess':0.2248E-05,'ctotal':0.3703E-05},
                        'co3-2':{'guess':0.4086E-18,'ctotal':0.2463E-17}, 'hsio3-':{'guess':0.8519E-06,'ctotal':0.8519E-05},
                        'k+':{'guess':0.2389E-17,'ctotal':0.2463E-17},'na+':{'guess':0.2423E-17,'ctotal':0.2463E-17},
                        'mg+2':{'guess':0.3440E-18,'ctotal':0.2463E-17},'al+3':{'guess':0.1544E-30,'ctotal':0.4843E-04},
                        'cl-':{'guess':0.1247E-16,'ctotal':0.8863E-16}}
minerals_in['BO-III-APOS'] = {'kuzel_salt':0.0,'Friedel_salt':0.,'portlandite':0.000375128,
                         'Monosulfoaluminate':0.028424729,'ettringite':0.0,'Jennite':0.09804379,
                         'Tobermorite':0.010418172,'Hydrotalcite':0.021594662,'Periclase':0.0,
                         'Chrysotile':0.0,'Sepiolite':0.0,'Gibbsite':0.0,'Gypsum':0.0,
                         'Anhydrite':0.0,'Magnesite':0.0,'Brucite':0.0,'thaumasite':0.0,'Monocarboaluminate':0.0,
                         'Dolomite(ordered)':0.0,'calcite':0.0}#,'goethite':0.000883572}
species_in['BO-III-APOS'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':0.6773E-13,'ctotal':-0.2034E-00},
                        'ca+2':{'guess':0.1162E-02,'ctotal':0.2108E-02},'so4-2':{'guess':0.6767E-04,'ctotal':0.9020E-04},
                        'co3-2':{'guess':0.1188E-17,'ctotal':0.2478E-17}, 'hsio3-':{'guess':0.1128E-04,'ctotal':0.1128E-04},
                        'k+':{'guess':0.2389E-17,'ctotal':0.3931887},'na+':{'guess':0.2423E-17,'ctotal':0.2463E-17},
                        'mg+2':{'guess':0.5755E-10,'ctotal':0.1263E-08},'al+3':{'guess':0.3946E-32,'ctotal':0.2426E-03},
                        'cl-':{'guess':0.2689E-13,'ctotal':0.2839E-13}}
minerals_in['BO-APOS'] = {'kuzel_salt':0.0,'Friedel_salt':0.,'portlandite':0.056133627,
                         'Monosulfoaluminate':0.02802296,'ettringite':0.0,'Jennite':0.082878334,
                         'Tobermorite':0.008810598,'Hydrotalcite':0.004735013,'Periclase':0.0,
                         'Chrysotile':0.0,'Sepiolite':0.0,'Gibbsite':0.0,'Gypsum':0.0,
                         'Anhydrite':0.0,'Magnesite':0.0,'Brucite':0.0,'thaumasite':0.0,'Monocarboaluminate':0.0,
                         'Dolomite(ordered)':0.0,'calcite':0.0}#,'Goethite':0.003384582}
species_in['BO-APOS'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.12,'ctotal':0.12},'na+':{'guess':0.12,'ctotal':0.12},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20}}

minerals_in['CEMI_SF_Rilem'] = {'kuzel_salt':0.0,'Friedel_salt':0.,'portlandite':0.2367E-01,
                         'Monosulfoaluminate':0.3753E-01,'ettringite':0.9179E-02,
                         'Jennite':0.2523E+00,'Tobermorite':0.1478E-01,
                         'Hydrotalcite':0.1050E-01,'Periclase':0.0,
                         'Gypsum':0.0,
                         'Anhydrite':0.0,'Magnesite':0.0,
                         'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                         'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,
                         'Dolomite(ordered)':0.0}##'Goethite':0.005721957647059}#'Gibbsite':0.0,
species_in['CEMI_SF_Rilem'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.17,'ctotal':0.17},'na+':{'guess':0.1,'ctotal':0.1},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20}}
minerals_in['CEMI_SF_Rilem_peau'] = minerals_in['CEMI_SF_Rilem']
species_in['CEMI_SF_Rilem_peau'] = species_in['CEMI_SF_Rilem']

minerals_in['Bonaduz_CEMI'] = {'Friedel_salt':0.,'portlandite':0.0747427967,
                         'Monosulfoaluminate':0.037501468961/3,'ettringite':0.010917294468,
                         'Jennite':0.11364964953,'Tobermorite':0.0126361545,
                         'Hydrotalcite':0.00525301062}
#'kuzel_salt':0.0,
#'Monocarboaluminate':0.0,'calcite':0.0,'thaumasite':0.0,'Magnesite':0.0,'Dolomite(ordered)':0.0,
#,'Periclase':0.0,'Gypsum':0.0,'Anhydrite':0.0,'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0
species_in['Bonaduz_CEMI'] = species_in_trame
species_in['Bonaduz_CEMI']['k+'] = {'guess':0.115326759150928,'ctotal':0.115326759150928}
species_in['Bonaduz_CEMI']['na+'] = {'guess':0.046130703660371,'ctotal':0.046130703660371}

minerals_in['Bonaduz_CEMI_SF'] = {'kuzel_salt':0.0,'Friedel_salt':0.,'portlandite':0.047581965556424584,
                         'Monosulfoaluminate':0.03754210912022346,'ettringite':0.011149784893072626,
                         'Jennite':0.1455235472178771,'Tobermorite':0.016105603974301677,
                         'Hydrotalcite':0.005393355405586593}
#,'Periclase':0.0,
#                         'Gypsum':0.0,
#                         'Anhydrite':0.0,'Magnesite':0.0,
#                         'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
#                         'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,
#                         'Dolomite(ordered)':0.0}
species_in['Bonaduz_CEMI_SF'] = species_in_trame
species_in['Bonaduz_CEMI_SF']['k+'] = {'guess':0.14295918695994764,'ctotal':0.14295918695994764}
species_in['Bonaduz_CEMI_SF']['na+'] = {'guess':0.08532024310425433,'ctotal':0.08532024310425433}

minerals_in['Naxberg'] = {'kuzel_salt':0.0,'Friedel_salt':0.,'portlandite':0.061423736,
                         'Monosulfoaluminate':0.03257598235333333,'ettringite':0.009482478817777777,
                         'Jennite':0.09895183133333334,'Tobermorite':0.01080135092222222,
                         'Hydrotalcite':0.004562969644444445,'Periclase':0.0,
                         'Gypsum':0.0,
                         'Anhydrite':0.0,'Magnesite':0.0,
                         'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                         'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,
                         'Dolomite(ordered)':0.0}
species_in['Naxberg'] = species_in_trame
species_in['Naxberg']['k+'] = {'guess':0.115326759150928,'ctotal':0.115326759150928}
species_in['Naxberg']['na+'] = {'guess':0.046130703660371,'ctotal':0.046130703660371}


#Auto-cicatrisation Benoit (ECN)
minerals_in['B_Cicat'] = {'kuzel_salt':0.0,'friedel_salt':0.0,'portlandite':0.1523E+00,'hydrotalcite':0.9901E+00,
                      'Monocarboaluminate':0.,'Monosulfoaluminate':0.9207E-01,'ettringite':0.3699E-04,'Jennite':0.1982E+00,
                      'Tobermorite':0.2111E-01,'Periclase':0.0,'Chrysotile':0.0,'Sepiolite':0.0,'Gibbsite':0.1572E-02,'Gypsum':0.0,
                      'Anhydrite':0.0,'Magnesite':0.0,'Brucite':0.6498E-11,'Monocarboaluminate':0.0,
                      'Dolomite(ordered)':0.0,'calcite':0.0}
species_in['B_Cicat'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':0.6643E-13,'ctotal':-0.3155E+00},
                      'ca+2':{'guess':0.1267E-02,'ctotal':0.2269E-02},'so4-2':{'guess':0.3965E-02,'ctotal':0.7701E-02},
                      'co3-2':{'guess':0.1941E-17,'ctotal':0.2541E-17},'hsio3-':{'guess':0.5522E-05,'ctotal':0.5522E-05},
                      'k+':{'guess':0.6841E+00,'ctotal':0.8017E+00},'na+':{'guess':0.4707E-01,'ctotal':0.5659E-01},
                      'mg+2':{'guess':0.1765E-09,'ctotal':0.1780E-09},'al+3':{'guess':0.1003E-32,'ctotal':0.5540E-04},
                      'cl-':{'guess':0.2831E+00,'ctotal':0.3154E+00}}

minerals_in_tmp = {}
minerals_in_tmp['Rion'] = {#'Jennite': 0.13412526493799323, 'Tobermorite': 0.014640619853438555, 'Monosulfoaluminate': 0.04056795855693349, 'ettringite': 0.0, 'Gibbsite': 0.015124584182638108, 'portlandite': 0.016914863201803833, 'Hydrotalcite': 0.0,
                       #'Jennite': 0.15849751251409244, 'Tobermorite': 0.017539996257046223, 'Monosulfoaluminate': 0.03459060716685457, 'ettringite': 0.0, 'Gibbsite': 0.006594206583990981, 'portlandite': 0.0021572000293122885, 'Hydrotalcite': 0.0350769190529876,
                       #'Jennite': 0.22798304372093026, 'Tobermorite': 0.03321258445219639, 'Monosulfoaluminate': 0.060413360104651155, 'ettringite': 0.0, 'Gibbsite': 0.008163796282945735, 'portlandite': 0.0, 'Hydrotalcite': 0.050148729121447015, 
                       'Jennite': 0.1523712940248027, 'Tobermorite': 0.009160224261555806, 'Monosulfoaluminate': 0.0, 'ettringite': 0.03094089453213078, 'Straetlingite': 0.049819699744757605, 'portlandite': 0.0, 'Hydrotalcite': 0.03366461330326945,#Lothenbach, 2012 wo monosulfo
                       #'Jennite': 0.061747420518602034, 'Tobermorite': 0.016421289740698983, 'Monosulfoaluminate': 0.0, 'ettringite': 0.0012050085682074408, 'Straetlingite': 0.002564009168534386, 'portlandite': 0.0, 'Hydrotalcite': 0.013465885005636979, 'kuzel_salt': 0.019791174515219844,
                       #'Jennite': 0.13735738444193912, 'Tobermorite': 0.025675310033821872, 'Monosulfoaluminate': 0.040567136414881626, 'ettringite': 0.0, 'Straetlingite': 0.030946216026606535, 'portlandite': 0.0, 'Hydrotalcite': 0.03366461330326945,#Lothenbach, 2012
                       #'Jennite': 0.06239846462232243, 'Tobermorite': 0.004126587312288613, 'Monosulfoaluminate': 0.0, 'ettringite': 0.004985745348590756, 'Straetlingite': 0.002564009168534386, 'portlandite': 0.0, 'Hydrotalcite': 0.01683076764374295, 'kuzel_salt': 0.025474291419391202,
                      'Gypsum':0.0,
                         'Anhydrite':0.0,'Magnesite':0.0,
                         'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                         'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,
                         'Dolomite(ordered)':0.0,'kuzel_salt':0.0,'Friedel_salt':0.}
minerals_in['Rion'] = {}
for elem in minerals_in_tmp['Rion'].keys():
    if elem == ('Jennite' or 'Tobermorite'):
        minerals_in['Rion'][elem] = minerals_in_tmp['Rion'][elem]
    else:
        minerals_in['Rion'][elem] = minerals_in_tmp['Rion'][elem]
# minerals_in['Rion'] = {'kuzel_salt':0.0,'Friedel_salt':0.,'portlandite':0.0,
#                          'Monosulfoaluminate':0.0405515,'ettringite':0.0,
#                          'Jennite':0.15302998,'Tobermorite':0.022293,
#                          'Hydrotalcite':0.0336615,'Periclase':0.0,
#                          'Gypsum':0.0, 'Gibbsite':0.0054798,
#                          'Anhydrite':0.0,'Magnesite':0.0,
#                          'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
#                          'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,
#                          'Dolomite(ordered)':0.0}##'Goethite':0.005721957647059}#'Gibbsite':0.0,
species_in['Rion'] = species_in_trame
species_in['Rion']['k+'] = {'guess':0.0653302279698305,'ctotal':0.0653302279698305}
species_in['Rion']['na+'] = {'guess':0.03970223325062034,'ctotal':0.03970223325062034}

minerals_in['Missiessy'] = {'Jennite': 0.12035566, 'Tobermorite': 0.013375678842105264, 
                       'Monosulfoaluminate': 0.019978385964912283, 'ettringite': 0.0236984514666666, 
                       'Gibbsite': 0.0, 'portlandite': 0.07519732000000001, 'Hydrotalcite': 0.006942779040935672, 
                       'Gypsum':0.0,
                         'Anhydrite':0.0,'Magnesite':0.0,
                         'thaumasite':0.0,'calcite':0.0,'Monocarboaluminate':0.0,
                         'Brucite':0.0,'Chrysotile':0.0,'Sepiolite':0.0,
                         'Dolomite(ordered)':0.0,'kuzel_salt':0.0,'Friedel_salt':0.}
species_in['Missiessy'] = {'h2o':{'guess':1.0,'ctotal':1.0},'h+':{'guess':1.0E-13,'ctotal':1.0e-13},
                        'ca+2':{'guess':1.0e-20,'ctotal':1.0e-20},'so4-2':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'co3-2':{'guess':1.0e-20,'ctotal':1.0e-20}, 'hsio3-':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'k+':{'guess':0.04246464818038983,'ctotal':0.17},'na+':{'guess':0.15053763440860213,'ctotal':0.1},
                        'mg+2':{'guess':1.0e-20,'ctotal':1.0e-20},'al+3':{'guess':1.0e-20,'ctotal':1.0e-20},
                        'cl-':{'guess':1.0e-20,'ctotal':1.0e-20}}

#minerals_in['cem1_ASE'] = {'portlandite':1.91,'Monosulfoaluminate':0.1655,'ettringite':0.0,
#                 'Jennite':1.22,'Tobermorite':0.1796,'Gypsum':0.0,
#                 'Hydrotalcite':0.0417}#,'C3AH6':0.0
#{'portlandite': 0.034987333333333336, 'Monosulfoaluminate': 0.021870333333333332, 
# 'ettringite': 0.0021995555555555553, 'Jennite': 0.05083866666666667, 
# 'Tobermorite': 0.005401777777777778, 'C3AH6': 0.0, 'Gypsum': 0.0, 
# 'Hydrotalcite': 0.00484}
#Van-Quan ?
minerals_in['cem1_ASE'] = {'portlandite':0.2701E+00,
           'Monosulfoaluminate':0.2311E+00,'ettringite':0.1367E-07,
           'Jennite':0.4268E+00,'Tobermorite':0.4546E-01,
           'Gypsum':0.0,'gibbsite':0.2544E-02,
           'hydrotalcite':0.2708E-01,'brucite':0.6498E-11}
species_in['cem1_ASE'] = species_in_trame
species_in['cem1_ASE']['k+'] = {'guess':0.3651959743513525,'ctotal':0.3651959743513525}
species_in['cem1_ASE']['na+'] = {'guess':0.0967741935483871,'ctotal':0.0967741935483871}

