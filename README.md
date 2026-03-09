# Setup & Running the Project

## Running the Project in Google Colab

If you don't want to install anything locally you can simply run the notebooks in **Google Colab**.

A typical workflow looks like this:

```bash
git clone https://github.com/your-repo/project.git
cd project
```

Then just open the notebook and run the cells from top to bottom.

If you have never used Colab before these two resources are good introductions:

DataCamp tutorial
[https://www.datacamp.com/tutorial/tutorial-google-colab-for-data-scientists](https://www.datacamp.com/tutorial/tutorial-google-colab-for-data-scientists)

Short intro video
[https://www.youtube.com/watch?v=rsBiVxzmhG0](https://www.youtube.com/watch?v=rsBiVxzmhG0)

Colab is great for quick experiments, teaching, and situations where you don't want to fight your local Python installation.

---

# Running the Project Locally

For local development we use **uv**. It manages Python environments and dependencies in a way that is fast and reproducible.

First install uv

```bash
pip install uv
```

Now move into the project directory and run

```bash
uv sync --frozen
```

This command does three things

1. creates a virtual environment
2. reads the lock file
3. installs the exact dependency versions used by the project

The result is that everyone working on the repository ends up with the same environment.

If something fails (this can happen on macOS because of different CPU architectures) simply run

```bash
uv sync
```

This allows uv to rebuild some packages locally.

Once the environment exists you can run Python commands inside it with

```bash
uv run python script.py
```

or

```bash
uv run jupyter lab
```

If you are working in **Visual Studio Code**, select the interpreter from `.venv` and everything should work automatically.
**Very important**: There is no need to run any of the cells that do `!pip install some-dependency` just never run them and you should be fine.

---

# Adding Dependencies

Here is a small comparison between the old way and the modern workflow.

### The classic pip approach

Many people instinctively do this

```bash
pip install pandas
```

This installs the package into the current environment. Great. The code works.

But the dependency is not recorded anywhere.

Now someone else clones the repository and runs the code.

Suddenly this happens

```
ModuleNotFoundError: No module named 'pandas'
```

Congratulations. You just created a mystery dependency.

---

### The uv workflow

With uv you add dependencies explicitly

```bash
uv add pandas
```

This command

* installs the package
* updates `pyproject.toml`
* updates the lock file

Everything about the environment is now recorded in the project configuration.

Anyone cloning the repository later can simply run

```bash
uv sync
```

and get exactly the same environment.

No guessing. No archaeology.

---

# Why Not Just Install Packages in the Notebook?

You will often see notebooks doing things like this

```python
!pip install numpy
```

or

```python
%pip install matplotlib
```

Yes, it works.

But it also means the notebook is secretly modifying the environment while it runs.

Now imagine the following scenario.

You run the notebook once. It installs a package. Everything works.

Later you restart the kernel and jump directly to cell 8.

Suddenly nothing works because cell 2 was the one installing the dependencies.

This is one of the reasons notebooks get a reputation for being chaotic.

In this project the environment is not managed **outside the notebook** this is only because students that use colab can come from all sorts of backgrounds so the executive decision was made to also provide installations scripts within cells (NEVER DO THIS EVER IN YOUR OWN PROJECT!). Any notebook should assume the environment already exists. This keeps the notebook focused on the actual work instead of turning it into a setup script.

---

# How Notebooks Actually Work

A **Jupyter** notebook is essentially a Python process with a user interface.

Every time you run a cell the code is executed inside the same Python interpreter. Variables remain in memory until the kernel restarts.

That means this works

```python
x = 10
```

and later

```python
print(x)
```

But if you restart the kernel and only run the second cell you will get an error because `x` does not exist anymore.

This hidden state is one of the most common sources of confusion when working with notebooks.

---

# Structuring Notebook Cells

A good notebook usually follows a simple pattern.

The first cell contains the imports

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

The next cells load data or define configuration variables.

```python
DATA_PATH = "data/sample.csv"

df = pd.read_csv(DATA_PATH)
```

After that the analysis begins.

The important idea is that the notebook should work if someone restarts the kernel and runs all cells from top to bottom. If it only works in a very specific execution order the notebook is probably relying on hidden state.

Try to avoid long chains where cell 12 depends on cell 11 which depends on cell 10 which depends on cell 3 which depends on something you executed two hours ago.

Flat structure beats clever structure.

---

# When Notebooks Get Too Big

Another common anti-pattern is putting an entire project inside a notebook.

You start with a few cells. Then a few helper functions. Then more functions. Suddenly you have a 2000 line notebook.

At that point it is usually better to move logic into normal Python modules.

Example

```python
from project.preprocessing import clean_text
from project.model import train_model
```

The notebook then becomes a place for exploration and visualization while the actual program logic lives in regular Python files where it is easier to test and maintain.

---

# A Short Note on Python Packaging

Python packaging has a long and slightly chaotic history.

For a long time people used `pip` together with `requirements.txt`. In the scientific ecosystem many projects adopted Conda environments. Recently the ecosystem has moved towards `pyproject.toml` as the standard way to define dependencies.

Modern tools like uv build on that standard while focusing on speed and reproducibility.

If you are curious about the details the official documentation is worth a look

[https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

It is surprisingly readable for documentation, which is already a strong endorsement.

---

If you want, I can also add a **short “Python packaging horror stories” section** (things like global pip installs, mixing conda and pip, system Python disasters, etc.). It usually gets a laugh from students and drives the point home why environments matter.
