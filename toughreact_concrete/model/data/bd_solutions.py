"""
Compositions des solutions de contact utilisées comme conditions aux limites.
Clés = nom de la base de données thermodynamique.
"""

bnd_solution = {
    'Thermoddem_2023.txt': [
        {
            'composition': {
                'h2o':    0.1700E+01,
                'H+':     1.7e-7,
                'Ca+2':   1e-30,
                'SO4-2':  0.0357,
                'h4sio4': 1.000e-30,
                'K+':     1e-30,
                'Mg+2':   1e-30,
                'Na+':    0.0714,
                'Al+3':   1.000e-30,
                'Cl-':    1e-30,
            },
            'temperature': 20.0,
        }
    ],
    'Th_Yoshida2021.txt': [
        {
            'composition': {
                'h2o':    0.1000E+01,
                'H+':     1.11E-10,
                'Na+':    0.679,
                'Cl-':    0.599,
                'Ca+2':   1e-20,
                'SO4-2':  1e-20,
                'h4sio4': 1e-20,
                'K+':     1e-20,
                'Mg+2':   1e-20,
                'Al+3':   1e-20,
                'HCO3-':  2.029e-3,
            },
            'temperature': 15.1,
        }
    ],
}

bnd_solution['kswitch.out'] = bnd_solution['Th_Yoshida2021.txt']
