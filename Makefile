build:
		docker build --network host --no-cache -t bliptrip/opensfm:detectron2-pytorch-2.1.1-cuda12.2-cudnn8-runtime -f Dockerfile.ceres2 .

build.amend:
		docker build --network host --no-cache -t bliptrip/opensfm:detectron2-pytorch-2.1.1-cuda12.2-cudnn8-runtime -f Dockerfile.ceres2.amend .

run:
		docker run -it --rm --network host -v $(PWD):/local bliptrip/opensfm:detectron2-pytorch-2.1.1-cuda12.2-cudnn8-runtime /bin/bash

push:
		docker push bliptrip/opensfm:detectron2-pytorch-2.1.1-cuda12.2-cudnn8-runtime

pull:
		docker pull bliptrip/opensfm:detectron2-pytorch-2.1.1-cuda12.2-cudnn8-runtime

