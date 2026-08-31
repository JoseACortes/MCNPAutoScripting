from .extra import fold128

min_x = -1000
max_x = 1000
min_y = -1000
max_y = 1000
min_z = -1000
max_z = 1000

class Surface:
    def __init__(self, surface_id, surface_type, parameters, label=None):
        self.surface_id = surface_id
        self.surface_type = surface_type
        self.parameters = parameters
        self.label = label

    def string(self):
        param_str = ' '.join(f"{k}={v}" for k, v in self.parameters.items())
        _cmt = ''
        if self.label:
            _cmt = f"$ {self.label}"
        _str = f"{self.surface_id} {self.surface_type} {param_str}{_cmt}"
        return fold128(_str)+"\n"

    def import_render(self):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        import numpy as np

    def render(self, ax, **kwargs):
        self.import_render()
        pass

def plot_box(ax, xmin, xmax, ymin, ymax, zmin, zmax, color, alpha=1, label=None, zorder=None):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    # Draw a rectangular box (RPP)
    x = [xmin, xmax]
    y = [ymin, ymax]
    z = [zmin, zmax]# Draw edges
    for s, e in [
        # bottom
        ([x[0], y[0], z[0]], [x[1], y[0], z[0]]),
        ([x[1], y[0], z[0]], [x[1], y[1], z[0]]),
        ([x[1], y[1], z[0]], [x[0], y[1], z[0]]),
        ([x[0], y[1], z[0]], [x[0], y[0], z[0]]),
        # top
        ([x[0], y[0], z[1]], [x[1], y[0], z[1]]),
        ([x[1], y[0], z[1]], [x[1], y[1], z[1]]),
        ([x[1], y[1], z[1]], [x[0], y[1], z[1]]),
        ([x[0], y[1], z[1]], [x[0], y[0], z[1]]),
        # sides
        ([x[0], y[0], z[0]], [x[0], y[0], z[1]]),
        ([x[1], y[0], z[0]], [x[1], y[0], z[1]]),
        ([x[1], y[1], z[0]], [x[1], y[1], z[1]]),
        ([x[0], y[1], z[0]], [x[0], y[1], z[1]])
    ]:
        ax.plot3D(*zip(s, e), color=color, alpha=alpha, zorder=zorder, linewidth=1.2)
    # Draw faces
    faces = [
        # bottom
        [[x[0], y[0], z[0]], [x[1], y[0], z[0]], [x[1], y[1], z[0]], [x[0], y[1], z[0]]],
        # top
        [[x[0], y[0], z[1]], [x[1], y[0], z[1]], [x[1], y[1], z[1]], [x[0], y[1], z[1]]],
        # front
        [[x[0], y[0], z[0]], [x[1], y[0], z[0]], [x[1], y[0], z[1]], [x[0], y[0], z[1]]],
        # back
        [[x[0], y[1], z[0]], [x[1], y[1], z[0]], [x[1], y[1], z[1]], [x[0], y[1], z[1]]],
        # left
        [[x[0], y[0], z[0]], [x[0], y[1], z[0]], [x[0], y[1], z[1]], [x[0], y[0], z[1]]],
        # right
        [[x[1], y[0], z[0]], [x[1], y[1], z[0]], [x[1], y[1], z[1]], [x[1], y[0], z[1]]]
    ]
    poly3d = Poly3DCollection(faces, facecolors=color, alpha=alpha, zorder=zorder, linewidths=0.5, edgecolors='k')
    ax.add_collection3d(poly3d)

class px(Surface):
    def __init__(self, surface_id, D, label=None):
        super().__init__(surface_id, 'PX', {'D': D}, label)
    def string(self):
        return f"{self.surface_id} PX {self.parameters['D']}"+"\n"

    # def render(self, ax, **kwargs):
    #     self.import_render()
    #     # Draw a plane at x = D
    #     D = self.parameters['D']
    #     plot_box(ax, D, D, kwargs.get('min_y', -10), kwargs.get('max_y', 10), kwargs.get('min_z', -10), kwargs.get('max_z', 10), color='red', alpha=0.5, **kwargs)
        
    

class py(Surface):
    def __init__(self, surface_id, D, label=None):
        super().__init__(surface_id, 'PY', {'D': D}, label)
    def string(self):
        return f"{self.surface_id} PY {self.parameters['D']}"+"\n"

class pz(Surface):
    def __init__(self, surface_id, D, label=None):
        super().__init__(surface_id, 'PZ', {'D': D}, label)
    def string(self):
        return f"{self.surface_id} PZ {self.parameters['D']}"+"\n"


