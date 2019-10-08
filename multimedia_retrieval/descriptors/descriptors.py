import open3d
import trimesh
import random
import sys
from math import pi
import numpy as np


from multimedia_retrieval.descriptors.helpers import get_eigen

from multimedia_retrieval.mesh_conversion.helpers import (trimesh_to_mesh,
                                                          mesh_to_trimesh)


# diameter
# eccentricity (ratio of largest to smallest eigenvalues of covariance matrix)
# Note that the definitions given in Module 4 are for 2D shapes. You need to adapt them to 3D shapes (easy).

def compute_global_descriptors(mesh):

    tri_mesh = mesh_to_trimesh(mesh)

    global_features = {}
    global_features['surface_area'] = tri_mesh.area
    global_features['compactness'] = compute_compactness(tri_mesh)
    global_features['bb_volume'] = tri_mesh.bounding_box.volume

    global_features['eccentricity'] = compute_eccentricity(mesh)


    # print(global_features)


def compute_local_descriptors(mesh):
    local_features = {}
    print(compute_angles(mesh, 200))



    return 0
# A3: angle between 3 random vertices
# D1: distance between barycenter and random vertex
# D2: distance between 2 random vertices
# D3: square root of area of triangle given by 3 random vertices
# D4: cube root of volume of tetrahedron formed by 4 random vertices


def compute_angles(mesh, samples):
    verts = mesh.vertices
    verts_len = len(mesh.vertices)

    angles = []

    for i in range(samples):
        pts = random.sample(range(0, verts_len), 3)
        v1 = pts[0]
        v2 = pts[1]
        v3 = pts[2]
        angles.append(compute_angle(verts[v1], verts[v2], verts[v3]))
    
    return angles


def compute_angle(v1, v2, v3):

    # Obtain the vector between v1 and v2 and v2 and v3.
    e = v1 - v2
    f = v2 - v3

    # Just the formula for an angle between two vectors.
    cos_angle = np.dot(e, f) / (np.linalg.norm(e) * np.linalg.norm(f))
    angle = np.arccos(cos_angle)

    # Convert radian to angles
    return np.degrees(angle)


def compute_compactness(tri_mesh):

    compactness = -1

    # Mesh should be watertight (and thus have a volume)
    if tri_mesh.is_volume:
        area = tri_mesh.area
        volume = tri_mesh.volume

        # Using the variant of compactness called sphericity
        compactness = ((pi ** (1/3)) * (6 * volume)**(2/3)) / area

    return compactness


def compute_eccentricity(mesh):
    val, vec = get_eigen(mesh)
    min_ev = val[0]
    max_ev = val[2]

    if min_ev == 0:
        min_ev += sys.float_info.min

    return max_ev / min_ev


def compute_diameter(mesh):
    val, vec = get_eigen(mesh)

    origin = np.array([0, 0, 0])
    largest_eigenvec = vec[:, 2]
    projections = []

    furthest_pos = - sys.maxsize
    furthest_neg = sys.maxsize

    furthest_proj = np.array([0, 0, 0])
    furthest_vert = np.array([0, 0, 0])

    for vert in tri_mesh.vertices:  
        res = get_vertex_projection(origin, largest_eigenvec, vert)
        # print(res)
        # dist = np.linalg.norm(res)
        # if furthest_dist < dist:
        #     furthest_dist = dist
        #     furthest_proj = res
        #     furthest_vert = vert

    
    # print('dist', furthest_dist)
    # print('projection', furthest_proj)
    # print('vertex', furthest_vert)

    # print(largest_eigenvec)
    




    
def get_vertex_projection(origin, eigenvec, vert):
    ap = vert - origin
    ab = eigenvec - origin
    return origin + np.dot(ap, ab) / np.dot(ab, ab) * ab




    
