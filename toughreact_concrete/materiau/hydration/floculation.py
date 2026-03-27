#!/usr/bin/python
'''
Created on 24 avr. 2017

@author: francis.lavergne
'''
import matplotlib.pyplot as plt
import nlopt
import numpy as np

if __name__ == '__main__':
    from hydrationDIM_CTOA4 import *
else:
    from .hydrationDIM_CTOA4 import *


    
# les différentes espèces, avec leur masse volumique

z={}
z["Ca2+"]=2.
z["H+"]=1.
z["OH-"]=1.
z["Na+"]=1.
z["Na+"]=1.
z["K+"]=1.
z["SO_42-"]=1.
#z["SO_42-"]=1.


def getHamacker(rho):
    # modèle de Flatt 2004 pour des particules dans l'eau
    #retourne la constante de Hamacker en Joule
    h=0.3413*1e-20*(rho-1)*(rho-1)
    return h

def DebyeLength(I,T):
    # retourne la longeur de Debye k^-1, en metre
    # I : charge ionique, mol(e-)/m3
    # T temperature, en celcius
    
    Tk=T+273.
    kb=1.38064852e-23 #J.K^-1
    q=1.602e-19 # coulomb, A.s  ou  J.V^-1
    Na= 6.022140857e23 #mol^-1
    eps0=8.85418782e-12 # A^2.s^4.kg^-1.m^-3
    eps_reau=78.5 # permitivité relative
    
    return np.sqrt(kb*Tk*eps0*eps_reau/(2*q*q*Na*I))


def getlogK(react,T,P):    
    # donne le log10 de K pour la reaction, a une temperature en kelvin et une pression
    log10ksandard={"water":-13.99,"portlandite":-5.18,"gypsum":-4.58,"ettringite":-15.57}
    deltaHr={"water":55.836,"portlandite":-16.728,"gypsum":-1.13,"ettringite":164.2} #en kJ/mol
    deltaCpr={"water":-223.791,"portlandite":-342.49,"gypsum":-286.438,"ettringite":-228.18} #en J/mol/K
    deltaVr={"water":-23.36,"portlandite":-61.356,"gypsum":-41.753,"ettringite":-43.03} #en cm3/mol
    
    # le deltaHr(T) est affine...
    log10k=log10ksandard[react]+1./(log(10.)*8.314)*((deltaHr[react]*1e3-298.15*deltaCpr[react])*(1./298.15-1./(T))+deltaCpr[react]*log((T)/298.15)-deltaVr[react]/(T)*(P-0.1))
    #print "react ", react, " log10k",log10k
    return log10k

def IonicStength(concentrations):
    # concentrations : un dictionnaire des concentrations en mol/m3
    II=0
    for ion in concentrations:
        II=II+0.5*z[ion]*z[ion]*concentrations[ion]
    return II

def activity(II,species,T):
    '''
    retourne le gamma _i"
    
    concentration mol/m3
    II en mol/m3
    '''
    
    radius={"Nap":4e-10, "Kp":3.5e-10, "Hp":9.0e-10, "OHm":3.5e-10,"Capp":5e-10,"SO4mm":5e-10,"Clm":3.5e-10}
    bi={"Nap":0.075, "Kp":0.015, "Hp":0.0, "OHm":0.0,"Capp":0.165,"SO4mm":-0.04,"Clm":0.015}
    
    #Lothenbach :
    #bi={"Nap":0.064, "Kp":0.064, "Hp":0.064, "OHm":0.064,"Capp":0.064,"SO4mm":0.064}
    
    charge={"Nap":1., "Kp":1., "Hp":1, "OHm":-1.,"Capp":2.,"SO4mm":-2.,"Clm":-1.}
    Tk=T+273.
    kb=1.38064852e-23 #J.K^-1
    #Na= 6.022140857e23 #mol^-1
    q=1.602e-19 # coulomb, A.s  ou  J.V^-1
    eps0=8.85418782e-12 # A^2.s^4.kg^-1.m^-3
    eps_reau=78.5 # permitivité relative
    # calcul de la longueur de Debye
    kdb=1./DebyeLength(II,T)
    #print "Debye length, m "+str(1./kdb)
    # calcul des activités
    #extended debye huckel...
    denom=8*np.pi*eps_reau*eps0*kb*Tk
        
    return np.exp(-(charge[species]*charge[species]*q*q/denom)*kdb/(1.+kdb*radius[species])+bi[species]*II/1000.*np.log(10.))
        

