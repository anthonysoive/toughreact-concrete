"""
Created on Fri Sep 18 09:47:55 2015

@author: anthony.soive
"""


# Composition du ciment
# compo={"C3S":57.63/100.,"C2S":17.84/100.,"C3A":2.22/100.,"C4AF":12.64/100.,"Carbonates":2.00/100.,"CaOl":0.71/100.,"CSbH2":6.15/100.}
# stage Maissa

#####################################################################################################################
#Base de données des composition des ciments et additions (pour le modèle d'hydratation de la DTechITM)
compo_ciment = {}
compo_ciment['CEM I 52.5 PM ES CP2'] = {"SiO2":21.39,"Al2O3":3.49,"TiO2":0.18,"Fe2O3":4.16,"CaO":65.12,"MgO":0.82,
                                      "Na2O":0.12,"K2O":0.3,"SO3":2.86,"Cl":0.0,"CO2":0.88}
compo_ciment['CEM I Le Teil'] = {"SiO2":21.55,"Al2O3":2.87,"Fe2O3":2.42,"CaO":66.31,"MgO":1.09,
                                      "Na2O":0.17,"K2O":0.27,"SO3":2.03,"Cl":0.0,"CO2":0.78}#BO -> Le Teil
compo_ciment['CEM I Vigor'] = {"SiO2":20.54,"Al2O3":3.59,"Fe2O3":4.13,"CaO":65.38,"MgO":1.09,
                                      "Na2O":0.18,"K2O":0.29,"SO3":2.67,"Cl":0.0,"CO2":0.3}#M25 -> Vigor

########################
#tests excel F. Lavergne
# compo_ciment['CEM I 52.5 PM ES CP2'] = {"SiO2":20.5,"Al2O3":4.7,"TiO2":0.18,"Fe2O3":2.8,"CaO":63.0,"MgO":1.9,
#                                       "Na2O":0.2,"K2O":1.0,"SO3":2.5,"Cl":0.0,"CO2":0.0}
# compo_ciment['CEM I 52.5 PM ES CP2'] = {"SiO2":23.0,"Al2O3":3.2,"TiO2":0.18,"Fe2O3":2.1,"CaO":67.0,"MgO":1.0,
#                                       "Na2O":0.1,"K2O":0.2,"SO3":2.1,"Cl":0.0,"CO2":0.0}
# compo_ciment['CEM I 52.5 PM ES CP2'] = {"SiO2":91.4,"Al2O3":0.6,"TiO2":0.18,"Fe2O3":0.9,"CaO":0.6,"MgO":1.1,
#                                       "Na2O":0.0,"K2O":0.0,"SO3":0.0,"Cl":0.0,"CO2":0.0}
# compo_ciment['CEM I 52.5 PM ES CP2'] = {"SiO2":20.0,"Al2O3":4.4,"TiO2":0.18,"Fe2O3":2.9,"CaO":64.2,"MgO":1.2,
#                                        "Na2O":0.0,"K2O":0.0,"SO3":2.05,"Cl":0.0,"CO2":1.2}
########################

ciment = {}
ciment['CEM I 52.5 PM ES CP2'] = {'composition':compo_ciment['CEM I 52.5 PM ES CP2'],'surface_specific':355.}
ciment['CEM I Vigor'] = {'composition':compo_ciment['CEM I Vigor'],'surface_specific':355.}
ciment['CEM I Le Teil'] = {'composition':compo_ciment['CEM I Le Teil'],'surface_specific':355.}


compo_fly_ash = {}
compo_fly_ash['BHP2000'] = {"SiO2":55.86,"Al2O3":25.40,"TiO2":0.84,"Fe2O3":6.05,"CaO":1.83,"MgO":0.63,
                                      "Na2O":0.24,"K2O":4.77,"SO3":0.11,"Cl":0.0,"CO2":0.0}
fly_ash = {}
fly_ash['BHP2000'] = {'composition':compo_fly_ash['BHP2000'],'surface_specific':1730.}


