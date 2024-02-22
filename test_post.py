import requests

def send_post_request(url, data):
    response = requests.post(url, json=data)
    return response

if __name__ == "__main__":
    url = 'http://127.0.0.1:8000/presiones/'
    data = {
        "DateTime_dev": "2021-12-31T23:59:39",
        "device": "Sensor3",
        "value": 123.4567
    }

    response = send_post_request(url, data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}")

