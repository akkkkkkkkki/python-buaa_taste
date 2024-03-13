import uuid
import random

import database.DataBase as DB
import backend.exceptions as exc

from backend.dish import dish_most_popular
from backend.dish import dish_top_rated

db = DB.DataBase()


def _query_user_name(user_name: str) -> bool:
    result = db.search_from_table(table_name='Users',
                                  column_list=['name'],
                                  value_list=[user_name])
    return result != []


def _query_user_uuid(user_uuid: str) -> bool:
    result = db.search_from_table(table_name='Users',
                                  column_list=['uuid'],
                                  value_list=[user_uuid])
    return result != []


def _query_dish_uuid(dish_uuid: str) -> bool:
    result = db.search_from_table(table_name='Dish',
                                  column_list=['uuid', 'available'],
                                  value_list=[int(dish_uuid), 1])
    return result != []


def _create_user(user_name: str, admin: int, password: str):
    user_uuid = uuid.uuid5(uuid.NAMESPACE_URL, user_name + password)
    db.insert_into_table(table_name='Users',
                         value_list=[str(user_uuid), user_name, admin, password])


def _check_login(user_name: str, password: str) -> str:
    user_uuid = ''
    result = db.search_from_table(table_name='Users',
                                  result_list=['uuid'],
                                  column_list=['name', 'password'],
                                  value_list=[user_name, password])
    if result:
        user_uuid += result[0][0]
    return user_uuid


def _get_recommend_dishes(user_uuid: str) -> list[str]:
    people_prefer_list = []
    popular_dishes = dish_most_popular()
    high_score_dishes = dish_top_rated()
    for dish_uuid in popular_dishes:
        if dish_uuid in high_score_dishes and dish_uuid not in people_prefer_list:
            people_prefer_list.append(dish_uuid)
    user_dishes = db.search_from_table(table_name='user_dish',
                                       result_list=['dish_id', 'favorite', 'recommend'],
                                       column_list=['user_id'],
                                       value_list=[user_uuid])
    user_tags = []
    for elm in user_dishes:
        if _query_dish_uuid(str(elm[0])) and elm[1] == 1 and elm[2] == 1:
            prefer_dish_id = elm[0]
            tmp = db.search_from_table(table_name='dish_tag',
                                       result_list=['tag_id'],
                                       column_list=['dish_id'],
                                       value_list=[prefer_dish_id])
            for user_tag_id in tmp:
                if user_tag_id[0] not in user_tags:
                    user_tags.append(user_tag_id[0])
    user_prefer_list = []
    for user_tag_id in user_tags:
        tag_related_dishes = db.search_from_table(table_name='dish_tag',
                                                  result_list=['dish_id'],
                                                  column_list=['tag_id'],
                                                  value_list=[user_tag_id])
        for dish in tag_related_dishes:
            dish_uuid = str(dish[0])
            if dish_uuid not in user_prefer_list and dish_uuid not in people_prefer_list:
                user_prefer_list.append(dish_uuid)
    if len(people_prefer_list) > 5:
        list1 = random.sample(people_prefer_list, 5)
    else:
        list1 = []
        for dish_uuid in people_prefer_list:
            list1.append(dish_uuid)
    if len(user_prefer_list) > 3:
        list2 = random.sample(user_prefer_list, 3)
    else:
        list2 = []
        for dish_uuid in user_prefer_list:
            list2.append(dish_uuid)
    result = list1 + list2
    if len(result) < 8:
        extend_list = db.search_from_table(table_name='Dish',
                                           result_list=['uuid'])
        while len(result) < 8:
            extend_dish = random.sample(extend_list, 1)[0][0]
            if str(extend_dish) not in result:
                result.append(str(extend_dish))
    return result


def _get_records_uuids(user_uuid: str) -> list[str]:
    tmp = db.search_from_table('Record',
                               result_list=['uuid', 'time'],
                               column_list=['user_id'],
                               value_list=[user_uuid])
    tmp = sorted(tmp, key=lambda elm: elm[1], reverse=True)
    result = []
    for record in tmp:
        result.append(str(record[0]))
    return result


def _get_favorite_dishes_uuids(user_uuid: str) -> list[str]:
    tmp = db.search_from_table('user_dish',
                               result_list=['dish_id'],
                               column_list=['user_id', 'favorite'],
                               value_list=[user_uuid, 1])
    result = []
    for dish in tmp:
        result.append(str(dish[0]))
    return result


def _get_favorite_counters_uuids(user_uuid: str) -> list[str]:
    tmp = db.search_from_table('user_counter',
                               result_list=['counter_id'],
                               column_list=['user_id', 'favorite'],
                               value_list=[user_uuid, 1])
    result = []
    for counter in tmp:
        result.append(str(counter[0]))
    return result


def _if_favorite_exists(user_uuid: str, dish_uuid: int) -> bool:
    result = db.search_from_table(table_name='user_dish',
                                  column_list=['user_id', 'dish_id'],
                                  value_list=[user_uuid, dish_uuid])
    return result != []


def user_register(username: str, password: str, is_admin: bool = False) -> bool:
    if _query_user_name(username):
        raise exc.UserAlreadyExists(username)
    else:
        if not is_admin:
            _create_user(username, 0, password)
        else:
            _create_user(username, 1, password)
        return True