compo_silica_fume = {}
compo_silica_fume['BHP2000'] = {"SiO2":94.75,"Al2O3":0.07,"TiO2":0.0,"Fe2O3":0.08,"CaO":0.34,"MgO":0.28,
                                      "Na2O":0.24,"K2O":0.70,"SO3":0.05,"Cl":0.0,"CO2":0.0}
silica_fume = {}
silica_fume['BHP2000'] = {'composition':compo_silica_fume['BHP2000'],'surface_specific':1620.}


compo_laitier = {}
compo_laitier['Rion'] = {"SiO2":35.0,"Al2O3":11.0,"TiO2":1.0,"Fe2O3":0.18,"CaO":39.5,"MgO":8.5,
                                      "Na2O":0.0,"K2O":0.0,"SO3":1.25,"Cl":0.0,"CO2":0.0}
laitier = {}
laitier['Rion'] = {'composition':compo_laitier['Rion'],'surface_specific':1620.}
####################################################################################################################

nature_granulat = {}
nature_granulat['boulonnais'] = {'densite':2.678,'capa':0.84}

formulation_beton = {}
formulation_beton['M25'] = {"granulats":{"g12.5/20":{"kg":619.,'nature':nature_granulat['boulonnais']},
                                         "g5/12.5":{"kg":388.,'nature':nature_granulat['boulonnais']},
                                         "g0/5":{"kg":453.,'nature':nature_granulat['boulonnais']},
                                         "s0/4":{"kg":446.,'nature':nature_granulat['boulonnais']}},
                            "binder":{"c":{"kg":230.,"compo":ciment['CEM I 52.5 PM ES CP2']}},
                            "e":193., "phiair":0.0}
formulation_beton['M25-EA'] = {"granulats":{"g12.5/20":{"kg":574.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":454.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":433.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":427.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":230.,"compo":ciment['CEM I 52.5 PM ES CP2']}},
                               "e":160., "phiair":0.0031}
