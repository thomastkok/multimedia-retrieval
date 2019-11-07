# multimedia-retrieval

The project for the course Multimedia Retrieval. Creating a 3D shape content-based retrieval system.

## Authors

Ruben Schenkhuizen - 4115325
Thomas Kok - 4124359

## Instructions for installation and execution

To be able to use the program, the Labeled PSB dataset must be available.
This dataset can be downloaded from [this location](https://people.cs.umass.edu/~kalo/papers/LabelMeshes/).
This dataset must be located at the file path: `..\LabeledDB_new`.
To illustrate, the directory structure must look as follows:
```
mr
|
+--multimedia-retrieval
|  |
|  +--multimedia_retrieval/
|  +--cache/
|  +--data/
|  +--docs/
|  +--requirements.txt
|  +--setup.py
|  +--Makefile
|  +--README.md
|
+--LabeledDB_new
   |
   +--Airplane/
   |  |
   |  +--61.off
   |  ...
   +--Ant/
   +--Armadillo/
   ...
```

Install packages with `make init` or `pip install -e .` and `pip install -r requirements.txt`.

Run the project with `make start` or `python -m multimedia_retrieval`.
