import importlib.resources
import yaml

def load_masking_config():
    with importlib.resources.files("logpie.config").joinpath("masking.yaml").open("r") as f:
        data = yaml.safe_load(f)

    masking_config = data.get("masking", {})
    if not masking_config.get("enabled", False):
        return []

    rules_dict = masking_config.get("rules", {})
    rules = [
        dict(name=name, **cfg)
        for name, cfg in rules_dict.items()
        if cfg.get("enabled", True)
    ]

    if all("priority" in r for r in rules):
        rules = sorted(rules, key=lambda r: r["priority"])

    return rules
