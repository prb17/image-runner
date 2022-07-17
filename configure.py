#!/usr/bin/python3


from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
import argparse
import logging
from logging import info, warning, debug, error
import sys

#logging dict
log_values = {'info': logging.INFO, 'warning': logging.WARN, 'debug': logging.DEBUG, 'error': logging.ERROR}

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--base-image', required=True, help='Desired image to pull')
    parser.add_argument('-r', '--registry', help="Desired base image registry to pull from. Default is my github registry", default="ghcr.io/prb17")
    parser.add_argument('-o', "--output-dir", help="desired location for the generated Dockerfile. Default is this current directory", default="./")
    parser.add_argument('-u', "--user", help="name of the user to be created in the image", default="img-rnr")
    parser.add_argument('-l', "--log-level", choices=list(log_values.keys()), help="desired level of logging", default="info")
    args = parser.parse_args()
    return args

def main():
    prog_args = get_args()
    logging.basicConfig(format="{asctime} [{levelname}] {message}", style='{', level=log_values[prog_args.log_level])

    #make sure registry doesn't have a trailing '/' character
    if prog_args.registry[-1] == '/':
        logging.error(f"Remove the trailing '/' from registry: '{prog_args.registry}'")
        sys.exit("Invalid registry name")

    logging.info("setting up jinja environment")
    env = Environment (
        loader=PackageLoader("__main__"),
        autoescape=select_autoescape()
    )
    

    pull_image = str(prog_args.registry) + "/" + str(prog_args.base_image)
    logging.info(f'pulling image: \'{pull_image}\'')
    dockerfile_template = "Dockerfile.jinja"
    composefile_template = "docker-compose.jinja"
    logging.debug(f'using Dockerfile template: \'{dockerfile_template}\'')
    logging.debug(f"using docker-compose template: '{composefile_template}'")
    # looks automatically in './templates' directory
    docker_template = env.get_template(dockerfile_template)
    compose_template = env.get_template(composefile_template)

    
    logging.info("rendering the Dockerfile and docker-compose.yml content based on the configuration values")
    dockerfile_contents = docker_template.render(pull_image=pull_image, user_name=prog_args.user)
    compose_contents = compose_template.render(pull_image=pull_image, user_name=prog_args.user)
    logging.debug(f'What will be written to the Dockerfile:\n\'{dockerfile_contents}\'')
    logging.debug(f"What will be written to the docker-compose.yml file:\n'{compose_contents}'")


    logging.info("saving configured templates to Dockerfile and docker-compose.yml")
    dockerfile_output = prog_args.output_dir + '/Dockerfile'
    with open(dockerfile_output, 'w') as file:
        file.write(dockerfile_contents + "\n")
    logging.debug(f'Dockerfile saved to: \'{dockerfile_output}\'')

    compose_output = prog_args.output_dir + '/docker-compose.yml'
    with open(compose_output, 'w') as file:
        file.write(compose_contents + "\n")
    logging.debug(f'docker-compose.yml saved to: \'{compose_output}\'')

    logging.info("Done")

if __name__ == "__main__":
    main()
