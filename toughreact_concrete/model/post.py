"""
Created on Tue Oct 21 12:52:04 2014

@author: anthony.soive
"""

import glob
import linecache
import os
import re

import matplotlib.pyplot as plt
import pandas as pd


def recup_entete_plot(fichier, toughreact_exe, pitzer, df_pos_x, complexation):
    if pitzer:
        num_line_header = 7
        line_header = linecache.getline(fichier, num_line_header)
        tmp_header = re.split(r'[;,\s]\s*', line_header)[2:-1]
        header = []
        for elem in tmp_header:
            if elem != '':
                header.append(elem)
        header.insert(0,'X')
        widths = [12]*2+[11]+[9]+[13]*3+[8]*2+[12]*(len(header)-9)
        nb_rows = num_line_header+1+len(df_pos_x)+1
    if "eco2" in toughreact_exe[-19:]:
        num_line_header = 10
        line_header = linecache.getline(fichier, num_line_header)
        tmp_header = re.split(r'[;,\s]\s*', line_header)[2:-1]
        header = []
        for elem in tmp_header:
            if elem != '':
                header.append(elem)
        header.insert(0,'X')
        widths = [11]*3+[12]*4+[8]*2+[12]+[12]*(len(header)-10)
        nb_rows = num_line_header+1
    else:
        if complexation:
            num_line_header = 9
        else:
            num_line_header = 8
        line_header = linecache.getline(fichier, num_line_header)
        tmp_header = re.split(r'[;,\s]\s*', line_header)[2:-1]
        header = []
        for elem in tmp_header:
            if elem != '':
                header.append(elem)
        header.insert(0,'X')
        widths = [12]*2+[11]+[9]+[13]*3+[8]*2+[12]*(len(header)-9)
        nb_rows = num_line_header+1#+len(df_pos_x)+1
    return header, widths, nb_rows

def recup_entete_solid(fichier, toughreact_exe):
    if "eco2" in toughreact_exe[-19:]:
        num_line_header = 10
        line_header = linecache.getline(fichier, num_line_header)
        tmp_header = re.split(r'[;,\s]\s*', line_header)[2:-1]
        header_out = []
        for elem in tmp_header:
            if elem != '':
                header_out.append(elem)
        header_out.insert(0,'X')
        widths = [11]*3+[10]+[12]+[10]+[13]+[12]*(len(header_out)-7)
        nb_rows = num_line_header+1
    else:
        num_line_header = 8
        result = open(fichier).readlines()
        #line_header = linecache.getline(fichier, num_line_header)
        line_header = result[num_line_header-1]
        tmp_header = re.split(r'[;,\s]\s*', line_header)[2:-1]
        header_out = []
        for elem in tmp_header:
            if elem != '':
                header_out.append(elem)
        header_out.insert(0,'X')
        widths = [12]*2+[11]+[9]*2+[13]*2+[12]+[13]+[12]+[12]*(len(header_out)-10)
        nb_rows = num_line_header+1
    return header_out, widths, nb_rows

def recup_coord(mesh):
    coord_x, coord_y, coord_z = "X\n", "Y\n", "Z\n"
    f = open("MESH")
    f.readline()
    for i in range(mesh.num_elem['X']):
        tmp = f.readline()
        coord_x += tmp[-31:-21]+"\n"
        coord_y += tmp[-21:-11]+"\n"
        coord_z += tmp[-11:-1]+"\n"
    
    fichier_pos = open('OUTPUT/Pos_x.txt', 'w')
    fichier_pos.write(coord_x)
    fichier_pos.close()


def convert_to_pandas(chemin, toughreact_exe, pitzer, complexation, time_output, init, mesh):
    if os.path.isfile(chemin):
        list_fich = [chemin]
    else:
        os.chdir(chemin)
        list_fich = glob.glob('*.dat')
    df_pos_x = pd.read_csv('OUTPUT/Pos_x.txt')
    header, widths, nb_rows = recup_entete_plot(list_fich[0], toughreact_exe, pitzer, df_pos_x, complexation)
    for fich in list_fich:
        data = pd.read_fwf(fich,skiprows=nb_rows,widths=widths,names=header)
        nb_lines_per_record = len(df_pos_x)*mesh.num_elem['Z']
        if init:
            i = nb_lines_per_record + 1
        else:
            i = 0
        dict_tmp = {}
        with pd.ExcelWriter(fich[0:-4]+'.xlsx') as writer:
        #with pd.ExcelWriter('OUTPUT/plot.xls') as writer:
            for elem in time_output:
                for elem_entete in header:
                    if elem_entete == 'X':
                        df_pos_x_tmp = df_pos_x['X']
                        for l in range(1,mesh.num_elem['Z']):
                            df_pos_x_tmp = pd.concat([df_pos_x_tmp, df_pos_x['X']], ignore_index=True)
                        dict_tmp['X'] = df_pos_x_tmp.reset_index(drop=True)
                    else:
                        dict_tmp[elem_entete] = data[elem_entete][i:nb_lines_per_record+i].reset_index(drop=True)
                df = pd.DataFrame(dict_tmp)
                sheet_name = "%.2f"%(elem/3600.0/24.0) + "j"
                df.to_excel(writer,sheet_name=str(sheet_name))
                i += nb_lines_per_record + 1
            #data.to_excel(fich[0:-4]+'.xls',sheet_name='Sheet1')
    for fich in list_fich:
        os.remove(fich)

