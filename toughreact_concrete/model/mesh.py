import t2grids

from toughreact_concrete.geometry_trc import constrgeom


class Mesh:

    def __init__(self, geom, CL, ep_couche_limite=20e-2):
        self.len_eau = geom[0]['points'][0][0]
        self.hauteur = geom[0]['elements']['Y'][0]
        self.num_elem = {
            'X': len(geom[0]['elements']['X']),
            'Y': len(geom[0]['elements']['Y']),
            'Z': len(geom[0]['elements']['Z']),
        }
        self.ep_couche_limite = ep_couche_limite
        self.CL = CL
        self.abscisses_x_txt = ''
        self.geo = t2grids.mulgrid()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _apply_cl_positions(self, pos_dx, pos_dy, cl_key, values, update_x_count=False):
        """Insert/append boundary-layer cell widths into pos_dx/pos_dy
        for every direction listed under self.CL[cl_key]."""
        for direction in self.CL.get(cl_key, []):
            if direction == 'left':
                pos_dx.insert(0, values['left'])
                if update_x_count:
                    self.num_elem['X'] += 1
            elif direction == 'right':
                pos_dx.append(values['right'])
                if update_x_count:
                    self.num_elem['X'] += 1
            elif direction == 'top':
                pos_dy.insert(0, values['top'])
            elif direction == 'bottom':
                pos_dy.append(values['bottom'])

    def _build_abscisses_x(self, pos_dx, origin=0.0):
        """Compute X cell-centre abscissae from cell widths and store as text."""
        centers = [origin - pos_dx[0] / 2.0]
        for i, dx in enumerate(pos_dx[1:], start=1):
            centers.append(centers[-1] + pos_dx[i - 1] / 2.0 + dx / 2.0)
        self.abscisses_x_txt = "X\n" + "\n".join(str(x) for x in centers) + "\n"

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def construct_mesh(self, geom):
        pos_dx, pos_dy, pos_dz = [], [], []
        for elem in geom:
            pos_dx += elem['elements']['X']
        pos_dy += elem['elements']['Y']
        pos_dz += elem['elements']['Z']

        if len(self.CL) > 0:
            if self.CL['maree']:
                self._apply_cl_positions(pos_dx, pos_dy, 'maree', {
                    'left':   -self.ep_couche_limite,  # Note: negative (water-side)
                    'right':   self.ep_couche_limite,
                    'top':     self.ep_couche_limite,
                    'bottom':  self.ep_couche_limite,
                }, update_x_count=True)
            self._apply_cl_positions(pos_dx, pos_dy, 'infini', {
                'left':   5e-5,
                'right':  5e-5,
                'top':    geom[-1]['elements']['Y'],
                'bottom': geom[-1]['elements']['Y'],
            }, update_x_count=True)

        self._build_abscisses_x(pos_dx, origin=geom[0]['points'][0][0])
        self.geo = t2grids.mulgrid().rectangular(
            pos_dx, pos_dy, pos_dz, origin=[0, 0, self.hauteur])

    def build_mesh(self, mesh_type, dims, num_elem):
        if mesh_type['name'] == "geometric_prog":
            pos_dx = constrgeom.suite_geom(dims['X'], num_elem['X'], mesh_type['common_ratio'])
            pos_dy = constrgeom.suite_geom(dims['Y'], num_elem['Y'], mesh_type['common_ratio'])
        else:
            pos_dx = [float(dims['X']) / float(num_elem['X'])] * num_elem['X']
            pos_dy = [float(dims['Y']) / float(num_elem['Y'])] * num_elem['Y']

        if len(self.CL) > 0:
            if self.CL['maree']:
                self._apply_cl_positions(pos_dx, pos_dy, 'maree', {
                    'left':   self.ep_couche_limite,
                    'right':  self.ep_couche_limite,
                    'top':    self.ep_couche_limite,
                    'bottom': self.ep_couche_limite,
                })
            self._apply_cl_positions(pos_dx, pos_dy, 'infini', {
                'left':   5e-5,
                'right':  5e-5,
                'top':    dims['Y'],
                'bottom': dims['Y'],
            })

        self._build_abscisses_x(pos_dx, origin=0.0)
        if float(num_elem['Y']) < 40:
            self.geo = t2grids.mulgrid().rectangular(
                pos_dx, pos_dy, [1.0], origin=[0, 0, sum(pos_dy[1:])])
        else:
            self.geo = t2grids.mulgrid().rectangular(
                pos_dx, pos_dy, [1.0], pos_dy, convention=1,
                origin=[0, 0, sum(pos_dy[1:])])

    def write_mesh_x(self):
        with open('OUTPUT/Pos_x.txt', 'w') as f:
            f.write(self.abscisses_x_txt)
