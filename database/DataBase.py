import os
import sqlite3
from typing import Literal

user_comment_table = 'user_comment'
_user_comment_create = "user_id TEXT NOT NULL,\
                        comment_id INTEGER NOT NULL,\
                        attitude INTEGER NOT NULL,\
                        PRIMARY KEY(user_id, comment_id)"
# attitude 0: dislike; 1 : like

comment_table_name = 'Comment'
_comment_table_create = "uuid INTEGER PRIMARY KEY AUTOINCREMENT,\
                        is_main INTEGER NOT NULL,\
                        user_id TEXT NOT NULL,\
                        time TIMESTAMP DEFAULT (datetime(\'now\',\'localtime\')),\
                        title TEXT,\
                        content TEXT,\
                        available INTEGER DEFAULT 1,\
                        image_uuid INTEGER,\
                        rating REAL,\
                        dish_id INTEGER,\
                        reply_to_id INTEGER"
_comment_table_updater = f"CREATE TRIGGER IF NOT EXISTS comment_table_updater BEFORE UPDATE ON {comment_table_name} BEGIN UPDATE {comment_table_name} set time=datetime(\'now\',\'localtime\') WHERE uuid=NEW.uuid; END;"
comment_require_list = ['uuid', 'is_main', 'user_uuid', 'time', 'title', 'content', 'available', 'image_uuid', 'rating']
comment_require_dict = {'like_count': user_comment_table, 'liked': user_comment_table,
                        'dislike_count': user_comment_table, 'disliked': user_comment_table,
                        'replies_uuid': comment_table_name}

user_dish_table = 'user_dish'
_user_dish_table_create = "user_id TEXT NOT NULL,\
                            dish_id INTEGER NOT NULL,\
                            favorite INTEGER DEFAULT 0,\
                            recommend INTEGER DEFAULT 1,\
                            PRIMARY KEY(user_id, dish_id)"
user_dish_column_list = ['user_id', 'dish_id', 'rate', 'favorite']

record_table_name = 'Record'
_record_table_create = "uuid INTEGER PRIMARY KEY AUTOINCREMENT,\
                        user_id TEXT NOT NULL,\
                        dish_id INTEGER NOT NULL,\
                        time TIMESTAMP DEFAULT (datetime(\'now\',\'localtime\'))"
_record_table_updater = f'CREATE TRIGGER IF NOT EXISTS record_table_updater BEFORE UPDATE ON {record_table_name} BEGIN UPDATE {record_table_name} set time=datetime(\'now\',\'localtime\') WHERE uuid=NEW.uuid; END;'
record_require_list = ['uuid', 'user_id', 'dish_uuid', 'time']

user_counter_table = 'user_counter'
_user_record_create = "user_id TEXT NOT NULL,\
                        counter_id INTEGER NOT NULL,\
                        favorite INTEGER DEFAULT 1,\
                        PRIMARY KEY(user_id, counter_id)"
user_counter_column_list = ['user_id', 'record_id', 'counter_id']

user_table_name = 'Users'
_user_table_create = "uuid TEXT PRIMARY KEY NOT NULL,\
                        name TEXT NOT NULL,\
                        is_admin INTEGER NOT NULL,\
                        password CHAR(20) NOT NULL"
user_require_list = ['uuid', 'username', 'is_admin', 'password']
user_inner_require_dict = {'recommend_dishes': user_dish_table, 'records_uuids': record_table_name,
                           'favorite_dishes_uuids': user_dish_table, 'favorite_counters_uuids': user_counter_table}

tag_table = 'tag'
_tag_table_create = "uuid INTEGER PRIMARY KEY AUTOINCREMENT,\
                    tag TEXT NOT NULL,\
                    count INTEGER DEFAULT 1"
tag_column_list = ['uuid', 'tag', 'count']

counter_dish_table = 'counter_dish'
_counter_dish_create = "counter_id INTEGER NOT NULL,\
                        dish_id INTEGER NOT NULL,\
                        PRIMARY KEY(counter_id, dish_id)"
counter_dish_column_list = ['counter_id', 'dish_id']

dish_tag_table = 'dish_tag'
_dish_tag_table_create = "dish_id INTEGER NOT NULL,\
                        tag_id INTEGER NOT NULL,\
                        PRIMARY KEY(dish_id, tag_id)"
dish_tag_column_list = ['dish_id', 'tag_id']

dish_table_name = 'Dish'
_dish_table_create = "uuid INTEGER PRIMARY KEY AUTOINCREMENT,\
                        available INTEGER DEFAULT 1,\
                        name TEXT NOT NULL,\
                        description TEXT,\
                        price REAL,\
                        image_uuid INTEGER"
