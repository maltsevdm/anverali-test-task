import enum
from bitrix_client import BitrixClient
from bitrix_mock import BitrixClientMock
from pg_db import PgDatabase

import config


db = PgDatabase(
    host=config.PG_HOST,
    port=config.PG_PORT,
    user=config.PG_USER,
    password=config.PG_PASSWORD,
    db_name=config.PG_DBNAME,
)

bitrix_client = BitrixClientMock(
    domain=config.BITRIX_DOMAIN,
    webhook=config.BITRIX_WEBHOOK,
)


class Gender(enum.Enum):
    man = "Мужчина"
    woman = "Женщина"


def define_gender_by_name(name: str) -> Gender:
    is_man = db.is_name_in_table(db.Tables.names_man, name)
    if is_man:
        return Gender.man
    is_woman = db.is_name_in_table(db.Tables.names_woman, name)
    if is_woman:
        return Gender.woman


def update_contact_gender(id: str) -> None:
    contact = bitrix_client.get_contact(id)
    gender = define_gender_by_name(contact["NAME"])
    if gender:
        fields = {"UF_CRM_GENDER": gender.value}
        bitrix_client.update_contact(id, fields)
    else:
        print("Такого имени нет в базе данных.")
