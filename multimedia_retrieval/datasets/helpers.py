import open3d
import trimesh


def mesh_to_trimesh(mesh):
    open3d.io.write_triangle_mesh("temp.ply", mesh)
    tri_mesh = trimesh.load_mesh("temp.ply")
    return tri_mesh


def trimesh_to_mesh(tri_mesh):
    trimesh.exchange.export.export_mesh(tri_mesh, 'temp.ply', 'ply')
    mesh = open3d.io.read_triangle_mesh('temp.ply')
    return mesh


def refine_outliers(mesh, file_path, is_small, is_triangles, dataset):
    """
    Refines the outliers
    By dividing the triangles or merging them using trimesh.
    """

    # open3d.visualization.draw_geometries([mesh])
    # tri_mesh.show();

    tri_mesh = mesh_to_trimesh(mesh)
    refined_mesh = None

    if is_small and is_triangles or is_small and not is_triangles:
        refined_mesh = tri_mesh.subdivide().subdivide()
    elif not is_small and is_triangles or not is_small and not is_triangles:
        if dataset == 'princeton':
            tri_mesh.merge_vertices(2)
        elif dataset == 'labeled':
            tri_mesh.merge_vertices(1)

        # Removing faces which do not have 3 unique vertex indices.
        tri_mesh.remove_degenerate_faces()
        tri_mesh.remove_duplicate_faces()
        refined_mesh = tri_mesh

    return trimesh_to_mesh(refined_mesh)

    if (len(refined_mesh.vertices) < 100 or
            len(refined_mesh.vertices) > 50000 or
            len(refined_mesh.triangles) < 100 or
            len(refined_mesh.triangles) > 50000):
         
        print('Path', file_path)
        print('Triangles', len(refined_mesh.triangles))
        print('Vertices', len(refined_mesh.vertices))
