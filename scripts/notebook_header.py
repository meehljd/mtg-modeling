"""This helper script is run as a header in the Jupyter Notebooks."""

# pylint: disable=undefined-variable, unused-import

import sys
import os
from pathlib import Path
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(
    description="Update working directory to project root."
)
parser.add_argument(
    "--path", type=str, default=None, help="Path to set as the working directory."
)
args = parser.parse_args()

# Convert the provided path to an absolute path
script_path = Path(args.path).resolve()

# Ensure the path ends with './scripts/notebook_header.py'
if script_path.name != "notebook_header.py" or "scripts" not in script_path.parts:
    raise ValueError(
        "The provided path must point to 'notebook_header.py' within a 'scripts' directory."
    )

# Get the parent directory of the './scripts/' directory
project_root = script_path.parents[1]

# Change the working directory to the project root
os.chdir(project_root)
print(f"Changed working directory to: {project_root}")


# Autoreload modules
if "IPython.extensions.autoreload" not in get_ipython().extension_manager.loaded:  # type: ignore
    get_ipython().run_line_magic("load_ext", "autoreload")  # type: ignore
    get_ipython().run_line_magic("autoreload", "2")  # type: ignore
