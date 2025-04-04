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

## Installation

Installation instructions for the tool and website can be found below.

**Note: These instructions are for linux (specifically, debian).**

```sh
$ git clone git@github.com:Dunc4nNT/bit.git
```

### Tool

To install the commandline wgd tool, please follow the instructions below.

As we'll be using the bioconda package, we need conda (v25.1) with the bioconda channel added:

```sh
# replace the URL in wget with the version and OS you want from: https://repo.anaconda.com/miniconda/
$ mkdir -p ~/miniconda3
$ wget https://repo.anaconda.com/miniconda/Miniconda3-py39_25.1.1-2-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
$ bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
$ rm ~/miniconda3/miniconda.sh
$ source ~/miniconda3/bin/activate
$ conda init --all

# add the bioconda channels
$ conda config --add channels bioconda
$ conda config --add channels conda-forge
$ conda config --set channel_priority strict
```

To install wgd, create a conda environment for it with the provided `wgd_environment.yml` which includes all the required packages:

```sh
$ conda env create -f wgd_environment.yml
```

### Website

As we'll be using [uv](https://docs.astral.sh/uv/) (v0.6) as package manager for our project, please install this first.

```sh
$ curl -LsSf https://astral.sh/uv/install.sh | sh # latest

$ curl -LsSf https://astral.sh/uv/0.6.12/install.sh | sh # v0.6.12 (tested with this)
```

1. `uv sync` Creates a virtual environment, and installs all the packages.
2. `cp .env.example .env` Creates a `.env` file for a few configuration options.
3. Update the `SECRET_KEY` in the `.env` to be a random string.

#### Running flask

```sh
$ uv run flask run
```

#### Sass

**This is only required for development of the website, the compiled stylesheet is in the repo.**

First, we need nodejs (v23):

```sh
$ curl -o- https://fnm.vercel.app/install | bash
$ fnm install 23
```

Installing sass (and stylelint):

```sh
$ cd bit/static # from the project go to the static directory.
$ npm install # download all the packages.
```

Running the sass compiler:

```sh
$ cd bit/static
$ npx sass scss/main.scss css/main.css # compiles once.

$ npx sass --watch scss/main.scss css/main.css # compiles on save.
```

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
