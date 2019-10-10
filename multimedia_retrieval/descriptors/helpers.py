import numpy as np
import open3d
import trimesh
import random


def sample_points(mesh, sample_size, num_points, func, **kwargs):
    res = []
    verts_len = len(mesh.vertices)

    for i in range(sample_size):
        pts = random.sample(range(0, verts_len), num_points)
        res.append(func(mesh, pts, **kwargs))
    return res


def get_eigen(mesh):
    vertices = mesh.vertices
    return np.linalg.eigh(np.cov(vertices, rowvar=False))


def compute_tetrahedron_volumes(mesh, sample_size):
    return sample_points(mesh, sample_size, 4, compute_tetrahedron_volume)


def compute_tetrahedron_volume(mesh, pts, **kwargs):
    verts = mesh.vertices
    
    v1 = verts[pts[0]]
    v2 = verts[pts[1]]
    v3 = verts[pts[2]]
    v4 = verts[pts[3]]

    v1v4 = v1 - v4
    v2v4 = v2 - v4
    v3v4 = v3 - v4
    
    volume = np.cbrt(np.abs(np.dot(v1v4, (np.cross(v2v4, v3v4)))) / 6)
    return volume



def compute_triangle_areas(tri_mesh, sample_size):
    return sample_points(tri_mesh, sample_size, 3, compute_triangle_area)
    

def compute_triangle_area(tri_mesh, pts, **kwargs):
    verts = tri_mesh.vertices

    v1 = verts[pts[0]]
    v2 = verts[pts[1]]
    v3 = verts[pts[2]]

    arr = [np.asarray((v1, v2, v3))]
   
    return np.sqrt(np.asscalar(trimesh.triangles.area(arr)))


def compute_dist(mesh, pts, **kwargs):
    
    verts = mesh.vertices

    v1 = verts[pts[0]]
    v2 = []
    if kwargs:
        v2 = kwargs['centroid']
    else:
        v2 = verts[pts[1]]

    return np.linalg.norm(np.asarray(v1) - np.asarray(v2))


def compute_dists(mesh, sample_size, is_d1=True):
    if is_d1:
        centroid = mesh.get_center()
        return sample_points(mesh, sample_size, 1, compute_dist, 
                             centroid=centroid)
    else:
        return sample_points(mesh, sample_size, 2, compute_dist)


def compute_angles(mesh, sample_size):
    return sample_points(mesh, sample_size, 3, compute_angle)


def compute_angle(mesh, pts, **kwargs):

    verts = mesh.vertices

    v1 = verts[pts[0]]
    v2 = verts[pts[1]]
    v3 = verts[pts[2]]

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
    return min(mesh.get_max_bound() - mesh.get_min_bound())





    
