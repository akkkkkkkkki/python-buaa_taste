from database import DataBase
from .exceptions import CanteenNotFound,UnauthorizedAccess,UserNotExist

connect = DataBase.DataBase().connect
cursor = connect.cursor()

def canteen_get_by_uuid(uuid:str):

    cursor.execute(f'SELECT * FROM {DataBase.canteen_table_name} WHERE uuid=?',(uuid,))
    temp = cursor.fetchone()
    if temp is None:
        raise CanteenNotFound(uuid)

    canteen_item = dict(zip(DataBase.canteen_require_list, temp))

    canteen_item['uuid'] = uuid
    canteen_item['image_uuid'] = str(canteen_item['image_uuid'])
    canteen_item['available'] = canteen_item['available'] == 1

    cursor.execute(f'SELECT uuid FROM {DataBase.counter_table_name} WHERE canteen_uuid=?',(uuid,))

    canteen_item['counters_uuids'] = [i[0] for i in cursor.fetchall()]

    return canteen_item

def canteen_get_all_ids():
    cursor.execute(f'SELECT uuid FROM {DataBase.canteen_table_name}')
    canteens_uuids = [str(i[0]) for i in cursor.fetchall()]
    return canteens_uuids



def canteen_search(keyword:str):
    cursor.execute(f'SELECT uuid FROM {DataBase.canteen_table_name} WHERE name LIKE ?', ("%"+keyword+"%",))
    canteens_uuids = [str(i[0]) for i in cursor.fetchall()]
    return canteens_uuids


def canteen_add(user_uuid:str, name:str, description: str, image: bytes):

    cursor.execute(f'SELECT is_admin FROM {DataBase.user_table_name} WHERE uuid=?', (user_uuid,))
    temp = cursor.fetchone()
    if temp is None:
        raise UserNotExist(user_uuid)
    if temp[0] != 1:
        raise UnauthorizedAccess(user_uuid)

    cursor.execute(f'INSERT INTO {DataBase.image_table_name} (content) VALUES (?)',(image,))
    image_uuid = cursor.lastrowid

    cursor.execute(f'INSERT INTO {DataBase.canteen_table_name} (name, image_uuid, description) VALUES (?,?,?)', (name, image_uuid, description))
    canteen_uuid = cursor.lastrowid

    connect.commit()
    return str(canteen_uuid)

def canteen_modify(user_uuid: str, canteen_uuid: str, name: str, description: str, image: bytes):
    
    cursor.execute(f'SELECT is_admin FROM {DataBase.user_table_name} WHERE uuid=?', (user_uuid,))
    temp = cursor.fetchone()
    if temp is None:
        raise UserNotExist(user_uuid)
    if temp[0] != 1:
        raise UnauthorizedAccess(user_uuid)
    
    cursor.execute(f'SELECT image_uuid FROM {DataBase.canteen_table_name} WHERE uuid=?',(canteen_uuid,))
    temp = cursor.fetchone()
    if temp is None:
        raise CanteenNotFound(canteen_uuid)
    image_uuid = temp[0]

    cursor.execute(f'UPDATE {DataBase.canteen_table_name} SET name=?,description=? WHERE uuid=?',(name, description, canteen_uuid))

    cursor.execute(f'UPDATE {DataBase.image_table_name} SET content=? WHERE uuid=?',(image, image_uuid))

    connect.commit()
    return True

def canteen_delete(user_uuid:str, canteen_uuid:str):

    cursor.execute(f'SELECT is_admin FROM {DataBase.user_table_name} WHERE uuid=?', (user_uuid, ))
    temp = cursor.fetchone()
    if temp is None:
        raise UserNotExist(user_uuid)
    if temp[0] != 1:
        raise UnauthorizedAccess(user_uuid)
    
    cursor.execute(f'SELECT available FROM {DataBase.canteen_table_name} WHERE uuid=?',(canteen_uuid,))
    temp = cursor.fetchone()
    if temp is None:
        raise CanteenNotFound(canteen_uuid)
    
    if temp[0] == 1:
        cursor.execute(f'UPDATE {DataBase.canteen_table_name} SET available = 0 WHERE uuid=?',(canteen_uuid,))
        connect.commit()
    
    return True