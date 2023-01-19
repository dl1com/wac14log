# Worked-all-... Online Logger

This small online contest log was developed for logging a competition at a 
local HAM Radio club. It was built with some kind of versatility in mind, 
so it can be altered to your own needs with the config file.

## Development

```
python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

Make a copy of *config/contestinfo.json.sample* to *config/contestinfo.json* 
and change content as you like.
Same with *config/description.md.sample*.

Run Streamlit server:

```
streamlit run home.py
```

## Build and run Docker container

```
docker-compose up -d
```

To rebuild container after changes:

```
docker-compose build
```