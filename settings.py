import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings():
    load_dotenv()
    return Settings(
        bots=Bots(
            bot_token=os.getenv("TG_TOKEN"),
            admin_id=os.getenv("TG_ADMIN")
        )
    )


stngs = get_settings()


@dataclass
class DB:
    db_user: str
    db_pass: str
    db_name: str
    db_host: str
    db_port: int

@dataclass
class DBSettings:
    db: DB


def get_db_settings():
    load_dotenv()
    return DBSettings(
        db=DB(
            db_user=os.getenv('DB_ADMIN'),
            db_pass=os.getenv('DB_PASS'),
            db_name=os.getenv('DB_NAME'),
            db_host=os.getenv('DB_HOST'),
            db_port=os.getenv('DB_PORT')
        )
    )


dbstng = get_db_settings()