from database import DataBase
from .exceptions import RecordNotFound,UnauthorizedAccess,UserNotExist

connect = DataBase.DataBase().connect
cursor = connect.cursor()

def record_get_by_uuid(uuid:str):
    
    cursor.execute(f'SELECT * FROM {DataBase.record_table_name} WHERE uuid = ?', (uuid, ))
    temp = cursor.fetchone()
    if temp is None:
        raise RecordNotFound(uuid)
    record_item = dict(zip(DataBase.record_require_list, temp))
    record_item.pop('user_id')
    record_item['uuid'] = uuid
    return record_item


def record_delete(uuid: str):

    cursor.execute(f'SELECT uuid FROM {DataBase.record_table_name} WHERE uuid = ?', (uuid, ))
    if cursor.fetchone() is None:
        raise RecordNotFound(uuid)

    cursor.execute(f'DELETE FROM {DataBase.record_table_name} WHERE uuid = ?', (uuid, ))
    connect.commit()
    return True

def record_modify(user_uuid:str, record_uuid:str, dish_uuid:str, time:str):

    cursor.execute(f'SELECT * FROM {DataBase.record_table_name} WHERE uuid = ?', (record_uuid, ))
    temp = cursor.fetchone()
    if temp is None:
        raise RecordNotFound(record_uuid)

    cursor.execute(f'SELECT is_admin FROM {DataBase.user_table_name} WHERE uuid=?', (user_uuid, ))
    temp = cursor.fetchone()
    if temp is None:
        raise UserNotExist(user_uuid)
    
    if temp[0] != 1:
        raise UnauthorizedAccess(user_uuid)
    
    cursor.execute(f'UPDATE {DataBase.record_table_name} SET time = ?, dish_id = ? WHERE uuid = ?', (time, dish_uuid, record_uuid))
    return True
