from database import DataBase
from .exceptions import CounterNotExist,UserNotExist,UnauthorizedAccess,CanteenNotExist

connect = DataBase.DataBase().connect
cursor = connect.cursor()

def counter_get_by_uuid(uuid:str):

    cursor.execute(f'SELECT * FROM {DataBase.counter_table_name} WHERE uuid = ?', (uuid, ))
    temp = cursor.fetchone()

    if temp is None:
        raise CounterNotExist(uuid)
    
    counter_item = dict(zip(DataBase.counter_require_list, temp))
    counter_item['uuid'] = uuid
    counter_item['available'] = counter_item['available']==1
    counter_item['image_uuid'] = str(counter_item['image_uuid'])
    counter_item['canteen_uuid'] = str(counter_item['canteen_uuid'])

    cursor.execute(f'SELECT dish_id FROM {DataBase.counter_dish_table} WHERE counter_id = ?', (uuid, ))
    counter_item['dishes_uuids'] = [i[0] for i in cursor.fetchall()]

    return counter_item

def counter_get_all():
    
    cursor.execute(f'SELECT uuid FROM {DataBase.counter_table_name}')
    temp = [str(i[0]) for i in cursor.fetchall()]
    return temp

def counter_search(keyword: str):

    cursor.execute(f'SELECT uuid FROM {DataBase.counter_table_name} WHERE name LIKE ?', ("%"+keyword+"%",))
    temp = [str(i[0]) for i in cursor.fetchall()]
    return temp

def counter_add(user_uuid:str, name: str, canteen_uuid:str, description: str, image: bytes):

    cursor.execute(f'SELECT is_admin FROM {DataBase.user_table_name} WHERE uuid=?', (user_uuid, ))
    temp = cursor.fetchone()
    if temp is None:
        raise UserNotExist(user_uuid)
    
    if temp[0] != 1:
        raise UnauthorizedAccess(user_uuid)
    
    cursor.execute(f'SELECT * FROM {DataBase.canteen_table_name} WHERE uuid=?', (canteen_uuid,))
    temp = cursor.fetchone()
    if temp is None:
        raise CanteenNotExist(canteen_uuid)
    
    cursor.execute(f'INSERT INTO {DataBase.image_table_name} (content) VALUES (?)',(image,))
    image_uuid = cursor.lastrowid

    cursor.execute(f'INSERT INTO {DataBase.counter_table_name} (name,description,image_uuid,canteen_uuid) VALUES (?,?,?,?)', (name, description, image_uuid, canteen_uuid))
    counter_uuid = cursor.lastrowid

    connect.commit()
    return str(counter_uuid)

def counter_modify(user_uuid:str, counter_uuid:str, name:str, canteen_uuid:str, description:str, image:bytes):

    cursor.execute(f'SELECT is_admin FROM {DataBase.user_table_name} WHERE uuid=?', (user_uuid, ))
    temp = cursor.fetchone()
    if temp is None:
        raise UserNotExist(user_uuid)
    
    if temp[0] != 1:
        raise UnauthorizedAccess(user_uuid)
    
    cursor.execute(f'SELECT * FROM {DataBase.canteen_table_name} WHERE uuid=?', (canteen_uuid,))
    temp = cursor.fetchone()
    if temp is None:
        raise CanteenNotExist(canteen_uuid)
    
    cursor.execute(f'SELECT image_uuid FROM {DataBase.counter_table_name} WHERE uuid=?',(counter_uuid,))
    temp = cursor.fetchone()
    if temp is None:
        raise CounterNotExist(counter_uuid)
    image_uuid = temp[0]
    
    cursor.execute(f'UPDATE {DataBase.counter_table_name} SET name=?,description=?,canteen_uuid=? WHERE uuid=?', (name, description, canteen_uuid, counter_uuid))

    cursor.execute(f'UPDATE {DataBase.image_table_name} SET content=? WHERE uuid=?',(image, image_uuid))
    connect.commit()
    return True

def counter_delete(user_uuid:str, counter_uuid:str):

    cursor.execute(f'SELECT is_admin FROM {DataBase.user_table_name} WHERE uuid=?', (user_uuid, ))
    temp = cursor.fetchone()
    if temp is None:
        raise UserNotExist(user_uuid)
    
    if temp[0] != 1:
        raise UnauthorizedAccess(user_uuid)
    
    cursor.execute(f'SELECT available FROM {DataBase.counter_table_name} WHERE uuid=?',(counter_uuid,))
    temp = cursor.fetchone()
    if temp is None:
        raise CounterNotExist(counter_uuid)
    
    if temp[0] == 1:
        cursor.execute(f'UPDATE {DataBase.counter_table_name} SET available = 0 WHERE uuid=?',(counter_uuid,))
        cursor.execute(f'DELETE FROM {DataBase.counter_dish_table} WHERE counter_id = ?', (counter_uuid, ))
        connect.commit()

    return True
