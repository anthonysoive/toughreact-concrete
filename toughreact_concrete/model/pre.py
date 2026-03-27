"""
Pre-simulation setup: copy TOUGHREACT binaries and input templates to the working directory.
"""
import os
import shutil
import sys


def initialize(eos: str, database: str, pitzer: bool = False) -> str:
    """Set up the TOUGHREACT working directory for a simulation.

    Creates (or resets) the ``../Calcul/`` working directory, copies the
    appropriate solver binary for the current platform, and copies all required
    input template files and the thermodynamic database. Also creates
    ``Boundary/`` and ``Material_equilibrium/`` subdirectories as copies of the
    working directory, then changes the current working directory to
    ``../Calcul/``.

    Parameters
    ----------
    eos : str
        Equation-of-state module identifier, e.g. ``'eos3'``, ``'eos4'``,
        ``'eos9'``, or ``'eco2n'``.
    database : str
        Filename of the thermodynamic database to copy (must exist in
        ``toughreact_concrete/data/``), e.g. ``'Thermoddem_2023.txt'``.
    pitzer : bool, optional
        If ``True``, use the Pitzer activity-coefficient solver binary instead
        of the standard one. Default is ``False``.

    Returns
    -------
    str
        Name of the solver executable copied to the working directory.
    """
    rep_outil = 'toughreact_concrete/'
    rep_travail = '../Calcul/'
    if not os.path.exists(rep_travail):
        os.mkdir(rep_travail)
    else:
        shutil.rmtree(rep_travail, ignore_errors=True)
        #shutil.rmtree(rep_travail)
        os.mkdir(rep_travail)
    
    if pitzer:
        if sys.platform == 'darwin':
            exe = 'treactv3omp_'+eos+'_macosx_intel'
            shutil.copyfile(rep_outil+'exe/'+exe,rep_travail+exe)
        elif sys.platform == 'linux2':
            exe = 'treactv3omp_'+eos+'_linux_intel'
            shutil.copyfile(rep_outil+'exe/'+exe,rep_travail+exe)
            #toughreact_exe = rep_travail+exe
        else:
            exe = 'trpz1.21_'+eos[0]+eos[-1]+'p-PC64.exe'
            shutil.copyfile(rep_outil+'exe/'+exe,rep_travail+exe)
            shutil.copyfile(rep_outil+'data/data0.ypf',rep_travail+'data0.ypf')
    else:
        if sys.platform == 'darwin':
            exe = 'treactv3omp_'+eos+'_macosx_intel'
            #Pour le calcul d'équilibre initial
            exe_ini = 'treactv3omp_eos9_macosx_intel'
            #shutil.copyfile(rep_outil+'exe/'+exe_ini,rep_travail+exe_ini)
            #toughreact_exe_ini = rep_travail+exe_ini        elif sys.platform == 'linux2':
            exe = 'treactv3omp_'+eos+'_macosx_intel'
        elif sys.platform == 'linux':
            exe = 'treactv3omp_'+eos+'_linux_intel'
            #Pour le calcul d'équilibre initial
            exe_ini = 'treactv3omp_eos9_macosx_intel'
            #shutil.copyfile(rep_outil+'exe/'+exe_ini,rep_travail+exe_ini)
            #toughreact_exe = rep_travail+exe
        else:
            #Pour le calcul d'équilibre initial
            exe_ini = 'tr3.0-omp_eos9_PC64.exe'
            exe = 'tr3.0-omp_'+eos+'_PC64.exe'
            shutil.copy(rep_outil+'exe/libifcoremd.dll',rep_travail)
            shutil.copy(rep_outil+'exe/libiomp5md.dll',rep_travail)
            shutil.copy(rep_outil+'exe/libmmd.dll',rep_travail)
            shutil.copy(rep_outil+'exe/svml_dispmd.dll',rep_travail)
        shutil.copyfile(rep_outil+'exe/'+exe_ini,rep_travail+exe_ini)
        shutil.copyfile(rep_outil+'exe/'+exe,rep_travail+exe)
        if eos == 'eco2n':
            shutil.copyfile(rep_outil+'data/CO2TAB',rep_travail+'CO2TAB')

    shutil.copyfile(rep_outil+'data/'+database,rep_travail+database)
    #shutil.copyfile(rep_outil+'data/'+database_phreeqc,rep_travail+database_phreeqc)
    shutil.copyfile(rep_outil+'data/trame_flow.inp',rep_travail+'trame_flow.inp')
    shutil.copyfile(rep_outil+'data/trame_flow_boundary.inp',rep_travail+'trame_flow_boundary.inp')
    shutil.copyfile(rep_outil+'data/trame_solute.inp',rep_travail+'trame_solute.inp')
    shutil.copyfile(rep_outil+'data/trame_solute_boundary.inp',rep_travail+'trame_solute_boundary.inp')
    shutil.copyfile(rep_outil+'data/trame_solute_reactive_transport.inp',rep_travail+'trame_solute_reactive_transport.inp')
    shutil.copyfile(rep_outil+'data/trame_chemical.inp',rep_travail+'trame_chemical.inp')
    shutil.copyfile(rep_outil+'data/trame_chemical_atl_seawater.inp',rep_travail+'trame_chemical_atl_seawater.inp')
    shutil.copyfile(rep_outil+'data/trame_chemical_bnd_solution.inp',rep_travail+'trame_chemical_bnd_solution.inp')
    shutil.copyfile(rep_outil+'data/trame_chemical_reactive_transport.inp',rep_travail+'trame_chemical_reactive_transport.inp')
    #shutil.copyfile(rep_outil+'data/chemical_in.inp',rep_travail+'chemical_in.inp')
    
    shutil.copytree(rep_travail,rep_travail+'Boundary')
    shutil.copytree(rep_travail,rep_travail+'Material_equilibrium')
    
    os.chdir(rep_travail)
    os.chmod(exe,0o777)
    os.chmod(exe_ini,0o777)
    os.chmod('Boundary/'+exe,0o777)
    os.chmod('Boundary/'+exe_ini,0o777)
    
    return exe
