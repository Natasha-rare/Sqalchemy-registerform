from datetime import datetime

from requests import get, post, delete, put


print(get('http://localhost:5000/api/v2/users').json())
print(post('http://localhost:5000/api/v2/users',
            json={'surname': 'Urna2',
                  'name': 'Ame',
                  'age': 25,
                  'position': 'marsolet',
                  'speciality': 'engineer',
                  'address': 'module_1',
                  'email': 'e12@mail.ru',
                  'hashed_password': '1234'
                  }).json())  # cool request
print(get('http://localhost:5000/api/v2/users').json())

print(get('http://localhost:5000/api/v2/users/1').json())

print(get('http://localhost:5000/api/v2/users/999').json())
# новости с id = 999 нет в базе
print(get('http://localhost:5000/api/v2/users/q').json())

print(delete('http://localhost:5000/api/v2/users/999').json())
# новости с id = 999 нет в базе

print(delete('http://localhost:5000/api/v2/users/1').json())



print(put('http://localhost:5000/api/v2/users/2',
            json={'age': 26
                  }).json())