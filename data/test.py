from requests import get, post, delete, put


print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/q').json())
print(get('http://localhost:5000/api/v2/users/2').json())
print(get('http://localhost:5000/api/v2/users/1').json())
print('---------------------')
print(post('http://localhost:5000/api/v2/users').json())
print(post('http://localhost:5000/api/v2/users',
           json={'nade': 'name',
                 'adasdut': 'about',
                 'hashfsaffafd_password': 'hashed_password',
                 'embvf': 'email'}).json())
print(post('http://localhost:5000/api/v2/users',
           json={'title': 'wwwe',
                 'name': 'name',
                 'about': 'about',
                 'hashed_password': 'hashed_password',
                 'email': 'email'}).json())
print('---------------------')
print(delete('http://localhost:5000/api/v2/users').json())
print(delete('http://localhost:5000/api/v2/users/q').json())
print(delete('http://localhost:5000/api/v2/users/141').json())
print(delete('http://localhost:5000/api/v2/users/1').json())