def convert_to_pandas_out(chemin, toughreact_exe, pitzer, time_output, init, mesh):
    if os.path.isfile(chemin):
        list_fich = [chemin]
    else:
        os.chdir(chemin)
        list_fich = glob.glob('*.out')
    df_pos_x = pd.read_csv('OUTPUT/Pos_x.txt')
    header_out, widths, nb_rows = recup_entete_solid(list_fich[0], toughreact_exe)
    for fich in list_fich:
        data = pd.read_fwf(fich,skiprows=nb_rows,widths=widths,names=header_out)
        nb_lines_per_record = len(df_pos_x)*mesh.num_elem['Z']
        if init:
            i = nb_lines_per_record + 1
        else:
            i = 0
        dict_tmp = {}
        with pd.ExcelWriter(fich[0:-4]+'.xlsx') as writer:
        #with pd.ExcelWriter('OUTPUT/solid.xls') as writer:
            for elem in time_output:
                for elem_entete in header_out:
                    if elem_entete == 'X':
                        df_pos_x_tmp = df_pos_x['X']
                        for l in range(1,mesh.num_elem['Z']):
                            df_pos_x_tmp = pd.concat([df_pos_x_tmp, df_pos_x['X']], ignore_index=True)
                        dict_tmp['X'] = df_pos_x_tmp.reset_index(drop=True)
                    else:
                        dict_tmp[elem_entete] = data[elem_entete][i:nb_lines_per_record+i].reset_index(drop=True)
                df = pd.DataFrame(dict_tmp)
                sheet_name = "%.2f"%(elem/3600.0/24.0) + "j"
                df.to_excel(writer,sheet_name=str(sheet_name))
                i += nb_lines_per_record + 1
        #data['X'] = df_pos_x['X']
        #data.to_excel(fich[0:-4]+'.xls',sheet_name='Sheet1')
    for fich in list_fich:
        os.remove(fich)

def pre_visu(list_fich):
    '''Function that contruct a dataframe from a list of files in order to be
    visualize by pandas'''
    tmp_df = pd.read_excel(list_fich[0],sheetname='Sheet1',parse_cols=[7])
    ts = pd.Series()#tmp_df.Sl)
    for fich in list_fich:
        tmp_df = pd.read_excel(fich,sheetname='Sheet1',parse_cols=[7])
        #ts[fich[5:-3]] = tmp_df.Sl
        ts_add = pd.Series(tmp_df.Sl, name=fich[5:-4])#.groupby(name=fich[5:-4]).sum(axis=1)
        ts = pd.concat([ts,ts_add], axis=1)#pd.Series(pd.concat([ts,ts_add],axis=1))
    return ts

if __name__ == '__main__':
    rep = '/Users/anthonysoive/Documents/CR_Nantes_2014_11/02-Modelisation/workspace/APOS/Sechage_CEM1_APOS'#/home/zivkovic/Documents/Models/OUTPUT/'
    os.chdir(rep)
    #convert_to_pandas(rep)
    list_fich = glob.glob('plot*.xls')
    titi = pre_visu(list_fich)
    porosite_BO_APOS = 0.159
    porosite_BO_III_APOS = 0.153
    porosite = porosite_BO_APOS
    volume_per_element = 3.14159 * 0.05**2 * 0.12 / 30.0 * porosite
    mass_eau_init = 3.14159 * 0.05**2 * 0.12 / 30.0 * porosite * 1000.0 * sum([elem for elem in titi['0.00'][0:]])
    print("masse d'eau initiale : ",mass_eau_init)
    masse_epr_init_BO_APOS = 1.9508
    masse_epr_init_BO_III_APOS = 1.92171
    masse_epr_init = masse_epr_init_BO_APOS
    x = [0]
    mass = [0]
    for fich in list_fich[1:]:
        x.append(int(fich[5:-7]))
        perte_masse_eau = mass_eau_init - volume_per_element*sum([elem for elem in titi[fich[5:-4]][0:]]) * 1000.0
        masse_epr = masse_epr_init - perte_masse_eau
        #print titi[fich[5:-4]]
        print(perte_masse_eau)
        perte_relative = perte_masse_eau/masse_epr_init * 100.0
        mass.append(perte_relative)
    x.sort()
    mass.sort()
    plt.plot(x,mass)
    #Expe
    time = [0.00,0.98,1.97,2.95,3.93,6.95,10.94,13.95,22.93,27.93,34.93,48.93,62.93,72.93,87.93,101.93,115.93,129.93,146.93,157.93,189.93,209.93]
    perte_relative_expe_BO_APOS = [0.00,0.19,0.31,0.41,0.49,0.69,0.91,1.05,1.33,1.53,1.70,1.98,2.17,2.27,2.39,2.49,2.58,2.67,2.76,2.82,2.94,2.99]
    perte_relative_expe_BO_III_APOS = [0.00,0.13,0.19,0.22,0.28,0.33,0.39,0.43,0.50,0.56,0.61,0.71,0.79,0.83,0.88,0.92,0.96,1.00,1.05,1.07,1.14,1.18]
    plt.plot(time,perte_relative_expe_BO_APOS,'x')
    plt.xlabel('temps (jours)')
    plt.ylabel('perte de masse [%]')
    plt.show()
    print('fini !')