formulation_beton['M25FA'] = {"granulats":{"g12.5/20":{"kg":623.,'nature':nature_granulat['boulonnais']},
                                           "g5/12.5":{"kg":369.,'nature':nature_granulat['boulonnais']},
                                           "g0/5":{"kg":456.,'nature':nature_granulat['boulonnais']},
                                           "s0/4":{"kg":449.,'nature':nature_granulat['boulonnais']}},
                              "binder":{"c":{"kg":195.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                           "fly_ash":{"kg":48.,"compo":fly_ash['BHP2000']}},
                              "e":187.,"phiair":0.0}
formulation_beton['M25FA-EA'] = {"granulats":{"g12.5/20":{"kg":586.,'nature':nature_granulat['boulonnais']},\
                                              "g5/12.5":{"kg":454.,'nature':nature_granulat['boulonnais']},\
                                              "g0/5":{"kg":411.,'nature':nature_granulat['boulonnais']},\
                                              "s0/4":{"kg":405.,'nature':nature_granulat['boulonnais']}},\
                                 "binder":{"c":{"kg":189.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                          "fly_ash":{"kg":49.,"compo":fly_ash['BHP2000']}},
                                 "e":159.,"phiair":0.0054}
formulation_beton['M30FA'] = {"granulats":{"g12.5/20":{"kg":565.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":421.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":443.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":436.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":223.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                          "fly_ash":{"kg":95.,"compo":fly_ash['BHP2000']}},
                               "e":166., "phiair":0.0}
formulation_beton['M50'] = {"granulats":{"g12.5/20":{"kg":509.,'nature':nature_granulat['boulonnais']},
                                         "g5/12.5":{"kg":428.,'nature':nature_granulat['boulonnais']},
                                         "g0/5":{"kg":406.,'nature':nature_granulat['boulonnais']},
                                         "s0/4":{"kg":400.,'nature':nature_granulat['boulonnais']}},
                            "binder":{"c":{"kg":410.,"compo":ciment['CEM I 52.5 PM ES CP2']}},
                            "e":197., "phiair":0.0}
formulation_beton['M50-EA'] = {"granulats":{"g12.5/20":{"kg":477.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":390.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":368.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":364.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":483.,"compo":ciment['CEM I 52.5 PM ES CP2']}},
                               "e":188., "phiair":0.0132}
formulation_beton['M50FA'] = {"granulats":{"g12.5/20":{"kg":503.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":453.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":408.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":401.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":325.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                          "fly_ash":{"kg":79.,"compo":fly_ash['BHP2000']}},
                               "e":181., "phiair":0.0}
formulation_beton['M50FA-EA'] = {"granulats":{"g12.5/20":{"kg":452.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":422.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":322.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":317.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":428.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                          "fly_ash":{"kg":107.,"compo":fly_ash['BHP2000']}},
                               "e":192., "phiair":0.0144}
formulation_beton['M75'] = {"granulats":{"g12.5/20":{"kg":550.,'nature':nature_granulat['boulonnais']},
                                         "g5/12.5":{"kg":475.,'nature':nature_granulat['boulonnais']},
                                         "g0/5":{"kg":407.,'nature':nature_granulat['boulonnais']},
                                         "s0/4":{"kg":401.,'nature':nature_granulat['boulonnais']}},
                            "binder":{"c":{"kg":461.,"compo":ciment['CEM I 52.5 PM ES CP2']}},
                            "e":146., "phiair":0.0}
formulation_beton['M75-EA'] = {"granulats":{"g12.5/20":{"kg":489.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":443.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":338.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":332.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":557.,"compo":ciment['CEM I 52.5 PM ES CP2']}},
                               "e":151., "phiair":0.0098}
formulation_beton['M75SF'] = {"granulats":{"g12.5/20":{"kg":579.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":465.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":442.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":435.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":360.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                          "silica_fume":{"kg":22.,"compo":silica_fume['BHP2000']}},
                               "e":136., "phiair":0.0}
formulation_beton['M75SF-EA'] = {"granulats":{"g12.5/20":{"kg":550.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":437.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":414.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":408.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":387.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                          "silica_fume":{"kg":23.,"compo":silica_fume['BHP2000']}},
                               "e":132., "phiair":0.0058}
formulation_beton['M100SF'] = {"granulats":{"g12.5/20":{"kg":561.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":488.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":439.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":432.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":377.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                          "silica_fume":{"kg":38.,"compo":silica_fume['BHP2000']}},
                               "e":124., "phiair":0.0}
formulation_beton['M120SF'] = {"granulats":{"g12.5/20":{"kg":554.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":437.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":413.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":407.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":470.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                          "silica_fume":{"kg":57.,"compo":silica_fume['BHP2000']}},
                               "e":124., "phiair":0.0}
formulation_beton['BO'] = {"granulats":{"g12.5/20":{"kg":1192.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":744.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":353.,"compo":ciment['CEM I Le Teil']}},
                               "e":172., "phiair":0.0031}
formulation_beton['BO-III'] = {"granulats":{"g12.5/20":{"kg":1036.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":715.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":342.,"compo":ciment['CEM I Le Teil']}},
                               "e":186., "phiair":0.0031}
formulation_beton['BO-III-APOS'] = {"granulats":{"g12.5/20":{"kg":760.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":320.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":430.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":430.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":342.,"compo":ciment['CEM I Le Teil']}},
                               "e":177., "phiair":0.0031}
formulation_beton['BOAPOS'] = {"granulats":{"g12.5/20":{"kg":760.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":320.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":560.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":300.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":305.,"compo":ciment['CEM I Le Teil']}},
                               "e":190., "phiair":0.0031}
formulation_beton['B_Cicat'] = {"granulats":{"g12.5/20":{"kg":760.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":320.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":560.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":300.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":305.,"compo":ciment['CEM I Le Teil']}},
                               "e":190., "phiair":0.0031}
formulation_beton['CEMI_SF_Rilem'] = {"granulats":{"g12.5/20":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":399.,"compo":ciment['CEM I Le Teil']}},
                               "e":168., "phiair":0.0059}
formulation_beton['CEMI_SF_Rilem_peau'] = {"granulats":{"g12.5/20":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":399.,"compo":ciment['CEM I Le Teil']}},
                               "e":168., "phiair":0.0059}
formulation_beton['Rion'] = {"granulats":{"g12.5/20":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":399.,"compo":ciment['CEM I Le Teil']}},
                               "e":168., "phiair":0.0059}
formulation_beton['Missiessy'] = {"granulats":{"g12.5/20":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                               "binder":{"c":{"kg":435.,"compo":ciment['CEM I Le Teil']}},
                               "e":323., "phiair":0.0059}
formulation_beton['Bonaduz_CEMI'] = {"granulats":{"g12.5/20":{"kg":1850.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                            "binder":{"c":{"kg":325.,"compo":ciment['CEM I 52.5 PM ES CP2']}},
                            "e":150., "phiair":0.0}
formulation_beton['Bonaduz_CEMI_SF'] = {"granulats":{"g12.5/20":{"kg":1850.,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                            "binder":{"c":{"kg":325.,"compo":ciment['CEM I 52.5 PM ES CP2']},
                                      "fly_ash":{"kg":20.,"compo":fly_ash['BHP2000']}},
                            "e":150., "phiair":0.0}
formulation_beton['Naxberg'] = {"granulats":{"g12.5/20":{"kg":1875.5,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                            "binder":{"c":{"kg":367.,"compo":ciment['CEM I 52.5 PM ES CP2']}},
                            "e":128.5, "phiair":0.0}
formulation_beton['cem1_ASE'] = {"granulats":{"g12.5/20":{"kg":1875.5,'nature':nature_granulat['boulonnais']},
                                            "g5/12.5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "g0/5":{"kg":0.,'nature':nature_granulat['boulonnais']},
                                            "s0/4":{"kg":0.,'nature':nature_granulat['boulonnais']}},
                            "binder":{"c":{"kg":420.,"compo":ciment['CEM I 52.5 PM ES CP2']}},
                            "e":210, "phiair":0.0}
#####################################################################################################################
# Étude Ravi — béton M70-30FA (granulat ISO, CEM I + FA + SF spécifiques)
nature_granulat['ISO'] = {'densite': 2.64, 'capa': 0.84}

compo_ciment['CEM I'] = {
    "SiO2": 20.00, "Al2O3": 4.60, "TiO2": 0.0, "Fe2O3": 3.20,
    "CaO": 64.00, "MgO": 1.30, "Na2O": 0.07, "K2O": 1.30,
    "SO3": 3.40, "Mn2O3": 0.0, "P2O5": 0.48, "Cl": 0.006, "CO2": 0, "Cr2O3": 0.00,
}
ciment['CEM I'] = {'composition': compo_ciment['CEM I'], 'surface_specific': 490.}

compo_fly_ash['FA_Ravi'] = {
    "SiO2": 52.00, "Al2O3": 27.50, "TiO2": 0.00, "Fe2O3": 4.80,
    "CaO": 6.42, "MgO": 1.85, "Na2O": 1.01, "K2O": 0.69,
    "SO3": 1.10, "Cl": 0.01, "CO2": 0.0,
}
fly_ash['FA_Ravi'] = {'composition': compo_fly_ash['FA_Ravi'], 'surface_specific': 340.}

compo_silica_fume['SF_Ravi'] = {
    "SiO2": 96.00, "Al2O3": 0.00, "TiO2": 0.0, "Fe2O3": 0.00,
    "CaO": 0.10, "MgO": 0.00, "Na2O": 0.60, "K2O": 0.00,
    "SO3": 0.50, "Cl": 0.02, "CO2": 0.0,
}
silica_fume['SF_Ravi'] = {'composition': compo_silica_fume['SF_Ravi'], 'surface_specific': 23200.}

formulation_beton['M70-30FA'] = {
    "granulats": {
        "g12.5/20": {"kg": 0., 'nature': nature_granulat['ISO']},
        "g5/12.5": {"kg": 0., 'nature': nature_granulat['ISO']},
        "g0/5":    {"kg": 0., 'nature': nature_granulat['ISO']},
        "s0/4":    {"kg": 0., 'nature': nature_granulat['ISO']},
    },
    "binder": {
        "c":          {"kg": 864.00, "compo": ciment['CEM I']},
        "fly_ash":    {"kg": 283.50, "compo": fly_ash['FA_Ravi']},
        "silica_fume":{"kg": 202.50, "compo": silica_fume['SF_Ravi']},
    },
    "e": 607.50, "phiair": 0.0,
}

indicateurs_deduits = {}
indicateurs_deduits['M70-30FA'] = {'K_eau': 8.0e-21, 'cl_adsorption_csh': 0.0001}
#####################################################################################################################

mesures_expe = {}
#BHP2000
mesures_expe['M25FA-EA'] = {'P_eau':0.164}
mesures_expe['M25FA'] = {'P_eau':0.145}
mesures_expe['M25'] = {'P_eau':0.162}
mesures_expe['M25-EA'] = {'P_eau':0.137}
mesures_expe['M30FA'] = {'P_eau':0.126}
mesures_expe['M50FA-EA'] = {'P_eau':0.143}
mesures_expe['M50-EA'] = {'P_eau':0.133}
mesures_expe['M50FA'] = {'P_eau':0.141}
mesures_expe['M50'] = {'P_eau':0.144}
mesures_expe['M75SF-EA'] = {'P_eau':0.103}
mesures_expe['M75-EA'] = {'P_eau':0.107}
mesures_expe['M75'] = {'P_eau':0.115}
mesures_expe['M75SF'] = {'P_eau':0.1}
mesures_expe['M100SF'] = {'P_eau':0.084}
mesures_expe['M120SF'] = {'P_eau':0.074}
#Complement BHP2000
mesures_expe['BO'] = {'R_28':58.6,'P_eau':0.124}
mesures_expe['BO-III'] = {'R_28':38.5,'P_eau':0.149}
mesures_expe['BO-III-APOS'] = {'R_28':0.0,'P_eau':0.149,'K_gaz':158.0e-18}
mesures_expe['BOAPOS'] = {'R_28':0.0,'P_eau':0.159,'K_gaz':84.0e-18}
mesures_expe['B_Cicat'] = {'R_28':0.0,'P_eau':0.13,'K_gaz':84.0e-18}
mesures_expe['CEMI_SF_Rilem'] = {'R_28':0.0,'P_eau':0.12}
mesures_expe['CEMI_SF_Rilem_peau'] = {'R_28':0.0,'P_eau':0.4}
mesures_expe['Rion'] = {'R_28':0.0,'P_eau':0.105}#'P_eau':0.105
mesures_expe['Missiessy'] = {'R_28':0.0,'P_eau':0.145}
mesures_expe['Bonaduz_CEMI'] = {'R_28':40.0,'P_eau':0.10}
mesures_expe['Bonaduz_CEMI_SF'] = {'R_28':40.0,'P_eau':0.105}
mesures_expe['Naxberg'] = {'R_28':68.0,'P_eau':0.08}
mesures_expe['cem1_ASE'] = {'R_28':68.0,'P_eau':0.3}

indicateurs_deduits = {}
indicateurs_deduits['M25FA-EA'] = {'K_eau':8.0e-21,'D_eff':2.8e-12,'cl_adsorption_csh':0.0001}
indicateurs_deduits['M25FA'] = {'K_eau':8.0e-21,'D_eff':3e-12,'cl_adsorption_csh':0.0036,'so4_adsorption_csh':0.048}#'D_eff':1.8e-12
indicateurs_deduits['M25'] = {'K_eau':4.0e-20,'D_eff':7.8e-12,'cl_adsorption_csh':0.0001}
indicateurs_deduits['M25-EA'] = {'K_eau':8.0e-21,'D_eff':2.8e-12}
indicateurs_deduits['M30FA'] = {'K_eau':8.0e-21,'D_eff':0.5e-12,'cl_adsorption_csh':0.0001}#A determiner!
indicateurs_deduits['M50FA-EA'] = {'K_eau':8.0e-21,'D_eff':1.8e-12,'cl_adsorption_csh':0.0001}#A determiner!
indicateurs_deduits['M50-EA'] = {'K_eau':8.0e-21,'D_eff':1.8e-12,'cl_adsorption_csh':0.0001}#A determiner!
indicateurs_deduits['M50FA'] = {'K_eau':8.0e-21,'D_eff':0.35e-12,'cl_adsorption_csh':0.0001}#A determiner!
indicateurs_deduits['M50'] = {'K_eau':8.0e-21,'D_eff':0.8e-12,'cl_adsorption_csh':0.16}
indicateurs_deduits['M75SF-EA'] = {'K_eau':8.0e-21,'D_eff':1.8e-12,'cl_adsorption_csh':0.0001}#A determiner!
indicateurs_deduits['M75-EA'] = {'K_eau':8.0e-21,'D_eff':1.8e-12,'cl_adsorption_csh':0.0001}#A determiner!
indicateurs_deduits['M75'] = {'K_eau':8.0e-21,'D_eff':1.0e-12,'cl_adsorption_csh':0.0001}#A determiner!
indicateurs_deduits['M75SF'] = {'K_eau':8.0e-21,'D_eff':0.35e-12,'cl_adsorption_csh':0.0025,'so4_adsorption_csh':0.0307}
indicateurs_deduits['M100SF'] = {'K_eau':8.0e-21,'D_eff':0.2e-12,'cl_adsorption_csh':0.0063,'so4_adsorption_csh':0.0361}
indicateurs_deduits['M120SF'] = {'K_eau':8.0e-21,'D_eff':1.8e-12,'cl_adsorption_csh':0.0001}#A determiner!
#indicateurs_deduits['BO'] = {'K_eau':8.0e-21,'D_eff':4.0e-12,'cl_adsorption_csh':0.16}#1.2e-12
indicateurs_deduits['BO'] = {'K_eau':1.0e-19,'D_eff':4.0e-12,'cl_adsorption_csh':0.16}#BO V. Picandet
indicateurs_deduits['BO-III'] = {'K_eau':8.0e-21,'D_eff':2.8e-12,'cl_adsorption_csh':0.16}
indicateurs_deduits['BO-III-APOS'] = {'K_eau':1.0e-21,'D_eff':0.3e-12,'cl_adsorption_csh':0.16}
indicateurs_deduits['BOAPOS'] = {'K_eau':2.0e-20,'D_eff':2.8e-12,'cl_adsorption_csh':0.16}
indicateurs_deduits['B_Cicat'] = {'K_eau':2.0e-20,'D_eff':3.497e-12,'cl_adsorption_csh':0.16}
#indicateurs_deduits['CEMI_SF_Rilem'] = {'K_eau':1.0e-19,'D_eff':1.15e-12,'cl_adsorption_csh':0.16}#First benchmark: 'D_eff':0.8e-12#'D_eff':3.2e-12*mesures_expe['CEMI_SF_Rilem']['P_eau']
#Fit 20 years
indicateurs_deduits['CEMI_SF_Rilem'] = {'K_eau':1.0e-19,'D_eff':1.15e-12,'cl_adsorption_csh':0.16}#First benchmark: 'D_eff':0.8e-12#'D_eff':3.2e-12*mesures_expe['CEMI_SF_Rilem']['P_eau']
indicateurs_deduits['CEMI_SF_Rilem_peau'] = {'K_eau':1.0e-19,'D_eff':0.8e-12,'cl_adsorption_csh':0.16}
indicateurs_deduits['Rion'] = {'K_eau':1.0e-19,'D_eff':0.4e-12,'cl_adsorption_csh':0.16}#'D_eff':3.2e-12#First benchmark: 'D_eff':0.8e-12#'D_eff':3.2e-12*mesures_expe['CEMI_SF_Rilem']['P_eau']
indicateurs_deduits['Missiessy'] = {'K_eau':1.0e-19,'D_eff':1.15e-12,'cl_adsorption_csh':0.16}#First benchmark: 'D_eff':0.8e-12#'D_eff':3.2e-12*mesures_expe['CEMI_SF_Rilem']['P_eau']
indicateurs_deduits['Bonaduz_CEMI'] = {'K_eau':1.0e-19,'D_eff':11.e-13,'cl_adsorption_csh':0.168}#Resultat d'inversion D = 4.9e-13 #test2 'D_eff':8.e-13 
indicateurs_deduits['Bonaduz_CEMI_SF'] = {'K_eau':1.0e-19,'D_eff':1.6e-12,'cl_adsorption_csh':0.15}
indicateurs_deduits['Naxberg'] = {'K_eau':1.0e-19,'D_eff':1.e-12,'cl_adsorption_csh':0.168}
indicateurs_deduits['cem1_ASE'] = {'K_eau':1.0e-19,'D_eff':3.4e-12,'cl_adsorption_csh':0.168}
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# #Analyse inverse
# indicateurs_deduits['M25FA'] = {'K_eau':8.0e-21,'D_eff':3.0e-12,'cl_adsorption_csh':0.0036,'so4_adsorption_csh':0.048}#'D_eff':1.8e-12
# indicateurs_deduits['M25'] = {'K_eau':4.0e-20,'D_eff':7.8e-12,'cl_adsorption_csh':0.0001}
# indicateurs_deduits['M25-EA'] = {'K_eau':8.0e-21,'D_eff':2.8e-12}
# indicateurs_deduits['M30FA'] = {'K_eau':8.0e-21,'D_eff':1.0e-12,'cl_adsorption_csh':0.0001}#A determiner!
# indicateurs_deduits['M50FA-EA'] = {'K_eau':8.0e-21,'D_eff':1.8e-12,'cl_adsorption_csh':0.0001}#A determiner!
# indicateurs_deduits['M50-EA'] = {'K_eau':8.0e-21,'D_eff':1.8e-12,'cl_adsorption_csh':0.0001}#A determiner!
# indicateurs_deduits['M50FA'] = {'K_eau':8.0e-21,'D_eff':6.29e-13,'cl_adsorption_csh':0.0001}#A determiner!
# indicateurs_deduits['M50'] = {'K_eau':8.0e-21,'D_eff':3.0e-12,'cl_adsorption_csh':0.16}
# indicateurs_deduits['M75SF-EA'] = {'K_eau':8.0e-21,'D_eff':1.8e-12,'cl_adsorption_csh':0.0001}#A determiner!
# indicateurs_deduits['M75-EA'] = {'K_eau':8.0e-21,'D_eff':1.8e-12,'cl_adsorption_csh':0.0001}#A determiner!
# indicateurs_deduits['M75'] = {'K_eau':8.0e-21,'D_eff':0.948e-12,'cl_adsorption_csh':0.0001}#A determiner!
# indicateurs_deduits['M75SF'] = {'K_eau':8.0e-21,'D_eff':0.452e-12,'cl_adsorption_csh':0.0025,'so4_adsorption_csh':0.0307}
# indicateurs_deduits['M100SF'] = {'K_eau':8.0e-21,'D_eff':0.288e-12,'cl_adsorption_csh':0.0063,'so4_adsorption_csh':0.0361}
# indicateurs_deduits['M120SF'] = {'K_eau':8.0e-21,'D_eff':0.136e-12,'cl_adsorption_csh':0.0001}#A determiner!
# #Fin analyse inverse
#-------------------------------------------------

#Parametres de calcul
krl_model = {'type':'genuchten','params':[4.396e-01,0.0,1.0,0.01]}
pc_model = {'type':'genuchten','params':[4.396e-01,0.0,5.369e-08,9.381e7,1.0]}

modele_adsorb_desorb = {'krl':krl_model, 'pc':pc_model}

klinkenberg_default = 1.e5
#cl_adsorption_csh_default = 3.0#0.4#1.386e-2

params_model_default = {'adsorb_desorb':modele_adsorb_desorb, 'klinkenberg':klinkenberg_default}#, 'cl_adsorption_csh':cl_adsorption_csh_default}

# #####################
# 
# compo_ciment['BO_Dundee']={"C3S":67.8/100.,"C2S":16.6/100.,"C3A":4./100.,"C4AF":7.2/100.,"Na2O":0.17/100.,"K2O":0.27/100.,"CSbH2":4.5/100.,"Cl":0.}
# compo_ciment['BO']={"CaO":66.31/100.,"SiO2":21.55/100.,"Al2O3":2.87/100.,"Fe2O3":2.42/100.,"Na2O":0.17/100.,"K2O":0.27/100.,"SO3":2.03/100.,"CSbH2":4.5/100.,"Cl":0.}
# compo_ciment['BO_APOS']={"C3S":64.1/100.,"C2S":11.8/100.,"C3A":8.4/100.,"C4AF":9.3/100.,"CSbH2":2.0/100.}
# compo_ciment['M25']={"C3S":72.42/100.,"C2S":4.255/100.,"C3A":2.53/100.,"C4AF":12.57/100.,"CSbH2":3.0/100.}
# 
# # Formulations de beton
# formulation = {}
# formulation['M40']={"g12.5/20":615.,"g5/12.5":386.,"g0/5":452.,"s0/4":445.,"c":300.,"e":187.,\
#      "e/ctot":0.62,"e/c":0.59,"g/c":6.33,"phiair":0.013}
# formulation['BO_Dundee']={"g12.5/20":733.,"g5/12.5":459.,"g0/5":0.,"s0/4":744.,"c":353.,"e":172.,\
#      "e/ctot":0.5,"e/c":0.49,"g/c":5.48,"phiair":0.012}
# formulation['BO_APOS']={"g12.5/20":760.,"g5/12.5":320.,"g0/5":0.,"s0/4":860.,"c":305.,"e":190.,\
#      "e/ctot":0.62,"e/c":0.61,"g/c":6.36,"phiair":0.012}
# 
# # Mesures effectués sur les bétons
# mesures = {}
# mesures['BO_Dundee'] = {'permeabilite':8.00e-21,'porosite':0.122,'D_eff':2.8e-12}#6.0e-12}#
# mesures['BO_APOS'] = {'permeabilite':4.00e-20,'porosite':0.16,'D_eff':13.1e-12}
# 
# # Modeles pour les matériaux
# modele_mat = {}
# modele_mat['M40']={'krl':krl_model, 'pc':pc_model, 'cl_adsorption_csh':1.386e-2}
# modele_mat['BO_Dundee']={'krl':krl_model, 'pc':pc_model, 'cl_adsorption_csh':1.386e-2}#0.1}#0.1}#0.1}#1.386e-2}#0.02}#
# modele_mat['BO_APOS']={'krl':krl_model, 'pc':pc_model, 'cl_adsorption_csh':1.386e-2}#0.1}#0.1}#0.1}#1.386e-2}#0.02}#
# 
# klinkenberg = {}
# klinkenberg['BO_Dundee']=1.e5
# klinkenberg['BO']=1.e5
# klinkenberg['BO_APOS']=1.e5
# klinkenberg['M50']=1.e5

# def liste_materiaux():
#     champs_mat = [cle for cle in prop_mat.values()[0]]
#     
#     liste_mat = []
#     for item,value in prop_mat.items():
#         tmp_liste = [item]
#         for elem in champs_mat:
#             tmp_liste.append(prop_mat[item][elem])
#         liste_mat.append(tmp_liste)
#     #print [[item for item,value in prop_mat.items()]+prop_mat.values()]
#     
#     df_mat = pandas.DataFrame(liste_mat,columns=['materiau']+champs_mat)
#     return df_mat
