#!/usr/bin/env python3
import requests
# from pathlib import Path


SUCCESS = "\033[32;1;1mSUCCESS\033[0m"
FAILED = "\033[31;1;1mFAILED\033[0m"


# BASE_URL = "https://ascript-valency.com/api"
# BASE_URL = "https://kubernetes.docker.internal/api"
requests.packages.urllib3.disable_warnings()

BASE_URL = f"https://alertifa_proxy/api"
# fake_cert = Path(__file__).parent.parent / "nginx" / "letsencrypt" / "nginx-selfsigned.crt"
# print(fake_cert)

token: str = ""
headers = {"Authorization": "Bearer " + token}

session: requests.Session = requests.Session()
session.verify = False
response = requests.get(BASE_URL, verify=False)
assert response.status_code != 502# and response.status_code != 404

url = f"{BASE_URL}/auth"

### INVALID REGISTER: INVALID PASSWORD ###
url = f"{BASE_URL}/auth"
params = {
  "user": {
    "email": "yulquen@protonmail.com",
    "password": "",
    "user_name": "yul"
  }
}
response = session.post(url=url, json=params)
message = "{}: Invalid register (invalid password)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### INVALID REGISTER: INVALID EMAIL ###
url = f"{BASE_URL}/auth"
params = {
  "user": {
    "email": "",
    "password": "123456789",
    "user_name": "yul"
  }
}
response = session.post(url=url, json=params)
message = "{}: Invalid register (invalid email)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### INVALID REGISTER: INVALID USERNAME ###
url = f"{BASE_URL}/auth"
params = {
  "user": {
    "email": "a@a.a",
    "password": "123456789",
    "user_name": "yu"
  }
}
response = session.post(url=url, json=params)
message = "{}: Invalid register (invalid username)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))


### VALID REGISTER ###
url = f"{BASE_URL}/auth"
params = {
  "user": {
    "email": "yulquen@protonmail.com",
    "password": "123456789",
    "user_name": "yul"
  }
}
response = session.post(url=url, json=params)
message = "{}: Valid register"
if response.status_code != 201:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))
token_old: str = response.json()["token"]

###  INVALID REGISTER: TAKEN USERNAME ###
url = f"{BASE_URL}/auth"
params = {
  "user": {
    "email": "a@a.com",
    "password": "123456789",
    "user_name": "yul"
  }
}
response = session.post(url=url, json=params)
message = "{}: Invalid register (taken username)"
if response.status_code != 400:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

###  INVALID REGISTER: TAKEN EMAIL ###
url = f"{BASE_URL}/auth"
params = {
  "user": {
    "email": "yulquen@protonmail.com",
    "password": "123456789",
    "user_name": "yulq"
  }
}
response = session.post(url=url, json=params)
message = "{}: Invalid register (taken email)"
if response.status_code != 400:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))


###  INVALID LOGIN: INVALID PASSWORD ###
url = f"{BASE_URL}/auth/login"
params = {
    "user": {
        "email": "yulquen@protonmail.com",
        "password": "",
        "user_name": "yul"
    }
}
response = session.post(url=url, json=params)
message = "{}: Invalid login (invalid password)"
if response.status_code != 400:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

###  INVALID LOGIN: INVALID FORM ###
url = f"{BASE_URL}/auth/login"
params = {
    "email": "yulquen@protonmail.com",
    "password": "12345678",
    "user_name": "yul"
}
response = session.post(url=url, json=params)
message = "{}: Invalid login (invalid form)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

###  INVALID LOGIN: INVALID PASSWORD ###
url = f"{BASE_URL}/auth/login"
params = {
    "user": {
        "email": "yulquen@protonmail.com",
        "password": "12345678910",
        "user_name": "yul"
    }
}
response = session.post(url=url, json=params)
message = "{}: Invalid login (wrong password)"
if response.status_code != 400:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

###  VALID LOGIN ###
url = "https://127.0.0.1/auth/login"
# url = f"{BASE_URL}/auth/login"
params = {
    "user": {
        "email": "yulquen@protonmail.com",
        "password": "123456789",
        "user_name": "yul"
    }
}
response = session.post(url=url, json=params)
message = "{}: Valid login"
if response.status_code != 200:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))
token: str = response.json()["token"]



### TOKEN VALID ###
url = f"{BASE_URL}/channels/100000000000000000"
headers = {"Authorization": "Bearer " + token}
response = session.get(url=url, json=params, headers=headers)
message = "{}: Valid token"
if response.status_code != 200:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### TOKEN INVALID: INVALIDATED ###
url = f"{BASE_URL}/channels/100000000000000000"
headers = {"Authorization": "Bearer " + token_old}
response = session.get(url=url, json=params, headers=headers)
message = "{}: Invalid token (invalidated)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### TOKEN INVALID: MANGLED ###
url = f"{BASE_URL}/channels/100000000000000000"
headers = {"Authorization": "Bearer " + token[1:]}
response = session.get(url=url, json=params, headers=headers)
message = "{}: Invalid token (mangled)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### TOKEN INVALID: INVALID SIGNATURE ###
url = f"{BASE_URL}/channels/100000000000000000"
headers = {"Authorization": "Bearer " + token[:-1]}
response = session.get(url=url, json=params, headers=headers)
message = "{}: Invalid token (invalid signature)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### TOKEN INVALID: AUTH HEADER ###
url = f"{BASE_URL}/channels/100000000000000000"
headers = {"Authorizatio": "Bearer " + token}
response = session.get(url=url, json=params, headers=headers)
message = "{}: Invalid token (invalid auth header)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### TOKEN INVALID: AUTH SCHEME ###
url = f"{BASE_URL}/channels/100000000000000000"
headers = {"Authorization": "bearer " + token}
response = session.get(url=url, json=params, headers=headers)
message = "{}: Invalid token (invalid auth scheme)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))
