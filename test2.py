from datetime import datetime

from requests import get, post, delete, put


print(get('http://localhost:5000/api/v2/jobs').json())

print(post('http://localhost:5000/api/v2/jobs',
            json={'job': 'development new robots',
                    'work_size': 25,
                    'collaborators': '2, 3',
                  'team_leader': 1,
                  'is_finished': False
                  }).json())  # cool request

print(post('http://localhost:5000/api/v2/jobs',
            json={'job': 'development new robots',
                  'team_leader': 1
                  }).json())  # cool request
print(get('http://localhost:5000/api/v2/jobs').json())

print(get('http://localhost:5000/api/v2/jobs/5').json())

print(get('http://localhost:5000/api/v2/jobs/q').json())

print(delete('http://localhost:5000/api/v2/jobs/4').json())

print(put('http://localhost:5000/api/v2/jobs/1',
            json={'team_leader': 2
                  }).json())