from os import environ as env

from dotenv import load_dotenv

load_dotenv(".env")

HOST = env.get("HOST") or "0.0.0.0"
PORT = env.get("PORT") or 80
MODULE_NAME = env.get("MODULE_NAME") or "pesopolis"

DB_HOST = env.get("DB_HOST")
DB_PORT = env.get("DB_PORT")
DB_NAME = env.get("DB_NAME")
DB_USER = env.get("DB_USER")
DB_PWD = env.get("DB_PWD")
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

IS_TEST = env.get("IS_TEST", "").lower() == "true"
TEST_DATABASE_URL = env.get("DATABASE_URL") or "sqlite+aiosqlite:///my_database.db"

LOG_LEVEL = env.get("LOG_LEVEL") or "INFO"