def plot_cylinder(ax, base, vec, radius, height, color, alpha=1, label=None, zorder=None):
    import numpy as np
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    # Draw a cylinder (RCC) with flat ends
    x0, y0, z0 = base
    dx, dy, dz = vec
    # Normalize direction vector
    length = np.sqrt(dx**2 + dy**2 + dz**2)
    if length == 0:
        return
    dx, dy, dz = dx/length, dy/length, dz/length
    # Create cylinder along z, then rotate
    z = np.linspace(0, height, 30)
    theta = np.linspace(0, 2*np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)
    # Build rotation matrix
    v = np.array([dx, dy, dz])
    v0 = np.array([0, 0, 1])
    if not np.allclose(v, v0):
        axis = np.cross(v0, v)
        angle = np.arccos(np.clip(np.dot(v0, v), -1.0, 1.0))
        K = np.array([[0, -axis[2], axis[1]],
                      [axis[2], 0, -axis[0]],
                      [-axis[1], axis[0], 0]])
        R = np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K@K)
        xyz = np.stack([x_grid.flatten(), y_grid.flatten(), z_grid.flatten()])
        xyz_rot = R @ xyz
        x_grid = xyz_rot[0].reshape(x_grid.shape)
        y_grid = xyz_rot[1].reshape(y_grid.shape)
        z_grid = xyz_rot[2].reshape(z_grid.shape)
    x_grid += x0
    y_grid += y0
    z_grid += z0
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, linewidth=0, shade=True, zorder=zorder)

    # Flat ends
    for zc in [0, height]:
        # Circle in xy-plane
        x_end = radius * np.cos(theta)
        y_end = radius * np.sin(theta)
        z_end = np.full_like(x_end, zc)
        # Rotate
        xyz_end = np.stack([x_end, y_end, z_end])
        if not np.allclose(v, v0):
            xyz_end = R @ xyz_end
        x_end = xyz_end[0] + x0
        y_end = xyz_end[1] + y0
        z_end = xyz_end[2] + z0
        # Use Poly3DCollection for flat ends
        verts = [list(zip(x_end, y_end, z_end))]
        poly = Poly3DCollection(verts, facecolors=color, alpha=alpha, zorder=zorder)
        ax.add_collection3d(poly)

class rcc(Surface):
    def __init__(self, surface_id, vx, vy, vz, h1, h2, h3, r, label=None):
        super().__init__(surface_id, 'RCC', {'VX': vx, 'VY': vy, 'VZ': vz, 'H1': h1, 'H2': h2, 'H3': h3, 'R': r}, label)

    def string(self):
        return f"{self.surface_id} RCC {self.parameters['VX']} {self.parameters['VY']} {self.parameters['VZ']} {self.parameters['H1']} {self.parameters['H2']} {self.parameters['H3']} {self.parameters['R']}"+"\n"

    def render(self, ax, **kwargs):
        import numpy as np
        self.import_render()
        base = (self.parameters['VX'], self.parameters['VY'], self.parameters['VZ'])
        vec = (self.parameters['H1'], self.parameters['H2'], self.parameters['H3'])
        radius = self.parameters['R']
        height = np.linalg.norm(vec)
        plot_cylinder(ax, base, vec, radius, height, **kwargs)


class rpp(Surface):
    def __init__(self, surface_id, x1, x2, y1, y2, z1, z2, label=None):
        super().__init__(surface_id, 'RPP', {'X1': x1, 'X2': x2, 'Y1': y1, 'Y2': y2, 'Z1': z1, 'Z2': z2}, label)

    def string(self):
        return f"{self.surface_id} RPP {self.parameters['X1']} {self.parameters['X2']} {self.parameters['Y1']} {self.parameters['Y2']} {self.parameters['Z1']} {self.parameters['Z2']}"+ "\n"

    def render(self, ax, **kwargs):
        plot_box(ax, self.parameters['X1'], self.parameters['X2'], self.parameters['Y1'], self.parameters['Y2'], self.parameters['Z1'], self.parameters['Z2'], **kwargs)

class cx(Surface):
    def __init__(self, surface_id, r, label=None):
        super().__init__(surface_id, 'CX', {'R': r}, label)

    def string(self):
        return f"{self.surface_id} CX {self.parameters['R']}"+"\n"

class so(Surface):
    def __init__(self, surface_id, r, label=None):
        super().__init__(surface_id, 'SO', {'R': r}, label)

    def string(self):
        return f"{self.surface_id} SO {self.parameters['R']}"+"\n"