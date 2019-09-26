import open3d
import trimesh
from math import pi

from multimedia_retrieval.mesh_conversion.helpers import (trimesh_to_mesh,
                                                          mesh_to_trimesh)


# surface area
# compactness (with respect to a sphere)
# axis-aligned bounding-box volume
# diameter
# eccentricity (ratio of largest to smallest eigenvalues of covariance matrix)
# Note that the definitions given in Module 4 are for 2D shapes. You need to adapt them to 3D shapes (easy).

def compute_global_descriptors(mesh):

    tri_mesh = mesh_to_trimesh(mesh)


    mesh_features = {}
    mesh_features['surface_area'] = tri_mesh.area
    mesh_features['compactness'] = compute_compactness(tri_mesh)

    print(mesh_features)


def compute_compactness(tri_mesh):

    compactness = -1

    # Mesh should be watertight (and thus have a volume)
    if tri_mesh.is_volume:
        area = tri_mesh.area
        volume = tri_mesh.volume

        # Using the variant of compactness called sphericity
        compactness = ((pi ** (1/3)) * (6 * volume)**(2/3)) / area

    return compactness




    
