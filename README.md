# image-runner
Repo designed to pull/run specific, already built, docker images from a specific docker repo

`NOTE` this repo is designed for developers to run a dev docker image, and therefore mounts the users home directory into the image.

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
  -l {info,warning,debug,error}, --log-level {info,warning,debug,error}
                        desired level of logging
```

### Example
`./configure.py -i ubuntu-dev -o test`
This generates a Dockerfile and docker-compose file in a directory called `test`.
