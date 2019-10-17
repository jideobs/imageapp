# Image app

A simple image upload and view app

## Installation

Clone the repo

```bash
git clone git@github.com:jideobs/imageapp.git
```

## Usage

```bash
python src/web.py

# Upload to image from URL

curl -d '{"image_url": "https://media.wired.com/photos/5b8999943667562d3024c321/master/w_2560%2Cc_limit/trash2-01.jpg"}'
-H "Content-Type: application/json" -X POST http://localhost:5000/image/upload

# To view in browser goto:
http://localhost:5000/image/view/trash2-01.jpg
```