def BrouwersEijk(mNasc,mKsc, phi, alpha,esc,sfsc, fillsc,T,gypsum,P=0.1,cClm=0.,cNap_add=0.):
    # mNasc : masse de Na dans le ciment
    # mKsc : masse de K dans le ciment
    #phi : porosité pleine d'eau
    # esc : rapprot esc
    # sfsc : fumee de silice, cendre volante, filler...
    #T : temperature
    #gypsum : boolean : is there some gypsum ?
    
    #T=25.

    Tk=T+273.
    kb=1.38064852e-23 #J.K^-1
    Na= 6.022140857e23 #mol^-1
    q=1.602e-19 # coulomb, A.s  ou  J.V^-1
    eps0=8.85418782e-12 # A^2.s^4.kg^-1.m^-3
    eps_reau=78.5 # permitivité relative
    
    #concetration en Na+ en mol/L
    cNap=(0.35+0.65*alpha)*(1-0.3/esc*alpha)*mNasc/(22.9898*phi*(esc/1000.+1./3150.+sfsc/2200.+fillsc/2650.))+cNap_add
    
    print("Na+ concentration, mol/L "+str(cNap))
    #concetration en K+ en mol/L
    cKp=(0.70+0.30*alpha)*(1-0.27/esc*alpha)*mKsc/(39.0983*phi*(esc/1000.+1./3150.+sfsc/2200.+fillsc/2650.))
    print("K+ concentration, mol/L "+str(cKp))
    II=3. #ionic strength, mol/m3
    # un algorithme de point fixe pour résoudre les concentrations
    for i in range (20):
        # calcul de la longueur de Debye
        kdb=1./DebyeLength(II,T)
        #print "Debye length, m "+str(1./kdb)
        # calcul des activités
        #extended debye huckel...
        denom=8*np.pi*eps_reau*eps0*kb*Tk
        '''
        gNap=np.exp(-(q*q/denom)*kdb/(1.+kdb*4e-10)+0.5085*0.3*II*q*q/1000.*np.log(10.))
        gKp=np.exp(-(q*q/denom)*kdb/(1.+kdb*3e-10)+0.5085*0.3*II*q*q/1000.*np.log(10.))
        gHp=np.exp(-(q*q/denom)*kdb/(1.+kdb*9e-10)+0.5085*0.3*II*q*q/1000.*np.log(10.))
        gOHm=np.exp(-(q*q/denom)*kdb/(1.+kdb*3.5e-10)+0.5085*0.3*II*q*q/1000.*np.log(10.))
        gCapp=np.exp(-(4*q*q/denom)*kdb/(1.+kdb*6e-10)+0.5085*0.3*II*4*q*q/1000.*np.log(10.))
        gSO4mm=np.exp(-(4*q*q/denom)*kdb/(1.+kdb*4e-10)+0.5085*0.3*II*4*q*q/1000.*np.log(10.))
        '''
        # source : https://wwwbrr.cr.usgs.gov/projects/GWC_chemtherm/pubs/wq4fdoc.pdf
        gNap=activity(II,"Nap",T)
        gKp=activity(II,"Kp",T)
        gHp=activity(II,"Hp",T)
        gOHm=activity(II,"OHm",T)
        gCapp=activity(II,"Capp",T)
        gSO4mm=activity(II,"SO4mm",T)
        #gClm=activity(II,"Clm",T)
        
        #print gNap,gKp,gHp,gOHm, gCapp,gSO4mm
        #calcul de la concentration en OHm
        # prise en compte de la temperature par l'équation de van hoff, voir  https://pdfs.semanticscholar.org/5d2a/7f201623c9d69d715a9117f0a6c363d5d20b.pdf
        #Kgyps=np.power(10,-4.58+(-17880./8.314*(1./298.-1./(Tk))))#*np.power(10,0.4)   #l'indice de saturation en gypse peut faire changer de signe le potentiel des sio2 !
        Kgyps=np.power(10,getlogK("gypsum",Tk,P))
        if gypsum ==False:
            #logKettringite=-45.0+(-204500./8.314*(1./298.-1./(Tk)))
            #logKmonosulphate=-29.43+(-45570./8.314*(1./298.-1./(Tk)))
            #Kgyps=np.power(10,(logKettringite-logKmonosulphate)*0.5)
            Kgyps=np.power(10,getlogK("ettringite",Tk,P)*0.5)
            
        #Kport=np.power(10,-5.18+(-460./8.314*(1./298.-1./(Tk))))*np.power(10,0.5)  # prise en compte d'un indice de saturation de 0.5
        Kwat=np.power(10,getlogK("water",Tk,P))
        Kport=np.power(10,getlogK("portlandite",Tk,P))*np.power(10,0.5)  # prise en compte d'un indice de saturation de 0.5
        p=np.zeros(5)
        p[4]=-2*Kport/(gCapp*gOHm*gOHm)
        p[3]=-Kwat/(gHp*gOHm)
        p[2]=-cKp-cNap+cClm
        p[1]=1
        p[0]=2*gOHm*gOHm*Kgyps/(gSO4mm*Kport)
        roots=np.roots(p)
        #print roots
        cOHm=np.real(np.max(roots))
        #print "OH- concentration, mol/L "+str(cOHm)
        
        
        #calcul des autres concentrations
        cCapp=-0.5*p[4]/(cOHm*cOHm)
        cHp=-p[3]/cOHm
        cSO4mm=0.5*p[0]*cOHm*cOHm
        
        #print "Ca2+ concentration, mol/L "+str(cCapp)
        #print "H+ concentration, mol/L "+str(cHp)
        #print "SO_42- concentration, mol/L "+str(cSO4mm)
        #print "charge",2*cCapp+cHp+cKp+cNap-cClm-cOHm-2*cSO4mm
        
        #mise à jour de la charge ionique, en mol/m3
        II=1e3*0.5*(4*cCapp+4*cSO4mm+cHp+cOHm+cNap+cKp+cClm)
        
    gHp=activity(II,"Hp",T)
    
    return {"cOHm":cOHm,"cHp":cHp,"cCapp":cCapp, "cSO4mm":cSO4mm, "cKp":cKp,"cNap":cNap,"cClm":cClm,"I":II,"kdb":kdb,"pH":-np.log10(cHp)-np.log10(gHp)}

