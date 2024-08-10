# Introduction

Modeling of aspects of the Magic: The Gathering game.  I will explore aspects of the game, such as latent card strength, deck strength, card scarcity, and card prices.

For more in-depth discussion on the topic, please refer to the [Introduction Notebook](notebooks/00-introduction.ipynb).


# Installation

This instructions assume you are running in WSL on a windows machine with VS Code.  

For Windows, run via [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) to support packages such as JAX.  We will use the [miniconda distribution of conda](https://docs.anaconda.com/miniconda/), since some packages, such as PyMC, are a pain to install via poetry.

Note that some distributions of WSL, like Alpine, don't support conda on a fresh install.  Recommend using Ubuntu.  



## Install Git (if needed)
```bash
apt update
sudo apt install -y git
git config --global user.name "Josh Meehl"
git config --global user.email "joshua@meehl.org"
```

## Clone Repo
To clone the git repository:

```bash
git clone https://github.com/meehljd/dl+bayes-template.git

```

## Install Conda (if needed)

Ideally I would use `poetry`, but is problematic with `pymc`.  So using `conda` instead.

If needed, install conda:
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
source ~/.bashrc

```

## Setup Conda Environment

Setup conda Environment.  Using mamba is faster than vanilla conda.

Note this is _not_ a lean environment.  Was ~7gb when last checked.

```bash
conda install -y mamba -n base -c conda-forge
mamba env create -f environment.yml # or `mamba env update -f environment.yml`
conda activate dl+bayes-env
python scripts/test_imports.py # test installs
```

## Install Additional Dependencies

Here are some additional dependencies that less straightforward to install:

```bash
# PyG: Additional library.  "dirty" pip install, since doesn't work with conda
pip install pyg-lib -f https://data.pyg.org/whl/torch-2.2.0+cu121.html 

# PyMC: Very much helps with optimal performance
apt update
sudo apt install -y g++

# GraphViz:  Visualization of graph structures
sudo apt install -y graphviz # also needs python-graphviz via conda.

# ...I can't remember what this one helps with...
sudo apt install -y xdg-utils

# Install nodejs for SQLTools extension in VS Code
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y
'''
