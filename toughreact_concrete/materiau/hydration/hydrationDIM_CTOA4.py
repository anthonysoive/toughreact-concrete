#!/usr/bin/python

'''

Created on 8 oct. 2015

@author: Francis Lavergne and Jean-François Barthélémy

'''

__author__ = "Francis Lavergne and Jean-François Barthélémy"
__copyright__ = "Copyright 2015, CEREMA"
__credits__ = ["Francis Lavergne", "Jean-François Barthélémy"]
__license__ = "..."
__version__ = "1.0.1"
__maintainer__ = "Francis Lavergne"
__email__ = "francis.lavergne@cerema.fr"
__status__ = "alpha"

if __name__ == '__main__':
    from pyisocalc import molmass
else:
    from .pyisocalc import molmass
from math import exp, log, log10, pow

#from numpy import *
#from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import numpy as np
import scipy.special
from numpy import logspace

#from hydration_data import dvs
#import pickle
#import xlrd
from xlwt import Workbook

C="CaO" ; S="SiO2" ; law="Al2O3" ; F="Fe2O3" ; H="H2O" ; Sb="SO3" ; Cb="CO2"

Hemi="CSbH1s2" ; Gypsum="CSbH2" ; AFt="C6ASb3H32" ; AFm="C4ASbH12"


def molecule(name,formula,rho,enthalpy,heatcapa):
    '''
    Creates a molecule, that is a dictionnary including name, formula, rho (density), M (molar mass, g/mol), hf (enthalpy of formation, kJ/mol @25C) and cp (heat capacity J/mol/K @25C) 
    '''
    M=sum([formula[elem]*molmass(elem) for elem in formula]) ; v=M/rho
    #print {"name":name,"formula":formula,"rho(g/cm3)":rho,"M(g/mol)":M,"v(cm3/mol)":v}
    return {"name":name,"formula":formula,"rho":rho,"M":M,"v":v,"hf":enthalpy,"cp":heatcapa}

C3S=molecule("C3S",                       {C:3,S:1},    3.150,-2929.2,171.88)
C2S=molecule("C2S",                       {C:2,S:1},    3.270,-2307.5,128.78)
C3A=molecule("C3A",                       {C:3,law:1},    3.030,-3587.8,209.87)
C4AF=molecule("C4AF",                 {C:4,law:1,F:1},    3.710,-5090.3,396)

SS=molecule("SS",                 {S:1},    2.22,-903.49,44.4)

CCb=molecule("CCb",                 {C:1,Cb:1},    2.71,-1128.79,81.88) #NBS chemical thermodynamic tables

d_anhyd={}
for molec in [C3S,C2S,C3A,C4AF,CCb,SS]: d_anhyd[molec["name"]]=molec
 
CSbH1s2=molecule("CSbH1s2",        {C:1,Sb:1,H:0.5},    2.740,-1576.74,119.41)
CSbH2=molecule("CSbH2",              {C:1,Sb:1,H:2},    2.310,-2022.6,186.02)
CSb=molecule("CSb",              {C:1,Sb:1},    2.97,-1434.11,99.04)

d_gypsum={}
for molec in [CSbH1s2,CSbH2,CSb]: d_gypsum[molec["name"]]=molec
 
CH=molecule("CH",                         {C:1,H:1},    2.260,-986.1,87.49)
#CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    2.2)
#CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    2.040)
#CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    1.96)
#CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    2.1,-3283,297) #previous
CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    2.03,-3283,297)

#CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    2.0,-3283,297)
#CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    1.9,-3283,297)
CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    2.1,-3283,297)
#en accord avec le modèle de Browers
CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    2.08,-3283,297)
#CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    1.99,-3283,297) #pichler 2007
#le CSH pouzzolanique de Bentz1998
# la masse volumique est ajust�e aux donn�es de Bentz, bas�e sur le chemical shrinkage
CSHp=molecule("CSHp",                 {C:1.1,S:1,H:3.9},    1.9,-2841,297)
#2841kJ/mol pour correspondre � la chaleur d'hydratation de Bentz, de Larrard et Waller 1999 (870KJ/kg of SiO2)

C4ACb11H=molecule("C4ACb11H",                 {C:4,Cb:1,law:1,H:11},    2.17,-8250,881)# Cp et densite d'apres Lothenbach2008, Matschei2007.
# Hf Lotenbach,Matschei : -8250 ; Thermodynamic,Tables 10,68H, 8176 ; Berman1961, 10,68H : 1956*4,18=8184
#CSH=molecule("CSH",                 {C:1.7,S:1,H:4},    2.0,-3283)
#densite CSH 2.74 dans Thierry 2005...
#densite C1.7SHx C/S=1.7 =3.274-0.368 Zhang 2013 
# Le CSH ci-dessous est celui du papier de M Thiery JOA 2005
# CSH=molecule("CSH",                   {C:3,S:2,H:3},    2.630)
C6ASb3H32=molecule("C6ASb3H32", {C:6,law:1,Sb:3,H:32},    1.780,-17539,2174)
C4ASbH12=molecule("C4ASbH12",   {C:4,law:1,Sb:1,H:12},    2.020,-8778,942)
FH3=molecule("FH3",                       {F:1,H:3},    2.200,2*-823.0,2*101.671)
C3AH6=molecule("C3AH6",               {C:3,law:1,H:6},    2.520,-5548,459)

C6AFS2H19=molecule("C6AFS2H19",               {C:6,law:1,F:1,S:2.18,H:19},    2.18,-14088,1682)
C3AFSH4=molecule("C3AFSH4",               {C:3,law:1,F:1,S:0.84,H:4.32},    4.4,-14088,145.51) #!!!!!! C6AFS2H19 remplacé par C3AFSH4 dans le reste du fichier

A=molecule("A",               {law:1},    3.97,-1663.52,79.04)

d_hydrate={}
for molec in [CH,CSH,C6ASb3H32,C4ASbH12,FH3,C3AH6,C4ACb11H,CSHp,C3AFSH4]: d_hydrate[molec["name"]]=molec
 
H=molecule("H",                               {H:1},    1.000,-285.83,75.291)
d_water={}
for molec in [H]: d_water[molec["name"]]=molec

d_A={}
d_A[A["name"]]=A
d_molec={}
d_molec.update(d_anhyd);d_molec.update(d_gypsum);d_molec.update(d_hydrate);d_molec.update(d_water);d_molec.update(d_A)

rho={}
for molec in d_molec: rho[molec]=d_molec[molec]["rho"]
M={}
for molec in d_molec: M[molec]=d_molec[molec]["M"]
v={}
for molec in d_molec: v[molec]=d_molec[molec]["v"]
hf={}
for molec in d_molec: hf[molec]=d_molec[molec]["hf"]
cp={}
for molec in d_molec: cp[molec]=d_molec[molec]["cp"]

class Reaction:
    '''
    A chemical reaction
    '''
    def __init__(self,name,anhyd,eq,alpha=0,k=0):
        '''
        Constructor
        
        
        :param name: the name of the reaction
        :type name: string
        :param anhyd: the anhydrous reactant driving the kinetics
        :type anhyd: string
        :param eq: the equation of the reaction : reactant with negative stochiometric coefficients and products with positive ones
        :type eq: dictionary (key=moelcules, value=coefficient)
        :param alpha: kinetics (depreciated)
        :type alpha: float
        :param k: kinetics (depreciated)
        :type k: float
        '''
        self.name=name
        self.anhyd=anhyd
        self.eq=eq
        self.alpha=alpha
        self.k=k
        self.F=lambda t:1.-(1.-k*(1.-alpha)*t)**(1./(1.-alpha))
        self.dv=sum([eq[molec]*v[molec] for molec in eq])
        self.dvs=sum([eq[molec]*v[molec] for molec in eq if molec!="H"])
        self.heat=sum([eq[molec]*hf[molec] for molec in eq])
        self.cp=sum([eq[molec]*cp[molec] for molec in eq])
    def __repr__(self):
        '''
        prints the equation
        :returns: the equation as a string
        '''
        reac=[] ; prod=[]
        eq=self.eq
        for molec in eq:
            coef=eq[molec]
            side=reac if coef<0 else prod
            s='+' if len(side)>0 else ''
            ac=abs(coef)
            s+='' if ac==1 else str(ac)
            s+=molec
            side.append(s)
        return ''.join(reac)+' -> '+''.join(prod)
    
    def react(self,dalphatarget,compo,N0):
        '''
        modify the composition until either the targeted evolution of the degree of reaction is reached or one of the reactant is depleted.
        
        :param dalphatarget: targeted evolution of the degree of reaction
        :type dalphatarget: float
        :param compo: the composition of the mix, in mol, is modified
        :type compo: dictionnary (key= molec, value=mol)
        :param N0: the initial content of the reactant driving the kinetics, in mol
        :type N0: float
        
        :returns: the effective increase of the degree of reaction
        '''
        if dalphatarget<0:
            return 0
        dalphaeffect=dalphatarget
        #on regarde si on a assez de reactif
        for molec in self.eq:
            if dalphaeffect*N0*self.eq[molec]/self.eq[self.anhyd]>compo[molec] and N0>0 : #and molec !='H'
                dalphaeffect=compo[molec]*self.eq[self.anhyd]/self.eq[molec]/N0
            if dalphaeffect<0 : #permet de traiter les quantités de réactif négative. Ex: l'eau des CSH en dessous de 80%RH
                return 0
        #on execute la reaction
        for molec in self.eq:
            compo[molec]-=dalphaeffect*N0*self.eq[molec]/self.eq[self.anhyd]
        
        return dalphaeffect
 
d_reac_gypsum={"RCSbH1s2":Reaction("RCSbH1s2","",{"CSbH1s2":-1,"H":-1.5,"CSbH2":1})}


# La reaction ci-dessous est celle de la these de Zhang 2014 (fluage+microindent)
d_reac_C3S={"RC3S":Reaction("RC3S","C3S",{"C3S":-1,"H":-5.3,"CH":1.3,"CSH":1},2.65,1.17e-5)}
# La reaction ci-dessous est celle du papier de M Thiery JOA 2005
# Le -1 du H correspond a une estimation de l'eau piegee dans les pores de gel
#d_reac_C3S={"RC3S":reaction("RC3S","C3S",{"C3S":-1,"H":-3-1,"CH":1.5,"CSH":0.5},2.65,1.17e-5)}

# La reaction ci-dessous est celle de la these de Zhang 2014 (fluage+microindent)
d_reac_C2S={"RC2S":Reaction("RC2S","C2S",{"C2S":-1,"H":-4.3,"CH":0.3,"CSH":1},3.10,0.16e-5)}
# La reaction ci-dessous est celle du papier de M Thiery JOA 2005
# Le -1 du H correspond a une estimation de l'eau piegee dans les pores de gel
#d_reac_C2S={"RC2S":reaction("RC2S","C2S",{"C2S":-1,"H":-2-1,"CH":0.5,"CSH":0.5},3.10,0.16e-5)}


d_reac_C3A={"RaC3A":Reaction("RaC3A","C3A",{"C3A":-1,"CSbH2":-3,"H":-26,"C6ASb3H32":1},3.81,1.00e-5),\
        "RbC3A":Reaction("RbC3A","C3A",{"C3A":-1,"C6ASb3H32":-0.5,"H":-2,"C4ASbH12":1.5},3.81,1.00e-5),\
        "RcC3A":Reaction("RcC3A","C3A",{"C3A":-1,"H":-6,"C3AH6":1},3.81,1.00e-5),\
        "RdC3A":Reaction("RdC3A","C3A",{"C3A":-1,"CCb":-1,"H":-11,"C4ACb11H":1},3.81,1.00e-5)}



d_reac_C4AF={"RaC4AF":Reaction("RaC4AF","C4AF",{"C4AF":-1,"CSbH2":-3,"H":-30,"C6ASb3H32":1,"CH":1,"FH3":1},2.41,2.46e-5),\
        "RbC4AF":Reaction("RbC4AF","C4AF",{"C4AF":-1,"C6ASb3H32":-0.5,"H":-6,"C4ASbH12":1.5,"CH":1,"FH3":1},2.41,2.46e-5),\
        "RcC4AF":Reaction("RcC4AF","C4AF",{"C4AF":-1,"H":-10,"C3AH6":1,"CH":1,"FH3":1},2.41,2.46e-5),\
        "RdC4AF":Reaction("RdC4AF","C4AF",{"C4AF":-1,"H":-15,"CCb":-1,"C4ACb11H":1,"CH":1,"FH3":1},2.41,2.46e-5),\
        "ReC4AF":Reaction("ReC4AF","C4AF",{"C4AF":-1,"H":-7,"C2S":-0.84,"C3AFSH4":1,"CH":2.68},2.41,2.46e-5),\
        "RfC4AF":Reaction("RfC4AF","C4AF",{"C4AF":-1,"H":-7.84,"C3S":-0.84,"C3AFSH4":1,"CH":3.52},2.41,2.46e-5) #Corrections AS
        # "ReC4AF":Reaction("ReC4AF","C4AF",{"C4AF":-1,"H":-21.36,"C2S":-2.18,"C6AFS2H19":1,"CH":2.36},2.41,2.46e-5),\
        # "RfC4AF":Reaction("RfC4AF","C4AF",{"C4AF":-1,"H":-23.54,"C3S":-2.18,"C6AFS2H19":1,"CH":4.54},2.41,2.46e-5) #Francis
        }

d_reac_SS={"RSS":Reaction("RSS","SS",{"SS":-1,"H":-2.8,"CH":-1.1,"CSHp":1},3.10,0.16e-5)}

d_reac_ms2mc={"Rms2mc":Reaction("Rms2mc","CCb",{"C4ASbH12":-1.5,"H":-9,"CCb":-1,"C4ACb11H":1,"C6ASb3H32":0.5},3.10,0.16e-5)}

d_reac_A={"RaA":Reaction("RaA","A",{"A":-1,"CH":-5,"C6ASb3H32":1,"H":-25,"CSbH2":-1},3.10,0.16e-5),\
          "RbA":Reaction("RbA","A",{"A":-1,"CH":-3,"C6ASb3H32":-0.5,"C4ASbH12":1.5,"H":1},3.10,0.16e-5),\
          "RcA":Reaction("RcA","A",{"A":-1,"CH":-3,"C3AH6":1,"H":-3},3.10,0.16e-5),\
          "RdA":Reaction("RdA","A",{"A":-1,"CH":-3,"CCb":-1,"H":-8,"C4ACb11H":1},3.10,0.16e-5)
          }