def saturationIndex(poresolution,T,P=0.1):
    #calcul de la force ionique
    cCapp=poresolution["cCapp"]
    cHp=poresolution["cHp"]
    cOHm=poresolution["cOHm"]
    cNap=poresolution["cNap"]
    cKp=poresolution["cKp"]
    cSO4mm=poresolution["cSO4mm"]
    cClm=0.
    if "cClm" in poresolution.keys():
        cClm=poresolution["cClm"]
    II=1e3*0.5*(4*cCapp+4*cSO4mm+cHp+cOHm+cNap+cKp+cClm)
    
    #T=20.
    Tk=T+273.
    kb=1.38064852e-23 #J.K^-1
    Na= 6.022140857e23 #mol^-1
    q=1.602e-19 # coulomb, A.s  ou  J.V^-1
    eps0=8.85418782e-12 # A^2.s^4.kg^-1.m^-3
    eps_reau=78.5 # permitivité relative
    
    # calcul des activités
    kdb=1./DebyeLength(II,T)
        #print "Debye length, m "+str(1./kdb)
        # calcul des activités
    denom=8*np.pi*eps_reau*eps0*kb*Tk
    
    
    # source : https://wwwbrr.cr.usgs.gov/projects/GWC_chemtherm/pubs/wq4fdoc.pdf
    gNap=activity(II,"Nap",T)
    gKp=activity(II,"Kp",T)
    gHp=activity(II,"Hp",T)
    gOHm=activity(II,"OHm",T)
    gCapp=activity(II,"Capp",T)
    gSO4mm=activity(II,"SO4mm",T)
       
    
    ISport=(cCapp*gCapp*gOHm*gOHm*cOHm*cOHm)/np.power(10,getlogK("portlandite",Tk,P))
    ISgyps=(cCapp*gCapp*gSO4mm*cSO4mm)/np.power(10,getlogK("gypsum",Tk,P))
    ISett=np.power(cCapp*gCapp*gSO4mm*cSO4mm,2)/np.power(10,getlogK("ettringite",Tk,P))
    print("saturation index / portlandite", ISport, " log10 ",np.log10(ISport))
    print("saturation index / gypsum", ISgyps, " log10 ",np.log10(ISgyps))
    print("saturation index / ett", ISett, " log10 ",np.log10(ISett))
    poresolution["kdb"]=kdb
    poresolution["I"]=II
    return poresolution

def conductivity(poresolution):
    #chargeabs={"Nap":1., "Kp":1., "Hp":0, "OHm":1.,"Capp":2.,"SO4mm":2.}
    zlambda0={"cNap":50.1, "cKp":73.5, "cHp":0, "cOHm":198.,"cCapp":59.,"cSO4mm":79., "cClm":76.4} #cm2 S/mol
    G={"cNap":0.733, "cKp":0.548, "cHp":0, "cOHm":0.353,"cCapp":0.771,"cSO4mm":0.877, "cClm":0.548} #mol/l ^-1/2
    
    cond=0
    for i in poresolution.keys():
        if i in zlambda0.keys():
            cond+=zlambda0[i]*poresolution[i]/(1.+np.sqrt(poresolution["I"]*0.001)*G[i])
    poresolution["sigma"]=cond*0.1  #en Siemens/mètre si concentration en mol/L   
    return poresolution

def fout(phi,grad):
    
    return phi[0]*phi[0]

