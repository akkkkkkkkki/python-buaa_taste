import random
from typing import Optional

import database.DataBase as DB
import backend.exceptions as exc

db = DB.DataBase()


def _query_dish_uuid(dish_uuid: str) -> bool:
    result = db.search_from_table(table_name='Dish',
                                  column_list=['uuid', 'available'],
                                  value_list=[int(dish_uuid), 1])
    return result != []


def _query_tag(tag: str) -> int:
    result = db.search_from_table(table_name='tag',
                                  column_list=['tag'],
                                  value_list=[tag])
    if result:
        return result[0][2]
    else:
        return 0


def _get_counters_by_dish(dish_uuid: str) -> list[str]:
    tmp = db.search_from_table(table_name='counter_dish',
                               result_list=['counter_id'],
                               column_list=['dish_id'],
                               value_list=[int(dish_uuid)])
    result = []
    for counter in tmp:
        result.append(str(counter[0]))
    return result


def _get_ratings(dish_uuid: str) -> list[int]:
    tmp = db.search_from_table(table_name='Comment',
                               result_list=['rating'],
                               column_list=['dish_id'],
                               value_list=[int(dish_uuid)])
    result = [0, 0, 0, 0, 0]
    for rate in tmp:
        result[int(rate[0]) - 1] += 1
    return result


def _get_comments(dish_uuid: str) -> list[str]:
    tmp = db.search_from_table(table_name='Comment',
                               result_list=['uuid'],
                               column_list=['is_main', 'dish_id'],
                               value_list=[1, int(dish_uuid)])
    result = []
    for comment in tmp:
        result.append(comment[0])
    return result


def _get_tags(dish_uuid: str) -> list[str]:
    result = []
    tag_id_list = db.search_from_table(table_name='dish_tag',
                                       result_list=['tag_id'],
                                       column_list=['dish_id'],
                                       value_list=[int(dish_uuid)])
    for elm in tag_id_list:
        tag_id = elm[0]
        tag = db.search_from_table(table_name='tag',
                                   result_list=['tag'],
                                   column_list=['uuid'],
                                   value_list=[tag_id])[0][0]
        result.append(tag)
    return result


def _calc_avg_rate(dish_uuid: str) -> float:
    sum = 0
    cnt = 0
    tmp = db.search_from_table(table_name='Comment',
                               result_list=['rating'],
                               column_list=['dish_id'],
                               value_list=[int(dish_uuid)])
    for rate in tmp:
        sum += rate[0]
        cnt += 1
    if cnt != 0:
        return sum / cnt
    else:
        return 0.0


def _check_privilege(user_uuid: str) -> bool:
    tmp = db.search_from_table(table_name='Users',
                               result_list=['is_admin'],
                               column_list=['uuid'],
                               value_list=[user_uuid])
    return tmp[0][0] == 1


# def _tag_list2str(tag_list: list) -> str:
#     result = tag_list[0]
#     for i in range(1, len(tag_list)):
#         result += ',%s' % tag_list[i]
#     return result


def _add_tags(tag_list: list):
    for tag in tag_list:
        cnt = _query_tag(tag)
        if cnt > 0:
            db.update_table(table_name='tag',
                            tgt_column_list=['count'],
                            tgt_value_list=[cnt + 1],
                            src_column_list=['tag'],
                            src_value_list=[tag])
        else:
            db.insert_into_table(table_name='tag',
                                 column_list=['tag', 'count'],
                                 value_list=[tag, 1])


def _remove_tags(tag_list: list):
    for tag in tag_list:
        cnt = _query_tag(tag)
        if cnt > 1:
            db.update_table(table_name='tag',
                            tgt_column_list=['count'],
                            tgt_value_list=[cnt - 1],
                            src_column_list=['tag'],
                            src_value_list=[tag])
        else:
            db.delete_from_table(table_name='tag',
                                 column_list=['tag'],
                                 value_list=[tag])


def _tag2tag_id(tag_list: list) -> list:
    result = []
    for tag in tag_list:
        tag_id = db.search_from_table(table_name='tag',
                                      result_list=['uuid'],
                                      column_list=['tag'],
                                      value_list=[tag])[0][0]
        result.append(tag_id)
    return result


def _extend2len(result: list[str], length: int):
    while len(result) < length:
        dish_list = db.search_from_table(table_name='Dish',
                                         result_list=['uuid'],
                                         column_list=['available'],
                                         value_list=[1])
        extend_list = random.sample(dish_list, length - len(result))
        for extend_dish in extend_list:
            if str(extend_dish[0]) not in result:
                result.append(str(extend_dish[0]))
    return result


