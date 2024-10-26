# Template instructions

## Set up a new Python project

Download the zipped repo from GitHub.
<!-- TODO a link to the download page. -->

Unzip the repo.

Run the
[rename_project.py](meta/rename_project.py)
script to rename the project.

<!-- Then run script [init.sh](meta/init.sh) to initialize the project. -->

Go to the new folder.

Install the project:

```bash
poetry install
```

<!-- Install the optional dependencies with the following command: -->
<!-- {{optional_dependencies}} -->
<!-- TODO automagically generate the optional dependencies list -->

Install the required dependencies:

```bash
poetry add loguru
poetry add --dev pytest
```

Initialize the git repository, set the identity, and make the first commit:

```bash
git init
git add .
gitid ...
git commit -m "Initial commit"
```

## Install additional dependencies

Install the dependencies you want with the following commands

Log and formatting dependencies

```bash
poetry add loguru rich
```

LLM dependencies

```bash
poetry add transformers accelerate
poetry add torch
poetry add \
    chromadb \
    langchain \
    langchain-chroma \
    langchain-community \
    langchain-huggingface \
    langchain-ollama ollama \
    langchain-openai \
    langgraph \
    sentence_transformers
```

Data dependencies

```bash
poetry add pandas numpy matplotlib seaborn scikit-learn
```

Web dependencies

```bash
poetry add fastapi uvicorn
poetry add streamlit
```

Notebook dependencies

```bash
poetry add ipykernel ipywidgets
```

Test dependencies

```bash
poetry add --dev pytest
```