def ViallisTerrisse(poresolution,T):
    #dans le dictionnaire poresolution, les concentrations et la force ionique sont en mol/L.
    
    #T=25.

    Tk=T+273.
    kb=1.38064852e-23 #J.K^-1
    Na= 6.022140857e23 #mol^-1
    q=1.602e-19 # coulomb, A.s  ou  J.V^-1
    eps0=8.85418782e-12 # A^2.s^4.kg^-1.m^-3
    eps_reau=78.5 # permitivité relative
    
    kdb=poresolution["kdb"]
    II=poresolution["I"]
    #calcul de l'activité des différents ions, en mol/L
    denom=8*np.pi*eps_reau*eps0*kb*Tk
    aHp=poresolution["cHp"]*activity(II,"Hp",T)
    #aOHm=poresolution["cOHm"]*np.exp(-(q*q/denom)*kdb/(1.+kdb*9e-10))
    
    aNap=poresolution["cNap"]*activity(II,"Nap",T)
    aKp=poresolution["cKp"]*activity(II,"Kp",T)
    aCapp=poresolution["cCapp"]*activity(II,"Capp",T)
    
    phi0=0.0001
    def f(phi,grad):
                #calcul de nSiOH a l'aide du nombre de site.
        fact=np.exp(phi[0]*q/(kb*Tk))
        #nombre de site disponible par metre carré
        ns=2./41.*1e20
        K1=np.power(10,-12.3)
        K2=np.power(10,-9.4)
        K3=np.power(10,-12.1)
        nSiOH=ns/(1.+K1*fact/(aHp)+K2*aCapp/(aHp*fact)+K3*(aNap+aKp)/aHp)
        #calcul des different complexes
        
        nSiOm=nSiOH*K1*fact/(aHp)
        nSiOCap=nSiOH*K2*aCapp/(aHp*fact)
        nSiONa=nSiOH*K3*(aNap)/aHp
        nSiOK=nSiOH*K3*(aKp)/aHp
        
        #calcul du potentiel par la charge
        sigma=q*(nSiOCap-nSiOm)
        phir=sigma/(eps0*eps_reau*kdb)
        return (phi[0]-phir)*(phi[0]-phir)
    
    opt = nlopt.opt(nlopt.LN_COBYLA, 1)
    opt.set_lower_bounds([-1.])
    opt.set_upper_bounds([1.])
    opt.set_min_objective(f)
    opt.set_xtol_rel(1e-12)
    res = opt.optimize([phi0])
    minf = opt.last_optimum_value()
    phi0=res[0]
    #print "optimum at ", phi0
    #print "minimum value = ", minf
    
    '''
    for i in range(20):
        
        #calcul de nSiOH a l'aide du nombre de site.
        fact=np.exp(phi0*q/(kb*Tk))
        #nombre de site disponible par metre carré
        ns=2./41.*1e20
        K1=np.power(10,-12.3)
        K2=np.power(10,-9.4)
        K3=np.power(10,-12.1)
        nSiOH=ns/(1.+K1*fact/(aHp)+K2*aCapp/(aHp*fact)+K3*(aNap+aKp)/aHp)
        #calcul des different complexes
        
        nSiOm=nSiOH*K1*fact/(aHp)
        nSiOCap=nSiOH*K2*aCapp/(aHp*fact)
        nSiONa=nSiOH*K3*(aNap)/aHp
        nSiOK=nSiOH*K3*(aKp)/aHp
        
        #calcul du potentiel par la charge
        sigma=q*(nSiOCap-nSiOm)
        phi0=sigma/(eps0*eps_reau*kdb)
        print phi0
    '''
    
    fact=np.exp(phi0*q/(kb*Tk))
    #nombre de site disponible par metre carré
    ns=2./41.*1e20
    K1=np.power(10,-12.3)
    K2=np.power(10,-9.4)
    K3=np.power(10,-12.1)
    nSiOH=ns/(1.+K1*fact/(aHp)+K2*aCapp/(aHp*fact)+K3*(aNap+aKp)/aHp)
    #calcul des different complexes
        
    nSiOm=nSiOH*K1*fact/(aHp)
    nSiOCap=nSiOH*K2*aCapp/(aHp*fact)
    nSiONa=nSiOH*K3*(aNap)/aHp
    nSiOK=nSiOH*K3*(aKp)/aHp
    
    nbCa2p=nSiOCap*(4*3.14*2.1*2.1)*1e-18   #nombre d'atome de calcium à la surface
    nbCa2p_vol= 4*3.14/3.*(2.1*2.1*2.1)*1e-27*2.52*1e6* 5/ 730.958*6.022e23 #nombre d'atome dans le volume 1e6 : 
    nbCa2p_vol= 4*3.14/3.*(2.1*2.1*2.1)*1e-27*2.604*1e6* 0.366/40.08 *6.022e23 #nombre d'atome dans le volume 1e6 : 
    print("calcium adsorbed/calcium volume %f",nbCa2p/nbCa2p_vol)
    
    
    return phi0

