from requests import get, post, delete, put

print(put('http://127.0.0.1:5000/api/users/1', json={'name': 'alinusik'}).json())
print(get('http://127.0.0.1:5000/api/users/1').json())

