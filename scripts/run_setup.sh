# Create virtualenv
virtualenv -p python3.7 virtualenv

source virtualenv/bin/activate

# install dependencies
pipenv sync