def ViallisTerrisseCl(poresolution,T):
    #dans le dictionnaire poresolution, les concentrations et la force ionique sont en mol/L.
    
    #T=25.

    Tk=T+273.
    kb=1.38064852e-23 #J.K^-1
    Na= 6.022140857e23 #mol^-1
    q=1.602e-19 # coulomb, A.s  ou  J.V^-1
    eps0=8.85418782e-12 # A^2.s^4.kg^-1.m^-3
    eps_reau=78.5 # permitivité relative
    
    kdb=poresolution["kdb"]
    II=poresolution["I"]
    #calcul de l'activité des différents ions, en mol/L
    denom=8*np.pi*eps_reau*eps0*kb*Tk
    aHp=poresolution["cHp"]*activity(II,"Hp",T)
    #aOHm=poresolution["cOHm"]*np.exp(-(q*q/denom)*kdb/(1.+kdb*9e-10))
    
    aNap=poresolution["cNap"]*activity(II,"Nap",T)
    aKp=poresolution["cKp"]*activity(II,"Kp",T)
    aCapp=poresolution["cCapp"]*activity(II,"Capp",T)
    aClm=poresolution["cClm"]*activity(II,"Clm",T)
    phi0=0.0001
    def f(phi,grad):
                #calcul de nSiOH a l'aide du nombre de site.
        fact=np.exp(phi[0]*q/(kb*Tk))
        #nombre de site disponible par metre carré
        ns=2./41.*1e20
        K1=np.power(10,-12.3)
        K2=np.power(10,-9.4)
        K3=np.power(10,-12.1)
        K4=np.power(10,-0.35)
        K5=np.power(10,-9.8)
        nSiOH=ns/(1.+K1*fact/(aHp)+K2*aCapp/(aHp*fact)+K3*(aNap+aKp)/aHp+K4*aClm*fact+K5*aCapp*aClm/aHp)
        #calcul des different complexes
        
        nSiOm=nSiOH*K1*fact/(aHp)
        nSiOCap=nSiOH*K2*aCapp/(aHp*fact)
        nSiONa=nSiOH*K3*(aNap)/aHp
        nSiOK=nSiOH*K3*(aKp)/aHp
        nSiOHClm=nSiOH*K4*aClm*fact
        nSiOCaCl=nSiOH*K5*aCapp*aClm/aHp
        
        #calcul du potentiel par la charge
        sigma=q*(nSiOCap-nSiOm-nSiOHClm)
        phir=sigma/(eps0*eps_reau*kdb)
        return (phi[0]-phir)*(phi[0]-phir)
    
    opt = nlopt.opt(nlopt.LN_COBYLA, 1)
    opt.set_lower_bounds([-1.])
    opt.set_upper_bounds([1.])
    opt.set_min_objective(f)
    opt.set_xtol_rel(1e-12)
    res = opt.optimize([phi0])
    minf = opt.last_optimum_value()
    phi0=res[0]
    #print "optimum at ", phi0
    #print "minimum value = ", minf
    
    '''
    for i in range(20):
        
        #calcul de nSiOH a l'aide du nombre de site.
        fact=np.exp(phi0*q/(kb*Tk))
        #nombre de site disponible par metre carré
        ns=2./41.*1e20
        K1=np.power(10,-12.3)
        K2=np.power(10,-9.4)
        K3=np.power(10,-12.1)
        nSiOH=ns/(1.+K1*fact/(aHp)+K2*aCapp/(aHp*fact)+K3*(aNap+aKp)/aHp)
        #calcul des different complexes
        
        nSiOm=nSiOH*K1*fact/(aHp)
        nSiOCap=nSiOH*K2*aCapp/(aHp*fact)
        nSiONa=nSiOH*K3*(aNap)/aHp
        nSiOK=nSiOH*K3*(aKp)/aHp
        
        #calcul du potentiel par la charge
        sigma=q*(nSiOCap-nSiOm)
        phi0=sigma/(eps0*eps_reau*kdb)
        print phi0
    '''
    
    fact=np.exp(phi0*q/(kb*Tk))
    #nombre de site disponible par metre carré
    ns=2./41.*1e20
    K1=np.power(10,-12.3)
    K2=np.power(10,-9.4)
    K3=np.power(10,-12.1)
    K4=np.power(10,-0.35)
    K5=np.power(10,-9.8)
    nSiOH=ns/(1.+K1*fact/(aHp)+K2*aCapp/(aHp*fact)+K3*(aNap+aKp)/aHp+K4*aClm*fact+K5*aCapp*aClm/aHp)
        #calcul des different complexes
        
    nSiOm=nSiOH*K1*fact/(aHp)
    nSiOCap=nSiOH*K2*aCapp/(aHp*fact)
    nSiONa=nSiOH*K3*(aNap)/aHp
    nSiOK=nSiOH*K3*(aKp)/aHp
    nSiOHClm=nSiOH*K4*aClm*fact
    nSiOCaCl=nSiOH*K5*aCapp*aClm/aHp
    '''
    nbCa2p=nSiOCap*(4*3.14*2.1*2.1)*1e-18   #nombre d'atome de calcium à la surface
    nbCa2p_vol= 4*3.14/3.*(2.1*2.1*2.1)*1e-27*2.52*1e6* 5/ 730.958*6.022e23 #nombre d'atome dans le volume 1e6 : 
    nbCa2p_vol= 4*3.14/3.*(2.1*2.1*2.1)*1e-27*2.604*1e6* 0.366/40.08 *6.022e23 #nombre d'atome dans le volume 1e6 : 
    print "calcium adsorbed/calcium volume) ",nbCa2p/nbCa2p_vol
    '''
    
    '''
    nSiOHClm is the number of SiOHClm complex per square meter of CSH surface.
    '''
    
    return phi0, nSiOHClm,nSiOCaCl

