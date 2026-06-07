from logging import exception
import requests
import json

if __name__ == '__main__':
    with open('example_instance.json') as f:
        instance = json.load(f)

    response = requests.post('http://localhost:5000/cmax', json=instance)
    if response.status_code == 200:
        print(response.json())
        with open('example_solution.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
        
    else:
        exception('An error has occured')
