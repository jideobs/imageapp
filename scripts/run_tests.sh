export PYTHONPATH=./src:$PYTHONPATH

source virtualenv/bin/activate
py.test tests/