def Milonjic(poresolution,T):
    #dans le dictionnaire poresolution, les concentrations et la force ionique sont en mol/L.
    
    #T=25.

    Tk=T+273.
    kb=1.38064852e-23 #J.K^-1
    Na= 6.022140857e23 #mol^-1
    q=1.602e-19 # coulomb, A.s  ou  J.V^-1
    eps0=8.85418782e-12 # A^2.s^4.kg^-1.m^-3
    eps_reau=78.5 # permitivité relative
    
    kdb=poresolution["kdb"]
    II=poresolution["I"]
    #calcul de l'activité des différents ions, en mol/L
    denom=8*np.pi*eps_reau*eps0*kb*Tk
    aHp=poresolution["cHp"]*activity(II,"Hp",T)
    #aOHm=poresolution["cOHm"]*np.exp(-(q*q/denom)*kdb/(1.+kdb*9e-10))
    
    aNap=poresolution["cNap"]*activity(II,"Nap",T)
    aKp=poresolution["cKp"]*activity(II,"Kp",T)
    aCapp=poresolution["cCapp"]*activity(II,"Capp",T)
     
    phi0=0.0001
    def f(phi,grad):
                #calcul de nSiOH a l'aide du nombre de site.
        fact=np.exp(phi[0]*q/(kb*Tk))
        #nombre de site disponible par metre carré
        ns=7.85e18
        K1=np.power(10,-8.2)
        K2=np.power(10,-5.6)
        K3=np.power(10,-7.0)
        
        K1=np.power(10,-7.2)
        K2=np.power(10,-4.3)
        K3=np.power(10,-6.7)
        nSiOH=ns/(1.+K1*fact/(aHp)+K2*aCapp/(aHp*fact)+K3*(aNap+aKp)/aHp)
        #calcul des different complexes
        
        nSiOm=nSiOH*K1*fact/(aHp)
        nSiOCap=nSiOH*K2*aCapp/(aHp*fact)
        nSiONa=nSiOH*K3*(aNap)/aHp
        nSiOK=nSiOH*K3*(aKp)/aHp
        
        #calcul du potentiel par la charge
        sigma=q*(nSiOCap-nSiOm)
        phir=sigma/(eps0*eps_reau*kdb)
        return (phi[0]-phir)*(phi[0]-phir)
    
    opt = nlopt.opt(nlopt.LN_COBYLA, 1)
    opt.set_lower_bounds([-1.])
    opt.set_upper_bounds([1.])
    opt.set_min_objective(f)
    opt.set_xtol_rel(1e-12)
    res = opt.optimize([phi0])
    minf = opt.last_optimum_value()
    phi0=res[0]
    #print "optimum at ", phi0
    #print "minimum value = ", minf
    
    fact=np.exp(phi0*q/(kb*Tk))
    #nombre de site disponible par metre carré
    ns=7.85e18
    K1=np.power(10,-8.2)
    K2=np.power(10,-5.6)
    K3=np.power(10,-7.0)
    nSiOH=ns/(1.+K1*fact/(aHp)+K2*aCapp/(aHp*fact)+K3*(aNap+aKp)/aHp)
    nSiOCap=nSiOH*K2*aCapp/(aHp*fact)
    
    # controle avec Adsorption on silica surface eugène papirer, persello p310
    #print "number of adsorbed calcium"+str(nSiOCap*1e-18)
    
    return phi0

def vanDerWallsEnergy(H,delta,R1,R2):
        # H en Joule, distances en metres
        #retour en Joule
        denom=delta*delta+2*delta*(R1+R2)
        top=4*R1*R2
        return -H/12.*(top/denom+top/(denom+top)+2*np.log(denom/(denom+top)))
        
def electrostaticEnergy(kdb,delta,R1,R2,phi1,phi2):
    #kdb en m^-1
    #delta R1 R2 en m
    #phi1 phi2 en volt
    #return en Joule
    eps0=8.85418782e-12 # A^2.s^4.kg^-1.m^-3
    eps_reau=78.5 # permitivité relative
    front=np.pi*eps0*eps_reau*R1*R2/(R1+R2)
    return front*((phi1*phi1+phi2*phi2)*np.log(1-np.exp(-2.*kdb*delta))+2*phi1*phi2*np.log((1+np.exp(-kdb*delta))/(1-np.exp(-kdb*delta))))

def geti_alpham(alpham,res):
    i=0
    #print res[i]['time']
    while res[i]['alpham']<alpham:
        i=i+1
    return i

