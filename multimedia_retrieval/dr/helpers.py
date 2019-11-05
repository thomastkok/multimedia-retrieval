import matplotlib.colors as mpl_colors
import matplotlib.pyplot as plt
import numpy as np

from multimedia_retrieval.evaluation.evaluation import get_labels


def unpack_feature_db(feature_db):
    """
    Given a feature database as a dataframe,
    unpack the values such that it is a list of feature vectors
    """
    #  Get unique classes and assign to them a number (index).
    labels = get_labels()
    unique_labels = set(labels.values())
    class_indices = list(range(0, len(unique_labels)))
    class_labels = dict(zip(unique_labels, class_indices))

    nr_bins = 10

    features = []
    indices_classes = []
    mesh_ids = []

    for index, row in feature_db.iterrows():
        # Classname
        mesh_class = labels[f"{index}"]
        indices_classes.append(class_labels[mesh_class])
        mesh_ids.append(index)
        feature_vect = []
        for col_name in feature_db.columns:
            #  Its a histogram
            if isinstance(row[col_name], tuple):
                hist_vals = row[col_name][0]
                for val in hist_vals:
                    feature_vect.append(val / nr_bins)
            else:
                feature_vect.append(row[col_name])
        features.append(feature_vect[0:45])

    return features, indices_classes, mesh_ids, unique_labels


def plot_embedding(X, labels, mesh_ids, nr_classes, title=None):
    """
    Plots the 2D data of the T-SNE procedure.
    """

    classes = get_labels()

    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    # Color map
    cmap = plt.cm.jet

    # Normalize values between 0 and 19 for color map.
    norm = mpl_colors.Normalize(0, nr_classes)
    fig, ax = plt.subplots()

    # Use colors of color map jet and assign to each class a color.
    colors = plt.cm.jet(np.linspace(0, 1, nr_classes))

    scatter = ax.scatter(x=X[:, 0], y=X[:, 1], c=labels, cmap=cmap,
                         alpha=0.6, edgecolors='none')

    # Create tooltip with its properties for annotation.
    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    ax.set_title('Scatterplot of T-SNE procedure')

    # Connects function to event manager
    fig.canvas. mpl_connect("motion_notify_event", lambda event: hover(
        fig, scatter, annot, ax, event, norm, cmap, labels, mesh_ids, classes))
    plt.show()

    if title is not None:
        plt.title(title)


def update_annot(scatter, annot, ind, norm, cmap, labels, mesh_ids, classes):
    """
    Update the tooltip with the correct mesh_id and class name.
    """
    idx = ind["ind"][0]
    mesh_id = mesh_ids[idx]

    pos = scatter.get_offsets()[idx]
    annot.xy = pos
    text = f"mesh: {mesh_id}, class: {classes[str(mesh_id)]}"
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(norm(labels[idx])))
    annot.get_bbox_patch().set_alpha(0.6)


def hover(fig, scatter, annot, ax, event, norm, cmap,
          labels, mesh_ids, classes):
    """
    Implements a hover event that call the update annot function.
    Continuously checks whether the mouse is on hovered on a point.
    """
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = scatter.contains(event)
        if cont:
            update_annot(scatter, annot, ind, norm,
                         cmap, labels, mesh_ids, classes)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()
