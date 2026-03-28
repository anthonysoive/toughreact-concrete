#!/usr/bin/env python3
"""
Created on Tue Mar 26 11:04:11 2019

@author: anthonysoive
"""
from math import log10

from numpy import logspace

from toughreact_concrete.materiau.hydration.hydrationDIM_CTOA4 import (
    Binder,
    Hydrationmodel,
    printXls,
)


def calcul_hydratation(formulation,temps_cure):                               
    binder = Binder()
    q_binder = 0
    for elem in formulation['binder']:
        q_binder += formulation['binder'][elem]['kg']
    ciment = formulation['binder']['c']
    q_ciment = ciment['kg']
    compo_ciment = ciment['compo']['composition_Bogues']
    s_specific_ciment = ciment['compo']['surface_specific']
    binder.addbinderBogue(100*q_ciment/q_binder,compo_ciment,s_specific_ciment)
    #binder.addbinderBogue(100*q_ciment,compo_ciment,s_specific_ciment)
    if 'fly_ash' in formulation['binder']:
        fly_ash = formulation['binder']['fly_ash']
        q_fly_ash = fly_ash['kg']
        compo_fly_ash = fly_ash['compo']['composition_Bogues']
        s_specific_fly_ash = fly_ash['compo']['surface_specific']
        compo_fly_ash['SS'] = compo_fly_ash['SS']*0.6
        compo_fly_ash['A'] = compo_fly_ash['A']*0.6
        binder.addbinderBogue(100*q_fly_ash/q_binder,compo_fly_ash,s_specific_fly_ash)
        #binder.addbinderBogue(100*q_fly_ash,compo_fly_ash,s_specific_fly_ash)
    if 'silica_fume' in formulation['binder']:
        silica_fume = formulation['binder']['silica_fume']
        q_silica_fume = silica_fume['kg']
        compo_silica_fume = silica_fume['compo']['composition_Bogues']
        s_specific_silica_fume = silica_fume['compo']['surface_specific']
        compo_silica_fume['SS'] = compo_silica_fume['SS']*0.9
        binder.addbinderBogue(100*q_silica_fume/q_binder,compo_silica_fume,s_specific_silica_fume)
        #binder.addbinderBogue(100*q_silica_fume,compo_silica_fume,s_specific_silica_fume)
    
    q_eau = formulation['e']
    cm=Hydrationmodel(binder,q_eau/q_binder)
    
    #cm.saturated=1
    cm.massc=(q_binder)/100
    cm.updatefiller()
    cm.setEntrainedAir(0.0)
    q_sable = formulation['granulats']['g0/5']['kg']+formulation['granulats']['s0/4']['kg']
    nature_sable = formulation['granulats']['g0/5']['nature']
    cm.addaggregate("sable",q_sable,nature_sable['densite'],nature_sable['capa'],75.,0.20)
    
    q_gravier = formulation['granulats']['g12.5/20']['kg']
    nature_gravier = formulation['granulats']['g12.5/20']['nature']
    cm.addaggregate("calcaires_gravier",q_gravier,nature_gravier['densite'],nature_gravier['capa'])
    
    q_gravillons = formulation['granulats']['g5/12.5']['kg']
    nature_gravillons = formulation['granulats']['g5/12.5']['nature']
    cm.addaggregate("calcaires_gravier",q_gravillons,nature_gravillons['densite'],nature_gravillons['capa'])
    cm.calo.setisotherm(20)
    #mcsb=223./(223.+95.)
    #mcvsb=95./(223.+95.)
    
    tfin=temps_cure
    n=1000
    T=[0.]+logspace(log10(0.01),log10(tfin),n).tolist()
    
    #launch of the hydration model
    #print("running hydration toughreact_concrete.model...")
    res=cm.run(T)
    statelast=res[len(res)-1]
    
    #print(cm.fraclargescale())
    fracls,vpate=cm.fraclargescale()
    cm.printXls("hydrationDIM_CTOA_in.xls")
    printXls(res, "hydrationDIM_CTOA.xls")
    
