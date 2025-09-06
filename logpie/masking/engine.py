import re
from typing import Any, Dict
from config.masking_config import load_masking_config


class MaskingEngine:
  def __init__(self):
    self.config = load_masking_config()
    self.compiled_rules = {}
    self._compile_rules()

  def _compile_rules(self):
    """Pre-compile all regex rules to avoiding recompiling on each usage"""
    if not self.config.get("masking",{}).get("enabled", False):
      return
    
    rules = self.config.get("masking", {}).get("rules", {})

    for rule_name, rule_config in rules.items():
      if rule_config.get("enabled", False):
        pattern = rule_config.get("pattern")
        replacement = rule_config.get("replacement", "***")

        self.compiled_rules[rule_name] = {
          "regex": re.compile(pattern),
          "replacement": replacement
        }
  def mask_text(self, text: str) -> str:
      """Apply all masking rules in one string"""
      if not isinstance(text, str):
          return text

      masked_text = text
      for _, rule in self.compiled_rules.items():
          masked_text = rule["regex"].sub(rule["replacement"], masked_text)
      return masked_text
  def mask_log_entry(self, log_entry: Dict[str, Any]) -> Dict[str, Any]:
      mask_entry = {}
      for name, value in log_entry.items():
          if isinstance(value, str):
              mask_entry[name] = self.mask_text(value)
          elif isinstance(value, dict):
              mask_entry[name] = self.mask_log_entry(value)
          elif isinstance(value, list):
             mask_entry[name] = [
                self.mask_log_entry(item) if isinstance(item, dict)
                else self.mask_text(item) if isinstance(item, str)
                else item
                for item in value
             ]
          else:
              mask_entry[name] = value
      return mask_entry
