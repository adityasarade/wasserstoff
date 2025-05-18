import os
import yaml

# Locate the params.yaml next to main.py
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'params.yaml')

with open(_CONFIG_PATH, 'r') as f:
    params = yaml.safe_load(f)