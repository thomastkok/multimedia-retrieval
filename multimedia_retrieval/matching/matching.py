from .distances import euclidean


def match_shapes(mesh, dataset, mesh_feat, ds_feat, k=None):
    # Get features for mesh
    # Get features for all meshes in dataset (pre-calculated)
    # For now, both are parameters
    # Compute distance between query mesh and all meshes in dataset
    results = {}
    for data_point in ds_feat:
        dist = euclidean(mesh_feat, ds_feat[data_point])
        results[data_point] = dist
    # Sort distances from low to high
    # Return the k best matching shapes
    if not k:
        return sorted(results, key=results.get)
    else:
        return sorted(results, key=results.get)[:k]
