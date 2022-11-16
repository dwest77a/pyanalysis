echo "pyanalysis: Setting up environment"

if [[ "$VIRTUAL_ENV" != ""]]
then
    echo "pyanalysis: Installing requirements into venv"
    pip install -r requirements.txt
else
    echo "pyanalysis: No venv currently activated"
    echo "pyanalysis: Create new local venv as ~/venvs/pyanalysis? [y/n]"
    read create_venv
    if [ $create_venv == "y"]
    then
        if [ ! -d "~/venvs/"]
        then
            mkdir ~/venvs
        fi
        python -m venv ~/venvs/pyanalysis
        source ~/venvs/pyanalysis/bin/activate
        pip install -r requirements.txt
    fi
fi
echo "pyanalysis: Setup complete"
