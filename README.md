# Spot development environment

This is a template repository for Spot development. When used with VSCode and a container environment like Docker, this repo provides all the necessary components to interact with a Spot robot.

This project can then be deployed to Spot as-is. <https://dev.bostondynamics.com/docs/payload/docker_containers.html>

## Getting started

VSCode and a container environment is required for this to work.

1. Clone this repository as a starting place for development.

1. Set the git remote to a new repository.

1. Install a container environment and VSCode extension

    <https://code.visualstudio.com/docs/remote/containers#_installation>

    <https://code.visualstudio.com/docs/remote/containers-tutorial#_install-the-extension>

1. Remote-Containers: Reopen in Container

## Package installation process

1. Install BD packages

    *Note:* This step is handled by the container environment if you are using `.devcontaainer` in VSCode.

    ```bash
    python3 -m pip install --upgrade bosdyn-client bosdyn-mission bosdyn-choreography-client
    ```

1. Verify installation

    ```bash
    python3 -m pip list --format=columns | grep bosdyn
    ```

    Expected output

    ```bash
    bosdyn-api                    3.0.1
    bosdyn-choreography-client    3.0.1
    bosdyn-choreography-protos    3.0.1
    bosdyn-client                 3.0.1
    bosdyn-core                   3.0.1
    bosdyn-mission                3.0.1
    ```

    Start Python repl

    ```python:repl
    >>> import bosdyn.client
    >>> help(bosdyn.client)
    ```

    Expect documentation output and not an error.

1. Fix versions with a requirements file

    *Note:* This shouldn't be needed if you are using the `.devcontainer` as the container always uses the most recent package versions.

    ```bash
    pip3 freeze > requirements.txt
    ```
