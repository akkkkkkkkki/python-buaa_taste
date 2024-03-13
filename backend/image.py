from database import DataBase

cursor = DataBase.DataBase().cursor
_default_image = bytes(0)

def image_get_by_uuid(uuid:str):
    
    cursor.execute(f'SELECT content from {DataBase.image_table_name} WHERE uuid = ?', (uuid,))
    temp = cursor.fetchone()
    if temp is None:
        return _default_image
    else:
        return temp[0]