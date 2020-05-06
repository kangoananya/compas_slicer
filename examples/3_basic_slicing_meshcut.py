import compas
import compas_am
import os
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

from compas_am.slicing.slicer import Slicer
from compas_am.input.input_geometry import InputGeometry

import meshcut
import stl
import numpy as np

######################## Logging
import logging
logger = logging.getLogger('logger')
logging.basicConfig(format='%(levelname)s-%(message)s', level=logging.INFO)
######################## 

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
FILE = os.path.abspath(os.path.join(DATA, 'eight_eight.stl'))


def main():

    ### --- Load stl
    compas_mesh = Mesh.from_stl(FILE)

    ### --- Slicer
    slicer = Slicer(compas_mesh, slicer_type = "planar_meshcut", layer_height = 1.0)

    slicer.slice_model(create_contours = True, create_infill = False, create_supports = False)

    slicer.simplify_paths(threshold = 0.3)

    slicer.sort_paths(sorting_type = "shortest_path")

    slicer.align_seams(seam_alignment = "align_seams")

    slicer.printout_info()

    slicer.save_contours_to_json(path = DATA, name = "eight_eight_contours.json")


    ### ----- Visualize 

    mesh = Mesh.from_stl(FILE)

    plotter = MeshPlotter(mesh, figsize=(16, 10))
    plotter.draw_edges(width=0.15)
    plotter.draw_faces()
    plotter.draw_lines(slicer.get_contour_lines_for_plotter(color = (255,0,0)))
    plotter.show()


if __name__ == "__main__":
    main()