#     print('advance of cement hydration', statelast["alpha"],statelast["alpham"])
#     print('advance of flyash', statelast["alphamp"])
#     print('porosity of active paste emptied at 40%RH', statelast['phic']*(1.0/(fracls['paste']/(fracls['paste']+fracls['filler']))))
#     print('volume of water remaining', statelast['phicw']*(1.0/(fracls['paste']/(fracls['paste']+fracls['filler']))))
#     if statelast["compo"]['CSbH2']>0:
#         print("remaining gypsum, mol/cm3 of paste",statelast["compo"]['CSbH2'])
#     if statelast["compo"]['C6ASb3H32']>0:
#         print("formed Ettringite, mol/cm3 of paste",statelast["compo"]['C6ASb3H32'])
#     if statelast["compo"]['C4ASbH12']>0 or statelast["compo"]['C4ACb11H']>0:
#         print("formed AFm, mol/cm3 of paste, C4ASbH12:",statelast["compo"]['C4ASbH12'], "   C4ACb11H :",statelast["compo"]['C4ACb11H'])
#     if statelast["compo"]['C3AH6']>0:
#         print("formed hydrogarnet, mol/cm3 of paste, C3AH6:",statelast["compo"]['C3AH6'])
    
    #print(statelast["compo"])
    #if statelast["compo"]['CH']>0:
    #    print("formed portlandite, mol/cm3 of paste, CH:",statelast["compo"]['CH'])
    
    #conversion from cm3/cm3 of paste to cm3/cm3 of material
    frac_vol_granulats = 0
    for elem in formulation["granulats"]:
        nature = formulation["granulats"][elem]['nature']
        frac_vol_granulats += formulation["granulats"][elem]['kg'] / nature['densite'] / 1000.
    print("Fraction volumique de granulats : ",frac_vol_granulats)
    frac_vol_pate = 1 - frac_vol_granulats
    print("Fraction volumique de pâte : ",frac_vol_pate)
    for elem in statelast["fracvol"]:
        statelast["fracvol"][elem] = statelast["fracvol"][elem]*frac_vol_pate
    #conversion from mol/cm3 of paste to mol/cm3 of material
    for elem in statelast["compo"]:
        statelast["compo"][elem] = statelast["compo"][elem]*frac_vol_pate
    
    # MODIF AS => remplacement de C6AFS2H19 en C3AFSH4
    # #transform C6AFS2H19 en C3FS1.34H + C3AS0.84H
    # statelast["compo"]["C3FS1.34H"] = statelast["compo"]["C6AFS2H19"]
    # statelast["compo"]["C3AS0.84H"] = statelast["compo"]["C6AFS2H19"]
    # statelast["fracvol"]["C3FS1.34H"] = statelast["compo"]["C3FS1.34H"]*145.*frac_vol_pate
    # statelast["fracvol"]["C3AS0.84H"] = statelast["compo"]["C3AS0.84H"]*frac_vol_pate*151.
    
    # Transform C3AFSH4 ...
    statelast["compo"]["C3AFS0.84H4.32"] = statelast["compo"]["C3AFSH4"]
    statelast["fracvol"]["C3AFS0.84H4.32"] = statelast["compo"]["C3AFSH4"]*145.51*frac_vol_pate
    # FIN MODIF AS
    
    #statelast["fracvol"]["CSH"] = statelast["compo"]["CSH"]*CSH['v']*volume_pate
    #statelast["fracvol"]["CSHp"] = statelast["compo"]["CSHp"]*CSHp['v']*volume_pate
    #print("Fractions volumiques (cm3/cm3 de materiau) : ",statelast["fracvol"])
    #print("molar quantity (mol/cm3 of material): ",statelast["compo"])
    #print(statelast["compo"].values())
    #print(statelast["compo"])
    
    return statelast
