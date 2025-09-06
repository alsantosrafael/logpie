import logging
import sys
import structlog
import os
from logpie.masking.engine import MaskingEngine

masking = MaskingEngine()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
numeric_level = getattr(logging, LOG_LEVEL, logging.INFO)

def mask_processor(logger, method_name, event_dict):
    return {
        k: masking.mask_text(v) if isinstance(v, str) else v
        for k, v in event_dict.items()
    }

def compat_processor(logger, method_name, event_dict):
    if "event" in event_dict:
        event_dict["message"] = event_dict.pop("event")
    if "level" in event_dict:
        event_dict["level"] = str(event_dict["level"]).upper()
    if "extra" in event_dict and isinstance(event_dict["extra"], dict):
        for k, v in event_dict["extra"].items():
            event_dict[k] = v
        del event_dict["extra"]
    return event_dict

def configure_logging():
    logging.basicConfig(
        format="%(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        level=numeric_level,
    )

    structlog.configure(
        processors=[
            mask_processor,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.add_log_level,
            compat_processor,
            structlog.processors.JSONRenderer(ensure_ascii=False),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

configure_logging()
log = structlog.get_logger("logpie")
