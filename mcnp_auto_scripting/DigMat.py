import numpy as np

# x_walls: np.array([x1, x2, x3, ... xn]) where xi is a float value
# y_walls: np.array([y1, y2, y3, ... yn]) where yi is a float value
# z_walls: np.array([z1, z2, z3, ... zn]) where zi is a float value
# f(X): a function that takes in x, y, z coordinates as np.array shape: (n, 3) and returns a numpy array of shape: (n, c), c being the number of characteristics

# each section has 6 walls 2x, 2y, 2z
# for the walls, we want to uniformly randomly sample points within the walls


def make_sections(x_walls, y_walls, z_walls):
    # return a numpy array of shape (sections, 6) with the 6 part being for each wall
    # eg one section is [0, 1, 10, 11, 20, 21]
    x0, x1 = x_walls[:-1], x_walls[1:]
    y0, y1 = y_walls[:-1], y_walls[1:]
    z0, z1 = z_walls[:-1], z_walls[1:]

    # Create meshgrid for all combinations
    xx0, yy0, zz0 = np.meshgrid(x0, y0, z0, indexing='ij')
    xx1, yy1, zz1 = np.meshgrid(x1, y1, z1, indexing='ij')

    # Stack and reshape to (sections, 6)
    sections = np.stack([
        xx0.ravel(), xx1.ravel(),
        yy0.ravel(), yy1.ravel(),
        zz0.ravel(), zz1.ravel()
    ], axis=1)
    return sections

def sample_sections(f, sections, n_samples=100):
    # sections: (n, 6) array where each row is [x0, x1, y0, y1, z0, z1]
    x0, x1 = sections[:, 0], sections[:, 1]
    y0, y1 = sections[:, 2], sections[:, 3]
    z0, z1 = sections[:, 4], sections[:, 5]

    # Shape: (sections, n_samples)
    x_samples = np.random.uniform(x0[:, None], x1[:, None], size=(sections.shape[0], n_samples))
    y_samples = np.random.uniform(y0[:, None], y1[:, None], size=(sections.shape[0], n_samples))
    z_samples = np.random.uniform(z0[:, None], z1[:, None], size=(sections.shape[0], n_samples))

    # Shape: (sections * n_samples, 3)
    points = np.stack([x_samples, y_samples, z_samples], axis=-1).reshape(-1, 3)

    # Apply f to all points, then reshape back to (sections, n_samples, c)
    results = f(points).reshape(sections.shape[0], n_samples, -1)
    # average
    return results.mean(axis=1)