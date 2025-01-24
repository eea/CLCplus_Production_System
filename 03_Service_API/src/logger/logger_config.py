const_log_class = 'logging.StreamHandler'

########################################################################################################################
# Logger configuration for the development environment
########################################################################################################################

log_config_dev = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(asctime)s :: %(client_addr)s - "%(request_line)s" %(status_code)s',
            "use_colors": True
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": const_log_class,
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": const_log_class,
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app_logger": {"handlers": ["default"], "level": "DEBUG"},
        "uvicorn.error": {"level": "DEBUG"},
        "uvicorn.access": {"handlers": ["access"], "level": "DEBUG", "propagate": False},
        "gunicorn.access": {"handlers": ["access"], "level": "DEBUG", "propagate": False},
        "gunicorn.error": {"level": "DEBUG"},
    },
}


########################################################################################################################
# Logger configuration for the production environment
########################################################################################################################

log_config_prod = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(asctime)s :: %(client_addr)s - "%(request_line)s" %(status_code)s',
            "use_colors": True
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": const_log_class,
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": const_log_class,
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app_logger": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        "gunicorn.access": {"handlers": ["access"], "level": "DEBUG", "propagate": False},
        "gunicorn.error": {"level": "DEBUG"}
    },
}
