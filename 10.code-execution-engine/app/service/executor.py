from app.service.docker_runner import run_in_docker

SUPPORTED_LANGUAGES = {
    "python": "python_runner",
    "javascript": "node_runner"
}


def execute_code(language:str, code:str, input_data:str):
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    image_name = SUPPORTED_LANGUAGES[language]
    try:
        output = run_in_docker(image_name, code, input_data,language)
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}