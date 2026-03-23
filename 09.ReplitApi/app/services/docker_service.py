# import docker 
# client =docker.from_env()
# IMAGE_NAME = "pysandbox:latest"

# def create_container(user_id:str,project_path):
#     #check for existing container with same name and remove it
#     container_name = f"sandbox_{user_id}"
#     try:
#         existing_container = client.containers.get(container_name)
#         existing_container.stop()
#         existing_container.remove()

#     except docker.errors.NotFound:
#         pass

#     container= client.containers.run(
#         image=IMAGE_NAME,
#         command="sleep infinity",
#         detach=True,
#         tty=True,
#         network_disabled=True,
#         mem_limit="512m",
#         cpu_period=100000,
#         cpu_quota=50000,  # Limit to 50% of CPU
#         ports={"8000/tcp": ("0.0.0.0", None)},  # 👈 FIX,  # Expose port 8000
#         volumes={
#             project_path: {'bind': '/app', 'mode': 'rw'}
#         },
#         name = f"sandbox_{user_id}"
#     )

#     return container.id

# def install_requirements(container_id):
#     container = client.containers.get(container_id)
#     exit_code, output = container.exec_run("pip install --no-cache-dir -r /app/requirements.txt")
#     if exit_code != 0:
#         raise Exception(f"Failed to install requirements: {output.decode()}")
#     return output.decode()

# def run_project(container_id):
#     container= client.containers.get(container_id)
#     #first check if container is running
#     # if container.status != "running":
#     #     container.start()
#     cmd =  "uvicorn main:app --host 0.0.0.0 --port 8000"
#     result =container.exec_run(cmd, detach=True)
#     print(f"exit code is :{result.exit_code}")
#     print(f"Container output is{result.output}")
#     return "Project is running on port 8000"

# def get_container_url(container_id):
#     container = client.containers.get(container_id)
#     ports = container.attrs['NetworkSettings']['Ports']
#     host_port = ports['8000/tcp'][0]['HostPort'] if ports and '8000/tcp' in ports else 'N/A'
#     logs = container.logs().decode()
#     return f"Container Logs:\n{logs}\n\nAccess the project at http://localhost:{host_port}"

# import time
# import docker

# client = docker.from_env()
# IMAGE_NAME = "pysandbox:latest"


# def create_container(user_id: str, project_path: str) -> str:
#     container_name = f"sandbox_{user_id}"
    
#     # Clean up any leftover container from a previous run
#     try:
#         existing = client.containers.get(container_name)
#         existing.stop()
#         existing.remove()
#     except docker.errors.NotFound:
#         pass

#     container = client.containers.run(
#         image=IMAGE_NAME,
#         command="sleep infinity",      # keeps container alive for exec_run calls
#         detach=True,
#         tty=True,
#         network_disabled=False,
#         mem_limit="512m",
#         cpu_period=100000,
#         cpu_quota=50000,
#         ports={"8000/tcp": ("0.0.0.0", None)},
#         volumes={project_path: {"bind": "/app", "mode": "rw"}},
#         name=container_name,
#     )
#     return container.id


# def install_requirements(container_id: str) -> str:
#     container = client.containers.get(container_id)
#     exit_code, output = container.exec_run(
#         "pip install --no-cache-dir -r /app/requirements.txt",
#         workdir="/app"
#     )
#     if exit_code != 0:
#         raise Exception(f"pip install failed:\n{output.decode()}")
#     return output.decode()


# def run_project(container_id: str) -> str:
#     container = client.containers.get(container_id)
    
#     # nohup detaches uvicorn from this exec session so it keeps running after exec exits
#     # stdout/stderr go to a log file because container.logs() only captures PID 1 output
#     container.exec_run(
#         "nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /app/uvicorn.log 2>&1 &",
#         workdir="/app",
#         detach=True
#     )
    
#     time.sleep(2)  # give uvicorn time to boot
    
#     _, log_output = container.exec_run("cat /app/uvicorn.log")
#     logs = log_output.decode()
    
#     if "Application startup complete" not in logs:
#         raise Exception(f"uvicorn may have failed:\n{logs}")
    
#     return logs


