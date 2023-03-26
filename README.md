# image-runner
Repo designed to pull/run specific, already built, docker images from a specific docker repo

`NOTE` this repo is designed for developers to run a dev docker image, and therefore mounts the users home directory into the image.
`NOTE` this repo assumes the developer is using bash

### Info on running an image

```
usage: configure.py [-h] -i BASE_IMAGE [-r REGISTRY] [-o OUTPUT_DIR] [-u USER] [-l {info,warning,debug,error}]

optional arguments:
  -h, --help            show this help message and exit
  -i BASE_IMAGE, --base-image BASE_IMAGE
                        Desired image to pull
  -r REGISTRY, --registry REGISTRY
                        Desired base image registry to pull from. Default is my github registry
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        desired location for the generated Dockerfile and docker-compose file. Default is this current directory
  -u USER, --user USER  name of the user to be created in the image
  -n IMAGE_NAME --image-name IMAGE_NAME "name of the local image to be created. Default is 'local-img-rnr'
  -l {info,warning,debug,error}, --log-level {info,warning,debug,error}
                        desired level of logging
```

### Example
```
mkdir dev

./configure.py -i ubuntu-dev -o dev
#This generates a Dockerfile and docker-compose file in a directory called `dev`.

dev/runner.sh
# This step build and runs the newly configured image and drops you in an interactive shell
NOTE: your home directory will be mounted in the container at this step.
```
