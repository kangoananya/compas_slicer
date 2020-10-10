import os
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter
from compas_slicer.slicers import PlanarSlicer
from compas_slicer.functionality import simplify_paths_rdp
from compas_slicer.functionality import sort_per_shortest_path_mlrose
from compas_slicer.functionality import align_seams
from compas_viewers.objectviewer import ObjectViewer

######################## Logging
import logging

logger = logging.getLogger('logger')
logging.basicConfig(format='%(levelname)s-%(message)s', level=logging.INFO)
######################## 

DATA = os.path.join(os.path.dirname(__file__), 'data')
FILE = os.path.abspath(os.path.join(DATA, 'vase.obj'))

def main():
    ### --- Load compas_mesh
    compas_mesh = Mesh.from_obj(os.path.join(DATA, FILE))

    ### --- Slicer
    slicer = PlanarSlicer(compas_mesh, slicer_type="planar_numpy", layer_height=10.0)
    slicer.slice_model()
    slicer.printout_info()

    simplify_paths_rdp(slicer, threshold=0.2)
    sort_per_shortest_path_mlrose(slicer, max_attempts=4 )
    align_seams(slicer)

    slicer.layers_to_json(filepath=DATA, name="slicer_data.json")

    ### ----- Visualize on viewer
    viewer = ObjectViewer()
    viewer.view.use_shaders = False
    slicer.visualize_on_viewer(viewer, visualize_mesh=False, visualize_paths=True)
    viewer.update()
    viewer.show()

if __name__ == "__main__":
    main()