d_reac_CnS={}
d_reac_CnS.update(d_reac_C3S);d_reac_CnS.update(d_reac_C2S)
d_reac={}
d_reac.update(d_reac_gypsum);d_reac.update(d_reac_C3S);d_reac.update(d_reac_C2S);d_reac.update(d_reac_C3A);d_reac.update(d_reac_C4AF);d_reac.update(d_reac_SS);d_reac.update(d_reac_ms2mc)
d_reac.update(d_reac_A)
dv={}
for eq in d_reac: dv[eq]=d_reac[eq].dv
dvs={}
for eq in d_reac: dvs[eq]=d_reac[eq].dvs
dheat={}
for eq in d_reac: dheat[eq]=d_reac[eq].heat
dcp={}
for eq in d_reac: dcp[eq]=d_reac[eq].cp

class Binder:
    '''
    A description of the binder
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.blaine=0
        self.weightfraction={'C2S':0,'C3S':0,'C3A':0,'C4AF':0,'CSbH2':0,'CSbH1s2':0,'CSb':0,'A':0,'SS':0,'CCb':0}
        self.filler=0
        self.fillerblaine=0
        self.rho=0
        
    def addbinderBogue(self,weightfraction,composition,blaine):
        '''
        initial content of the cement paste, as mix is performed
        
        :param weightfraction: weight fraction of this binder in the global binder
        :type weightfraction: weight fraction in %
        :param composition: composition of this binder
        :type composition: dictionnary (key=molec, value=weight fraction in %), C3S, C2S, C3A, C4AF, CSbH2, CSbH1s2, A, S, CCb
        :param blaine: Blaine fineness, in m^2/kg. 
        :param blaine: float
        '''
        filler=100.0
        for i in composition:
            self.weightfraction[i]+=weightfraction*composition[i]/10000.0
            filler-=composition[i]
            
        self.blaine+=weightfraction*blaine/100.0
        self.filler+=filler*weightfraction/10000.0
        #self.fillerblaine+=(filler+composition['CCb']+composition['SS']+composition['AA'])*weightfraction*blaine/10000.0
        return
    
    def getrho(self):
        '''
        get the density of the binder
        
        .. warning:: do not call before all calls to :func:`addbinderBogue` !
        
        :returns: the density of the binder
        '''
        if self.rho==0:
            list_elem=[x for x in self.weightfraction if x in rho]
            self.rho=sum([self.weightfraction[x] for x in list_elem])/sum([self.weightfraction[x]/rho[x] for x in list_elem])
        return self.rho
    
    def getinitialcontent(self,wsc):
        '''
        initial content of the cement paste, as mix is performed
        
        :param wsc: water to binder ratio, fillers being excluded
        :type wsc: a float, like 0.42
        :returns: a dictionnary, (key=molec, value= mol / cm^3 of cement paste)
        '''
        #return self.binder.getinitialcontent(wsc)
        N0={}
        rhoc=self.getrho()
        rcre=rhoc/rho["H"]
        for elem in self.weightfraction:
            N0[elem]=self.weightfraction[elem]*rhoc/(M[elem]*(1.+wsc*rcre))
            
        N0["H"]=wsc*rhoc/(M["H"]*(1.+wsc*rcre))-1.5*N0["CSbH1s2"]-2*N0["CSb"]
        N0["CSbH2"]+=N0["CSbH1s2"]+N0["CSb"]
        N0["CSbH1s2"]=0
        N0["CSb"]=0
    
        #l'hydratation de l'hemidrate entraine un petit retrait, dans le retrait le chatelier. On remet à jour les quantités pour avoir un volume de 1cm3
        vol=0
        for espece in N0:
            vol+=N0[espece]*v[espece]
        for espece in N0:
            N0[espece]=N0[espece]/vol
        N0['CSH']=0
        N0['CSHp']=0
        N0['CH']=0
        N0['C6ASb3H32']=0
        N0['C4ASbH12']=0
        N0['C4ACb11H']=0
        N0['C3AFSH4']=0
        N0['FH3']=0
        N0['C3AH6']=0

        return N0
    def getd0(self,n,blainecement):
        return 0          
    def __repr__(self):
        '''
        prints the binder
        
        :returns: the binder as a string
        '''
        s="blaine: "+str(self.blaine)+"\n"
        s+="filler: "+str(self.filler)+"\n"
        for i in self.weightfraction:
            s+="  "+str(i)+": "+str(self.weightfraction[i])
        return s

class Slag:
    '''
    A description of the binder
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.blaine=0
        self.mineral={'C':0,'S':0,'A':0,'M':0}
        self.compo={}
        self.activity=0. #the glassy fraction
    
        
    def addslagSlag(self,weightfraction,mineral,blaine,activity=0.9):
        for i in mineral:
            self.weightfraction[i]+=weightfraction*mineral[i]/10000.0
        self.blaine+=weightfraction*blaine/100.0
        self.activity+=weightfraction*activity/100.0

    def computeCompo(self):
        return
        #calcul du M5AH19 hydrotalcite
        #self.compo['M5AH19']=self.mineral['M']*
        #nal=
        #calcul du CSA, avec les n qui vont bien #TODO
class Calorimeter:
    '''
    A description of the calorimeter
    '''
    def __init__(self):
        '''
        Constructor
        default calorimeter is adiabatic
        
        '''
        #default is adiabatic
        self.capa=0
        self.alpha=0
        self.beta=0
        self.Tmix=20
        self.Text=20
        self.isotherm=0
        self.functemp=0
        
    def setsemiadiabatic(self,alpha,beta,temperature):
        '''
        set a semi adiabatic calorimeter, cf NF EN 196-9
        
        :param alpha: cf NF EN 196-9, in J/h/K
        :type alpha: float
        :param beta: cf NF EN 196-9, in J/h/K^2
        :type alpha: float
        :param temperature: the external temperature and temperature of the mix in celcius
        :type temperature: float
        '''
        self.capa=0 #kJ/K
        self.alpha=alpha  #70  #J/h/K
        self.beta=beta  #0.236 #J/h/K2
        self.Tmix=temperature #celcius
        self.Text=temperature
        self.isotherm=0
        
    def setisotherm(self,temperature,functemp=0):
        '''
        set an isotherm calorimeter
        
        :param temperature: the external temperature and temperature of the mix in celcius
        :type temperature: float
        :param functemp: a function describing the temperature as a function of time. Only called if temperature<-300.
        :type functemp: a function
        '''
        self.capa=0 #kJ/K
        self.alpha=1e23  #J/h/K
        self.beta=0 #J/h/K2
        if temperature>-300:
            self.Tmix=temperature #celcius
        else:
            self.Tmix=functemp(0)
        self.Text=temperature
        self.isotherm=1
        self.functemp=functemp
    def gettemp(self,t=0):
        '''
        get the temperature of the isotherm calorimeter
        
        :param t: time
        :type t: float
        :returns: the temperature (a float)
        ''' 
        if self.Text>-300:
            return self.Text

        return self.functemp(t)    
    
class Dessicator:
    '''
    A description of the dessicator
    '''
    def __init__(self):
        '''
        Constructor
        default calorimeter is adiabatic
        
        '''
        #default is autogeneous
        self.tcure=0
        self.rhtcure=0
        self.rhext=100
        self.depth=0         # en m
        self.diffusion=3e-10 # en m2/s
        self.seasonal_rh_ampli=0 # amplitude of seasonal changes
        self.seasonal_rh_offset=20 #offset par rapport a l'automne
        self.functemp=0
        
        #on passe la diffusion en m2/j:
        self.diffusion=self.diffusion*3600.*24.
        
    def getrh(self,t=0):
        '''
        get the relative humidity
        '''    
        if self.tcure>-1:
            #condition endogène
            if self.tcure==0:
                return -1 
            if t<=self.tcure:
                return -1
            rhperm= self.rhext+(self.rhtcure-self.rhext)*scipy.special.erf(self.depth/(2*np.sqrt(self.diffusion*(t-self.tcure))))
            rh=rhperm+self.seasonal_rh_ampli*np.sin((t-self.seasonal_rh_offset)*2*np.pi/365.)
            if rh>100:
                rh=100
            if rh<0:
                rh=0
            return rh

        return self.functemp(t)
    
def ParrotKilloh(anhyd,alpha,timeeqprev,timeeq):
    '''
    The hydration model of Parrot and Killoh, used by Lothenbach 2008
    
    :param anhyd: the element of the Bogue composition being considered
    :type anhyd: one of 'C3S', 'C2S', 'C3A', 'C4AF'
    :param alpha: the actual degree of hydration of the considered element
    :type alpha: float
    :param timeeqprev: equivalent time, previous time step
    :type timeeqprev: float
    :param timeeq: equivalent time
    :type timeeq: float
    
    :returns: the increment of the degree of hydration on the current time step for a reference Blaine fineness of 350m^2/kg
    '''
    K1={'C3S':1.5,'C2S':0.5, 'C3A':1, 'C4AF':0.37}
    N1={'C3S':0.7,'C2S':1., 'C3A':0.85, 'C4AF':0.7}
    K2={'C3S':0.05,'C2S':0.006, 'C3A':0.04, 'C4AF':0.015}
    K3={'C3S':1.1,'C2S':0.2, 'C3A':1., 'C4AF':0.4}
    N3={'C3S':3.3,'C2S':5.0, 'C3A':3.2, 'C4AF':3.7}
    unmalpha=1-alpha
    if unmalpha>0:   
        if unmalpha<1:
            parrotalpha1=K1[anhyd]/N1[anhyd]*unmalpha*pow(-log(unmalpha),1.-N1[anhyd])
        else:
            navra=1./N1[anhyd]
            kavra=pow(K1[anhyd],navra)
            parrotalpha1=(1.-exp(-kavra*pow(timeeq,navra)))/(timeeq-timeeqprev)
        if unmalpha<1.-0.001 :
            parrotalpha2=K2[anhyd]*pow(unmalpha,2./3.)/(1.-pow(unmalpha,1./3.))
        else :
            parrotalpha2=2.*parrotalpha1
        parrotalpha3=K3[anhyd]*pow(unmalpha,N3[anhyd])
        parrotalpha=min(parrotalpha1,parrotalpha2 ,parrotalpha3)
        return parrotalpha*(timeeq-timeeqprev)
    return 0

def Waller(anhyd,alpha,timeeqprev,timeeq):
    '''
    Hydration of poozolanic species according to Waller 1999
    
    :param anhyd: the element of the Bogue composition being considered
    :type anhyd: one of 'SS', 'A'
    :param alpha: the actual degree of hydration of the considered element
    :type alpha: float
    :param timeeqprev: equivalent time, previous time step
    :type timeeqprev: float
    :param timeeq: equivalent time
    :type timeeq: float
    
    :returns: the increment of the degree of hydration on the current time step for a reference Blaine fineness of 350m^2/kg
    '''
    
    
    
    #tau={'SS':700./24.*400./385.,'A':700./24.*400./385.,'C3A':24./24.}
    #n={'SS':0.9,'A':0.9,'C3A':1.}
    
    tau={'SS':80.*400./385.,'A':80.*400./385.,'C3A':24./24.}   
    n={'SS':0.7,'A':0.7,'C3A':1.} 
    # d'après Waller 1999
    if alpha >= 1: 
        return 0
    if alpha>0.00001:
        #print 'anhyd'+str(anhyd)+' alpha '+str(alpha)
        tostau=timeeqprev/tau[anhyd]-pow((1-alpha)/alpha,-1./n[anhyd])
        alphaend=1./(1.+pow(tau[anhyd]/(timeeq-tostau*tau[anhyd]),n[anhyd]))
        dalpha=(alphaend-alpha)/(timeeq-timeeqprev)
        #dalpha=(n[anhyd]/tau[anhyd])*pow(1-alpha,1+1./n[anhyd])/pow(alpha,3+1/n[anhyd]) #faux
    else:
        dalpha=1./(1.+pow(tau[anhyd]/timeeq,n[anhyd]))/(timeeq-timeeqprev)
    return dalpha*(timeeq-timeeqprev)


def printXls(statel,filename):
    '''
    Print the states at the different time steps in a .xls file
    
    :param statel: the result
    :type statel: a dictionnary produced by :func:`run` of :class:`Hydration_model`
    :param filename: name of the file
    :type filename: a string
    
    '''
    classeur = Workbook()
    
    feuille = classeur.add_sheet("cement")
    
    #header
    feuille.write(1, 0, "step")
    feuille.write(1, 1, "time")
    feuille.write(2, 1, "days")
    
    feuille.write(1, 2, "temperature")
    feuille.write(2, 2, "C")
    feuille.write(1, 3, "heat capacity")
    feuille.write(2, 3, "kJ/kg/K")
    
    feuille.write(0, 5, "cement paste")
    feuille.write(1, 5, "capillary porosity")
    feuille.write(1, 6, "eps chemical shrinkage")
    feuille.write(1, 7, "water filled capillary porosity")
    feuille.write(1, 8, "moisture content")
    feuille.write(1, 9, "rH")
    
    feuille.write(1, 10, "weight of CH formed/g of binder")
    feuille.write(2, 10, "g/g of binder")
    
    feuille.write(1, 11, "weight of bounded water/ g of binder")
    feuille.write(2, 11, "g/g of binder")
    
    feuille.write(1, 12, "volume fraction capillary pores(RH>40%)")
    feuille.write(2, 12, "1")
    
    feuille.write(1, 13, "volume fraction water filled capillary pores")
    feuille.write(2, 13, "1")
    
    
    
    j=0
    for espece in sorted([x for x in statel[0]["fracvol"]]):
        feuille.write(1, 15+j, espece)
        j+=1
    
    #data
    for i in statel:
        feuille.write(i+3, 0, i)
        feuille.write(i+3, 1, statel[i]["time"])
        feuille.write(i+3, 2, statel[i]["temperature"])
        feuille.write(i+3, 3, statel[i]["cpt_mass_beton"])
        
        feuille.write(i+3, 5, statel[i]["phi_cap"])
        feuille.write(i+3, 6, statel[i]["eps_ch"])
        feuille.write(i+3, 7, statel[i]["phi_cap"]+3*statel[i]["eps_ch"])
        feuille.write(i+3, 8, statel[i]["moisture"])
        feuille.write(i+3, 9, statel[i]["rH"])
        
        feuille.write(i+3, 10, statel[i]["wCH"])
        feuille.write(i+3, 11, statel[i]["wb"])
        
        feuille.write(i+3, 12, statel[i]["phic"])
        feuille.write(i+3, 13, statel[i]["phicw"])
        
        j=0
        for espece in sorted([x for x in statel[0]["fracvol"]]):
            feuille.write(i+3, 15+j, statel[i]["fracvol"][espece])
            j+=1
            
        
    classeur.save(filename)
    return

