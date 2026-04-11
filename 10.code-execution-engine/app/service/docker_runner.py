# import docker
# import uuid
# import os
# import tempfile

# client = docker.from_env()

# # TEMP_DIR = os.path.join(tempfile.gettempdir(), "code_exec")
# # print(f"Using temporary directory: {TEMP_DIR}")
# # os.makedirs(TEMP_DIR, exist_ok=True)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# TEMP_DIR = os.path.join(BASE_DIR, "temp_jobs")
# print(f"Using temporary directory: {TEMP_DIR}")
# os.makedirs(TEMP_DIR, exist_ok=True)

# def run_in_docker(image_name: str, code: str, input_data: str, language: str):
#     job_id = str(uuid.uuid4())
#     job_dir = os.path.join(TEMP_DIR, job_id)
#     print(f"Creating job directory: {job_dir}")
#     os.makedirs(job_dir, exist_ok=True)

#     extensions = {"python": "code.py", "javascript": "code.js"}
#     with open(os.path.join(job_dir, extensions[language]), "w") as f:
#         f.write(code)
#     with open(os.path.join(job_dir, "input.txt"), "w") as f:
#         f.write(input_data)

#     container = client.containers.run(
#         image=image_name,
#         volumes={job_dir: {'bind': '/app', 'mode': 'rw'}},
#         command="sh /run.sh",
#         mem_limit="512m",
#         cpu_period=100000,
#         cpu_quota=50000,
#         network_disabled=True,
#         detach=True
#     )

#     container.wait()
#     result = container.logs().decode('utf-8')
#     container.remove(force=True)
#     return result

# import docker
# import uuid
# import os

# client = docker.from_env()

# TEMP_DIR = "/temp_jobs"
# os.makedirs(TEMP_DIR, exist_ok=True)

# def run_in_docker(image_name: str, code: str, input_data: str, language: str):
#     job_id = str(uuid.uuid4())
#     job_dir = f"/temp_jobs/{job_id}"
#     os.makedirs(job_dir, exist_ok=True)

#     extensions = {"python": "code.py", "javascript": "code.js"}
#     with open(f"{job_dir}/{extensions[language]}", "w") as f:
#         f.write(code)
#     with open(f"{job_dir}/input.txt", "w") as f:
#         f.write(input_data)

#     container = client.containers.run(
#         image=image_name,
#         volumes={job_dir: {'bind': '/app', 'mode': 'rw'}},
#         command="sh /run.sh",
#         mem_limit="512m",
#         cpu_period=100000,
#         cpu_quota=50000,
#         network_disabled=True,
#         detach=True
#     )

#     container.wait()
#     result = container.logs().decode('utf-8')
#     container.remove(force=True)
#     return result


import docker
import uuid
import os

client = docker.from_env()

TEMP_DIR = "/temp_jobs"
os.makedirs(TEMP_DIR, exist_ok=True)

def run_in_docker(image_name: str, code: str, input_data: str, language: str):
    job_id = str(uuid.uuid4())
    job_dir = f"/temp_jobs/{job_id}"
    os.makedirs(job_dir, exist_ok=True)

    extensions = {"python": "code.py", "javascript": "code.js"}
    with open(f"{job_dir}/{extensions[language]}", "w") as f:
        f.write(code)
    with open(f"{job_dir}/input.txt", "w") as f:
        f.write(input_data)

    container = client.containers.run(
        image=image_name,
        command="sh /run.sh",
        volumes_from=["api"],  # ← inherit volumes from api container
        working_dir=job_dir,
        environment={"JOB_DIR": job_dir},
        mem_limit="512m",
        cpu_period=100000,
        cpu_quota=50000,
        network_disabled=True,
        detach=True
    )

    container.wait()
    result = container.logs().decode('utf-8')
    container.remove(force=True)
    return result