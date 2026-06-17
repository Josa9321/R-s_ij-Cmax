from logging import exception
import requests
import json

if __name__ == '__main__':
    with open('example_instance.json') as f:
        instance = json.load(f)

    response_cmax = requests.post('http://localhost:5000/cmax', json=instance)
    if response_cmax.status_code == 200:
        print(response_cmax.json())
        with open('example_solution_cmax.json', 'w') as f:
            json.dump(response_cmax.json(), f, indent=4)

    response_et = requests.post('http://localhost:5000/et', json=instance)
    if response_et.status_code == 200:
        print(response_et.json())
        with open('example_solution_et.json', 'w') as f:
            json.dump(response_et.json(), f, indent=4)

    else:
        exception('An error has occured')
