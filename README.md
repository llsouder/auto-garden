# Auto-Pi-Garden


### Setup

#### Create virtual environment _(optional)_

```bash
python3 -m pip install virtualenv
```
Create virtual environment with 
```bash
python3 -m virtualenv venv
```

Activate virtual environment (before installing dependencies) with
```bash
source ./venv/bin/activate
```

Deactivate virtual environment with 
```bash
deactivate
```

#### Install WiringPi

```bash
python3 -m pip install -r requirements.txt 
```

### Run
```bash
python app.py
```

### View web interface
```
http://<host>:8000/static/index.html
```

### Not a Pi

Not a problem. remove -shunt from the RPi-Shunt directory
