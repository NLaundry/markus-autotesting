import os
import json
import subprocess


def create_environment(_settings, _env_dir, default_env_dir):
    return {"PYTHON": os.path.join(default_env_dir, "bin", "python3")}


def install():
    schema = settings()

    # Get the default value for the def file from the schema
    def_file = schema["properties"]["env_data"]["properties"][
        "image_definition_file_name"
    ]["default"]

    sif_file = os.path.splitext(def_file)[0] + ".sif"

    if not os.path.exists(sif_file):
        subprocess.run(["apptainer", "build", sif_file, def_file], check=True)


def settings():
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "settings_schema.json"
        )
    ) as f:
        return json.load(f)