def cookDiam2poro(diam,phimax): 
    #diameter from Cook MIP measurments
    #retourne la fraction en eau
    # diam en m, phimax en %
    if diam<=0.:
        return 0.
    phismall=1.
    if phimax>30:
        phismall=1.-(phimax-30)/(20.)*0.6
    if phismall<0:
        phismall=0
    
    dsmall=2e-8
    sigsmall=0.7
    if phimax>15:
        dsmall=2e-8+6e-8*(phimax-15)/(45.-15.)
        sigsmall=0.7+(1.3-0.7)*(phimax-15)/(45.-15.)
    if dsmall>8e-8:
        dsmall=8e-8
        sigsmall=1.3
        
    dbig=2e-7
    if phimax>30:
        dbig=2e-7+2e-6*np.power((phimax-30)/(20.),2)
        
    sigbig=0.4
    return phimax*(0.5*phismall*(1.+scipy.special.erf((np.log(diam)-np.log(dsmall))/(np.sqrt(2)*sigsmall)))+0.5*(1.-phismall)*(1.+scipy.special.erf((np.log(diam)-np.log(dbig))/(np.sqrt(2)*sigbig))))

def cookPoro2diam(phi,phimax):
    
    if phi>=phimax:
        return 1e-5
    if phimax-phi<1e-5*phimax:
        return 1e-5
    if phi==0:
        return 2e-9
    if phi==phimax:
        return 1.
    #par dichotomie !
    diammin=1e-9
    diammax=6e-2
    poromin=cookDiam2poro(diammin,phimax)
    poromax=cookDiam2poro(diammax,phimax)
    while(phi<poromin):
        diammin=diammin*0.5
        poromin=cookDiam2poro(diammin,phimax)
    while(phi>poromax and diammax<1e-1):
        diammax=diammax*2
        poromax=cookDiam2poro(diammax,phimax)
        if diammax>=1e-1:
            return 1e-5
    #print diammax, poromax
    while diammax-diammin>1e-2*diammax:
        diamtest=np.sqrt(diammin*diammax)
        porotest=cookDiam2poro(diamtest,phimax)
        if porotest>phi:
            diammax=diamtest
        if porotest<phi:
            diammin=diamtest
        #print diammin, diammax, porotest,phi, phimax
    
    #si diamètre inférieur à 2nm, retour 2nm
    if diammin<2e-9:
        return 2e-9
    return diammin

def pvsat(T): #T en celcius, pvsat en Pa
    # Arden Buck equation
    return 1000.*0.61121*np.exp((18.678-T/234.5)*T/(257.14+T))
    
def dpvsat_dT(T): #T en celcius, la dérivée de pvsat en Pa/K
    return ((-1./234.5)*T/(257.14+T)+(18.678-T/234.5)/(257.14+T)-(18.678-T/234.5)*T/np.square(257.14+T))*pvsat(T)
    
def dgamma_dT(T=25.): #T en celcius, retour en mN/m/K
    return 235.8*(1.256*np.power(1-(T+273)/647.096,0.256)*(-1/647.096))*(1-0.625*(1-(T+273)/647.096))+235.8*np.power(1-(T+273)/647.096,1.256)*(0.625/647.096)

def gamma(T=25.):
    return 235.8*np.power(1-(T+273)/647.096,1.256)*(1-0.625*(1-(T+273)/647.096)) #en mN/m

def capillarypressure(waterRadius,T): #T en celcius
    return 2*gamma(T)*0.001/waterRadius

def rh(waterRadius,T): #T en celcius
    vh=18.015e-6
    R=8.314
    #T=293
    gammav=gamma(T)*0.001
    lnrh=-2.*gammav*vh/(waterRadius*R*(T+273.15))
    return np.exp(lnrh)

def waterRadius(rh,T): #T en celcius
    lnrh=np.log(rh)
    vh=18.015e-6
    R=8.314
    #T=293
    gammav=gamma(T)*0.001
    wrad=-2.*gammav*vh/(lnrh*R*(T+273.15))
    return wrad
            
