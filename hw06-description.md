# Homework No 6 - _From Notebooks to Research Packages, Part II_

* **Statistics 159/259, Spring 2022**
* **Due Friday 04/22/2022, 11:59PM PT**
* Prof. F. Pérez and GSI F. Sapienza, Department of Statistics, UC Berkeley.
* This assignment is worth a maximum of **45 points**.
* Assignment type: **individual**.

For this assignment, we will start from the conclusion of HW05 and continue improving the structure of your repository as a Reproducible Research Package, using again the code from the [LIGO Gravitational Wave Detection Tutorial](https://github.com/losc-tutorial/LOSC_Event_tutorial).

In this assignment we are giving you as a starting point effectively the solution to HW05, and you will now add a bit more structure, tests, documentation, etc, to complete the picture.

## Deliverables

### [5 points] Repository structure

The repository starts with all the code and data with the same layout as LIGO created it. You will reorganize it, while checking that the code still runs, so that all data files live in a `data` directory, generated figures get saved to `figurs`, and generated audio goes into `audio`.  

These directories should be present in the repo even before you run any code. Since Git will not let you add an empty dir to a repo, you will need to use a little hack by putting an empty `.gitkeep` file in those directories (as explained [here](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/gitkeep-push-empty-folders-git-commit)). 

### [ 5 points] Installable package

In HW05 you made `ligotools` usable as a local package that could be imported from the current directory. Now you will make it an actually installable package as discussed in class, with the appropriate `pyproj.toml`, `setup.py` and `setup.cfg` files. 

Note: for the authorship, you should list as authors "Ligo Scientific Collaboration (LSC) and `<your name>`".

### [ 5 points ] Add tests to `readligo.py`

You should add four separate small tests to the functions in `readligo.py` that are part of the `ligotools` package.  Make a subfolder called `tests` and put in there `tests_readligo.py` with your tests.

The command `pytest ligotools` should run all those tests.

### [ 5 points ] Create `utils.py`

In the `ligotools` package, make a new module called `utils.py` and move the following functions from the notebook into `utils`: `whiten`, `write_wavfile`, `reqshift`. You will then need to update the notebook to use these functions imported from `ligotools.utils` instead.

### [ 5 points ] Make new plotting utility in `utils.py`

Find the notebook cell that begins with

```
# -- To calculate the PSD of the data, choose an overlap and a window (common to all detectors)
#   that minimizes "spectral leakage" https://en.wikipedia.org/wiki/Spectral_leakage
```

and move its plotting code into a separate utility function, then call that from the notebook.

### [ 5 points ] Add tests to `utils.py`

You should add four separate small tests to the functions in `utils.py`. These should test the three functions you moved from the notebook and the new plotting one you made above.

The command `pytest ligotools` should run all those tests.

### [ 5 points ] JupyterBook

Set up the repository to be a proper JupyterBook one that builds a page for the main notebook and includes a visible Binder link in the JupyterBook build.

Remember that on the hub, in order to be able to view the book build without having to use the VNC desktop, we need to run sphinx manually. These are the key commands for your reference:

```bash
jupyter-book config sphinx .
sphinx-build  . _build/html -D html_baseurl=${JUPYTERHUB_SERVICE_PREFIX}/proxy/absolute/8000
```

Then we can view the code with (in another terminal), going to the `_build/html` folder and running:

```bash
python -m http.server
```

and then heading to this URL:

[https://stat159.datahub.berkeley.edu/user-redirect/proxy/8000/index.html](https://stat159.datahub.berkeley.edu/user-redirect/proxy/8000/index.html)


### [ 5 points ] GitHub Pages and Actions

Configure your repo to have a public GitHub Pages URL and set up a GitHub Action that builds the JupyterBook build of the repo on all pushes to the main branch (like the class repo works).

Note that the code to execute the notebooks is based on Python 2.7 while the JupyterBook build tools are based on Python 3. You'll need to treat the build and science code separately.

### [ 5 points ] Makefile

There should be a Makefile with the following targets

- `env`: creates and configures the environment.
- `html`: build the JupyterBook normally (calling `jupyterbook build .`). Note this build can only be viewed if the repo is cloned locally, or with the VNC desktop on the hub.
- `html-hub`: build the JupyterBook so that you can view it on the hub with the URL proxy trick as indicated above.
- `clean`: clean up the `figures`, `audio`  and `_build` folders.
