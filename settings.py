from environs import Env, EnvError

env = Env()
env.read_env()

# Logging Setup
LOG_TYPE = env.str("LOG_TYPE", "rotate") # can be set to 'stream' 'watched' or 'rotate'
LOG_LEVEL = env.str("LOG_LEVEL", "INFO")

# File Logging Setup
LOG_DIR = env.str("LOG_DIR", "logs")
APP_LOG_NAME = env.str("APP_LOG_NAME", "app.log")
WWW_LOG_NAME = env.str("WWW_LOG_NAME", "www.log")  # watched log
LOG_MAX_BYTES = env.int("LOG_MAX_BYTES", 100000000)  # 100MB in bytes
LOG_COPIES = env.int("LOG_COPIES", 5)
