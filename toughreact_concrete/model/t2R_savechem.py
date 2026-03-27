"""
Created on Tue Aug 26 07:59:35 2014

@author: thony
"""
from fixed_format_file import fortran_float


class t2rsavechem:
    def __init__(self,nb_block,nb_species,nb_minerals,toughreact_exe,pitzer,kinetic,complexation,filename='savechem'):
        self.nb_block = nb_block
        #self.species = species #liste des especes
        if complexation:
            self.nb_species = nb_species #+ 2#17 #nombre d'especes (+ complexation de surface)
        else:
            self.nb_species = nb_species
        self.nb_minerals = nb_minerals #liste des mineraux
        self.file = filename
        self.exe = toughreact_exe
        self.nb_lines_block = self.nb_lines_per_block()
        self.pitzer = pitzer
        self.kinetic = kinetic
        self.contenu = self.read_savechem()

#    def __getitem__(self,key):
#        if isinstance(key,(int,slice)): return self._blocklist[key]
#        elif isinstance(key,str): return self._block[key]
#        else: return None
#    def __setitem__(self,key,value):
#        if isinstance(value,(list,tuple)): value=t2rblocksavechem(value,key)
#        if value.block<>key: value.block=key
#        self.add_incon(value)

    def nb_lines_per_block(self):
        #Description du fichier savechem (en nombre de lignes)
        # "Geochemical state variables at restart time (s):"
        nb_line_geochemical_state = 1
        # "Concentration of primary and secondary species mol/kgw :"
        if self.nb_species%6 == 0:
            nb_line_concentration_primary = (self.nb_species//6)
        else:
            nb_line_concentration_primary = (self.nb_species//6+1)
        # "pH :"
        nb_line_pH = 1
        # "Concentration of secondary species mol/kgw :"
        nb_line_concentration_secondary = 0 #Calcul a effectuer (cf. fonction read)
        # "Water Activity :"
        nb_line_water_activity = 1
        # "Initial mineral amount mol/dm^3 :"
        if (self.nb_minerals+1)%4 == 0:
            nb_line_initial_mineral = ((self.nb_minerals+1)//4)
        else:
            nb_line_initial_mineral = ((self.nb_minerals+1)//4+1)
        # "Current mineral amount mol/dm^3 :"
        if self.nb_minerals%4 == 0:
            nb_line_current_mineral = (self.nb_minerals//4)
        else:
            nb_line_current_mineral = (self.nb_minerals//4+1)
        # "Residual Solute after Dryout moles/dm^3 :"
        if self.nb_species%6 == 0:
            nb_line_residual_solute = (self.nb_species//6)
        else:
            nb_line_residual_solute = (self.nb_species//6+1)
        # "UT   Concentration of primary species mol/L :"
        if self.nb_species%6 == 0:
            nb_line_UT_species = (self.nb_species//6)
        else:
            nb_line_UT_species = (self.nb_species//6+1)
        # "Initial porosity phi0 :"
        nb_line_porosity = 1
        # "Initial permeability perm0 m2 :"
        nb_line_permeability = 1
        return {'geochemical_state':nb_line_geochemical_state,\
        'concentration_primary':nb_line_concentration_primary,\
        'pH':nb_line_pH,'concentration_secondary':nb_line_concentration_secondary,\
        'water_activity':nb_line_water_activity,'initial_mineral':nb_line_initial_mineral,\
        'current_mineral':nb_line_current_mineral,'residual_solute':nb_line_residual_solute,\
        'UT_species':nb_line_UT_species,'porosity':nb_line_porosity,\
        'permeability':nb_line_permeability,'grains':nb_line_initial_mineral}
    
    def read_savechem(self):
        """Reads initial conditions from file."""
        infos = False
        f=open(self.file)
        line=f.readline()
        if infos == True:
            print(line)
        #Geochemical state variables at restart time (s):
        line=f.readline()
        tmp_line = line.split()
        geochemical_state = fortran_float(tmp_line[0])
        if infos == True:
            print(line)
        #Concentration of primary species mol/kgw :
        line=f.readline()
        line.split()
        if infos == True:
            print(line)
        concentration_primary=[]
        for i in range(self.nb_block):
            tmp = []
            for j in range(self.nb_lines_block['concentration_primary']):
                line=f.readline()
                tmp += [fortran_float(line[i:i+15]) for i in [0,15,30,45,60,75]]
            concentration_primary.append(tmp[0:self.nb_species])
        if infos == True:
            print(line)
        #pH :
        line=f.readline()
        line.split()
        if infos == True:
            print(line)
        pH=[]
        for i in range(self.nb_block):
            line=f.readline()
            tmp_line = line.split()
            pH.append(fortran_float(tmp_line[0]))
        if infos == True:
            print(line)
        #Concentration of secondary species mol/kgw :
        line=f.readline()
        line.split()
        if infos == True:
            print(line)
        concentration_secondary_tmp=[]
        line=f.readline()
        while not tmp_line[0]=='Water':
            concentration_secondary_tmp+=[fortran_float(elem) for elem in line.split()]
            line=f.readline()
            tmp_line = line.split()
        self.nb_secondary_species = int(len(concentration_secondary_tmp)/self.nb_block)
        if self.nb_species%6 == 0:
            self.nb_lines_block['concentration_secondary'] = (self.nb_secondary_species//6)
        else:
            self.nb_lines_block['concentration_secondary'] = (self.nb_secondary_species//6+1)
        concentration_secondary=[]
        for i in range(self.nb_block):
            concentration_secondary.append(concentration_secondary_tmp[i*self.nb_secondary_species:(i+1)*self.nb_secondary_species])
#         if infos == True:
#             print(line)
#         if infos == True:
#             print(line)
#         line=f.readline()
#         tmp_line = line.split()
#         concentration_secondary=''
#         while not tmp_line[0]=='Water':
#             concentration_secondary+=line
#             line=f.readline()
#             tmp_line = line.split()
#         if infos == True:
#             print(line)
        #Water Activity :
#         line=f.readline()
#         line.split()
        if infos == True:
            print(line)
        water_activity=[]
        for i in range(self.nb_block):
            line=f.readline()
            tmp_line = line.split()
            water_activity.append(fortran_float(tmp_line[0]))
        if infos == True:
            print(line)
        #--------------Minerals----------------------
        if self.nb_minerals > 0:
            #Initial mineral amount mol/dm^3 :
            line=f.readline()
            #line.split()
            if infos == True:
                print(line)
#             initial_mineral_amount=[]
#             for i in range(self.nb_block):
#                 tmp = []
#                 for j in range(self.nb_lines_block['initial_mineral']):
#                     line=f.readline()
#                     tmp += [fortran_float(line[i:i+21]) for i in [0,21,42,63]]
#                 initial_mineral_amount.append(tmp[0:self.nb_minerals+1])
            line=f.readline()
            tmp_line = line.split()
            initial_mineral_amount=''
            while not tmp_line[0]=='Current':
                initial_mineral_amount+=line
                line=f.readline()
                tmp_line = line.split()
            if infos == True:
                print(line)
            #Current mineral amount mol/dm^3 :
            line=f.readline()
            line.split()
            if infos == True:
                print(line)
            #line=f.readline()
            current_mineral_amount=''
            while not tmp_line[0]=='Residual':
                current_mineral_amount+=line
                line=f.readline()
                tmp_line = line.split()
#             current_mineral_amount=[]
#             for i in range(self.nb_block):
#                 tmp = []
#                 for j in range(self.nb_lines_block['current_mineral']):
#                     line=f.readline()
#                     tmp += [fortran_float(line[i:i+21]) for i in [0,21,42,63]]
#                 current_mineral_amount.append(tmp[0:self.nb_minerals])
            if infos == True:
                print(line)
        #Residual Solute after Dryout moles/dm^3 :
        line.split()
        if infos == True:
            print(line)
        line=f.readline()
        residual_solute=''
        while not tmp_line[0]=='UT':
            residual_solute+=line
            line=f.readline()
            tmp_line = line.split()
#         residual_solute=[]
#         for i in range(self.nb_block):
#             tmp = []
#             for j in range(self.nb_lines_block['residual_solute']):
#                 line=f.readline()
#                 tmp_line = line.split()
#                 tmp += [fortran_float(line[i:i+15]) for i in [0,15,30,45,60,75]]
#             residual_solute.append(tmp[0:self.nb_species])
        if infos == True:
            print(line)
        #UT   Concentration of primary species mol/L :
#         line=f.readline()
#         line.split()
        if infos == True:
            print(line)
        UT_concentration_primary=[]
        for i in range(self.nb_block):
            tmp = []
            for j in range(self.nb_lines_block['UT_species']):
                line=f.readline()
                tmp += [fortran_float(line[i:i+15]) for i in [0,15,30,45,60,75]]
            UT_concentration_primary.append(tmp[0:self.nb_species])
        if infos == True:
            print(line)
        if not self.pitzer:
            #CO2 trapped in the solid phase :
            if "eco2" in self.exe:
                line=f.readline()
                line.split()
                if infos == True:
                    print(line)
                CO2_trapped=[]
                for i in range(self.nb_block):
                    tmp = []
                    line=f.readline()
                    tmp_line = line.split()
                    CO2_trapped.append(fortran_float(tmp_line[0]))
                if infos == True:
                    print(line)
            #Kinetic (Number of grains):
            if self.kinetic:
                line=f.readline()
                line.split()
                if infos == True:
                    print(line)
                line=f.readline()
                number_grains=''
                while not tmp_line[0]=='Initial':
                    number_grains+=line
                    line=f.readline()
                    tmp_line = line.split()
#                 kinetic_tab=[]
#                 for i in range(self.nb_block):
#                     tmp_line = []
#                     for j in range(1):
#                         line=f.readline()
#                         tmp_grains = line.split()
#                         tmp_line.extend(tmp_grains)
#                     kinetic_tab.append([fortran_float(tmp) for tmp in tmp_line])
#                 if infos == True:
#                     print(line)
            #Initial porosity phi0 : 
            line.split()
            if infos == True:
                print(line)
            initial_porosity=[]
            for i in range(self.nb_block):
                tmp = []
                line=f.readline()
                tmp_line = line.split()
                initial_porosity.append(fortran_float(tmp_line[0]))
            if infos == True:
                print(line)
            #Initial permeability perm0 m2 : 
            line=f.readline()
            line.split()
            if infos == True:
                print(line)
            initial_permeability=[]
            for i in range(self.nb_block):
                tmp = []
                line=f.readline()
                tmp_line = line.split()
                initial_permeability.append([fortran_float(tmp) for tmp in tmp_line])
            if infos == True:
                print(line)
        f.close()
        dict_total = {'geochemical_state':geochemical_state,\
        'concentration_primary':concentration_primary,\
        'pH':pH,'concentration_secondary':concentration_secondary,\
        'water_activity':water_activity,'residual_solute':residual_solute,\
        'UT_species':UT_concentration_primary}
        if not self.pitzer:
            dict_total['porosity'] = initial_porosity
            dict_total['permeability'] = initial_permeability
        if self.nb_minerals > 0:
            dict_total['initial_mineral'] = initial_mineral_amount
            dict_total['current_mineral'] = current_mineral_amount
        if "eco2" in self.exe:
            dict_total['CO2_trapped'] = CO2_trapped
        if self.kinetic:
            dict_total['kinetic'] = number_grains
        return dict_total
    
    def write_savechem(self,filename):
        f=open(filename,'w')
        #Geochemical state variables at restart time (s):
        f.write("Geochemical state variables at restart time (s):\n")
        f.write(' %14.8e\n'%self.contenu['geochemical_state'])
        #Concentration of primary species mol/kgw :
        f.write("Concentration of primary species mol/kgw :")
        for elem in self.contenu['concentration_primary']:
            for j in range(len(elem)):
                if j%6==0:
                    f.write("\n")
                    f.write('%15.8e'%elem[j])
                else:
                    f.write('%15.8e'%elem[j])
        f.write("\n")
        #pH :
        f.write("pH :\n")
        for elem in self.contenu['pH']:
            f.write('%10.6f'%elem)
            f.write("\n")
        #Concentration of secondary species mol/kgw :
        f.write("Concentration of secondary species mol/kgw :")
        for elem in self.contenu['concentration_secondary']:
            for j in range(len(elem)):
                if j%6==0:
                    f.write("\n")
                    f.write('%15.8e'%elem[j])
                else:
                    f.write('%15.8e'%elem[j])
        f.write("\n")
        #Water Activity :
        f.write("Water Activity :\n")
        for elem in self.contenu['water_activity']:
            f.write('%15.8e'%elem)
            f.write("\n")
        #--------------Minerals----------------------
        if self.nb_minerals > 0:
            #Initial mineral amount mol/dm^3 :
            f.write("Initial mineral amount mol/dm^3 :")
#             for elem in self.contenu['initial_mineral']:
#                 for j in range(len(elem)):
#                     if j%4==0:
#                         f.write("\n")
#                         f.write('%21.14e'%elem[j])
#                     else:
#                         f.write('%21.14e'%elem[j])
            f.write("\n")
            f.write(self.contenu['initial_mineral'])
            #Current mineral amount mol/dm^3 :
            f.write("Current mineral amount mol/dm^3 :\n")
            f.write(self.contenu['current_mineral'])
#             for elem in self.contenu['current_mineral']:
#                 for j in range(len(elem)):
#                     if j%4==0:
#                         f.write("\n")
#                         f.write('%21.14e'%elem[j])
#                     else:
#                         f.write('%21.14e'%elem[j])
#             f.write("\n")
        #Residual Solute after Dryout moles/dm^3 :
        f.write("Residual Solute after Dryout moles/dm^3 :")
#         for elem in self.contenu['residual_solute']:
#             for j in range(len(elem)):
#                 if j%6==0:
#                     f.write("\n")
#                     f.write('%15.8e'%elem[j])
#                 else:
#                     f.write('%15.8e'%elem[j])
        f.write("\n")
        f.write(self.contenu['residual_solute'])
        #UT   Concentration of primary species mol/L :
        f.write("UT   Concentration of primary species mol/L :")
        for elem in self.contenu['UT_species']:
            for j in range(len(elem)):
                if j%6==0:
                    f.write("\n")
                    f.write('%15.8e'%elem[j])
                else:
                    f.write('%15.8e'%elem[j])
        f.write("\n")
        #CO2 trapped in the solid phase :
        if "eco2" in self.exe:
            f.write("CO2 trapped in the solid phase :\n")
            for elem in self.contenu['CO2_trapped']:
                f.write(' %21.14e\n'%elem)
        #Number of grains :
        if self.kinetic:
            f.write("Number of Grains :\n")
            f.write(self.contenu['kinetic'])
#             for elem in self.contenu['kinetic']:
#                 for j in range(len(elem)):
#                     if j%4==0:
#                         f.write("\n")
#                         f.write('%21.14e'%elem[j])
#                     else:
#                         f.write('%21.14e'%elem[j])
#             f.write("\n")
                #f.write('%21.14e\n'%elem[0])
                #f.write('%21.14e%21.14e%21.14e%21.14e%21.14e\n'%tuple([elem[0],elem[1],elem[2],elem[3],elem[4]]))
        if not self.pitzer:
            #Initial porosity phi0 :
            f.write("Initial porosity phi0 :\n")
            for elem in self.contenu['porosity']:
                f.write(' %14.8e\n'%elem)
            #Initial permeability perm0 m2 : 
            f.write("Initial permeability perm0 m2 : \n")
            for elem in self.contenu['permeability']:
                #print elem
                f.write('%15.8e%15.8e%15.8e\n'%tuple([elem[0],elem[1],elem[2]]))
        #fin
        f.write("\n")
        f.close()

    def nb_lines_savechem(self):
        #Description du fichier savechem (en nombre de lignes)
        # 1 ligne de description "Geochemical state variables at restart time (s):"
        # 1 ligne de valeur
        nb_line_geochemical_state = 1+1
        print(nb_line_geochemical_state)
        # 1 ligne de description "Concentration of primary species mol/kgw :"
        # nb_line * nb_elem avec nb_line = self.nb_species % 6      (6 concentrations par ligne)
        if self.nb_species%6 == 0:
            nb_line_concentration_primary = 1+(self.nb_species//6)*self.nb_block
        else:
            nb_line_concentration_primary = 1+(self.nb_species//6+1)*self.nb_block
        print(nb_line_concentration_primary)
        # 1 ligne de description "pH :"
        # nb_elem valeurs
        nb_line_pH = 1+self.nb_block
        print(nb_line_pH)
        # 1 ligne de description "Concentration of secondary species mol/kgw :"
        # nb_line * nb_elem representant le nombre de lignes contenant les especes secondaires
        nb_line_concentration_secondary = 1+10*self.nb_block #cf. fichier savechem...
        print(nb_line_concentration_secondary)
        # 1 ligne de description "Water Activity :"
        # nb_elem valeurs
        nb_line_water_activity = 1+self.nb_block
        print(nb_line_water_activity)
        # 1 ligne de description "Initial mineral amount mol/dm^3 :"
        # nb_line * nb_elem avec nb_line = self.nb_minerals % 4      (4 concentrations par ligne)
        if (self.nb_minerals+1)%4 == 0:
            nb_line_initial_mineral = 1+((self.nb_minerals+1)//4)*self.nb_block
        else:
            nb_line_initial_mineral = 1+((self.nb_minerals+1)//4+1)*self.nb_block
        print(self.nb_minerals,"    ",nb_line_initial_mineral)
        # 1 ligne de description "Current mineral amount mol/dm^3 :"
        # nb_line * nb_elem avec nb_line = (self.nb_minerals-1) % 4      (4 concentrations par ligne)
        if self.nb_minerals%4 == 0:
            nb_line_current_mineral = 1+(self.nb_minerals//4)*self.nb_block
        else:
            nb_line_current_mineral = 1+(self.nb_minerals//4+1)*self.nb_block
        print(nb_line_current_mineral)
        # 1 ligne de description "Residual Solute after Dryout moles/dm^3 :"
        # nb_line * nb_elem avec nb_line = self.nb_species % 6      (6 concentrations par ligne)
        if self.nb_species%6 == 0:
            nb_line_residual_solute = 1+(self.nb_species//6)*self.nb_block
        else:
            nb_line_residual_solute = 1+(self.nb_species//6+1)*self.nb_block
        print(nb_line_residual_solute)
        # 1 ligne de description "UT   Concentration of primary species mol/L :"
        # nb_line * nb_elem avec nb_line = self.nb_species % 6      (6 concentrations par ligne)
        if self.nb_species%6 == 0:
            nb_line_UT_species = 1+(self.nb_species//6)*self.nb_block
        else:
            nb_line_UT_species = 1+(self.nb_species//6+1)*self.nb_block
        print(nb_line_UT_species)
        # 1 ligne de description "Initial porosity phi0 :"
        # nb_elem valeurs
        nb_line_porosity = 1+self.nb_block
        print(nb_line_porosity)
        # 1 ligne de description "Initial permeability perm0 m2 :"
        # nb_elem valeurs
        nb_line_permeability = 1+self.nb_block
        print(nb_line_permeability)
        return {'geochemical_state':nb_line_geochemical_state,\
        'concentration_primary':nb_line_concentration_primary,\
        'pH':nb_line_pH,'concentration_secondary':nb_line_concentration_secondary,\
        'water_activity':nb_line_water_activity,'initial_mineral':nb_line_initial_mineral,\
        'current_mineral':nb_line_current_mineral,'residual_solute':nb_line_residual_solute,\
        'UT_species':nb_line_UT_species,'porosity':nb_line_porosity,\
        'permeability':nb_line_permeability}

if __name__=='__main__':
    rep_test = '/Users/anthonysoive/Documents/CR_Nantes_2014_11/02-Modelisation/Durabilite_marnage/'
    #liste des especes chimiques presentes
    liste_especes=['H2O','H+','Cl-','Ca++','SO4--','H4SiO4(aq)','K+','Mg++','Na+',\
    'Al+++','O2(aq)','Fe++']
    #liste des mineraux
    liste_mineraux=['C3FH6','CSH_1.6','Ettringite','Hydrotalcite','KatoiteSi1',\
    'Portlandite','Friedel_Salt','Halite']
    titi=t2rsavechem(2,liste_especes,liste_mineraux,rep_test+"savechem")
    titi.write_savechem(rep_test+"test.txt")