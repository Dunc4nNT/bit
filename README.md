# Bio-informatics Toolbox

*2025-02-25 version 0.2.0a*

The purpose of this website is to simplify the tool [wgd v2](https://github.com/heche-psb/wgd), by 
making it accesible to users who may not have a background
in programming. Our goal is to provide an intuitive interface that
allows users to easily import FASTA files and receive a model in return.

Wgd stands for whole genome duplication, the tool can get DNA-sequences from a FASTA file. The
tool can eventually convert the sequence into a plot that shows when a wgd has occured. Comprising
seven sub-tools: *dmd, focus, ksd, mix, peak, syn and viz.* Because every sub-tool is extensive enough
to be a project itself. For this reason we focused on the sub-tool dmd. This tool can help with drawing 
conclusions from the sequences, such as determing orthological groups, and phylogeny.

## Prerequisites

- Python 3.7
- Python 3.13
- uv
- dart-sass

## Installation

Installation instructions for the tool and website can be found below.

To start, clone the repository including its submodule.

```sh
$ git clone --recurse-submodules -j8 git@github.com:Dunc4nNT/bit.git
```

As we'll be using [uv](https://docs.astral.sh/uv/) as package manager for our python projects, please install this first.

```sh
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Tool

To install the commandline wgd tool, please follow the instructions below.

#### Python

To use the wgd tool, python 3.7 is required, newer versions won't work.
Please follow the instructions below to install python 3.7.

```sh
$ mkdir python
$ cd python
$ wget https://www.python.org/ftp/python/3.7.17/Python-3.7.17.tgz
$ tar xvzf Python-3.7.17.tgz
$ cd Python-3.7.17
$ ./configure --enable-optimizations --prefix=/home/<username>/python
$ make altinstall
$ export PATH=$HOME/python/bin:$PATH
```

#### wgd

1. `cd tools/wgd` Go inside the tool's directory.
2. `python3.7 -m venv .venv` Create a virtual environment.
3. `source .venv/bin/activate` Activate the virtual environment.
4. `pip3 install setuptools`
5. `pip3 install -r requirements.txt` Install the necessary packages.
6. `pip3 install -e .` Install the tool.
7. `wgd -h` The tool should be installed and print its manual here.

### Website

1. `cd website` Go inside the website's directory.
2. `uv sync` Creates a virtual environment, and installs all the packages.
3. `cp .env.example .env` Creates a `.env` file for a few configuration options.

#### Sass

**This is only required for development of the website, the compiled stylesheet is in the repo.**

Follow the instructions on the [sass website](https://sass-lang.com/install/) to install sass, or follow the instructions below.

```sh
$ mkdir sass
$ cd sass
$ wget https://github.com/sass/dart-sass/releases/download/1.85.1/dart-sass-1.85.1-linux-x64.tar.gz
$ tar xvzf dart-sass-1.85.1-linux-x64.tar.gz
$ export PATH=$HOME/sass/dart-sass:$PATH
```

Running the sass compiler:

```sh
$ cd /path/to/repo/website/static
$ sass scss/main.scss css/main.css # compiles once.

$ sass --watch scss/main.scss css/main.css # compiles on save.
```

#### Running flask

```sh
$ cd /path/to/repo/website
$ uv run flask run
```

### Wgd Manager

1. `cd tools/wgd_manager` Go inside the wgd manager's directory.
2. `uv sync` Creates a virtual environment, and installs all the packages.

## Configuration

*describe config options here, e.g. path to tool*

## Usage

*how to run this app*

### Example (num)

*describe an example workflow, add images as well*

## Contact

For bug reports please use https://github.com/Dunc4nNT/bit/issues.<br>
For questions about the app, please use *github discussions link here*.<br>

## References

1. Chen, A. Zwaenepoel, and Y. Van De Peer, “wgd v2: 
a suite of tools to uncover and date ancient polyploidy and 
whole-genome duplication,” Bioinformatics, vol. 40, no. 5, Apr. 2024, 
doi: 10.1093/bioinformatics/btae272.

## License

PLACEHOLDER: This project is licensed under *INSERT LICENSE HERE*.

## Authors

[Duncan](https://github.com/Dunc4nNT)

[Sven](https://github.com/svenstaats)

[Johanna](https://github.com/j0w0j)

[Tarnished-06](https://github.com/Tarnished-06)
