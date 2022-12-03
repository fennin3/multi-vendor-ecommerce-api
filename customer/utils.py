

def pop_value(user_data: dict,key: str):
    try:
        user_data.pop(key)
    except KeyError:
        pass
    return user_data