import docker 
client =docker.from_env()
IMAGE_NAME = "sandbox:latest"

def create_container(user_id:str,project_path):
    container= client.containers.run(
        image=IMAGE_NAME,
        command="sleep infinity",
        detach=True,
        tty=True,
        network_disabled=True,
        mem_limit="512m",
        cpu_period=100000,
        cpu_quota=50000,  # Limit to 50% of CPU
        ports={"8000/tcp": None},  # Expose port 8000
        volumes={
            project_path: {'bind': '/app', 'mode': 'rw'}
        },
        name = f"sandbox_{user_id}"
    )

    return container.id

def install_requirements(container_id):
    container = client.containers.get(container_id)
    exit_code, output = container.exec_run("pip install --no-cache-dir -r /app/requirements.txt")
    if exit_code != 0:
        raise Exception(f"Failed to install requirements: {output.decode()}")
    return output.decode()

def run_project(container_id):
    container= client.containers.get(container_id)
    cmd =  "uvicorn main:app --host 0.0.0.0 --port 8000"
    container.exec_run(cmd, detach=True)
    return "Project is running on port 8000"

def get_container_logs(container_id):
    container = client.containers.get(container_id)
    ports = container.attrs['NetworkSettings']['Ports']
    host_port = ports['8000/tcp'][0]['HostPort'] if ports and '8000/tcp' in ports else 'N/A'
    logs = container.logs().decode()
    return f"Container Logs:\n{logs}\n\nAccess the project at http://localhost:{host_port}"