dish_require_list = ['uuid', 'available', 'name', 'description', 'price', 'image_uuid', 'tags']
dish_inner_require_dict = {'counters_uuids': counter_dish_table, 'rating_average': user_dish_table,
                           'ratings': comment_table_name, 'comments_ids': comment_table_name}

canteen_table_name = 'Canteen'
_canteen_table_create = "uuid INTEGER PRIMARY KEY AUTOINCREMENT,\
                        name TEXT NOT NULL,\
                        image_uuid INTEGER,\
                        available INTEGER DEFAULT 1,\
                        description TEXT"
canteen_require_list = ['uuid', 'name', 'image_uuid', 'available', 'description']

counter_table_name = 'Counter'
_counter_table_create = "uuid INTEGER PRIMARY KEY AUTOINCREMENT,\
                        name TEXT NOT NULL,\
                        available INTEGER DEFAULT 1,\
                        description TEXT,\
                        image_uuid INTEGER,\
                        canteen_uuid INTEGER"
counter_require_list = ['uuid', 'name', 'available', 'description', 'image_uuid', 'canteen_uuid']

image_table_name = "Image"
_image_table_create = "uuid INTEGER PRIMARY KEY AUTOINCREMENT,\
                        content BLOB"


class DataBase:
    _instance = None
    _flag = False
    db_path = './database/'
    db_name = 'data'

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._flag:
            current_directory = os.getcwd()
            parent_directory = os.path.dirname(current_directory)
            # self.connect = None
            try:
                self.connect = sqlite3.connect(os.path.join(current_directory, self.db_path, self.db_name + '.db'))
            except sqlite3.OperationalError:
                self.connect = sqlite3.connect(os.path.join(parent_directory, self.db_path, self.db_name + '.db'))
            self.cursor = self.connect.cursor()
            self._flag = True
            x = lambda table_name, table_create: self.cursor.execute(
                'CREATE TABLE IF NOT EXISTS %s (%s);' % (table_name, table_create))
            x(user_comment_table, _user_comment_create)
            x(comment_table_name, _comment_table_create)
            x(user_dish_table, _user_dish_table_create)
            x(record_table_name, _record_table_create)
            x(user_counter_table, _user_record_create)
            x(user_table_name, _user_table_create)
            x(counter_dish_table, _counter_dish_create)
            x(dish_table_name, _dish_table_create)
            x(canteen_table_name, _canteen_table_create)
            x(counter_table_name, _counter_table_create)
            x(image_table_name, _image_table_create)
            x(tag_table, _tag_table_create)
            x(dish_tag_table, _dish_tag_table_create)

            self.cursor.execute(_record_table_updater)
            self.cursor.execute(_comment_table_updater)

    def set_db_path(self, new_path: str):
        self.db_path = new_path

    def set_db_name(self, new_name: str):
        self.db_name = new_name

    def create_table(self, table_name: str, column_list: list):
        """
        常用类型:
        TEXT 字符串, CHAR(length) 固长字符串,\n
        INTEGER 整型, BIGINT 长整型, REAL 实数,\n
        BOOL 布尔值, BLOB 二进制, DATETIME 时间\n
        \b\n
        常用约束: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT
        """
        sql = 'CREATE TABLE IF NOT EXISTS %s (%s);' % (table_name, column_list2str(column_list))
        self.cursor.execute(sql)
        self.connect.commit()

    def insert_into_table(self, table_name: str, value_list: list, column_list=None):
        """
        INSERT INTO table_name (column1, ...) VALUES (value1, ...)
        """
        sql = 'INSERT INTO %s' % table_name
        if column_list is not None:
            sql += ' (%s)' % column_list2str(column_list)
        sql += ' VALUES (%s)' % value_list2str(value_list)
        # print(sql)
        self.cursor.execute(sql)
        self.connect.commit()

    def insert_image(self, table_name: str, column_name: str, image: bytes):
        sql = 'INSERT INTO %s (%s) VALUES (?);' % (table_name, column_name)
        self.cursor.execute(sql, (sqlite3.Binary(image), ))
        self.connect.commit()

    def search_from_table(self, table_name: str, result_list=None,
                          column_list=None, value_list=None, mode='AND') -> list:
        """
        SELECT */result FROM table_name WHERE condition
        """
        if result_list is not None:
            sql = 'SELECT %s FROM %s' % (column_list2str(result_list), table_name)
        else:
            sql = 'SELECT * FROM %s' % table_name
        if column_list is not None:
            sql += ' WHERE %s' % trans2condition(column_list, value_list, mode)
        sql += ';'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def search_last_record(self, table_name: str, key_name: str) -> list:
        """
        SELECT * FROM 表名 ORDER BY 主键 DESC LIMIT 1;
        主键类型应为自增INTEGER
        """
        sql = 'SELECT * FROM %s ORDER BY %s DESC LIMIT 1;' % (table_name, key_name)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update_table(self, table_name: str, tgt_column_list: list, tgt_value_list: list,
                     src_column_list=None, src_value_list=None, mode='AND'):
        """
        UPDATE table_name SET column1 = value1, ... WHERE condition
        """
        sql = 'UPDATE %s SET %s' % (table_name, trans2update(tgt_column_list, tgt_value_list))
        if src_column_list is not None:
            sql += ' WHERE %s' % trans2condition(src_column_list, src_value_list, mode)
        sql += ';'
        self.cursor.execute(sql)
        self.connect.commit()

    def delete_from_table(self, table_name: str, column_list: list, value_list: list,
                          mode: Literal['AND', 'OR'] = 'AND'):
        sql = 'DELETE FROM %s' % table_name
        sql += ' WHERE %s' % trans2condition(column_list, value_list, mode)
        sql += ';'
        self.cursor.execute(sql)
        self.connect.commit()

    def delete_all_data_from_table(self, table_name: str):
        sql = 'DELETE FROM %s;' % table_name
        self.cursor.execute(sql)
        self.connect.commit()

    def drop_table(self, table_name: str):
        sql = 'DROP TABLE IF EXISTS %s;' % table_name
        self.cursor.execute(sql)
        self.connect.commit()

    def fuzzy_search(self,
                     table_name: str,
                     result_list=None,
                     column_list=None,
                     value_list=None,
                     mode='AND') -> list:
        """
            SELECT */result FROM table_name WHERE condition
        """
        if result_list is not None:
            sql = 'SELECT %s FROM %s' % (column_list2str(result_list), table_name)
        else:
            sql = 'SELECT * FROM %s' % table_name
        if column_list is not None:
            sql += ' WHERE %s' % trans2fuzzy_condition(column_list, value_list, mode)
        sql += ';'
        # print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()


