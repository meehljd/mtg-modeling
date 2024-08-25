"""This helper script is run as a header in the Jupyter Notebooks."""

# pylint: disable=undefined-variable, unused-import

import sys
import os
from pathlib import Path


# Define project root
project_root = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))


# Change the working directory to the project root
os.chdir(project_root)
print(f"Changed working directory to: {project_root}")


# Autoreload modules
if "IPython.extensions.autoreload" not in get_ipython().extension_manager.loaded:  # type: ignore
    get_ipython().run_line_magic("load_ext", "autoreload")  # type: ignore
    get_ipython().run_line_magic("autoreload", "2")  # type: ignore
