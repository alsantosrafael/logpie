import re
from logpie.config.masking_config import load_masking_config


class MaskingEngine:
    def __init__(self):
        self.rules = load_masking_config()

    def mask_text(self, text):
        if not isinstance(text, str):
            return text
        masked = text
        for rule in self.rules:
            if rule.get("enabled", True):
                masked = re.sub(rule["pattern"], rule["replacement"], masked)
        return masked

    def mask_log_entry(self, obj):
        if isinstance(obj, dict):
            masked_obj = {}
            for key, value in obj.items():
                if isinstance(value, str):
                    masked_obj[key] = self.mask_text(value)
                elif isinstance(value, dict):
                    masked_obj[key] = self.mask_log_entry(value)
                elif isinstance(value, list):
                    masked_obj[key] = [
                        (
                            self.mask_log_entry(v)
                            if isinstance(v, (dict, list))
                            else self.mask_text(v)
                            if isinstance(v, str)
                            else v
                        )
                        for v in value
                    ]
                else:
                    masked_obj[key] = value
            return masked_obj
        elif isinstance(obj, list):
            return [
                (
                    self.mask_log_entry(v)
                    if isinstance(v, (dict, list))
                    else self.mask_text(v)
                    if isinstance(v, str)
                    else v
                )
                for v in obj
            ]
        else:
            return obj
