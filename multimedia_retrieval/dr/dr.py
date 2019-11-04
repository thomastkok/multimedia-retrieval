from sklearn import manifold

from .helpers import unpack_feature_db, plot_embedding


def dimensionality_reduction(feature_db):
    """
    Perform dimensionality reduction in the form of T-SNE.
    """

    features, labels, mesh_ids, unique_labels = unpack_feature_db(feature_db)

    tsne = manifold.TSNE(init="pca", perplexity=19, learning_rate=200)
    feature_tsne = tsne.fit_transform(features)

    plot_embedding(feature_tsne, labels, mesh_ids, len(unique_labels))
