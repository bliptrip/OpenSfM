import logging
import os

import numpy as np

from opensfm import dataset
from opensfm import io
from opensfm.dense import depthmap_to_ply, scale_down_image
from . import command


logger = logging.getLogger(__name__)


class Command(command.CommandBase):
    def __init__(self):
        super(Command, self).__init__()
        self.name = "export_ply"
        self.help = "Export reconstruction to PLY format"

        self.args["--no-cameras"] = {
            "help": "Do not save camera positions",
            "action": "store_true",
            "default": False,
        }
        self.args["--no-points"] = {
            "help": "Do not save points",
            "action": "store_true",
            "default": False,
        }
        self.args["--depthmaps"] = {
            "help": "Export per-image depthmaps as pointclouds",
            "action": "store_true",
            "default": False,
        }

    def run_dataset(self, options, data):
        reconstructions = data.load_reconstruction()
        no_cameras = options.no_cameras
        no_points = options.no_points

        if reconstructions:
            data.save_ply(reconstructions[0], None, no_cameras, no_points)

        if options.depthmaps and reconstructions:
            udata = dataset.UndistortedDataSet(data, 'undistorted')
            for id, shot in reconstructions[0].shots.items():
                rgb = udata.load_undistorted_image(id)
                for t in ('clean', 'raw'):
                    path_depth = udata._depthmap_file(id, t + '.npz')
                    if not os.path.exists(path_depth):
                        continue
                    depth = np.load(path_depth)['depth']
                    rgb = scale_down_image(rgb, depth.shape[1], depth.shape[0])
                    ply = depthmap_to_ply(shot, depth, rgb)
                    with io.open_wt(udata._depthmap_file(id, t + '.ply')) as fout:
                        fout.write(ply)
