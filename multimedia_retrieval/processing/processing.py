from helpers import translate_to_origin, scale_to_unit


def normalization_tool(meshes):
    for mesh in meshes:
        translate_to_origin(mesh)
        scale_to_unit(mesh)
