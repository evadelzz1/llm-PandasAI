# Quiz

### Cloning the Repository

    git clone https://github.com/evadelzz1/experiment3.git

### Setting up a Virtual Environment

    cd ./experiment3

    pyenv versions

    pyenv local 3.11.6

    pyenv versions

    echo '.env'  >> .gitignore
    echo '.venv' >> .gitignore

    echo 'OPENAI_API_KEY=sk-9jz....'    >> .env
    echo 'USER_PASSWORD="passwd"'       >> .env

    ls -la

### Activate the virtual environment

    python -m venv .venv

    source .venv/bin/activate

    python -V

### Install the required dependencies

    pip list

    pip install -r requirements.txt

    pip freeze | tee requirements.txt.detail

### Running the Application

    python -m streamlit run Home.py

### Deactivate the virtual environment

    deactivate