class Hydrationmodel:
    '''
    The hydration model, computing the composition of the cement paste as a function of time
    '''
    
    def __init__(self, binder,wsc):
        '''
        Constructor
        
        :param wsc: the water to cement ratio, filler included
        :type wsc: float
        '''
        
        self.binder=binder
        self.wsc=wsc
        
        self.massc=0.5  #masse de ciment, Kg
  
        self.aggregate={}   #liste d'aggregat [densite-masse-cp]
        self.air_content=0 #la fraction volumique d'air (occlus+ entrainé), teneur en air
        
        self.calo=Calorimeter()
        self.dessicator=Dessicator() #dessicateur par defaut en endogène
        
        self.masshumic=0.  #mass of humic acid in kg.
        self.saturated=0
    def updatefiller(self):
        '''
        The fillers in the cement and in additives is handled as an aggregate.
        It is added to the list of aggregate.
        The mass of cement is reduced accordingly, and the water-to-binder ratio increases.
        
        .. warning:: This function must be called after all calls to :py:func:`addaggregate`, and before any call to :py:func:`run`
        '''
        filler=self.binder.filler*self.massc
        #ajout du filler dans la liste
        self.addaggregate("filler",filler,2.716,0.84) #//filler calcaire
        #le filler est retiré de la masse de pâte de ciment, il devient de l'aggregat
        masscprev=self.massc
        self.massc-=filler
        #le rapport wsc doit être corrigé des fillers.
        self.wsc=self.wsc*(self.massc+filler)/self.massc
        
        #la surface de réaction doit être conservée et affectée au ciment...
        

        #ainsi que la composition massique
        for i in self.binder.weightfraction:
            self.binder.weightfraction[i]*=masscprev/self.massc
        self.binder.filler=0.
        
        self.binder.blaine=self.binder.blaine*masscprev/(self.massc*(self.binder.weightfraction['C3S']+self.binder.weightfraction['C2S']+self.binder.weightfraction['C3A']+self.binder.weightfraction['C4AF']))
        #print "binder blaine",self.binder.blaine
        
        
    def addaggregate(self,name,mass,density,capa,modulus=65,poisson=0.2):
        '''
        Add an aggregate
        
        :param name: the name of the aggregate. 
        :type name: string
        
        .. warning:: Do not use ``"filler"``
        
        :param mass: the mass of aggregate, in kg
        :type mass: float
        :param density: the density of the aggregate
        :type density: float
        :param capa: the heat capactity of the aggregate, in kJ/kg/K
        :type capa: float
        :param modulus: the Young Modulus, GPa
        :type modulus: float
        :param poisson: the Poisson ratio
        :type poisson: float
        '''
        self.aggregate[name]={}
        self.aggregate[name]['mass']=mass    #kg
        self.aggregate[name]['density']=density   #kg/L
        self.aggregate[name]['capa']=capa        #kJ/kg
        self.aggregate[name]['modulus']=modulus       #GPa
        self.aggregate[name]['poisson']=poisson        #
    
    def addsediment(self,mass,blaine,w_clay,active_clay,blaine_clay,w_orga,humic_orga=60.):
        '''
        Add an sediment
        
        :param mass: the mass of sediment, in kg
        :type mass: float
        :param blaine: Blaine fineness, in m^2/kg. 
        :type blaine: float
        :param w_clay: mass fraction of dry clay in the sediment, in %
        :type w_clay: float
        :param active_clay: activity of the clay, if activated by treatment. Between 0 and 1, Suggest 0.6 similar to fly ashes if calcination
        :type active_clay: float
        :param blaine_clay: blaine surface of the clay, in m^2/kg.  Suggest \approx 1000 m^2/kg.
        :type blaine_clay: float
        :param w_orga: mass fraction of organic matter in the sediment, in %
        :type w_orga: float
        :param humic_orga: mass fraction of humic acid in the organic matter, in %. Default is 60%
        :type humic_orga: float
        
        '''
        #la partie organique va compter comme un aggregat très mou.
        mass_orga=mass*w_orga/100.
        mass_sedim=mass-mass_orga
        
        weightfraction_sediment=(mass-mass_orga)/(mass-mass_orga+self.massc)
        
        #on définit un nouveau liant, en considérant que l'argile activée est assimilée à de la silice.
        newbinder=Binder()
        newbinder.addbinderBogue(100.*(1.-weightfraction_sediment), {i:100.*self.binder.weightfraction[i] for i in self.binder.weightfraction}, self.binder.blaine)
        if(w_orga<100.):
            newbinder.addbinderBogue(100.*(weightfraction_sediment),{'SS':100*w_clay/(100.-w_orga)*active_clay},blaine_clay)
        
        
        #on change le liant
        self.binder=newbinder
        self.massc=self.massc+mass_sedim
        
        
        #cette matiere organique devient un aggregat aux propriétés particulières (proche de l'eau)
        self.addaggregate("organic_matter",mass_orga,1.1,4.185,modulus=0.0132,poisson=0.499)
        
        #cette quantité de matière organique va jouer sur la cinétique d'hydratation
        self.masshumic=mass_orga*humic_orga*0.01
        
        
          
    def setEntrainedAir(self,air_content):
        '''
        Set the air content, as measured by NF EN 12350-7
        
        This parameter is only used by :func:`fraclargescale`
        :param air_content: the air content, in %
        :type air_content: float
        '''
        self.air_content=air_content/100.0
        
    def fraclargescale(self):
        '''
        Compute the volume fraction at the macroscopic scale.
        
        :returns: a dictionary (key=phase, value= volume fraction) and the volume of the paste ( binder+water)
        '''
        #calcul des fractions volumiques a l'echelle macro et le volume de la p�te en litre
        fracvol={}
        for name in self.aggregate:
            fracvol[name]=self.aggregate[name]['mass']/self.aggregate[name]['density']
        
        N0=self.initial_content()
        vpaste=0
        mpaste=0
        for i in N0:
            if i!="phi":
                vpaste+=N0[i]*v[i]
                mpaste+=N0[i]*M[i]
        fracvol['paste']=vpaste/mpaste*self.massc*(1+self.wsc)
        
        summ=0
        for i in fracvol:
            summ+=fracvol[i]
        for i in fracvol:
            fracvol[i]=fracvol[i]/summ
            
        #prise en compte de la teneur en air
        for i in fracvol:
            fracvol[i]=fracvol[i]*(1-self.air_content)
        fracvol['air_content']=self.air_content   
        
        return fracvol,vpaste/mpaste*self.massc*(1+self.wsc)
    
    def getrho(self):
        rhoc=self.binder.getrho()
        rhopaste=(1+self.wsc)/(1./rhoc+self.wsc)
        fracvol,vpaste=self.fraclargescale()
        rhocc=fracvol['paste']*rhopaste
        for name in self.aggregate:
            rhocc+=fracvol[name]*self.aggregate[name]['density']
        return rhocc
    
    def getrhoact(self,state):
        # à partir de la composition, la densité de la pâte de ciment
        mass=0.
        volume=1.  #cm3
        for i in state['compo'].keys():
            mass+=state['compo'][i]*M[i]
        rhopaste=mass/volume  #en g/cm3
        
        #rhoc=self.binder.getrho()
        #rhopaste=(1+self.wsc)/(1./rhoc+self.wsc)
        fracvol,vpaste=self.fraclargescale()
        rhocc=fracvol['paste']*rhopaste
        for name in self.aggregate:
            rhocc+=fracvol[name]*self.aggregate[name]['density']
        return rhocc
    
    def iter(self,stateprev,tpun):
        '''
        Compute the state of hydration at the end of a type step
        
        :param stateprev: the state at the beginning of the time step
        :type stateprev: a dictionnary
        :param tpun: the time at the end of the time step
        :type tpun: float
        
        :returns: the state at the end of the time step, a dictionnary
        '''
        state={}
        state['time']=tpun
        
        #calcul de la variation du taux d'avancement des reactions
        
        #acceleration due a la temperature :
        state['timeeqC3S']=stateprev['timeeqC3S']+exp(-42000./8.31*(1./(stateprev['temperature']+273.)-1./293.))*(state['time']-stateprev['time'])
        state['timeeqC2S']=stateprev['timeeqC2S']+exp(-21000./8.31*(1./(stateprev['temperature']+273.)-1./293.))*(state['time']-stateprev['time'])
        state['timeeqC3A']=stateprev['timeeqC3A']+exp(-54000./8.31*(1./(stateprev['temperature']+273.)-1./293.))*(state['time']-stateprev['time'])
        state['timeeqC4AF']=stateprev['timeeqC4AF']+exp(-32000./8.31*(1./(stateprev['temperature']+273.)-1./293.))*(state['time']-stateprev['time'])
        
        # Bentz 1998
        state['timeeqSS']=stateprev['timeeqSS']+exp(-83140./8.31*(1./(stateprev['temperature']+273.)-1./293.))*(state['time']-stateprev['time'])
        # Baert, 5th international Essen workshop
        #state['timeeqSS']=stateprev['timeeqSS']+exp(-46400./8.31*(1./(stateprev['temperature']+273.)-1./293.))*(state['time']-stateprev['time'])

        #taux d'avancement hors temperature, calcule sur la base des temps equivalents :
        # Cinetique d'après le modèle de Parrot et Killoh

        dalphaC3S=ParrotKilloh('C3S', stateprev['alphaC3S'], stateprev['timeeqC3S'], state['timeeqC3S'])    
        dalphaC2S=ParrotKilloh('C2S', stateprev['alphaC2S'], stateprev['timeeqC2S'], state['timeeqC2S'])
        dalphaC4AF=ParrotKilloh('C4AF', stateprev['alphaC4AF'], stateprev['timeeqC4AF'], state['timeeqC4AF'])
        dalphaC3A=ParrotKilloh('C3A', stateprev['alphaC3A'], stateprev['timeeqC3A'], state['timeeqC3A'])

        
        #Waller, cendres volantes, courbe de Bezjah et Knudsen.
        dalphaSS=Waller('SS',stateprev['alphaSS'],stateprev['timeeqSS'],state['timeeqSS'])
        dalphaA=Waller('A',stateprev['alphaA'],stateprev['timeeqSS'],state['timeeqSS'])      
               
        
        
        #influence de la finesse Blaine
        Hl=self.binder.blaine/385.0
        # d'après le modèle de F Lin
        dalphaC3S=dalphaC3S*Hl
        dalphaC2S=dalphaC2S*Hl
        dalphaC3A=dalphaC3A*Hl
        dalphaC4AF=dalphaC4AF*Hl
        dalphaSS=dalphaSS*Hl
        dalphaA=dalphaA*Hl
        
        
        #influence humidité relative
        fracls,vpate=self.fraclargescale()
        #le dessicateur nous retourne un rh cible
        rhtarget=self.dessicator.getrh(stateprev['time'])
        if self.saturated==1:
            rhtarget=0.99
        rH=100.   
        
        #condition endogène : l'évolution du RH est dictée par l'eau disponible.
        # Vp : volume d'eau capillaire+espace en air
        # Vfree : volume d'eau capilaire
        
        # l'eau capillaire à partir de d=2.6nm, à plus que 40% RH au premier séchage. QENS : H=2.65 rho=2.31 molar mass 203, molar vol 88
        Vp=1.
        Vp-=stateprev['compo']['C3S']*v['C3S']+stateprev['compo']['C2S']*v['C2S']+stateprev['compo']['C3A']*v['C3A']+stateprev['compo']['C4AF']*v['C4AF']
        Vp-=stateprev['compo']['SS']*v['SS']+stateprev['compo']['A']*v['A']+stateprev['compo']['CCb']*v['CCb']
        Vp-=stateprev['compo']['CSbH2']*v['CSbH2']+stateprev['compo']['CH']*v['CH']
        Vp-=stateprev['compo']['C6ASb3H32']*v['C6ASb3H32']
        Vp-=stateprev['compo']['C4ASbH12']*v['C4ASbH12']
        Vp-=stateprev['compo']['C4ACb11H']*v['C4ACb11H']
        Vp-=stateprev['compo']['C3AFSH4']*v['C3AFSH4']
        Vp-=stateprev['compo']['C3AH6']*v['C3AH6']
        Vp-=stateprev['compo']['FH3']*v['FH3']
        
        # l'eau capillaire à partir de d=2.6nm, à plus que 40% RH au premier séchage. QENS : H=2.65 rho=2.31 molar mass 203, molar vol 88
        Vp-=stateprev['compo']['CSH']*89.+stateprev['compo']['CSHp']*79.5
        Vfree=(stateprev['compo']['H']+stateprev['compo']['CSH']*(4.-2.7)+stateprev['compo']['CSHp']*(3.9-2.7))*v['H']
        
        
        Vp=Vp*fracls['paste']/(fracls['paste']+fracls['filler'])
        Vfree=Vfree*fracls['paste']/(fracls['paste']+fracls['filler'])
        
        #Vp=(stateprev['phi_cap']+stateprev['compo']['CSH']*v['H']*(4-2.65)+stateprev['compo']['CSHp']*v['H']*(3.9-2.65))*fracls['paste']/(fracls['paste']+fracls['filler'])
        #Vfree=(stateprev['compo']['H']*v['H']+stateprev['compo']['CSH']*v['H']*(4-2.65)+stateprev['compo']['CSHp']*v['H']*(3.9-2.65))*fracls['paste']/(fracls['paste']+fracls['filler'])
        
        #calcul du diamètre du dernier pore plein:
        if Vfree>Vp:
            "oups.... Vfree>Vp..."
            Vfree=Vp
        if Vfree<0:
            "no more water..."
        #print "Vfree, Vp", Vfree, Vp
        
        effectivediam=cookPoro2diam(100*Vfree, 100*Vp)
        #print "effectivediam",effectivediam
        rH=rh(effectivediam*0.5,stateprev['temperature'])
        #print 'rH', rH
        state['cap_pressure']=capillarypressure(effectivediam*0.5,stateprev['temperature']) #capillary pressure en MPa
        
        
        if stateprev['time']<self.dessicator.tcure:
            #mise a jour du dessicateur :
            self.dessicator.rhtcure=rH
            
        if rhtarget>0:
            #condition d'échange : l'evolution de RH est fixée par les echanges.
            #rH=rhtarget
            effectivediam=2.*waterRadius(rhtarget,stateprev['temperature'])
            #effectivediam=-0.6237/(lnRH*(stateprev['temperature']+273.))
            #print "effectivediam", effectivediam
            
            # porosité pleine d'eau liée au diamètre du plus gros pore plein:
            vcap=cookDiam2poro(effectivediam, 100*Vp)
            if vcap<0:
                vcap=0
            #cette eau correspond à l'eau dont on doit tenir compte. On doit soustraire l'eau pour retrouver la stochiometrie de 4
            vcap=vcap-stateprev['compo']['CSH']*v['H']*(4-2.7)-stateprev['compo']['CSHp']*v['H']*(3.9-2.7)
            waterend=(vcap)*(fracls['paste']+fracls['filler'])/fracls['paste']/v['H']

            if (self.dessicator.rhext<rH and rhtarget<rH) or (self.dessicator.rhext>rH):   #on autorise la réhumidification
                rH=rhtarget
                state['cap_pressure']=capillarypressure(effectivediam*0.5,stateprev['temperature']) #capillary pressure en MPa
                stateprev['compo']['H']=waterend
            
            
        state['rH']=rH
        #print self.wsc, state['time'],  rH, pow((rH-0.55)/0.45,4.)
        
        #print 'rh',rH
        # Parrot, cite par Von Breugel
        Hl=1.
        Hl=pow((rH-0.55)/0.45,4.)
        #Hl=redfact
        #mine
        #Hl=pow((rH-0.8)/0.2,1.)
        #Hl=1.
        #Hl=1.
        #print  self.wsc, state['time'], rH
        if rH<0.80:
            Hl=0
            #print "dry", self.wsc
        #print "time"+str(tpun)+ "Hl "+str(Hl)
        if self.saturated==1:
            Hl=1.
        #Hl=1.
        
            #on bouche les vides avec de l'eau
            #stateprev['compo']['H']+=-3.*stateprev['eps_ch']/v['H']
            
            #state
        #influence du rapport w/c, d'après Bentz 2006
        #tot=0
        #for x in stateprev['compo']:
        #    tot+=stateprev['compo'][x]*v[x]
        #Hl=stateprev['compo']['H']*v['H']/(tot)*5.
        #Hl*=self.wsc/0.4
        #Hl=1.
        #print Hl
        #Hl=stateprev['compo']['H']*v['H']/stateprev['phi_cap']
        dalphaC3S=dalphaC3S*Hl
        dalphaC2S=dalphaC2S*Hl
        dalphaC3A=dalphaC3A*Hl
        dalphaC4AF=dalphaC4AF*Hl
        dalphaSS=dalphaSS*Hl
        dalphaA=dalphaA*Hl
        
        
        #influence de la matière organique, en particulier, de l'acide humique
        Hl=1-self.masshumic/(0.03*self.massc)
        if Hl<0.:
            Hl=0.
        
        dalphaC3S=dalphaC3S*Hl
        dalphaC2S=dalphaC2S*Hl
        dalphaC3A=dalphaC3A*Hl
        dalphaC4AF=dalphaC4AF*Hl
        dalphaSS=dalphaSS*Hl
        dalphaA=dalphaA*Hl
        
        #limitation des alphas
        if(stateprev['alphaC3S']+dalphaC3S>1):
            dalphaC3S=1-stateprev['alphaC3S']
        if(stateprev['alphaC2S']+dalphaC2S>1):
            dalphaC2S=1-stateprev['alphaC2S']
        if(stateprev['alphaC3A']+dalphaC3A>1):
            dalphaC3A=1-stateprev['alphaC3A']
        if(stateprev['alphaC4AF']+dalphaC4AF>1):
            dalphaC4AF=1-stateprev['alphaC4AF']
        if(stateprev['alphaSS']+dalphaSS>1):
            dalphaSS=1-stateprev['alphaSS']
        if(stateprev['alphaA']+dalphaA>1):
            dalphaA=1-stateprev['alphaA']
        
        #reactions, par ordre de priorité
        N0=self.initial_content()
        dalphaR={}
        compo=stateprev['compo'].copy()
        #C3S
        #dalphaR['RC3S']=d_reac['RC3S'].react(dalphaC3S,compo,N0['C3S'])
        #C2S
        #dalphaR['RC2S']=d_reac['RC2S'].react(dalphaC2S,compo,N0['C2S'])
        #C3A
        # gypse to ettringite
        dalphaR['RaC3A']=d_reac['RaC3A'].react(dalphaC3A,compo,N0['C3A'])
        
        #d'après Lothenbach2008
        dalphaR['RdC3A']=0
        if stateprev['temperature']<48:
            #C3A to monocarboaluminate
            dalphaR['RdC3A']=d_reac['RdC3A'].react(dalphaC3A-dalphaR['RaC3A'],compo,N0['C3A'])
        # ettringite to monosulphoaluminate
        dalphaR['RbC3A']=d_reac['RbC3A'].react(dalphaC3A-dalphaR['RaC3A']-dalphaR['RdC3A'],compo,N0['C3A'])
        # C3A to C3AH6
        dalphaR['RcC3A']=d_reac['RcC3A'].react(dalphaC3A-dalphaR['RaC3A']-dalphaR['RdC3A']-dalphaR['RbC3A'],compo,N0['C3A'])
        
        #C4AF
        
        #D'après Brouwers, Dilnesa, Lothenbach 2014, C4AF réagit avec le C2S et le C3S pour formet des hydrogarnets
        dalphaR['RfC4AF']=d_reac['RfC4AF'].react(dalphaC4AF,compo,N0['C4AF'])
        dalphaR['ReC4AF']=d_reac['ReC4AF'].react(dalphaC4AF-dalphaR['RfC4AF'],compo,N0['C4AF'])
        
        # gypse to ettringite
        dalphaR['RaC4AF']=d_reac['RaC4AF'].react(dalphaC4AF-dalphaR['RfC4AF']-dalphaR['ReC4AF'],compo,N0['C4AF'])
        #idem Lothenbach2008
        dalphaR['RdC4AF']=0
        
        if stateprev['temperature']<48:
            #C4AF to monocarboaluminate
            dalphaR['RdC4AF']=d_reac['RdC4AF'].react(dalphaC4AF-dalphaR['RfC4AF']-dalphaR['ReC4AF']-dalphaR['RaC4AF'],compo,N0['C4AF'])
        # ettringite to monosulphoaluminate
        dalphaR['RbC4AF']=d_reac['RbC4AF'].react(dalphaC4AF-dalphaR['RfC4AF']-dalphaR['ReC4AF']-dalphaR['RaC4AF']-dalphaR['RdC4AF'],compo,N0['C4AF'])
        # C4AF to C3AH6
        dalphaR['RcC4AF']=d_reac['RcC4AF'].react(dalphaC4AF-dalphaR['RfC4AF']-dalphaR['ReC4AF']-dalphaR['RaC4AF']-dalphaR['RdC4AF']-dalphaR['RbC4AF'],compo,N0['C4AF'])
        
        #C3S
        #print "reste "+str(dalphaC3S-dalphaR['RfC4AF']*d_reac['RfC4AF'].eq['C3S']/d_reac['RfC4AF'].eq['C4AF']*N0[])
        #print "ratio"+str(d_reac['RfC4AF'].eq['C3S']/d_reac['RfC4AF'].eq['C4AF'])
        #print ""
        dalphaR['RC3S']=0
        dalphaR['RC2S']=0
        if(N0['C3S']>0):
            dalphaR['RC3S']=d_reac['RC3S'].react(dalphaC3S-dalphaR['RfC4AF']*d_reac['RfC4AF'].eq['C3S']/d_reac['RfC4AF'].eq['C4AF']*N0['C4AF']/N0['C3S'],compo,N0['C3S'])
        #C2S
        if N0['C2S']>0:
            dalphaR['RC2S']=d_reac['RC2S'].react(dalphaC2S-dalphaR['ReC4AF']*d_reac['ReC4AF'].eq['C2S']/d_reac['ReC4AF'].eq['C4AF']*N0['C4AF']/N0['C2S'],compo,N0['C2S'])
        
        #reaction pouzzolanique
        # reaction SS silice
        dalphaR['RSS']=d_reac['RSS'].react(dalphaSS,compo,N0['SS'])
        # reaction A alumine
        # gypse to ettringite
        dalphaR['RaA']=d_reac['RaA'].react(dalphaA,compo,N0['A'])
        #idem Lothenbach 2008
        dalphaR['RdA']=0
        if stateprev['temperature']<48:
            #C4AF to monocarboaluminate
            dalphaR['RdA']=d_reac['RdA'].react(dalphaA-dalphaR['RaA'],compo,N0['A'])
        # ettringite to monosulphoaluminate
        dalphaR['RbA']=d_reac['RbA'].react(dalphaA-dalphaR['RaA']-dalphaR['RdA'],compo,N0['A'])
        # C4AF to C3AH6
        dalphaR['RcA']=d_reac['RcA'].react(dalphaA-dalphaR['RaA']-dalphaR['RdA']-dalphaR['RbA'],compo,N0['A'])
      
        state['compo']=compo
        # mise a jour des degres d'hydratation
        state['alphaC3S']=0
        state['alphaC2S']=0
        state['alphaC3A']=0
        state['alphaC4AF']=0
        state['alphaSS']=0
        state['alphaA']=0
        if N0['C3S']>0:
            state['alphaC3S']=1-state['compo']['C3S']/N0['C3S']
        if N0['C2S']>0:
            state['alphaC2S']=1-state['compo']['C2S']/N0['C2S']
        if N0['C3A']>0:
            state['alphaC3A']=1-state['compo']['C3A']/N0['C3A']
        if N0['C4AF']>0:
            state['alphaC4AF']=1-state['compo']['C4AF']/N0['C4AF']
        if N0['SS']>0:
            state['alphaSS']=1-state['compo']['SS']/N0['SS']
        if N0['A']>0:
            state['alphaA']=1-state['compo']['A']/N0['A']
        #calcul du retrait chimique :
        
        
        #mise a jour de la temperature equivalente des csh et cshp
        state['Tcsh']=0
        state['Tcshp']=0
        if(state['compo']['CSH']>0):
            state['Tcsh']=(stateprev['Tcsh']*stateprev['compo']['CSH']+(state['compo']['CSH']-stateprev['compo']['CSH'])*stateprev['temperature'])/state['compo']['CSH']
        if(state['compo']['CSHp']>0):
            state['Tcshp']=(stateprev['Tcshp']*stateprev['compo']['CSHp']+(state['compo']['CSHp']-stateprev['compo']['CSHp'])*stateprev['temperature'])/state['compo']['CSHp']
        #print "time "+str(state['time'])+" Tcsh "+str(state['Tcsh'])+" temperature "+str(stateprev['temperature'])
        #calcul  du retrait chimique
        volume=0
        for molec in state['compo']:
                volume+=state['compo'][molec]*v[molec]
        
        state['eps_ch']=(volume-1.)/3.
        
        #calcul de la grosse porosite capillaire, en dehors du gel de C-S-H
        volume=0
        for molec in state['compo']:
                if molec!='H':
                    volume+=state['compo'][molec]*v[molec]
        if volume>1:
            print("volume is %f", volume)
            volume=1.
        state['phi_cap']=1-volume
                
        #TODO 2 : la porosite capillaire et le retrait de la pâte de ciment doivent être mis à jour en prenant en compte la fraction de filler.
        
        #calcul de la teneur en eau : masse d'eau encore à secher sur masse d'eau complétement humide.
        state['moisture']=((4-1.4)*state['compo']['CSH']+state['compo']['H']+(3.9-1.4)*state['compo']['CSHp'])*M['H']/(((4-1.4)*state['compo']['CSH']+state['compo']['H']+(3.9-1.4)*state['compo']['CSHp'])*M['H']-3*state['eps_ch'])
        #calcul du degagement de chaleur:
        deltaH=0
        deltaH+=dalphaR['RC3S']*N0['C3S']*(dheat['RC3S']+dcp['RC3S']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RC2S']*N0['C2S']*(dheat['RC2S']+dcp['RC2S']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RaC3A']*N0['C3A']*(dheat['RaC3A']+dcp['RaC3A']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RbC3A']*N0['C3A']*(dheat['RbC3A']+dcp['RbC3A']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RcC3A']*N0['C3A']*(dheat['RcC3A']+dcp['RcC3A']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RdC3A']*N0['C3A']*(dheat['RdC3A']+dcp['RdC3A']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RaC4AF']*N0['C4AF']*(dheat['RaC4AF']+dcp['RaC4AF']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RbC4AF']*N0['C4AF']*(dheat['RbC4AF']+dcp['RbC4AF']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RcC4AF']*N0['C4AF']*(dheat['RcC4AF']+dcp['RcC4AF']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RdC4AF']*N0['C4AF']*(dheat['RdC4AF']+dcp['RdC4AF']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['ReC4AF']*N0['C4AF']*(dheat['ReC4AF']+dcp['ReC4AF']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RfC4AF']*N0['C4AF']*(dheat['RfC4AF']+dcp['RfC4AF']/1000.*(stateprev['temperature']-25))
        
        deltaH+=dalphaR['RSS']*N0['SS']*(dheat['RSS']+dcp['RSS']/1000.*(stateprev['temperature']-25))
        
        deltaH+=dalphaR['RaA']*N0['A']*(dheat['RaA']+dcp['RaA']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RbA']*N0['A']*(dheat['RbA']+dcp['RbA']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RcA']*N0['A']*(dheat['RcA']+dcp['RcA']/1000.*(stateprev['temperature']-25))
        deltaH+=dalphaR['RdA']*N0['A']*(dheat['RdA']+dcp['RdA']/1000.*(stateprev['temperature']-25))
        
        state['deltaH']=deltaH

        #calcul de la capacit� calorifique:
        cpt=0
        for molec in state['compo']:
            cpt+=state['compo'][molec]*cp[molec]
                   
        state['cpt']=cpt  #J/cm3
        #il faut passer au volume de b�ton consid�r�.
        fracls,vpate=self.fraclargescale()
        deltaH=deltaH*vpate*1000.  # kJ
        #if deltaH>0:
            #print "deltaH is "+str(deltaH)
        state['cumulHsc']=stateprev['cumulHsc']+deltaH/(self.massc+self.aggregate['filler']['mass'])
        state['derivHsc']=deltaH/(self.massc+self.aggregate['filler']['mass'])/(state['time']-stateprev['time'])
        
        cpt=cpt*vpate*1000./1000.  #kJ/K
       
        masse=self.massc*(1+self.wsc)
        #ajout des aggregats
        for i in self.aggregate:
            cpt+=self.aggregate[i]['mass']*self.aggregate[i]['capa']
            masse+=self.aggregate[i]['mass']
        
        state['cpt_mass_beton']=cpt/masse
        
        #ajout de la capacite du calorimetre en kJ/K
        cpt+=self.calo.capa
        
        #terme de perte sur le pas de temps
        #print "diffT="+str(stateprev['temperature']-self.calo['Text'])+" alphaSS "+str(state['alphaSS'])
        if stateprev['temperature']>self.calo.Text :
            qq=(stateprev['temperature']-self.calo.Text)*(self.calo.alpha+self.calo.beta*(stateprev['temperature']-self.calo.Text))
        else:
            qq=(stateprev['temperature']-self.calo.Text)*(self.calo.alpha)
        
        qq=qq*(state['time']-stateprev['time'])*24./1000. # kJ sur le pas de temps, perte
        
        #mise a jour de la temperature: cas isotherme
        if(((deltaH+qq)/cpt>(stateprev['temperature']-self.calo.gettemp(state['time'])) and qq>0) or self.calo.isotherm==1):
            state['temperature']=self.calo.gettemp(state['time'])
            #print "here ! temperature is "+str(state['temperature'])
        else:
            if((deltaH+qq)/cpt<(stateprev['temperature']-self.calo.gettemp(state['time'])) and qq<0):
                state['temperature']=self.calo.gettemp(state['time'])
                #if state['temperature']==0: print "error"+str(state['time'])
            else:
                state['temperature']=stateprev['temperature']+(-deltaH-qq)/cpt
        #calcul des fractions volumiques:
        fracvol={}
        #fracvol['phi_cap_tot']=state['phi_cap']
        
        fracvol['anhydre']=state['compo']['C3S']*v['C3S']+state['compo']['C2S']*v['C2S']+state['compo']['C3A']*v['C3A']+state['compo']['C4AF']*v['C4AF']
        fracvol['SS']=state['compo']['SS']*v['SS']
        fracvol['A']=state['compo']['A']*v['A']
        fracvol['CCb']=state['compo']['CCb']*v['CCb']
        fracvol['CSbH2']=state['compo']['CSbH2']*v['CSbH2']
        fracvol['CH']=state['compo']['CH']*v['CH']
        fracvol['C6ASb3H32']=state['compo']['C6ASb3H32']*v['C6ASb3H32']
        fracvol['C4ASbH12']=state['compo']['C4ASbH12']*v['C4ASbH12']
        fracvol['C4ACb11H']=state['compo']['C4ACb11H']*v['C4ACb11H']
        fracvol['C3AFSH4']=state['compo']['C3AFSH4']*v['C3AFSH4']
        fracvol['C3AH6']=state['compo']['C3AH6']*v['C3AH6']
        fracvol['FH3']=state['compo']['FH3']*v['FH3']
        #ajout AS
        fracvol['C3A']=state['compo']['C3A']*v['C3A']
        fracvol['C3S']=state['compo']['C3S']*v['C3S']
        fracvol['C2S']=state['compo']['C2S']*v['C2S']
        fracvol['C4AF']=state['compo']['C4AF']*v['C4AF']
        #fin ajout AS
        
        fracvolleft=1-fracvol['anhydre']-fracvol['CSbH2']-fracvol['CH']-fracvol['SS']-fracvol['A']-fracvol['CCb']
        fracvolleft-=fracvol['C6ASb3H32']
        fracvolleft-=fracvol['C4ASbH12']
        fracvolleft-=fracvol['C4ACb11H']
        fracvolleft-=fracvol['C3AFSH4']
        fracvolleft-=fracvol['C3AH6']
        fracvolleft-=fracvol['FH3']
        
        #calcul de la microstructure au niveau du gel:
        # Tennis et Jennis : on va confondre CSH-LD et surface specifique accessible au N2
        # Tennis et Jennings donne un rapport de surfaces entre CSH-LD et CSH total, appelé rapport de masse dans l'article
        #on part du principe que ce ratio est un rapport de nombre de globules, cad un rapport de nombre de mol.
        #le alpha tot de T et J est un rapport de volume
        #du reste, il est proche du rapport de masse.
        alpha=1-fracvol['anhydre']/(N0['C3S']*v['C3S']+N0['C2S']*v['C2S']+N0['C3A']*v['C3A']+N0['C4AF']*v['C4AF'])
        
        state['alpha']=alpha
        
        
        
        #vCSHHD=(state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp'])/(state['compo']['CSH']+state['compo']['CSHp'])
        
        #influecne de la temperature Galluci 2013
        #vCSHHD=-0.48*(state['Tcsh']-20.)+vCSHHD
        
        #vCSHLD=127.
        #vCSHHD=105.
        #print 'MCSH',M['CSH']-2.5*M['H'], "mcshp", M['CSHp']-2.4*M['H']
        #la masse de CSH LD (sec) est fonction de la masse totale de CSH (sec), Tennis & Jennings 2000 CCR 30 [6]
        #le CSH sec correspond à H=1.5, soit 2.5H de moins que le CSH classique
        #rhoCSHLD=1.44
        rhoCSHLD=1.44
        
        #model de Konigsberger et. al. 2016 : la densité du CSH dépend de l'espace disponible.
        #Nombre de mol de CSH
        nCSH=state['compo']['CSH']+state['compo']['CSHp']
        #volume de CSH dense, en cm3
        vsCSH=nCSH*72.1
        #volume total disponible
        vavail=state['phi_cap']+state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp']
        
        #print "vavail",vavail,"vsCSH",vsCSH,"frac_solid",vsCSH/(vavail+vsCSH)
        #porosité totale
        gamma=(vavail-vsCSH)/vavail
        #if gamma>0.55:
        #    rhoCSHLD=1.44-(gamma-0.55)*(1.44-0.8)/(1-0.55)
        #print "rhCSHLD",rhoCSHLD
        
        mCSHdrytot=((M['CSH']-2.5*M['H'])*state['compo']['CSH']+(M['CSHp']-2.4*M['H'])*state['compo']['CSHp'])
        mCSHdrytot=(M['CSH']-2.5*M['H'])*(state['compo']['CSH']+state['compo']['CSHp'])
        mCSHLDdry=(3.017*self.wsc*alpha-1.347*alpha+0.538)*mCSHdrytot
        #if self.wsc>0.5:
        #    mCSHLDdry=(3.017*0.5*alpha-1.347*alpha+0.538)*mCSHdrytot
            
        if mCSHLDdry>mCSHdrytot:
            mCSHLDdry=mCSHdrytot
        #la densité sèche du CSH LD est de 1.44, celle du CSH HD dry est de 1.75
        vvCSHLD=mCSHLDdry/rhoCSHLD
        vvCSHHD=(mCSHdrytot-mCSHLDdry)/1.75
        vvCSHLP=0
        '''
        #introduction d'un CSH de très basse densité
        #model de Konigsberger et. al. 2016
        #Nombre de mol de CSH
        nCSH=state['compo']['CSH']+state['compo']['CSHp']
        #volume de CSH dense, en cm3
        vsCSH=nCSH*72.1
        #volume total disponible
        vavail=state['phi_cap']+state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp']
        #porosité totale
        gamma=(vavail-vsCSH)/vavail
        
        mCSHLPdry=(0.1+(gamma-0.56)*0.9/(1.-0.56))*mCSHLDdry
        if mCSHLPdry<0:
            mCSHLPdry=0
        mCSHLDdry=mCSHLDdry-mCSHLPdry
        vvCSHLD=mCSHLDdry/1.44
        vvCSHLP=mCSHLPdry/1.23
        '''    
        if vvCSHHD<0:
            vvCSHHD=0
            vvCSHLD=mCSHdrytot/rhoCSHLD
        if vvCSHLD<0:
            vvCSHLD=0
            vvCSHHD=mCSHdrytot/1.75
        
        '''
        if vvCSHHD<stateprev['fracvol']['CSHHD']:
            vvCSHHD=stateprev['fracvol']['CSHHD']
            
            
            mCSHLDdry=(mCSHdrytot-vvCSHHD*1.75) 
            mCSHLPdry=(0.1+(gamma-0.56)*0.9/(1.-0.56))*mCSHLDdry
            mCSHLPdry=0.
            if mCSHLPdry<0:
                mCSHLPdry=0
            mCSHLDdry=mCSHLDdry-mCSHLPdry
            vvCSHLD=mCSHLDdry/rhoCSHLD
            vvCSHLP=mCSHLPdry/1.23
        '''     
        #print "rho CSH-HD saturated",  (state['compo']['CSH']*M['CSH']+state['compo']['CSHp']*M['CSHp'])/(state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp'])
        #vCSHLD=(state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp'])
        #veau=vCSHLD*0.18/(1+0.18)
        #mtot=(state['compo']['CSH']*M['CSH']+state['compo']['CSHp']*M['CSHp'])+veau*M['H']/v['H']
        #print "rho CSH-LD saturated", mtot/(veau+vCSHLD)
        #le volume des gros pores.
        
        
        
        
        bbigcapvoid=state['phi_cap']+state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp']
        bbigcapvoid-=vvCSHLD
        bbigcapvoid-=vvCSHHD
        bbigcapvoid-=vvCSHLP

        if bbigcapvoid<0:
            bbigcapvoid=0
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            vvCSHLD=(mCSHdrytot-(state['phi_cap']+state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp'])*1.75)/(rhoCSHLD-1.75)
            vvCSHHD=state['phi_cap']+state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp']-vvCSHLD 
        
        fracvol['CSHLP']=vvCSHLP    
        fracvol['CSHLD']=vvCSHLD
        fracvol['CSHHD']=vvCSHHD
        fracvol['bigcapillaryvoids']=bbigcapvoid
        
        #print "gamma",(fracvolleft-72.*(state['compo']['CSH']+state['compo']['CSHp']))/fracvolleft
        #print "CSHLP",fracvol['CSHLP'],"CSHLD",fracvol['CSHLD'],"CSHHD", fracvol['CSHHD']," bigcap",fracvol['bigcapillaryvoids']
        
        #model de Konigsberger et. al. 2016
        #Nombre de mol de CSH
        nCSH=state['compo']['CSH']+state['compo']['CSHp']
        #volume de CSH dense, en cm3
        vsCSH=nCSH*72.1
        #volume total disponible
        vavail=state['phi_cap']+state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp']
        
        vavail=state['compo']['H']*v['H']+state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp']
        #print "vavail",vavail,"vsCSH",vsCSH,"frac_solid",vsCSH/(vavail+vsCSH)
        #porosité totale
        gamma=(vsCSH)/vavail
        #print 'time',state['time'], 'gamma',gamma, 'tot vnull', state['phi_cap']+state['compo']['CSH']*v['CSH']+state['compo']['CSHp']*v['CSHp']-(1-0.942)*vavail
        #quantité de volume de CSH-A
        VCSHA=0
        VCSHB=0
        rhoCSHB=0
        if gamma>0.942:
            VCSHA=vsCSH
        else:
            if stateprev['VCSHA']==0:
                VCSHA=(1.-0.942)*vavail
            else:
                VCSHA=stateprev['VCSHA']
            #la densité du CSH B
            rhoCSHB=(0.901-0.411*gamma)*2.604
            VCSHB=(2.604-1)*(vsCSH-VCSHA)/(rhoCSHB-1.)
        VCSH=VCSHA+VCSHB
        if VCSH>vavail:
            VCSH=vavail
            rhoCSHB=((vsCSH-VCSHA)*2.604+(vavail-vsCSH)*1.)/(vavail-VCSHA)
        state['vavail']=vavail
        state['VCSHA']=VCSHA
        state['VCSHB']=VCSHB
        state['rhoBCSH']=rhoCSHB
            
        #print 'AVAIL',state['vavail'],'CSHA',state['VCSHA'],'CSHB',state['VCSHB'],'rhoB',state['rhoBCSH'],'rhoCSH',(2.604*VCSHA+state['rhoBCSH']*VCSHB)/(VCSHA+VCSHB)
        
        
        state['fracvol']=fracvol
        
        #stokage de la masse de CH/masse ciment et de la quantité d'eau liée/ masse ciment
        masscement=1./(self.wsc+1./self.binder.getrho())
        state['wCH']=M['CH']*state['compo']['CH']/masscement
        #calcul de la quantité d'eau liée chimiquement
        # P-dried density of C-S-H, d'après Brouwers
        state['wb']=(1.2*(state['compo']['CSH']+state['compo']['CSHp']))
        #state['wb']=(2.1*(state['compo']['CSH']+state['compo']['CSHp'])) #2.1 pour 11%RH
        state['wb']+=state['compo']['CH']
        state['wb']+=9.*state['compo']['C6ASb3H32']  #Powers and Bonwyard, cited by Brouwers
        state['wb']+=10.*state['compo']['C4ASbH12']
        state['wb']+=11.*state['compo']['C4ACb11H']
        state['wb']+=7.64*state['compo']['C3AFSH4']
        state['wb']+=6.*state['compo']['C3AH6']
        state['wb']+=3.*state['compo']['FH3']
        state['wb']+=2.*state['compo']['CSbH2']
        state['wb']=state['wb']*M['H']/masscement
        
        if 'filler' in self.aggregate:
            state['wCH']=state['wCH']*(self.massc)/(self.massc+self.aggregate['filler']['mass'])
            state['wb']=state['wb']*(self.massc)/(self.massc+self.aggregate['filler']['mass'])
            
        #le degree d'hydratation massique
        alpha=1-(state['compo']['C3S']*M['C3S']+state['compo']['C2S']*M['C2S']+state['compo']['C3A']*M['C3A']+state['compo']['C4AF']*M['C4AF'])/(N0['C3S']*M['C3S']+N0['C2S']*M['C2S']+N0['C3A']*M['C3A']+N0['C4AF']*M['C4AF'])
        state['alpham']=alpha
        
        alphap=0.
        if (N0['SS']*M['SS']+N0['A']*M['A'])>0:
            alphap=1-(state['compo']['SS']*M['SS']+state['compo']['A']*M['A'])/(N0['SS']*M['SS']+N0['A']*M['A'])
        state['alphamp']=alphap
        
        # la porosité capillaire (>40% RH...)
        # le volume d'eau dans cette porosité capilaire
        
        # l'eau capillaire à partir de d=2.6nm, à plus que 40% RH au premier séchage. QENS : H=2.65 rho=2.31 molar mass 203, molar vol 88
        Vp=1.
        Vp-=state['compo']['C3S']*v['C3S']+state['compo']['C2S']*v['C2S']+state['compo']['C3A']*v['C3A']+state['compo']['C4AF']*v['C4AF']
        Vp-=state['compo']['SS']*v['SS']+state['compo']['A']*v['A']+state['compo']['CCb']*v['CCb']
        Vp-=state['compo']['CSbH2']*v['CSbH2']+state['compo']['CH']*v['CH']
        Vp-=state['compo']['C6ASb3H32']*v['C6ASb3H32']
        Vp-=state['compo']['C4ASbH12']*v['C4ASbH12']
        Vp-=state['compo']['C4ACb11H']*v['C4ACb11H']
        Vp-=state['compo']['C3AFSH4']*v['C3AFSH4']
        Vp-=state['compo']['C3AH6']*v['C3AH6']
        Vp-=state['compo']['FH3']*v['FH3']
        
        # l'eau capillaire à partir de d=2.6nm, à plus que 40% RH au premier séchage. QENS : H=2.65 rho=2.31 molar mass 203, molar vol 88
        Vp-=state['compo']['CSH']*89.+state['compo']['CSHp']*79.5
        Vfree=(state['compo']['H']+state['compo']['CSH']*(4.-2.7)+state['compo']['CSHp']*(3.9-2.7))*v['H']
        
        Vp=Vp*fracls['paste']/(fracls['paste']+fracls['filler'])
        Vfree=Vfree*fracls['paste']/(fracls['paste']+fracls['filler'])
        
        #Vp=(stateprev['phi_cap']+stateprev['compo']['CSH']*v['H']*(4-2.35)+stateprev['compo']['CSHp']*v['H']*(3.9-2.35))*fracls['paste']/(fracls['paste']+fracls['filler'])
        #Vfree=(stateprev['compo']['H']*v['H']+stateprev['compo']['CSH']*v['H']*(4-2.35)+stateprev['compo']['CSHp']*v['H']*(3.9-2.35))*fracls['paste']/(fracls['paste']+fracls['filler'])
        if Vfree>Vp:
            Vfree=Vp
        if Vfree<0:
            "no more water... oups..."
        state['phic']=Vp
        state['phicw']=Vfree
        
        #print 'volume',fracvol['CSHLD']+fracvol['CSHHD'],VCSHA+VCSHB
        #print 'TTTT',alpha,gamma,(2.604*VCSHA+state['rhoBCSH']*VCSHB)/(VCSHA+VCSHB)
        
        return state
    
    def initial_content(self):
        '''
        Compute the initial content of the binder, that is the composition of 1cm^3 of the paste
        
        :returns: a dictionnary, (key=molec, value= mol / cm^3 of cement paste)
        '''
        return self.binder.getinitialcontent(self.wsc)
     
    def initialize(self):
        '''
        build up an initial state
        
        :returns: a state (a dictionnary) at a fresh start
        '''
        stateprev={}
        stateprev['time']=0
        
        stateprev['timeeqC3S']=0
        stateprev['timeeqC2S']=0
        stateprev['timeeqC3A']=0
        stateprev['timeeqC4AF']=0
        stateprev['timeeqSS']=0
        stateprev['temperature']=self.calo.Tmix
        
        
        stateprev["compo"]=self.initial_content()
        stateprev['phi_cap']=stateprev['compo']['H']*v['H']
        stateprev['eps_ch']=0
        stateprev['moisture']=1
        stateprev['rH']=1.
        
        stateprev['alphaC3S']=0
        stateprev['alphaC2S']=0
        stateprev['alphaC3A']=0
        stateprev['alphaC4AF']=0
        stateprev['alphaSS']=0
        stateprev['alphaA']=0
        
        stateprev['alpha']=0
        stateprev['alpham']=0
        stateprev['alphamp']=0
        
        fracvol={}
        fracvol['anhydre']=stateprev['compo']['C3S']*v['C3S']+stateprev['compo']['C2S']*v['C2S']+stateprev['compo']['C3A']*v['C3A']+stateprev['compo']['C4AF']*v['C4AF']
        fracvol['SS']=stateprev['compo']['SS']*v['SS']
        fracvol['A']=stateprev['compo']['A']*v['A']
        fracvol['CCb']=stateprev['compo']['CCb']*v['CCb']
        fracvol['CSbH2']=stateprev['compo']['CSbH2']*v['CSbH2']
        fracvol['CH']=0
        fracvol['C6ASb3H32']=0
        fracvol['C4ASbH12']=0
        fracvol['C4ACb11H']=0
        fracvol['C3AH6']=0
        fracvol['FH3']=0
        fracvol['C3AFSH4']=0
        fracvol['CSHHD']=0
        fracvol['CSHLD']=0
        fracvol['CSHLP']=0
        fracvol['bigcapillaryvoids']=stateprev['phi_cap']
        
        
        stateprev['fracvol']=fracvol
        
        stateprev['VCSHA']=0.
        
        stateprev['deltaH']=0
        stateprev['cumulHsc']=0 #la chaleur cumul�e d�gag�e par les r�actions chimique, en kJ/kg de ciment.
        stateprev['derivHsc']=0
        
        #calcul de la capacit� calorifique:
        cpt=0
        for molec in stateprev['compo']:
            cpt+=stateprev['compo'][molec]*cp[molec]
                   
        stateprev['cpt']=cpt  #J/cm3
        #il faut passer au volume de b�ton consid�r�.
        fracls,vpate=self.fraclargescale()

        cpt=cpt*vpate*1000./1000.  #kJ/K
       
        masse=self.massc*(1+self.wsc) #kg
        #ajout des aggregats
        for i in self.aggregate:
            cpt+=self.aggregate[i]['mass']*self.aggregate[i]['capa']
            masse+=self.aggregate[i]['mass']
        
        
        stateprev['cpt_mass_beton']=cpt/masse #kJ/kg/K
        
        stateprev['wCH']=0
        stateprev['wb']=0
        
        stateprev['Tcsh']=0
        stateprev['Tcshp']=0
        
        stateprev['phic']=stateprev['phi_cap']
        stateprev['phicw']=stateprev['phi_cap']
        
        return stateprev
    
    def run(self,times):
        '''
        runs the hydration model
        :param times: the time steps
        :type times: a list of float
        
        :returns: the state (a dictionnary) on each time step.
        '''
        res={}
        stateprev=self.initialize()
        
        res[0]=stateprev
        i=0
        for t in times:
            if t>0:
                i=i+1
                stateprev=self.iter(stateprev,t)
                #print self.getrhoact(stateprev)
                res[i]=stateprev
        return res
     
    def printXls(self,filename):
        '''
        Prints information on the cement paste and concrete in a .xls file
        
        :param filename: the name of the file
        :type filename: a string
        
        
        '''
        classeur = Workbook()
    
        feuille = classeur.add_sheet("input")
    
        #header
        feuille.write(0, 0, "input")
        
        
        feuille.write(2, 0, "binder+filler")
        feuille.write(3, 0, "mass");feuille.write(3, 1, "kg");feuille.write(3, 2, self.massc+self.aggregate['filler']['mass'])
        feuille.write(4, 0, "water/(binder+filler)");feuille.write(4, 1, "");feuille.write(4, 2, self.wsc*self.massc/(self.massc+self.aggregate['filler']['mass']))
        feuille.write(6, 0, "Bogue composition, mass fraction")
        i=7
        for esp in self.binder.weightfraction:
            feuille.write(i, 1, esp);feuille.write(i, 2, self.binder.weightfraction[esp])
            i+=1
        feuille.write(i, 1, "filler");feuille.write(i, 2, self.aggregate["filler"]["mass"]/(self.aggregate["filler"]["mass"]+self.massc))
        i+=2
        feuille.write(i, 0, "Aggregates")
        i+=1
        feuille.write(i, 1, "name");feuille.write(i, 2, "mass,kg");feuille.write(i, 3, "density");feuille.write(i, 4, "Cp,kJ/kg/K")
        i+=1
        for agg in self.aggregate:
            feuille.write(i, 1, agg);feuille.write(i, 2, self.aggregate[agg]['mass']);feuille.write(i, 3, self.aggregate[agg]['density']);feuille.write(i, 4, self.aggregate[agg]['capa'])
            i+=1
        i+=1 
        feuille.write(i, 0, "binder");i+=1
        feuille.write(i, 0, "density");feuille.write(i, 1, "");feuille.write(i, 2, self.binder.getrho());i+=1
        feuille.write(i, 0, "effective mass of binder");feuille.write(i, 1, "kg");feuille.write(i, 2, self.massc);i+=1
        feuille.write(i, 0, "effective water/binder");feuille.write(i, 1, "");feuille.write(i, 2, self.wsc);i+=1
        
        i+=1
        feuille.write(i, 0, "volume fractions");i+=1
        fracvol,vpaste=self.fraclargescale()
        for eps in fracvol:
            feuille.write(i, 1, eps);feuille.write(i, 2, fracvol[eps]);i+=1
        i+=1
        feuille.write(i, 0, "volume of paste (water+binder), no filler");feuille.write(i, 1, "L");feuille.write(i, 2, vpaste);i+=1
        
        
        classeur.save(filename)
        return
        
if __name__ == '__main__':
    '''
    the main
    '''
    np.seterr(invalid='raise')
    
    for m in d_molec:
        print("M[MOLEC_"+m+"]="+str(round(d_molec[m]["M"],6))+";")
    for m in d_molec:
        print("RHO[MOLEC_"+m+"]="+str(round(d_molec[m]["M"]/d_molec[m]["v"],6))+";")
    for m in d_molec:
        print("V[MOLEC_"+m+"]="+str(round(d_molec[m]["v"],6))+";")
    for m in d_molec:
        print("HF[MOLEC_"+m+"]="+str(round(d_molec[m]["hf"],6))+";")
    for m in d_molec:
        print("CP[MOLEC_"+m+"]="+str(round(d_molec[m]["cp"],6))+";")
              
    for m in d_molec:
        print(m+"&"+str(round(d_molec[m]["M"],3))+"&"+str(round(d_molec[m]["M"]/d_molec[m]["v"],3))+"&"+str(round(d_molec[m]["v"],1))+"&"+str(d_molec[m]["hf"])+"&"+str(d_molec[m]["cp"]))
    
    print("reac")
    for r in d_reac:
        print(r+"&"+str(int(round(d_reac[r].dv,0)))+"&"+str(int(round(-d_reac[r].dvs,0)))+"&"+str(int(round(d_reac[r].heat,0)))+"&"+str(int(round(d_reac[r].cp,0))))
    
    print("phiw(1e-5,50%) ",cookDiam2poro(1e-5,50.))
    print("phiw(1e-6,50%) ",cookDiam2poro(1e-6,50.))
    print("phiw(1e-7,50%) ",cookDiam2poro(1e-7,50.))
    
    print("diam(49%,50%)", cookPoro2diam(49., 50.))
    #cm=Hydrationmodel(64,9.27,8.35,8.35,7.24,2.78,0.3,375)
    
    #composition moyenne d'apres Waller
    
    #cm=Hydrationmodel(65,20,7,4,4,0,0.5,375)
    #cm=Hydrationmodel(65,20,7,4,4,100-65-20-7-4-4,0.5,375)
    
    # Waller ca55
    #cm=Hydrationmodel(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.50,397)
    #cm.massc=0.36
    #cm.updatefiller()
    
    #cm=Nguyen2009(0,0,0,34,66,0,0.4,375)
    #cm=Nguyen2009(100,0,0,0,0,0,0.5,375)
    
    # ajout de 1.4 kg de sable, de densit� 2.65 et de capacit� calorifique 0.8kJ/kg
    #cm.addaggregate("sable",1.080,2.65,0.8)
    
    # Waller ca30
    #cm=Hydrationmodel(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.3,397)
    #cm.massc=530
    #cm.updatefiller()
    #cm.addaggregate("calcaires_Gb",701,2.678,0.84)    #silicieux=0.73 J/K/g
    #cm.addaggregate("calcaires_gb",468,2.672,0.84)
    #cm.addaggregate("calcaires_sb",580,2.716,0.84)
    
    # Waller ca35
    #cm=Hydrationmodel(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.35,397)
    #cm.massc=455
    #cm.updatefiller()
    #cm.addaggregate("calcaires_Gb",729,2.678,0.84)    #silicieux=0.73 J/K/g
    #cm.addaggregate("calcaires_gb",485,2.672,0.84)
    #cm.addaggregate("calcaires_sb",607,2.716,0.84)
    
    # Waller ca45
    #cm=Hydrationmodel(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.45,397)
    #cm.massc=438
    #cm.updatefiller()
    #cm.addaggregate("calcaires_Gb",695,2.678,0.84)    #silicieux=0.73 J/K/g
    #cm.addaggregate("calcaires_gb",463,2.672,0.84)
    #cm.addaggregate("calcaires_sb",574,2.716,0.84)
    
    # Waller ca55
    #cm=Nguyen2009(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.55,397)
    
    #cm=Hydrationmodel(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.55,397)

    binder=Binder()
    #binder.addbinderBogue(100,{'C3S':57.9,'C2S':15., 'C3A':7.7, 'C4AF':8.5,'CSbH2':5.3}, 397)
    #binder.addbinderBogue(95,{'C3S':57.9,'C2S':15., 'C3A':7.7, 'C4AF':8.5,'CSbH2':5.3}, 397)
    #binder.addbinderBogue(100,{'C3S':57.9,'C2S':15., 'C3A':7.7, 'C4AF':8.5,'CSbH2':5.3}, 400)
    #binder.addbinderBogue(100,{'C3S':57.9,'C2S':15., 'C3A':7.7, 'C4AF':8.5,'CSbH2':3.3}, 400)
    #binder.addbinderBogue(100,{'C3S':61.,'C2S':15., 'C3A':6., 'C4AF':10.,'CSb':4.}, 400)
    #binder.addbinderBogue(100,{'C3S':33.5,'C2S':53.6, 'C3A':2.3, 'C4AF':6.,'CSb':1.4}, 350)
    #binder.addbinderBogue(90,{'C3S':57.9,'C2S':15., 'C3A':7.7, 'C4AF':8.5,'CSbH2':5.3}, 397)
    #B11 : CPJ45 Airvault
    #binder.addbinderBogue(100,{'C3S':63.6,'C2S':9.4, 'C3A':6.7, 'C4AF':8.8,'CSb':3.5,'CCb':2.7}, 380)
    
    #BHP :266kg CPJ45 Airvault, 40,3 fumée silice, 57 filler calcaires
    #eau 161
    
    binder.addbinderBogue(100*266./(266.+40.3+57.),{'C3S':63.6,'C2S':9.4, 'C3A':6.7, 'C4AF':8.8,'CSb':3.5,'CCb':2.7}, 380.)
    binder.addbinderBogue(100*57./(266.+40.3+57.),{'CCb':100.}, 380.)
    binder.addbinderBogue(100*40.3/(266.+40.3+57.),{'SS':90.}, 2000.)
    
    #binder.addbinderBogue(10,{'SS':90}, 21000)
    #binder.addbinderBogue(10,{'SS':90}, 2100)
    #binder.addbinderBogue(25,{'SS':55,'A':15}, 400)
    print(binder)
    
    #cm=Hydrationmodel(binder,161./(266.+40.3+57.))
    cm=Hydrationmodel(binder,0.4)
    #cm=Hydrationmodel(binder,0.4)
    #cm=Hydrationmodel(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.42,397,silice=0,alumine=0,calcite=10)
    cm.massc=0.5
    cm.updatefiller()
    #print "fineness "+str(cm.binder.blaine)
    
    cm.addaggregate("calcaires_Gb",1.5,2.678,0.84)    #silicieux=0.73 J/K/g
    #cm.addaggregate("calcaires_gb",497,2.672,0.84)
    #cm.addaggregate("calcaires_sb",616,2.716,0.84)
    
    #cm.setEntrainedAir(0.05)
    print(cm.aggregate)
    
    cm.calo.setsemiadiabatic(70, 0.236, 20)
    #cm.calo.setisotherm(20)
    
    
    #ca30
    bogue_ca={'C3S':58.0,'C2S':15., 'C3A':7.7, 'C4AF':8.5,'CSb':4.2}
    binder=Binder()
    binder.addbinderBogue(100,bogue_ca, 397)
    cm=Hydrationmodel(binder,0.45)
    cm.massc=530
    cm.updatefiller()
    cm.setEntrainedAir(0.0)
    cm.addaggregate("calcaires_Gb",701,2.678,0.84)    #silicieux=0.73 J/K/g
    cm.addaggregate("calcaires_gb",468,2.672,0.84)
    cm.addaggregate("calcaires_sb",580,2.716,0.84)
    cm.calo.setisotherm(40)
    #res=cm.run(T)
    
    # Waller ca65
    #cm=Nguyen2009(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.65,397)
    #cm.massc=275
    #cm.updatefiller()
    #cm.addaggregate("calcaires_Gb",772,2.678,0.84)    #silicieux=0.73 J/K/g
    #cm.addaggregate("calcaires_gb",509,2.672,0.84)
    #cm.addaggregate("calcaires_sb",633,2.716,0.84)
    
    # Waller ca45fsa10
    #cm=Hydrationmodel(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.45,397)
    #cm.massc=344
    #cm.updatefiller()
    #cm.addaggregate("calcaires_Gb",755,2.678,0.84)    #silicieux=0.73 J/K/g
    #cm.addaggregate("calcaires_gb",504,2.672,0.84)
    #cm.addaggregate("calcaires_sb",625,2.716,0.84)
    #cm.addsilicafume(0.1*cm.massc, 0.914, 1940)
    
    # Waller ca45fsa20
    #cm=Hydrationmodel(57.9,15,7.7,8.5,5.3,(100-57.9-15-7.7-8.5-5.3),0.45,397)
    #cm.massc=323
    #cm.updatefiller()
    #cm.addaggregate("calcaires_Gb",751,2.678,0.84)    #silicieux=0.73 J/K/g
    #cm.addaggregate("calcaires_gb",501,2.672,0.84)
    #cm.addaggregate("calcaires_sb",622,2.716,0.84)
    #cm.addsilicafume(0.2*cm.massc, 0.914, 1940)
    
    #C3A
    
    #bogue_ca={'C3S':65.,'C2S':20., 'C3A':7., 'C4AF':4.,'CSb':4.}
    #bogue_fill={'CCb':90.}
    ciment={'C3S':65/1.046,'C2S':11/1.046, 'C3A':11/1.046, 'C4AF':8/1.046,'CSbH2':4.6/1.046,'CCb':3.5/1.046} #Beffes CEM I 52,5 N CE CP2 NF , XRD
    sf={'SS':0.9*95}
    

    
    binder=Binder()
    binder.addbinderBogue(100,ciment, 380.)
    #binder.addbinderBogue(10,sf, 2000.)
    cm=Hydrationmodel(binder,0.3)
    #cm.saturated=1
    cm.massc=350
    cm.updatefiller()
    cm.setEntrainedAir(0.0)
    cm.addaggregate("calcaires_Gb",701,2.678,0.84)    #silicieux=0.73 J/K/g
    cm.addaggregate("calcaires_gb",468,2.672,0.84)
    cm.addaggregate("calcaires_sb",580,2.716,0.84)
    cm.calo.setisotherm(20)
    
    
    slag={'SS':20.,'A':10.}
    ciment={'C3S':64.8,'C2S':16.6, 'C3A':4.04, 'C4AF':5.6,'CSbH2':4.8,'CCb':3.9} 
    
    binder=Binder()
    binder.addbinderBogue(100.,ciment, 380.)
    #binder.addbinderBogue(40.,sf, 400.)
    cm=Hydrationmodel(binder,0.45)
    #cm.saturated=1
    cm.massc=350
    cm.updatefiller()
    cm.setEntrainedAir(0.0)
    cm.addaggregate("calcaires_Gb",701,2.678,0.84)    #silicieux=0.73 J/K/g
    cm.addaggregate("calcaires_gb",468,2.672,0.84)
    cm.addaggregate("calcaires_sb",580,2.716,0.84)
    cm.calo.setisotherm(20)
    # 
    #cm.dessicator.tcure=7.
    #cm.dessicator.rhext=1.0
    #cm.dessicator.depth=0.001
    
    tfin=365#*60
    n=2000
    T=[0.]+logspace(log10(0.01),log10(tfin),n).tolist()
    #T=[0.]+np.linspace(0.01,tfin,n).tolist()
    
    res=cm.run(T)
    
    cm.printXls("hydrationDIM_CTOA_in.xls")
    printXls(res, "hydrationDIM_CTOA.xls")
    timesl=[]
    alphal=[]
    temperaturel=[]
    phil=[]
    waterfilledphil=[]
    enthalpypercl=[]
    moisturel=[]
    
    cumulHscl=[]
    derivHscl=[]
    Cpt=[]
    
    fillbetweenC=[]
    fillbetweenSS=[]
    fillbetweenA=[]
    fillbetweenCC=[]
    fillbetweenG=[]
    fillbetweenAFTAFM=[]
    fillbetweenCH=[]
    fillbetweenCSHHD=[]
    fillbetweenCSHLD=[]
    
    fillbetweenCSH=[]
    fillbetweenH=[]
    
    fillbetweenbigcapillaryvoids=[]
    
    for i in res:
        #print str(res[i]['time'])+' : '+str(res[i]['phi_cap'])
        timesl.append(res[i]['time'])
        alphal.append(res[i]['alpham'])
        temperaturel.append(res[i]['temperature'])
        phil.append(res[i]['phi_cap'])
        waterfilledphil.append(res[i]['phi_cap']+3*res[i]['eps_ch'])
        moisturel.append(res[i]['moisture'])
        cumulHscl.append(-res[i]['cumulHsc'])
        derivHscl.append(-res[i]['derivHsc'])
        Cpt.append(res[i]['cpt_mass_beton'])
        
        fillbetweenC.append(res[i]['fracvol']['anhydre'])
        fillbetweenSS.append(fillbetweenC[i]+res[i]['fracvol']['SS'])
        fillbetweenA.append(fillbetweenSS[i]+res[i]['fracvol']['A'])
        fillbetweenCC.append(fillbetweenA[i]+res[i]['fracvol']['CCb'])
        fillbetweenG.append(fillbetweenCC[i]+res[i]['fracvol']['CSbH2'])
        fillbetweenAFTAFM.append(fillbetweenG[i]+res[i]['fracvol']['C6ASb3H32']+res[i]['fracvol']['C4ASbH12']+res[i]['fracvol']['C3AH6']+res[i]['fracvol']['FH3']+res[i]['fracvol']['C4ACb11H']+res[i]['fracvol']['C3AFSH4'])
        fillbetweenCH.append(fillbetweenAFTAFM[i]+res[i]['fracvol']['CH'])
        
        fillbetweenCSH.append(1.-res[i]['phi_cap'])
        fillbetweenH.append(fillbetweenCSH[i]+np.max((0,res[i]['compo']['H']*v['H']))) # res[i]['phi_cap']+3*res[i]['eps_ch'])
        
        fillbetweenCSHHD.append(fillbetweenCH[i]+res[i]['fracvol']['CSHHD'])
        fillbetweenCSHLD.append(fillbetweenCSHHD[i]+res[i]['fracvol']['CSHLD']+res[i]['fracvol']['CSHLP'])
        fillbetweenbigcapillaryvoids.append(fillbetweenCSHLD[i]+res[i]['fracvol']['bigcapillaryvoids'])
        
    
    #outfile=open("save_cement05_dqdt.p","wb")
    #pickle.dump(derivHscl,outfile)
    #outfile.close()
    
    #outfile=open("save_cement05_temp2.p","wb")
    #pickle.dump(temperaturel,outfile)
    #outfile.close()
    
    plt.subplot(5,2,1)
    plt.title("volume fraction VS t")
    plt.fill_between(timesl, 0,fillbetweenC , facecolor='red', interpolate=True)
    plt.fill_between(timesl, fillbetweenC,fillbetweenSS , facecolor='magenta', interpolate=True)
    plt.fill_between(timesl, fillbetweenSS,fillbetweenA , facecolor='cyan', interpolate=True)
    plt.fill_between(timesl, fillbetweenA,fillbetweenCC , facecolor='white', interpolate=True)
    plt.fill_between(timesl, fillbetweenCC,fillbetweenG , facecolor='orange', interpolate=True)
    plt.fill_between(timesl, fillbetweenG ,fillbetweenAFTAFM , facecolor='yellow', interpolate=True)
    plt.fill_between(timesl, fillbetweenAFTAFM ,fillbetweenCH , facecolor='white', interpolate=True)
    plt.fill_between(timesl, fillbetweenCH ,fillbetweenCSH , facecolor='black', interpolate=True)
    plt.fill_between(timesl, fillbetweenCSH ,fillbetweenH , facecolor='blue', interpolate=True)
    #plt.fill_between(timesl, fillbetweenCSHHD ,fillbetweenCSHLD , facecolor='grey', interpolate=True)
    #plt.fill_between(timesl, fillbetweenCSHLD ,fillbetweenbigcapillaryvoids , facecolor='blue', interpolate=True)
    plt.xlim([0.,tfin])
    
    plt.subplot(5,2,2)
    plt.title("volume fraction VS t")
    plt.fill_between(timesl, 0,fillbetweenC , facecolor='red', interpolate=True)
    plt.fill_between(timesl, fillbetweenC,fillbetweenSS , facecolor='magenta', interpolate=True)
    plt.fill_between(timesl, fillbetweenSS,fillbetweenA , facecolor='cyan', interpolate=True)
    plt.fill_between(timesl, fillbetweenA,fillbetweenCC , facecolor='white', interpolate=True)
    plt.fill_between(timesl, fillbetweenCC,fillbetweenG , facecolor='orange', interpolate=True)
    plt.fill_between(timesl, fillbetweenG ,fillbetweenAFTAFM , facecolor='yellow', interpolate=True)
    plt.fill_between(timesl, fillbetweenAFTAFM ,fillbetweenCH , facecolor='white', interpolate=True)
    plt.fill_between(timesl, fillbetweenCH ,fillbetweenCSHHD , facecolor='black', interpolate=True)
    plt.fill_between(timesl, fillbetweenCSHHD ,fillbetweenCSHLD , facecolor='grey', interpolate=True)
    plt.fill_between(timesl, fillbetweenCSHLD ,fillbetweenbigcapillaryvoids , facecolor='blue', interpolate=True)
    plt.xlim([0.,2*24./24.])
    
    plt.subplot(5,2,3)
    plt.title("Capillary porosity VS t")
    plt.plot(timesl,phil)
    plt.fill_between(timesl, 0 ,waterfilledphil , facecolor='blue', interpolate=True)
    #plt.xlim([0.,130./24.])
    plt.xlim([0.,tfin])
    
    plt.subplot(5,2,4)
    plt.title("Capillary porosity VS t")
    plt.plot(timesl,phil)
    plt.fill_between(timesl, 0 ,waterfilledphil , facecolor='blue', interpolate=True)
    #plt.xlim([0.,130./24.])
    plt.xlim([0.,48./24.])
    
    plt.subplot(5,2,5)
    plt.title("moisture content VS t")
    plt.plot(timesl,moisturel)
    #plt.xlim([0.,130./24.])
    plt.xlim([0.,tfin])
    
    plt.subplot(5,2,6)
    plt.title("moisture content VS t")
    plt.plot(timesl,moisturel)
    #plt.xlim([0.,130./24.])
    plt.xlim([0.,48./24.])
    
    
    plt.subplot(5,2,7)
    plt.title("temperature VS t")
    plt.plot(timesl,temperaturel)
    #plt.xlim([0.,130./24.])
    plt.xlim([0.,tfin])
    
    plt.subplot(5,2,8)
    plt.title("temperature VS t")
    plt.plot(timesl,temperaturel)
    #plt.xlim([0.,130./24.])
    plt.xlim([0.,48./24.])
    
    plt.subplot(5,2,9)
    plt.title("Q/c (kJ/kg) VS t")
    plt.plot(timesl,cumulHscl)
    #plt.xlim([0.,130./24.])
    plt.xlim([0.,tfin])
    
    plt.subplot(5,2,10)
    plt.title("Q/c (kJ/kg) VS t")
    plt.plot(timesl,cumulHscl)
    #plt.xlim([0.,130./24.])
    plt.xlim([0.,48./24.])
    
    plt.savefig("cement.pdf")
    plt.show()
    
    '''
    infile=open("save_cement05_dqdt.p","rb")
    derivHscl2=pickle.load(infile)
    infile.close()
    
    infile=open("save_cement05_temp.p","rb")
    temperaturel2=pickle.load(infile)
    infile.close()
    
    infile=open("save_cement05_temp2.p","rb")
    temperaturel3=pickle.load(infile)
    infile.close()
    '''
    
    '''
    plt.title("d(Q/c)/dt (kJ/kg)/d VS t")
    plt.plot(timesl,derivHscl, label='C$=10')
    plt.plot(timesl,derivHscl2, label='C$=5.3')
    plt.xlim([0.,1.])
    plt.show()
    
    plt.title("Cp concrete (kJ/kg)/K VS t")
    plt.plot(timesl,Cpt)
    plt.xlim([0.,tfin])
    plt.show()
    '''
    
    plt.title("volume fraction VS t")
    plt.fill_between(timesl, 0,fillbetweenC , facecolor='red', interpolate=True)
    plt.fill_between(timesl, fillbetweenC,fillbetweenSS , facecolor='magenta', interpolate=True)
    plt.fill_between(timesl, fillbetweenSS,fillbetweenG , facecolor='orange', interpolate=True)
    plt.fill_between(timesl, fillbetweenG ,fillbetweenAFTAFM , facecolor='yellow', interpolate=True)
    plt.fill_between(timesl, fillbetweenAFTAFM ,fillbetweenCH , facecolor='white', interpolate=True)
    plt.fill_between(timesl, fillbetweenCH ,fillbetweenCSHHD , facecolor='black', interpolate=True)
    plt.fill_between(timesl, fillbetweenCSHHD ,fillbetweenCSHLD , facecolor='grey', interpolate=True)
    plt.fill_between(timesl, fillbetweenCSHLD ,fillbetweenbigcapillaryvoids , facecolor='blue', interpolate=True)
    plt.xlim([0.,5*24./24.])
    plt.ylim([0.,1.])
    plt.savefig("cement5j.pdf")
    
    plt.clf()
    
    
    #plt.title("volume fraction VS t")
    plt.fill_between(timesl, 0,fillbetweenC , facecolor='red', interpolate=True)
    plt.fill_between(timesl, fillbetweenC,fillbetweenSS , facecolor='magenta', interpolate=True)
    plt.fill_between(timesl, fillbetweenSS,fillbetweenG , facecolor='orange', interpolate=True)
    plt.fill_between(timesl, fillbetweenG ,fillbetweenAFTAFM , facecolor='yellow', interpolate=True)
    plt.fill_between(timesl, fillbetweenAFTAFM ,fillbetweenCH , facecolor='white', interpolate=True)
    plt.fill_between(timesl, fillbetweenCH ,fillbetweenCSHHD , facecolor='black', interpolate=True)
    plt.fill_between(timesl, fillbetweenCSHHD ,fillbetweenCSHLD , facecolor='grey', interpolate=True)
    plt.fill_between(timesl, fillbetweenCSHLD ,fillbetweenbigcapillaryvoids , facecolor='blue', interpolate=True)
    plt.xlim([0.,28*24./24.])
    plt.ylim([0.,1.])
    plt.ylabel('volume fraction', fontsize=18)
    plt.xlabel('t, days', fontsize=18)
    
    plt.savefig("cement28j.pdf")
    plt.clf()
    
    plt.fill_between(timesl, 0,fillbetweenC , facecolor='red',edgecolor="red", interpolate=True)
    plt.fill_between(timesl, fillbetweenC,fillbetweenSS , facecolor='magenta',edgecolor="magenta", interpolate=True)
    plt.fill_between(timesl, fillbetweenSS,fillbetweenA , facecolor='cyan',edgecolor="cyan", interpolate=True)
    plt.fill_between(timesl, fillbetweenA,fillbetweenCC , facecolor='white',edgecolor="white", interpolate=True)
    plt.fill_between(timesl, fillbetweenCC,fillbetweenG , facecolor='orange',edgecolor="orange", interpolate=True)
    plt.fill_between(timesl, fillbetweenG ,fillbetweenAFTAFM , facecolor='yellow',edgecolor="yellow", interpolate=True)
    plt.fill_between(timesl, fillbetweenAFTAFM ,fillbetweenCH , facecolor='white',edgecolor="white", interpolate=True)
    plt.fill_between(timesl, fillbetweenCH ,fillbetweenCSH , facecolor='black',edgecolor="black", interpolate=True)
    plt.fill_between(timesl, fillbetweenCSH ,fillbetweenH , facecolor='cyan',edgecolor="cyan", interpolate=True)
    plt.xlim([0.1,100.])
    plt.ylim([0.,1.])
    plt.ylabel('volume fraction', fontsize=18)
    plt.xlabel('t, days', fontsize=18)
    
    plt.xscale('log')
    plt.savefig("cement5j.pdf")
    plt.clf()
    
    fig, ax = plt.subplots()
    plt.fill_between(alphal, 0,fillbetweenC , facecolor='red',edgecolor="red", interpolate=True)
    plt.fill_between(alphal, fillbetweenC,fillbetweenSS , facecolor='magenta',edgecolor="magenta", interpolate=True)
    plt.fill_between(alphal, fillbetweenSS,fillbetweenA , facecolor='cyan',edgecolor="cyan", interpolate=True)
    plt.fill_between(alphal, fillbetweenA,fillbetweenCC , facecolor='white',edgecolor="white", interpolate=True)
    plt.fill_between(alphal, fillbetweenCC,fillbetweenG , facecolor='orange',edgecolor="orange", interpolate=True)
    plt.fill_between(alphal, fillbetweenG ,fillbetweenAFTAFM , facecolor='yellow',edgecolor="yellow", interpolate=True)
    plt.fill_between(alphal, fillbetweenAFTAFM ,fillbetweenCH , facecolor='white',edgecolor="white", interpolate=True)
    plt.fill_between(alphal, fillbetweenCH ,fillbetweenCSH , facecolor='black',edgecolor="black", interpolate=True)
    plt.fill_between(alphal, fillbetweenCSH ,fillbetweenH , facecolor='cyan',edgecolor="cyan", interpolate=True)
    
    plt.text(0.7,0.6,'C-S-H gel',color='white',fontsize=18)
    plt.text(0.7,0.35,'Portlandite',color='black',fontsize=18)
    plt.text(0.7,0.2,'Aft, Afm',color='black',fontsize=18)
    #plt.text(0.4,0.2,'silica fume',color='black',fontsize=18)
    
    plt.text(0.75,0.95,'air',color='black',fontsize=18)
    
    plt.text(0.1,0.7,'capillary water',color='black',fontsize=18)
    plt.text(0.1,0.1,'unhydrated cement',color='black',fontsize=18)
    
    ax.annotate('calcite', xy=(0.15, 0.30), xytext=(0.2, 0.18),color="white",size=18,fontsize=18, arrowprops=dict(facecolor='white', shrink=0.05),)
    ax.annotate('gypsum', xy=(0.05, 0.35), xytext=(0.17, 0.44),color="orange",size=18,fontsize=18, arrowprops=dict(facecolor='orange', shrink=0.05),)
    
    plt.xlim([0.,1.])
    plt.ylim([0.,1.])
    plt.ylabel('volume fraction', fontsize=18)
    plt.xlabel(r'$\alpha$', fontsize=22)
    
    for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(18) 
    for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(18) 
    
    fig.tight_layout()
    
    #plt.savefig("cement05.pdf")
    plt.show()
    plt.clf()
    
    fig, ax = plt.subplots()
    plt.fill_between(alphal, 0,fillbetweenC , facecolor='red',edgecolor="red", interpolate=True)
    plt.fill_between(alphal, fillbetweenC,fillbetweenSS , facecolor='magenta',edgecolor="magenta", interpolate=True)
    plt.fill_between(alphal, fillbetweenSS,fillbetweenA , facecolor='cyan',edgecolor="cyan", interpolate=True)
    plt.fill_between(alphal, fillbetweenA,fillbetweenCC , facecolor='white',edgecolor="white", interpolate=True)
    plt.fill_between(alphal, fillbetweenCC,fillbetweenG , facecolor='orange',edgecolor="orange", interpolate=True)
    plt.fill_between(alphal, fillbetweenG ,fillbetweenAFTAFM , facecolor='yellow',edgecolor="yellow", interpolate=True)
    plt.fill_between(alphal, fillbetweenAFTAFM ,fillbetweenCH , facecolor='white',edgecolor="white", interpolate=True)
    plt.fill_between(alphal, fillbetweenCH ,fillbetweenCSH , facecolor='black',edgecolor="black", interpolate=True)
    plt.fill_between(alphal, fillbetweenCSH ,fillbetweenH , facecolor='cyan',edgecolor="cyan", interpolate=True)
    
    plt.text(0.4,0.6,'C-S-H gel',color='white',fontsize=18)
    plt.text(0.4,0.45,'Portlandite',color='black',fontsize=18)
    plt.text(0.4,0.35,'Aft, Afm',color='black',fontsize=18)
    plt.text(0.4,0.2,'silica fume',color='black',fontsize=18)
    
    plt.text(0.55,0.95,'air',color='black',fontsize=18)
    
    plt.text(0.1,0.8,'capillary water',color='black',fontsize=18)
    plt.text(0.1,0.1,'unhydrated cement',color='black',fontsize=18)
    
    ax.annotate('calcite', xy=(0.15, 0.39), xytext=(0.2, 0.25),color="white",size=18,fontsize=18, arrowprops=dict(facecolor='white', shrink=0.05),)
    ax.annotate('gypsum', xy=(0.05, 0.43), xytext=(0.17, 0.55),color="orange",size=18,fontsize=18, arrowprops=dict(facecolor='orange', shrink=0.05),)
    
    plt.xlim([0.,1.])
    plt.ylim([0.,1.])
    plt.ylabel('volume fraction', fontsize=18)
    plt.xlabel(r'$\alpha$', fontsize=22)
    
    for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(18) 
    for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(18) 
    
    fig.tight_layout()
    plt.savefig("cement035fs10.pdf")
    plt.show()
    plt.clf()
    
    
    '''
    plt.title("temperature VS t")
    plt.plot(timesl,temperaturel)
    l1=plt.plot(timesl,temperaturel,'k--', label='Waller low C3A')
    l2=plt.plot(timesl,temperaturel2,'k-', label='Waller typ.')
    l2=plt.plot(timesl,temperaturel3,'k:', label='Waller ca')
    legend = plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    #plt.legend([l1,l2],['Waller ca','Waller typ.'])
    plt.xlim([0.,5*24./24.])
    plt.savefig("cement5j_temp.pdf")
    plt.clf()
   
   
    
    '''
    
    plt.title("d(Q/c)/dt (kJ/kg)/d VS t")
    l1=plt.plot(timesl,derivHscl, label='C$=10')
    #l2=plt.plot(timesl,derivHscl2, label='C$=5.3')
    #plt.legend([l1,l2],['C$=10','C$=5.3'])
    #plt.legend([l1],['C$=5.3'])
    
    #plt.plot(timesl,derivHscl)
    plt.xlim([0.,5*24./24.])
    plt.savefig("cement5j_dqsc.pdf")
    plt.show()
    plt.clf()