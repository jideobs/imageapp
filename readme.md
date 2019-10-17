# Image app

A simple image upload and view app

## Installation

```bash
git clone git@github.com:jideobs/imageapp.git

cd imageapp

# Create virtualenv
virtualenv -p python3.7 virtualenv

source virtualenv/bin/activate

# install dependencies
pipenv sync
```

## Usage

```bash
./scripts/run_server.sh

# Upload image from URL to server

curl -d '{"image_url": "https://media.wired.com/photos/5b8999943667562d3024c321/master/w_2560%2Cc_limit/trash2-01.jpg"}'
-H "Content-Type: application/json" -X POST http://localhost:5000/image/upload

# To view in browser goto:
http://localhost:5000/image/view/trash2-01.jpg
```

## Test

```bash
./scripts/run_tests.sh

```