def user_login(username: str, password: str) -> str:
    if not _query_user_name(username):
        raise exc.UserNotFound(username)
    user_uuid = _check_login(username, password)
    if user_uuid == '':
        raise exc.WrongPassword()
    return user_uuid


def user_get_uuids(user_uuid: str) -> dict[str, str | bool | list[str]]:
    """{
        'uuid': str,
        'username': str,
        'is_admin': bool,
        'recommend_dishes': List[str],
        'records_uuids': List[str],  # 按照时间顺序排列
        'favorite_dishes_uuids': List[str],
        'favorite_counters_uuids': List[str],
    }"""
    result = dict()
    result['uuid'] = user_uuid
    tmp = db.search_from_table('Users',
                               result_list=['name', 'is_admin'],
                               column_list=['uuid'],
                               value_list=[user_uuid])
    result['username'] = tmp[0][0]
    result['is_admin'] = tmp[0][1] == 1
    result['recommend_dishes'] = _get_recommend_dishes(user_uuid)
    result['records_uuids'] = _get_records_uuids(user_uuid)
    result['favorite_dishes_uuids'] = _get_favorite_dishes_uuids(user_uuid)
    result['favorite_counters_uuids'] = _get_favorite_counters_uuids(user_uuid)
    return result


def user_update_username(user_uuid: str, new_username: str) -> bool:
    if not _query_user_uuid(user_uuid):
        raise exc.UserNotFound(user_uuid)
    if _query_user_name(new_username):
        raise exc.UsernameTaken(new_username)
    db.update_table('Users',
                    tgt_column_list=['name'],
                    tgt_value_list=[new_username],
                    src_column_list=['uuid'],
                    src_value_list=[user_uuid])
    return True


def user_update_password(user_uuid: str, new_password: str) -> bool:
    if not _query_user_uuid(user_uuid):
        raise exc.UserNotFound(user_uuid)
    db.update_table('Users',
                    tgt_column_list=['password'],
                    tgt_value_list=[new_password],
                    src_column_list=['uuid'],
                    src_value_list=[user_uuid])
    return True


def user_record(user_uuid: str, dish_uuid: str, time: str) -> str:
    if not _query_user_uuid(user_uuid):
        raise exc.UserNotFound(user_uuid)
    if not _query_dish_uuid(dish_uuid):
        raise exc.DishNotFound(dish_uuid)
    db.insert_into_table(table_name='Record',
                         value_list=[user_uuid, int(dish_uuid), time],
                         column_list=['user_id', 'dish_id', 'time'])
    record = db.search_from_table(table_name='Record',
                                  result_list=['uuid'],
                                  column_list=['user_id', 'dish_id', 'time'],
                                  value_list=[user_uuid, int(dish_uuid), time])
    return record[0][0]


def user_add_favorite(user_uuid: str, dish_uuid: str) -> bool:
    if not _query_user_uuid(user_uuid):
        raise exc.UserNotFound(user_uuid)
    if not _query_dish_uuid(dish_uuid):
        raise exc.DishNotFound(dish_uuid)
    if _if_favorite_exists(user_uuid, int(dish_uuid)):
        db.update_table(table_name='user_dish',
                        tgt_column_list=['favorite'],
                        tgt_value_list=[1],
                        src_column_list=['user_id', 'dish_id'],
                        src_value_list=[user_uuid, int(dish_uuid)])
    else:
        db.insert_into_table(table_name='user_dish',
                             column_list=['user_id', 'dish_id', 'favorite'],
                             value_list=[user_uuid, int(dish_uuid), 1])
    return True


def user_remove_favorite(user_uuid: str, dish_uuid: str) -> bool:
    if not _query_user_uuid(user_uuid):
        raise exc.UserNotFound(user_uuid)
    if not _query_dish_uuid(dish_uuid):
        raise exc.DishNotFound(dish_uuid)
    db.update_table(table_name='user_dish',
                    tgt_column_list=['favorite'],
                    tgt_value_list=[0],
                    src_column_list=['user_id', 'dish_id'],
                    src_value_list=[user_uuid, int(dish_uuid)])
    return True


def user_get_favorite(user_uuid: str) -> list[str]:
    if not _query_user_uuid(user_uuid):
        raise exc.UserNotFound(user_uuid)
    return _get_favorite_dishes_uuids(user_uuid)


def user_get_records(user_uuid: str) -> list[str]:
    if not _query_user_uuid(user_uuid):
        raise exc.UserNotFound(user_uuid)
    return _get_records_uuids(user_uuid)


def check_record(user_uuid: str, dish_uuid: str) -> bool:
    result = db.search_from_table(table_name='Record',
                                  column_list=['user_id', 'dish_id'],
                                  value_list=[user_uuid, int(dish_uuid)])
    return result != []


def check_favorite(user_uuid: str, dish_uuid: str) -> bool:
    result = db.search_from_table(table_name='user_dish',
                                  column_list=['user_id', 'dish_id', 'favorite'],
                                  value_list=[user_uuid, int(dish_uuid), 1])
    return result != []


if __name__ == '__main__':
    pass
