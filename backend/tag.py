import random

from database import DataBase

connect = DataBase.DataBase().connect
cursor = connect.cursor()


def get_all_tags():
    # not all
    cursor.execute(f'SELECT tag FROM {DataBase.tag_table}')
    tags = [i[0] for i in cursor.fetchall()]
    result = random.sample(tags, 12)
    return result
