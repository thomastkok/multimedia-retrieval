import numpy as np


def get_eigen(mesh):
    vertices = mesh.vertices
    return np.linalg.eigh(np.cov(vertices, rowvar=False))
