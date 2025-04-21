from typing import Dict

user_database = {
    "Alice": {"age": 28, "city": "New York"},
    "Bob": {"age": 32, "city": "Los Angeles"},
}

def update_profile(name, new_data) -> str:
    if name in user_database:
        user_database[name].update(new_data)
        return "successful update"
    else:
        return "no profile found"


update_profile("Alice", {"city": "San Jose"})

print(f"After update_profile, global user_database: {user_database}")


# so how to make the function pure? We need to eliminate the side effect it produces.
# But technically, we if we create a pure function, then it is pretty useless as side effects are required in daily life
# So, how do we remove side effects. It turns out we don't need to remove the side effects. We need to just separate them
# from the rest of our pure functional operations. In our case the side effect is mutation of the user_database. So
# we will remove the side effect by taking the database as an input, creating a copy of it and then changing the copy
# and finally returning it.

def pure_update_profile(database, name, new_data) -> Dict[str, str]:
    if name in database:
        new_database = database.copy()
        new_database[name] = new_database[name].copy()
        new_database[name].update(new_data)
        return new_database
    else:
        return database


new_db = pure_update_profile(user_database, "Alice", {"city": "Texas"})

print(f"modified data: \n\t\t{new_db}")
print(f"old data: \n\t\t{user_database}")

# Output:
# After update_profile, global user_database: {'Alice': {'age': 28, 'city': 'San Jose'}, 'Bob': {'age': 32, 'city': 'Los Angeles'}}
# modified data:
# 		{'Alice': {'age': 28, 'city': 'Texas'}, 'Bob': {'age': 32, 'city': 'Los Angeles'}}
# old data:
# 		{'Alice': {'age': 28, 'city': 'San Jose'}, 'Bob': {'age': 32, 'city': 'Los Angeles'}}