from database import DataBase
from .exceptions import CommentNotExist
from typing import Literal

cursor = DataBase.DataBase().cursor
connect = DataBase.DataBase().connect


def comment_get_by_uuid(user_uuid: str, comment_uuid: str):
    """
    :param user_uuid: the universally unique identifier of user\n
    :param comment_uuid: the universally unique identifier of comment\n
    :returns: a dict contains items of a comment\n
    :raise CommentNotExist: if there is no such a comment
    """
    cursor.execute(f'SELECT * FROM {DataBase.comment_table_name} WHERE uuid = ?', (comment_uuid, ))
    temp = cursor.fetchone()
    if temp is None:
        raise CommentNotExist(comment_uuid)
    comment_item = dict(zip(DataBase.comment_require_list, temp))
    comment_item['uuid'] = str(comment_item['uuid'])
    comment_item['is_main'] = comment_item['is_main'] == 1
    comment_item['available'] = comment_item['available'] == 1
    comment_item['image_uuid'] = str(comment_item['image_uuid'])

    # cursor.execute(f'SELECT name FROM {DataBase.user_table_name} WHERE uuid=?',(comment_item['user_id'],))
    # comment_item['username'] = cursor.fetchone()[0]
    # comment_item.pop('user_id')

    cursor.execute('SELECT %s from %s WHERE comment_id = %s'%('attitude', DataBase.user_comment_table, comment_uuid))
    temp = cursor.fetchall()
    comment_item['like_count'] = temp.count((1,))
    comment_item['dislike_count'] = temp.__len__() - comment_item['like_count']
    cursor.execute(f'SELECT attitude from {DataBase.user_comment_table} WHERE user_id = ? AND comment_id = ?', (user_uuid, comment_uuid))
    temp = cursor.fetchone()
    if temp is None:
        comment_item['liked'] = comment_item['disliked'] = False
    else:
        comment_item['liked'] = temp[0] == 1
        comment_item['disliked'] = not comment_item['liked']
    cursor.execute('SELECT %s from %s WHERE reply_to_id = %s'%('uuid', DataBase.comment_table_name, comment_uuid))
    comment_item['replies_uuids'] = [i[0] for i in cursor.fetchall()]

    return comment_item


def comment_like(user_uuid:str, comment_uuid):
    """
    :param user_uuid: the universally unique identifier of user\n
    :param comment_uuid: the universally unique identifier of comment\n
    :returns: True\n
    :raise CommentNotExist: if there is no such a comment
    """
    return _comment_set_attituded(user_uuid, comment_uuid, 1)


def comment_dislike(user_uuid:str, comment_uuid):
    """
    :param user_uuid: the universally unique identifier of user\n
    :param comment_uuid: the universally unique identifier of comment\n
    :returns: True\n
    :raise CommentNotExist: if there is no such a comment
    """
    return _comment_set_attituded(user_uuid, comment_uuid, 0)


def comment_reply(user_uuid: str, comment_uuid: str, time:str, content:str, image_uuid:str|None = None):

    cursor.execute('SELECT * FROM %s WHERE uuid = ?'%(DataBase.comment_table_name), (comment_uuid, ))
    if cursor.fetchone() is None:
        raise CommentNotExist(comment_uuid)
    
    if image_uuid is None:
        cursor.execute(f'INSERT INTO {DataBase.comment_table_name} (is_main, user_id, time, content, reply_to_id) VALUES (?,?,?,?,?)', (0, user_uuid, time, content, comment_uuid))
    else:
        cursor.execute(f'INSERT INTO {DataBase.comment_table_name} (is_main, user_id, time, content, image_uuid, reply_to_id) VALUES (?,?,?,?,?,?)', (0, user_uuid, time, content, comment_uuid, image_uuid))
    connect.commit()

    return True


def comment_delete(user_uuid: str, comment_uuid:str):

    cursor.execute('SELECT user_id,available FROM %s WHERE uuid = ?'%(DataBase.comment_table_name), (comment_uuid, ))
    temp = cursor.fetchone()

    if temp is None:
        raise CommentNotExist(comment_uuid)
    
    user_id, available = temp

    if user_id != user_uuid:
        return False
    
    if available == 1:
        cursor.execute(f'UPDATE {DataBase.comment_table_name} SET available = 0 WHERE uuid = ?', (comment_uuid, ))
        connect.commit()

    return True
    
def comment_like_cancel(user_uuid:str, comment_uuid:str):
    return _comment_cancel_attitude(user_uuid, comment_uuid, 1)

def comment_dislike_cancel(user_uuid:str, comment_uuid:str):
    return _comment_cancel_attitude(user_uuid, comment_uuid, 0)
    
    





#########################################################################################################################################
########################################                                                #################################################
########################################                  break line                    #################################################
########################################                                                #################################################
#########################################################################################################################################

def _comment_set_attituded(user_uuid:str, comment_uuid:str, attitude:Literal[0, 1]):
    cursor.execute('SELECT * FROM %s WHERE uuid = ?'%(DataBase.comment_table_name), (comment_uuid, ))
    if cursor.fetchone() is None:
        raise CommentNotExist(comment_uuid)

    try:
        cursor.execute('INSERT INTO %s (user_id, comment_id, attitude) values (?,?,?)'%(DataBase.user_comment_table), (user_uuid, comment_uuid, attitude))
    except:
        cursor.execute(f'UPDATE {DataBase.user_comment_table} set attitude=? WHERE user_id = ? AND comment_id = ?', (attitude, user_uuid, comment_uuid))
    connect.commit()

    return True

def _comment_cancel_attitude(user_uuid:str, comment_uuid:str, attitude:Literal[0, 1]):
    cursor.execute('SELECT * FROM %s WHERE uuid = ?'%(DataBase.comment_table_name), (comment_uuid, ))
    if cursor.fetchone() is None:
        raise CommentNotExist(comment_uuid)
    cursor.execute(f'SELECT attitude FROM {DataBase.user_comment_table} WHERE user_id = ? AND comment_id = ?',(user_uuid, comment_uuid))
    temp = cursor.fetchone()
    if temp is not None and temp[0] == attitude:
        cursor.execute(f'DELETE FROM {DataBase.user_comment_table} WHERE user_id = ? AND comment_id = ?',(user_uuid, comment_uuid))
    return True
