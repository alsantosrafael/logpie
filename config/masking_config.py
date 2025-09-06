
from pathlib import Path

import yaml


def load_masking_config():
  # Looking for pre-configured masking settings
  config_path = Path("config/masking.yaml") 

  if not config_path.exists():
    # If no config was provided, return basic config with disabled rules
    return {"masking": {"enabled": False, "rules": {}}}
  
  with open(config_path, 'r') as file:
    return yaml.safe_load(file)