'''
Estimation de la viscosité dynamique
'''
def dynamicvisco(poresolution):
    #on retourne la viscosité dynamique
    
    eta=1.0
    #conductivité ionic molaire: S.cm2.mol-1
    lambda0={"cNap":50.1, "cKp":73.5, "cHp":349.6, "cOHm":199.1,"cCapp":119.,"cSO4mm":160.} #cm2 S/mol
    zi={"cNap":1., "cKp":1., "cHp":1., "cOHm":1.,"cCapp":2.,"cSO4mm":2.} #cm2 S/mol
    
    #mu_i
    mu_i={} #unitless
    somm=0.
    zsltop=0.
    zsldown=0.
    zslsqtop=0.
    
    for i in lambda0.keys():
        mu_i[i]=lambda0[i]*zi[i]*zi[i]*poresolution[i]
        somm+=mu_i[i]
        zsltop+=poresolution[i]*zi[i]*zi[i]*zi[i]/lambda0[i]
        zslsqtop+=poresolution[i]*zi[i]*zi[i]*zi[i]*zi[i]/(lambda0[i]*lambda0[i])
        zsldown+=poresolution[i]*zi[i]*zi[i]
    for i in lambda0.keys():
        mu_i[i]=mu_i[i]/somm
    zsl= zsltop/ zsldown 
    zslsq= zslsqtop/ zsldown
     
    r={}
    for i in lambda0.keys():
        r[i]=1-zi[i]/lambda0[i]/zsl
    
    # les binomiaux (1/2  p) font référence aux coefficients du DL de \sqrt{1+x}  
    nbit=6 
    c=np.zeros(nbit)
    binom=np.zeros(nbit)
    c[0]=-3.+np.sqrt(2.)
    binom[0]=1.
    summ=1.
    for i in range(nbit-1):
        binom[i+1]=binom[i]*(0.5-(i))/(i+1)
        
        c[i+1]=-2*np.sqrt(2)*(np.sqrt(2)-summ)
        summ+=binom[i+1]
    
    #construction des s
    s=[]
    si=np.zeros(6)
    ii=0
    for i in lambda0.keys():
        si[ii]=mu_i[i]*(zi[i]/lambda0[i]-zslsq/zsl)
        ii+=1
    s.append(np.copy(si))
    #construction de la matrice H
    H=np.zeros((6,6))
    ii=0
    for i in lambda0.keys():
        jj=0
        for j in lambda0.keys():
            H[ii][jj]+=2*mu_i[i]*lambda0[i]/zi[i]/(lambda0[i]/zi[i]+lambda0[j]/zi[j])
            H[ii][ii]+=2*mu_i[j]*lambda0[j]/zi[j]/(lambda0[i]/zi[i]+lambda0[j]/zi[j])
            jj+=1
        
        H[ii][ii]+=-1.

        ii+=1
    
    print(H)
    
    for i in range(nbit-1):
        si=H.dot(si)
        s.append(np.copy(si))
    
    st=np.zeros(6)
    for i in range(nbit):
        st=st+c[i]*s[i]
        
    eta1=0.
    eta2=0.
    ii=0
    for i in lambda0.keys():
        eta1+=mu_i[i]*zi[i]/lambda0[i]
        eta2+=-4*r[i]*st[ii]
        ii+=1
    
    print(r, st)
    eta=eta1+eta2
    
    print(eta1, eta2, eta)
    epsilonr=78.4
    #epsilon0=8.854187817e-12
    T=298.
    
    #calcul de la force ionique
    cCapp=poresolution["cCapp"]
    cHp=poresolution["cHp"]
    cOHm=poresolution["cOHm"]
    cNap=poresolution["cNap"]
    cKp=poresolution["cKp"]
    cSO4mm=poresolution["cSO4mm"]
    II=0.5*(4*cCapp+4*cSO4mm+cHp+cOHm+cNap+cKp)
    
    etaw= 8.90e-4
    #print eta
    eta=eta*0.36454*np.sqrt(2*II/(epsilonr*T))+ etaw
    
    # les coefficients B, voir Jenkins 1995
    eta+=poresolution["cCapp"]*0.284*etaw
    eta+=poresolution["cHp"]*0.068*etaw
    eta+=poresolution["cOHm"]*0.122*etaw
    eta+=poresolution["cNap"]*0.085*etaw
    eta+=poresolution["cKp"]*-0.009*etaw
    eta+=poresolution["cSO4mm"]*0.206*etaw
    
    return eta
