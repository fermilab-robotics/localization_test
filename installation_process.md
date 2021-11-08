# Installation process

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
