import requests


def request_quote():
    r = requests.get(input("Input the URL:\n"))
    try:
        print(r.json()["content"])
    except KeyError:
        print("Invalid quote resource!")


request_quote()