def column_list2str(column_list: list) -> str:
    result = '%s' % column_list[0]
    for i in range(1, len(column_list)):
        result += ', %s' % column_list[i]
    return result


def value_list2str(value_list: list) -> str:
    if type(value_list[0]) is str:
        result = "'%s'" % str(value_list[0])
    else:
        result = '%s' % str(value_list[0])
    for i in range(1, len(value_list)):
        if type(value_list[i]) is str:
            result += ", '%s'" % str(value_list[i])
        else:
            result += ', %s' % str(value_list[i])
    return result


def trans2update(column_list: list, value_list: list) -> str:
    if type(value_list[0]) is str:
        result = "%s = '%s'" % (column_list[0], value_list[0])
    else:
        result = '%s = %s' % (column_list[0], str(value_list[0]))
    for i in range(1, len(column_list)):
        if type(value_list[i]) is str:
            result += ", %s = '%s'" % (column_list[i], value_list[i])
        else:
            result += ', %s = %s' % (column_list[i], str(value_list[i]))
    return result


def trans2condition(column_list: list, value_list: list | None, mode='AND') -> str:
    if value_list is None:
        raise SystemError("\033[0;31;40;mvalue_list is None\033[0m")
    if type(value_list[0]) is str:
        result = "%s = '%s'" % (column_list[0], value_list[0])
    else:
        result = '%s = %s' % (column_list[0], str(value_list[0]))
    for i in range(1, len(column_list)):
        if mode == 'AND':
            result += ' AND '
        else:
            result += ' OR '
        if type(value_list[i]) is str:
            result += "%s = '%s'" % (column_list[i], value_list[i])
        else:
            result += '%s = %s' % (column_list[i], str(value_list[i]))
    return result


def trans2fuzzy_condition(column_list: list, value_list: list | None, mode='AND') -> str:
    if value_list is None:
        raise SystemError("\033[0;31;40;mvalue_list is None\033[0m")
    if type(value_list[0]) is str:
        result = f"{column_list[0]} LIKE '%{value_list[0]}%'"
    else:
        result = '%s = %s' % (column_list[0], str(value_list[0]))
    for i in range(1, len(column_list)):
        if mode == 'AND':
            result += ' AND '
        else:
            result += ' OR '
        if type(value_list[i]) is str:
            result += f"{column_list[i]} LIKE '%{value_list[i]}%'"
        else:
            result += '%s = %s' % (column_list[i], str(value_list[i]))
    return result


if __name__ == '__main__':
    DB = DataBase()
    print('main code in database/DataBase.py end')