def dish_get_by_uuid(uuid: str) -> dict[str, str | int | float | bool | list[str] | list[int]]:
    """{
        'uuid': str,
        'available': bool
        'name': str,
        'description': str,
        'price': float,
        'image_uuid': str
        'tags': List[str],
        'counters_uuids': List[str],
        'rating_average': float,
        'ratings': List[int],
        'comments_ids': List[str]
    }"""
    if not _query_dish_uuid(uuid):
        raise exc.DishNotFound(uuid)
    result = dict()
    tmp = db.search_from_table(table_name='Dish',
                               column_list=['uuid'],
                               value_list=[int(uuid)])[0]
    result['uuid'] = uuid
    result['available'] = tmp[1] == 1
    result['name'] = tmp[2]
    result['description'] = tmp[3]
    result['price'] = tmp[4]
    result['image_uuid'] = str(tmp[5])
    # result['tags'] = tmp[6].split(',')
    result['tags'] = _get_tags(uuid)
    result['counters_uuids'] = _get_counters_by_dish(uuid)
    result['rating_average'] = _calc_avg_rate(uuid)
    result['ratings'] = _get_ratings(uuid)
    result['comments_ids'] = _get_comments(uuid)
    """DataBase = DB.DataBase()
    result['tags'] = []
    DataBase.cursor.execute(f'SELECT tag_id FROM dish_tag WHERE dish_id = ?', (uuid, ))
    temp = DataBase.cursor.fetchall()
    for i in temp:
        DataBase.cursor.execute(f'SELECT tag FROM tag WHERE uuid = ?', (i[0], ))
        result['tags'].append(DataBase.cursor.fetchone()[0])"""
    return result


def dish_get_all_uuids() -> list[str]:
    tmp = db.search_from_table(table_name='Dish',
                               result_list=['uuid'],
                               column_list=['available'],
                               value_list=[1])
    result = []
    for dish in tmp:
        result.append(str(dish[0]))
    return result


def dish_search(keyword: str) -> list[str]:
    list1 = db.fuzzy_search(table_name='Dish',
                            result_list=['uuid'],
                            column_list=['name', 'available'],
                            value_list=[keyword, 1],
                            mode='AND')
    list2 = db.fuzzy_search(table_name='tag',
                            result_list=['uuid'],
                            column_list=['tag'],
                            value_list=[keyword])
    result = []
    for dish_uuid in list1:
        if str(dish_uuid[0]) not in list1:
            result.append(str(dish_uuid[0]))
    for tag_uuid in list2:
        tmp = db.search_from_table(table_name='dish_tag',
                                   result_list=['dish_id'],
                                   column_list=['tag_id'],
                                   value_list=[tag_uuid[0]])
        for elm in tmp:
            if str(elm[0]) not in result:
                result.append(str(elm[0]))
    return result


def dish_add(
        user_uuid: str,
        name: str,
        description: str,
        price: float,
        image: bytes,
        tags: list[str],
        counters_uuids: list[str]) -> str:
    if not _check_privilege(user_uuid):
        raise exc.UnauthorizedAccess()
    db.insert_image('Image', 'content', image)
    image_uuid = db.search_last_record('Image', 'uuid')[0][0]
    db.insert_into_table(table_name='Dish',
                         column_list=['available', 'name', 'description', 'price', 'image_uuid'],
                         value_list=[1, name, description, price, image_uuid])
    dish_uuid = db.search_last_record('Dish', 'uuid')[0][0]
    for counter in counters_uuids:
        db.insert_into_table(table_name='counter_dish',
                             value_list=[int(counter), dish_uuid])
    _add_tags(tags)
    for tag in tags:
        tag_id = db.search_from_table(table_name='tag',
                                      result_list=['uuid'],
                                      column_list=['tag'],
                                      value_list=[tag])[0][0]
        db.insert_into_table(table_name='dish_tag',
                             value_list=[dish_uuid, tag_id])
    return str(dish_uuid)


def dish_modify(
        user_uuid: str,
        dish_uuid: str,
        name: str,
        description: str,
        price: float,
        image: bytes,
        tags: list[str],
        counters: list[str]
) -> bool:
    if not _check_privilege(user_uuid):
        raise exc.UnauthorizedAccess()
    if not _query_dish_uuid(dish_uuid):
        raise exc.DishNotFound(dish_uuid)
    origin_tag_list = _get_tags(dish_uuid)
    _add_tags(tags)
    _remove_tags(origin_tag_list)
    db.delete_from_table(table_name='dish_tag',
                         column_list=['dish_id'],
                         value_list=[int(dish_uuid)])
    new_tag_id_list = _tag2tag_id(tags)
    for new_tag_id in new_tag_id_list:
        db.insert_into_table(table_name='dish_tag',
                             value_list=[int(dish_uuid), new_tag_id])
    db.insert_image('Image', 'content', image)
    image_uuid = db.search_last_record('Image', 'uuid')[0][0]
    db.update_table(table_name='Dish',
                    tgt_column_list=['name', 'description', 'price', 'image_uuid'],
                    tgt_value_list=[name, description, price, image_uuid],
                    src_column_list=['uuid'],
                    src_value_list=[int(dish_uuid)])
    db.delete_from_table(table_name='counter_dish',
                         column_list=['dish_id'],
                         value_list=[int(dish_uuid)])
    for counter in counters:
        db.insert_into_table(table_name='counter_dish',
                             column_list=['counter_id', 'dish_id'],
                             value_list=[int(counter), int(dish_uuid)])
    return True


