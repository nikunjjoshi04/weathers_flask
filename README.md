# Weathers

Weathers is python system for manage weather details

## Step 1
Move to weather dir
```bash
cd weathers
```

## Step 2
Install python dependencies
```bash
pip install -r requirements.txt
```

## Step 3
Run the development server
```bash
python run.py
```

## Step 4
Swagger API docs [URL](http://127.0.0.1:5000/)

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## API_KEY
Authentication API_KEY

You can find api key in ``` weathers/.env``` file

## Testing
For run the test cases

```bash
pytest -p no:cacheprovider
```