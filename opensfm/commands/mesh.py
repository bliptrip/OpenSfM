import logging
import time

from opensfm import mesh
from . import command


logger = logging.getLogger(__name__)


class Command(command.CommandBase):
    def __init__(self):
        super(Command, self).__init__()
        self.name = "mesh"
        self.help = "Add delaunay meshes to the reconstruction"

    def run_dataset(self, options, data):
        start = time.time()
        tracks_manager = data.load_tracks_manager()
        reconstructions = data.load_reconstruction()

        all_shot_ids = set(tracks_manager.get_shot_ids())
        for r in reconstructions:
            for shot in r.shots.values():
                if shot.id in all_shot_ids:
                    vertices, faces = mesh.triangle_mesh(
                        shot.id, r, tracks_manager, data)
                    shot.mesh.vertices = vertices
                    shot.mesh.faces = faces

        data.save_reconstruction(reconstructions,
                                    filename='reconstruction.meshed.json',
                                    minify=True)

        end = time.time()
        with open(data.profile_log(), 'a') as fout:
            fout.write('mesh: {0}\n'.format(end - start))