def dish_delete(user_uuid: str, dish_uuid: str) -> bool:
    if not _check_privilege(user_uuid):
        raise exc.UnauthorizedAccess()
    if not _query_dish_uuid(dish_uuid):
        raise exc.DishNotFound(dish_uuid)
    origin_tag_list = _get_tags(dish_uuid)
    _remove_tags(origin_tag_list)
    db.delete_from_table(table_name='dish_tag',
                         column_list=['dish_id'],
                         value_list=[int(dish_uuid)])
    db.delete_from_table(table_name='counter_dish',
                         column_list=['dish_id'],
                         value_list=[int(dish_uuid)])
    db.update_table(table_name='Dish',
                    tgt_column_list=['available'],
                    tgt_value_list=[0],
                    src_column_list=['uuid'],
                    src_value_list=[int(dish_uuid)])
    return True


def dish_comment(
        user_uuid: str,
        dish_uuid: str,
        time: str,  # YYYY-MM-DD HH:MM
        title: str,
        content: str,
        rating: float,
        image: Optional[bytes]
) -> str:
    if not _query_dish_uuid(dish_uuid):
        raise exc.DishNotFound(dish_uuid)
    if image is not None:
        db.insert_image('Image', 'content', image)
        image_uuid = db.search_last_record('Image', 'uuid')[0][0]
        db.insert_into_table(table_name='Comment',
                             column_list=['is_main', 'user_id', 'time', 'title', 'content',
                                          'image_uuid', 'dish_id', 'rating'],
                             value_list=[1, user_uuid, time, title, content, image_uuid, int(dish_uuid), rating])
    else:
        db.insert_into_table(table_name='Comment',
                             column_list=['is_main', 'user_id', 'time', 'title', 'content', 'dish_id', 'rating'],
                             value_list=[1, user_uuid, time, title, content, int(dish_uuid), rating])
    comment = db.search_last_record('Comment', 'uuid')
    return comment[0][0]


def dish_most_popular() -> list[str]:
    comment_list = db.search_from_table(table_name='Comment',
                                        result_list=['dish_id'],
                                        column_list=['is_main'],
                                        value_list=[1])
    comment_cnt_dict = dict()
    for comment in comment_list:
        dish_uuid = comment[0]
        if _query_dish_uuid(str(dish_uuid)):
            if dish_uuid in comment_cnt_dict.keys():
                comment_cnt_dict[dish_uuid] += 1
            else:
                comment_cnt_dict[dish_uuid] = 1
    comment_cnt_list = sorted(comment_cnt_dict.items(), key=lambda item: item[1], reverse=True)
    i = 0
    result = []
    while i < len(comment_cnt_list) and i < 20:
        result.append(str(comment_cnt_list[i][0]))
        i += 1
    if len(result) < 20:
        _extend2len(result, 20)
    return result


def dish_top_rated() -> list[str]:
    rate_list = db.search_from_table(table_name='Comment',
                                     result_list=['dish_id', 'rating'],
                                     column_list=['is_main'],
                                     value_list=[1])
    rate_sum_dict = dict()
    rate_cnt_dict = dict()
    for elm in rate_list:
        dish_uuid = elm[0]
        rate = elm[1]
        if _query_dish_uuid(str(dish_uuid)):
            if dish_uuid in rate_sum_dict.keys():
                rate_sum_dict[dish_uuid] += rate
                rate_cnt_dict[dish_uuid] += 1
            else:
                rate_sum_dict[dish_uuid] = rate
                rate_cnt_dict[dish_uuid] = 1
    rate_avg_dict = dict()
    for dish_uuid in rate_sum_dict.keys():
        rate_avg_dict[dish_uuid] = rate_sum_dict[dish_uuid] / rate_cnt_dict[dish_uuid]
    rate_avg_list = sorted(rate_avg_dict.items(), key=lambda item: item[1], reverse=True)
    i = 0
    result = []
    while i < len(rate_avg_list) and i < 20:
        result.append(str(rate_avg_list[i][0]))
        i += 1
    if len(result) < 20:
        _extend2len(result, 20)
    return result