# def get_container_url(container_id: str) -> str:
#     container = client.containers.get(container_id)
#     ports = container.attrs["NetworkSettings"]["Ports"]
#     host_port = (
#         ports["8000/tcp"][0]["HostPort"]
#         if ports and "8000/tcp" in ports
#         else "N/A"
#     )
#     return f"http://localhost:{host_port}"


import time
import docker
from docker.errors import NotFound, APIError

client = docker.from_env()
IMAGE_NAME = "pysandbox:latest"


def create_container(user_id: str, project_path: str) -> str:
    container_name = f"sandbox_{user_id}"

    # Remove any leftover container from a previous session
    try:
        existing = client.containers.get(container_name)
        existing.stop()
        existing.remove()
    except docker.errors.NotFound:
        pass

    container = client.containers.run(
        image=IMAGE_NAME,
        # sleep infinity keeps the container alive so we can exec_run into it.
        # This overrides CMD in the Dockerfile entirely — that's intentional.
        command="sleep infinity",
        detach=True,
        tty=True,
        network_disabled=False,   # needs network for pip install
        mem_limit="512m",
        cpu_period=100000,
        cpu_quota=50000,          # 0.5 CPU
        ports={"8000/tcp": ("0.0.0.0", None)},  # Docker picks a free host port
        volumes={project_path: {"bind": "/app", "mode": "rw"}},
        name=container_name,
    )
    return container.id


def install_requirements(container_id: str) -> str:
    container = client.containers.get(container_id)

    exit_code, output = container.exec_run(
        "pip install --no-cache-dir -r /app/requirements.txt",
        workdir="/app"
    )
    decoded = output.decode()

    if exit_code != 0:
        raise Exception(f"pip install failed:\n{decoded}")

    return decoded


def run_project(container_id: str) -> str:
    container = client.containers.get(container_id)

    # Sanity check — make sure uvicorn is actually available in the container
    exit_code, output = container.exec_run("which uvicorn")
    if exit_code != 0:
        raise Exception(
            "uvicorn not found in container. "
            "Make sure it's in requirements.txt or baked into the image."
        )

    # setsid creates a new process session so uvicorn keeps running
    # after this exec session ends — nohup is not available in slim images.
    # Output is redirected to a log file because container.logs() only
    # captures PID 1 (sleep infinity) output, not exec children.
    container.exec_run(
        cmd=[
            "/bin/sh", "-c",
            "setsid uvicorn main:app --host 0.0.0.0 --port 8000 > /app/uvicorn.log 2>&1 &"
        ],
        workdir="/app",
        detach=True
    )

    # Give uvicorn time to boot before checking the log
    time.sleep(3)

    # Read the log file to verify startup
    exit_code, output = container.exec_run("cat /app/uvicorn.log")

    if exit_code != 0:
        # Log file doesn't exist at all — setsid/uvicorn command itself failed
        raw_logs = container.logs().decode()
        raise Exception(
            f"uvicorn.log was never created — command likely failed.\n"
            f"Container PID 1 logs:\n{raw_logs}"
        )

    logs = output.decode()

    if "Application startup complete" not in logs:
        raise Exception(f"uvicorn started but application failed to load:\n{logs}")

    return logs


def get_container_url(container_id: str) -> str:
    container = client.containers.get(container_id)

    # Reload attrs to get the latest network info after the container started
    container.reload()

    ports = container.attrs["NetworkSettings"]["Ports"]

    if not ports or "8000/tcp" not in ports or ports["8000/tcp"] is None:
        raise Exception("Port 8000 is not mapped — container may not have started correctly.")

    host_port = ports["8000/tcp"][0]["HostPort"]
    return f"http://localhost:{host_port}"


def stop_container(container_id: str) -> None:
    try:
        container = client.containers.get(container_id)
        container.stop(timeout=10)
        container.remove(force=True)
    except NotFound:
        pass
    except APIError as e:
        print(f"[docker] warning: could not stop {container_id}: {e}")


def get_logs(container_id: str) -> str:
    """Read uvicorn's log file directly — container.logs() won't show it."""
    container = client.containers.get(container_id)
    exit_code, output = container.exec_run("cat /app/uvicorn.log")
    if exit_code != 0:
        return "No log file found."
    return output.decode()