# 
if __name__ == '__main__':
    
    saturationIndex({"cOHm":0.160,"cHp":0,"cCapp":0.023, "cSO4mm":0.123, "cKp":0.365,"cNap":0.023},T=20.)
    
    # appel au modèle d'hydratation
    #c11={'C3S':60.7,'C2S':18.7, 'C3A':2.8, 'C4AF':12.2,'CSb':3.0,'CCb':3.0}
   
    #c11={'C3S':61.,'C2S':18., 'C3A':3.9, 'C4AF':5.8,'CSb':2,'CCb':3.7}
    #c11={'C3S':61.,'C2S':18., 'C3A':3.9, 'C4AF':5.8,'CSb':1,'CCb':3.7}
    c11={'C3S':63.3,'C2S':9.6, 'C3A':10.6, 'C4AF':7.7,'CSb':3.8,'CCb':5.0}
    
    blaine=385.0
    esc=0.45
    #notre ciment
    mNa2Ocement=0.0016
    mK2Ocement=0.0097
    
    '''
    #Lothenbach
    c11={'C3S':61.,'C2S':18., 'C3A':3.9, 'C4AF':5.8,'CSb':3.6,'CCb':3.7}
    blaine=354.0
    esc=0.55
    #ciment Lothenbach
    mNa2Ocement=0.0013
    mK2Ocement=0.0022
    '''
    
    binder=Binder()
    binder.addbinderBogue(100,c11, blaine)
    #binder.getd0(npsd, binder.blaine)
    #cm=Hydrationmodel(binder,171./342.)
    cm=Hydrationmodel(binder,esc)
    cm.massc=342.
    cm.updatefiller()
    cm.setEntrainedAir(1.9)
    cm.addaggregate("sable",670.+1200.,2.65,0.84,75.,0.20)
    
    Temp=25.
    P=0.1
    print('rho concrete '+str(cm.getrho()))
    cm.calo.setisotherm(Temp)
    tfin=28
    n=2000
    T=[0.]+logspace(log10(0.01),log10(tfin),n).tolist()
    
    res=cm.run(T)
    
    distl=logspace(log10(1e-10),log10(100e-9),50).tolist()
    
    
    for alpham in [0.01,0.02,0.03,0.04,0.05,0.06,0.08,0.1,0.15,0.2,0.25,0.5,0.6]:
        # on trouve le temps qui correspond au degree d'hydratation massique
        j=geti_alpham(alpham,res)
        
        
        
        
        
        #truc de malade
        #mNa2Ocement=0.00
        #mK2Ocement=0.00
                  
        mNasc=2*22.9898/(61.97894)*mNa2Ocement
        mKsc=2*39.0983/(94.196)*mK2Ocement
        
        #mNasc=0.
        #mKsc=0.
        
        
        #mNasc=2*22.9898/(61.97894)*0.0005
        #mKsc=2*39.0983/(94.196)*0.002
        
        phi=res[j]['compo']['H']*v['H']+0.36*(res[j]['compo']['CSH']*v['CSH']+res[j]['compo']['CSHp']*v['CSHp'])# volume de la porosité totale en eau
        print("porosity %f",phi)
        #alpha=0.05
        sfsc=0
        fillsc=0
        
        
        poresolution= BrouwersEijk(mNasc,mKsc, phi, alpham,esc,sfsc, fillsc,Temp,res[j]['compo']['CSbH2']>0,P=P)
        poresolution=conductivity(poresolution)
        #poresolution=saturationIndex({"cOHm":0.160,"cHp":1e-14/0.160,"cCapp":0.023, "cSO4mm":0.123, "cKp":0.365,"cNap":0.023})
        print('alpham is %f', alpham, " real is %f", res[j]['alpham'], " at time %f", res[j]['time'])
        print('gypsum %F', res[j]['compo']['CSbH2'])
        print(poresolution)
        print("pH %f", poresolution["pH"])
        print("conductivity %f", poresolution["sigma"])
        print("dynamic viscosity %f", dynamicvisco(poresolution))
        
        phi0=ViallisTerrisse(poresolution,Temp)
        print("potential, CSH, V %f",phi0)
        
        phis=Milonjic(poresolution,Temp)
        print("potential, SiO2, V %f",phis)
        
        
        # affichage du potentiel entre deux particules de CSH
        #R=4.2e-9
        R=2.1e-9
        hamacker=getHamacker(2.604)
        #phi0=0.05
        wCSHl=[]
        for i in range(len(distl)):
            wCSH=vanDerWallsEnergy(hamacker,distl[i],R,R)+electrostaticEnergy(poresolution['kdb'],distl[i],R,R,phi0,phi0)
            wCSHl.append(wCSH)
        
        # affichage du potentiel entre deux particules de fumée de silice
        R=7e-8
        #R=5e-9
        hamacker=getHamacker(2.2)
        #phis=0.02
        wSiO2l=[]
        for i in range(len(distl)):
            wSiO2=vanDerWallsEnergy(hamacker,distl[i],R,R)+electrostaticEnergy(poresolution['kdb'],distl[i],R,R,phis,phis)
            wSiO2l.append(wSiO2)
        
        # affichage du potentiel entre deux particules de silice NS
        R=6e-9
        #R=5e-9
        hamacker=getHamacker(2.2)
        #phis=0.02
        wSiO2lNS=[]
        for i in range(len(distl)):
            wSiO2=vanDerWallsEnergy(hamacker,distl[i],R,R)+electrostaticEnergy(poresolution['kdb'],distl[i],R,R,phis,phis)
            wSiO2lNS.append(wSiO2)
                
            
        fig, ax = plt.subplots()
        plt.plot(distl,wSiO2l,'k',lw=4, color='red',label='silica fume, 100nm')
        plt.plot(distl,wSiO2lNS,'k',lw=4, color='green',label='NS, 12nm')
        plt.plot(distl,wCSHl,'k',lw=4, color='blue',label='C-S-H globule, 4.2nm')
        
        
        plt.text(1e-8,-1.5e-20,r'$\alpha$='+str(alpham),size=22,fontsize=22)
        
        plt.ylabel('interaction energy, J', fontsize=22)
        plt.xlabel('$\delta$, m', fontsize=22)
        legend = ax.legend(loc='lower right', shadow=True,fontsize=22)
        plt.ylim([-4e-20,0.5e-20])
        plt.xscale('log')
        
        for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(18) 
        for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(18) 
    
        fig.tight_layout()
    
        plt.savefig("interaction.pdf")
        plt.show()
        
        #ce qu'il faut pour le modèle de floculation
        # les paramètres d'entrée.
        V=1
        vCSHLD=0.022
        vCSHHD=0.013
        vanhydre=0.30
        vSS=0.0
        
        vanhydre0=0.32
        vSS0=0.0
    
    #il faut passer au nombre de particules via la surface spécifique
        
    
    
    '''
    # cadrage de la constante d'équiblre pour colloidal silica, Ca2+
    # solution à pH9.
    
    cCa=2e-8 # en mol/L
    cOHm=1e-14/1e-9     #cCa+np.sqrt(cCa*cCa+1e-14)
    cHp=1e-9      #1e-14/cOHm
    print (cOHm-cHp-2*cCa)
    II=1e3*0.5*(4*cCa+cHp+cOHm+(cOHm-cHp-2*cCa))
    kdb=1./DebyeLength(II,25.)
    poresolution={"cOHm":cOHm,"cHp":cHp,"cCapp":cCa, "cSO4mm":0, "cKp":0,"cNap":0,"I":II,"kdb":kdb}
    print -np.log10(cHp)
    Milonjic(poresolution)
    '''
    
    
    pass