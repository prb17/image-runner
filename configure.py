#!/usr/bin/python3


from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
import argparse
import logging
from logging import info, warning, debug, error
import sys
import os

#logging dict
log_values = {'info': logging.INFO, 'warning': logging.WARN, 'debug': logging.DEBUG, 'error': logging.ERROR}

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--base-image', required=True, help='Desired image to pull')
    parser.add_argument('-r', '--registry', help="Desired base image registry to pull from. Default is my github registry", default="ghcr.io/prb17")
    parser.add_argument('-o', "--output-dir", help="desired location for the generated Dockerfile and docker-compose file. Default is this current directory", default="./")
    parser.add_argument('-u', "--user", help="name of the user to be created in the image", default="img-rnr")
    parser.add_argument('-n', "--image-name", help="name of the local image to be created", default="local-img-rnr")
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
        loader=PackageLoader("configure"),
        autoescape=select_autoescape()
    )
    

    pull_image = str(prog_args.registry) + "/" + str(prog_args.base_image)
    logging.info(f'pulling image: \'{pull_image}\'')
    dockerfile_template = "Dockerfile.jinja"
    composefile_template = "docker-compose.jinja"
    runner_template = "runner.jinja"
    logging.debug(f'using Dockerfile template: \'{dockerfile_template}\'')
    logging.debug(f"using docker-compose template: '{composefile_template}'")
    logging.debug(f"using run template: '{runner_template}'")

    # looks automatically in './templates' directory
    docker_template = env.get_template(dockerfile_template)
    compose_template = env.get_template(composefile_template)
    runner_template = env.get_template(runner_template)

    
    logging.info("rendering the content based on the configuration values")
    dockerfile_contents = docker_template.render(pull_image=pull_image)
    compose_contents = compose_template.render(pull_image=pull_image, 
                                                base_image=prog_args.base_image,
                                                user_name=prog_args.user,
                                                local_image_name=prog_args.image_name,
                                                docker_context=prog_args.output_dir,
                                                user_id=os.getuid(),
                                                group_id=os.getgid())
    runner_contents = runner_template.render(docker_context=prog_args.output_dir)
    logging.debug(f'What will be written to the Dockerfile:\n\'{dockerfile_contents}\'')
    logging.debug(f"What will be written to the docker-compose.yml file:\n'{compose_contents}'")
    logging.debug(f"What will be written to the runner.sh file:\n'{runner_contents}'")


    logging.info("saving configured templates to Dockerfile and docker-compose.yml")
    dockerfile_output = prog_args.output_dir + './Dockerfile'
    with open(dockerfile_output, 'w') as file:
        file.write(dockerfile_contents + "\n")
    logging.debug(f'Dockerfile saved to: \'{dockerfile_output}\'')

    compose_output = prog_args.output_dir + './docker-compose.yml'
    with open(compose_output, 'w') as file:
        file.write(compose_contents + "\n")
    logging.debug(f'docker-compose.yml saved to: \'{compose_output}\'')

    runner_output = prog_args.output_dir + './runner.sh'
    with open(runner_output, 'w') as file:
        file.write(runner_contents + "\n")
        os.chmod(runner_output, 0o500)
    logging.debug(f'runner.sh saved to: \'{runner_output}\'')

    logging.info("Done")

if __name__ == "__main__":
    main()
