# Bio-informatics Toolbox

*2025-02-25 version 0.1.0a*

*The purpose of this website is to simplify the tool Wgd v2, by 
making it accesible to users who may not have a background
in programming. Our goal is to provide an intuitive interface that
allows users to easily import FASTA files and receive a model in return.*

## Prerequisites

- Python 3.6

## Installation

Installation instructions for the tool and website can be found below.

### Python

To use the wgd tool, python 3.6 is required, newer versions won't work.
Please follow the instructions below to install python 3.6.

```sh
$ mkdir python
$ cd python
$ wget https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz
$ tar xzf Python3.6.15.tgz
$ cd Python3.6.15
$ ./configure --enable-optimizations --prefix=/home/<username>/python
$ make altinstall
$ export PATH=$HOME/python/bin:$PATH
```

### Tool installation (wgd)

To install the commandline wgd tool, please follow the instructions below.

1. Go to a directory you want to install the tool in.
2. `git clone https://github.com/heche-psb/wgd` Clone the repository.
3. `cd wgd` Go inside the tool's directory.
4. `python3.6 -m venv .venv` Create a virtual environment.
5. `source .venv/bin/activate` Activate the virtual environment.
6. `pip3 install -r requirements.txt` Install the necessary packages.
7. `pip3 install -e .` Install the tool.
8. `wgd -h` The tool should be installed and print its manual here.

### Website

*installation instructions for our website*

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

*list of references*

1. [wgd v2 github](https://github.com/heche-psb/wgd)

## License

PLACEHOLDER: This project is licensed under *INSERT LICENSE HERE*.

## Authors

[Duncan](https://github.com/Dunc4nNT)

[Sven](https://github.com/svenstaats)

[Johanna](https://github.com/j0w0j)

[Tarnished-06](https://github.com/Tarnished-06)
