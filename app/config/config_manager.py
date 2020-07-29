import configparser


config_path = "./app/config/config.ini"

config = configparser.ConfigParser()
config.read(config_path)
config_state = config["vars"]["config_state"]


def get_token() -> str:
    return config["release"]["token"]


def get_backend_url() -> str:
    return config[config_state]["backend_url"]


def get_webhook_url() -> str:
    return "%s/%s" % (config[config_state]["webhook_url"], get_token())


def get_redis_url() -> str:
    return config[config_state]["redis_url"]


def get_db_index() -> str:
    return config[config_state]["db_index"]


def get_server_host() -> str:
    return config[config_state]["server_host"]


def get_server_port() -> str:
    return config[config_state]["server_port"]


def get_postgresql_url() -> str:
    return config[config_state]["postgresql_url"]
