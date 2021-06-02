#!/usr/bin/env python3
import sys
import subprocess
import asyncio

import requests


SUCCESS = "\033[32;1;1mSUCCESS\033[0m"
FAILED = "\033[31;1;1mFAILED\033[0m"
# BASE_URL = "http://127.0.0.1:8000/api"
requests.packages.urllib3.disable_warnings()
BASE_URL = "https://alertifa_nginx/api"

session = requests.Session()
session.verify = False

url = f"{BASE_URL}/auth/login"
params = {
  "user": {
    "email": "yulquen@protonmail.com",
    "password": "123456789",
    "user_name": "yul"
  }
}
response = session.post(url=url, json=params, verify=False)
privileged_user = {"Authorization": "Bearer " + response.json()["token"]}


url = f"{BASE_URL}/auth"
params = {
  "user": {
    "email": "yul@protonmail.com",
    "password": "12345678",
    "user_name": "roger"
  }
}
response = session.post(url=url, json=params)
unprivileged_user = {"Authorization": "Bearer " + response.json()["token"]}

url = f"{BASE_URL}/auth"
params = {
  "user": {
    "email": "yulq@protonmail.com",
    "password": "12345678",
    "user_name": "serge"
  }
}
response = session.post(url=url, json=params)
normal_user = {"Authorization": "Bearer " + response.json()["token"]}

params = {
  "user": {
    "email": "yu@protonmail.com",
    "password": "12345678",
    "user_name": "maurice"
  }
}
response = session.post(url=url, json=params)
normal_user = {"Authorization": "Bearer " + response.json()["token"]}


import set_permissions



### AUTHORIZED USER: POST MESSAGE: VALID FORM ###
url = f"{BASE_URL}/messages/me/100000000000000000"
params = {"body": "ceci est un message"}
response = session.post(url=url, json=params, headers=normal_user)
message = "{}: Authorized user, post message (valid form)"
if response.status_code != 201:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNAUTHORIZED USER: POST MESSAGE: VALID FORM ###
url = f"{BASE_URL}/messages/me/100000000000000000"
params = {"body": "ceci est un message"}
response = session.post(url=url, json=params, headers=unprivileged_user)
message = "{}: Unauthorized user, post message (valid form)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### AUTHORIZED USER: POST MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/me/100000000000000000"
params = {"bug": "ceci est un message"}
response = session.post(url=url, json=params, headers=normal_user)
message = "{}: Authorized user, post message (invalid form)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNAUTHORIZED USER: POST MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/me/100000000000000000"
params = {"bug": "ceci est un message"}
response = session.post(url=url, json=params, headers=unprivileged_user)
message = "{}: Unauthorized user, post message (invalid form)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))


### AUTHORIZED USER: GET MESSAGE ###
url = f"{BASE_URL}/messages/1"
response = session.get(url=url, headers=normal_user)
message = "{}: Authorized user, get message (valid)"
if response.status_code != 200:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNAUTHORIZED USER: GET MESSAGE ###
url = f"{BASE_URL}/messages/1"
response = session.get(url=url, headers=unprivileged_user)
message = "{}: Unauthorized user, get message (valid)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### AUTHORIZED USER: GET MESSAGE: INVALID MSG_ID###
url = f"{BASE_URL}/messages/2"
response = session.get(url=url, headers=normal_user)
message = "{}: Authorized user, get message (invalid msg_id)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNAUTHORIZED USER: GET MESSAGE: INVALID MSG_ID###
url = f"{BASE_URL}/messages/2"
response = session.get(url=url, headers=unprivileged_user)
message = "{}: Unauthorized user, get message (invalid msg_id)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### AUTHORIZED USER: OWNER: EDIT MESSAGE: VALID FORM ###
url = f"{BASE_URL}/messages/me/1"
params = {"body": "ceci est un message édité"}
response = session.patch(url=url, headers=normal_user, json=params)
message = "{}: Authorized user, edit message (owner) (valid form)"
if response.status_code != 200:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNAUTHORIZED USER: OWNER: EDIT MESSAGE: VALID FORM ###
url = f"{BASE_URL}/messages/me/1"
params = {"body": "ceci est un message édité"}
response = session.patch(url=url, headers=unprivileged_user, json=params)
message = "{}: Unauthorized user, edit message (owner) (valid form)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### PRIVILEGED USER: OWNER: EDIT MESSAGE: VALID FORM ###
url = f"{BASE_URL}/messages/me/1"
params = {"body": "ceci est un message édité"}
response = session.patch(url=url, headers=privileged_user, json=params)
message = "{}: Privileged user, edit message (owner) (valid form)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### AUTHORIZED USER: OWNER: EDIT MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/me/1"
params = {"bug": "ceci est un message édité"}
response = session.patch(url=url, headers=normal_user, json=params)
message = "{}: Authorized user, edit message (owner) (invalid form)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNAUTHORIZED USER: OWNER: EDIT MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/me/1"
params = {"bug": "ceci est un message édité"}
response = session.patch(url=url, headers=unprivileged_user, json=params)
message = "{}: Unauthorized user, edit message (owner) (invalid form)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### PRIVILEGED USER: OWNER: EDIT MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/me/1"
params = {"bug": "ceci est un message édité"}
response = session.patch(url=url, headers=privileged_user, json=params)
message = "{}: Privileged user, edit message (owner) (invalid form)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### AUTHORIZED USER: OWNER: DELETE MESSAGE ###
url = f"{BASE_URL}/messages/me/100000000000000000"
session.post(url=url, json={"body": "ceci est un message"}, headers=normal_user)

url = f"{BASE_URL}/messages/me/2"
response = session.delete(url=url, headers=normal_user)
message = "{}: Authorized user, delete message (owner)"
if response.status_code != 200:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNAUTHORIZED USER: OWNER: DELETE MESSAGE ###
url = f"{BASE_URL}/messages/me/1"
response = session.delete(url=url, headers=unprivileged_user)
message = "{}: Unauthorized user, delete message (owner)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### PRIVILEGED USER: OWNER: DELETE MESSAGE ###
url = f"{BASE_URL}/messages/me/1"
response = session.delete(url=url, headers=privileged_user)
message = "{}: Unauthorized user, delete message (owner)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### PRIVILEGED USER: MOD: EDIT MESSAGE: VALID FORM VALID MSG_ID###
url = f"{BASE_URL}/messages/1"
params = {"body": "ceci est un message édité par un moderateur"}
response = session.patch(url=url, headers=privileged_user, json=params)
message = "{}: Privileged user, edit message (mod) (valid form) (valid msg_id)"
if response.status_code != 200:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNPRIVILEGED USER: MOD: EDIT MESSAGE: VALID FORM VALID MSG_ID###
url = f"{BASE_URL}/messages/1"
params = {"body": "ceci est un message édité par un moderateur"}
response = session.patch(url=url, headers=unprivileged_user, json=params)
message = "{}: Unprivileged user, edit message (mod) (valid form) (valid msg_id)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### PRIVILEGED USER: MOD: EDIT MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/1"
params = {"bug": "ceci est un message édité par un moderateur"}
response = session.patch(url=url, headers=privileged_user, json=params)
message = "{}: Privileged user, edit message (mod) (invalid form) (valid msg_id)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNPRIVILEGED USER: MOD: EDIT MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/1"
params = {"bug": "ceci est un message édité par un moderateur"}
response = session.patch(url=url, headers=unprivileged_user, json=params)
message = "{}: Unprivileged user, edit message (mod) (invalid form) (valid msg_id)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### PRIVILEGED USER: MOD: EDIT MESSAGE: INVALID MSG_ID ###
url = f"{BASE_URL}/messages/2"
params = {"body": "ceci est un message édité par un moderateur"}
response = session.patch(url=url, headers=privileged_user, json=params)
message = "{}: Privileged user, edit message (mod) (valid form) (invalid msg_id)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNPRIVILEGED USER: MOD: EDIT MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/2"
params = {"body": "ceci est un message édité par un moderateur"}
response = session.patch(url=url, headers=unprivileged_user, json=params)
message = "{}: Unprivileged user, edit message (mod) (valid form) (invalid msg_id)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### PRIVILEGED USER: MOD: EDIT MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/2"
params = {"bug": "ceci est un message édité par un moderateur"}
response = session.patch(url=url, headers=privileged_user, json=params)
message = "{}: Privileged user, edit message (mod) (invalid form) (invalid msg_id)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

### UNPRIVILEGED USER: MOD: EDIT MESSAGE: INVALID FORM ###
url = f"{BASE_URL}/messages/2"
params = {"bug": "ceci est un message édité par un moderateur"}
response = session.patch(url=url, headers=unprivileged_user, json=params)
message = "{}: Unprivileged user, edit message (mod) (invalid form) (invalid msg_id)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: DELETE MESSAGE: INVALID MSG_ID ###
url = f"{BASE_URL}/messages/2"
response = session.delete(url=url, headers=privileged_user)
message = "{}: Privileged user, delete message (mod) (invalid msg_id)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: DELETE MESSAGE: INVALID MSG_ID ###
url = f"{BASE_URL}/messages/2"
response = session.delete(url=url, headers=unprivileged_user)
message = "{}: Unprivileged user, delete message (mod) (invalid msg_id)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: DELETE MESSAGE: VALID MSG_ID ###
url = f"{BASE_URL}/messages/1"
response = session.delete(url=url, headers=unprivileged_user)
message = "{}: Unprivileged user, delete message (mod) (valid msg_id)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: DELETE MESSAGE: VALID MSG_ID ###
url = f"{BASE_URL}/messages/1"
response = session.delete(url=url, headers=privileged_user)
message = "{}: Privileged user, edit message (mod) (valid msg_id)"
if response.status_code != 200:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: MODIFY PERMISSIONS: VALID FORM, VALID CHANNEL, VALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 0,
    "user_id": 2
}
response = session.patch(url=url, headers=privileged_user, json=payload)
message = "{}: Privileged user, modify permission (mod) (valid form) (valid channel) (valid user) (valid role)"
if response.status_code != 200:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: MODIFY PERMISSIONS: VALID FORM, VALID CHANNEL, VALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 0,
    "user_id": 2
}
response = session.patch(url=url, headers=unprivileged_user, json=payload)
message = "{}: Unprivileged user, modify permission (mod) (valid form) (valid channel) (valid user) (valid role)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: MODIFY PERMISSIONS: INVALID FORM, VALID CHANNEL, VALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channelid": 100000000000000000,
    "role_id": 0,
    "user_id": 2
}
response = session.patch(url=url, headers=privileged_user, json=payload)
message = "{}: Privileged user, modify permission (mod) (invalid form) (valid channel) (valid user) (valid role)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: MODIFY PERMISSIONS: INVALID FORM, VALID CHANNEL, VALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channelid": 10000000000000000,
    "role_id": 0,
    "user_id": 2
}
response = session.patch(url=url, headers=unprivileged_user, json=payload)
message = "{}: Unprivileged user, modify permission (mod) (invalid form) (valid channel) (valid user) (valid role)"
if response.status_code != 422:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, INVALID CHANNEL, VALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 10000000000000000,
    "role_id": 0,
    "user_id": 2
}
response = session.patch(url=url, headers=privileged_user, json=payload)
message = "{}: Privileged user, modify permission (mod) (valid form) (invalid channel) (valid user) (valid role)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, INVALID CHANNEL, VALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 1000000000000000,
    "role_id": 0,
    "user_id": 2
}
response = session.patch(url=url, headers=unprivileged_user, json=payload)
message = "{}: Unprivileged user, modify permission (mod) (valid form) (invalid channel) (valid user) (valid role)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, VALID CHANNEL, INVALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 1000000000000000000,
    "role_id": 0,
    "user_id": 10
}
response = session.patch(url=url, headers=privileged_user, json=payload)
message = "{}: Privileged user, modify permission (mod) (valid form) (valid channel) (invalid user) (valid role)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, VALID CHANNEL, INVALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 1000000000000000000,
    "role_id": 0,
    "user_id": 10
}
response = session.patch(url=url, headers=unprivileged_user, json=payload)
message = "{}: Unprivileged user, modify permission (mod) (valid form) (valid channel) (invalid user) (valid role)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, VALID CHANNEL, VALID USER, INVALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 9,
    "user_id": 2
}
response = session.patch(url=url, headers=privileged_user, json=payload)
message = "{}: Privileged user, modify permission (mod) (valid form) (valid channel) (valid user) (invalid role)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, VALID CHANNEL, VALID USER, INVALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 9,
    "user_id": 2
}
response = session.patch(url=url, headers=unprivileged_user, json=payload)
message = "{}: Unprivileged user, modify permission (mod) (valid form) (valid channel) (valid user) (invalid role)"
if response.status_code != 404:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, VALID CHANNEL, VALID USER, UNAUTHORIZED ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 4,
    "user_id": 2
}
response = session.patch(url=url, headers=privileged_user, json=payload)
message = "{}: Privileged user, modify permission (mod) (valid form) (valid channel) (valid user) (unauthorized role)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, VALID CHANNEL, VALID USER, UNAUTHORIZED ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 4,
    "user_id": 2
}
response = session.patch(url=url, headers=unprivileged_user, json=payload)
message = "{}: Unprivileged user, modify permission (mod) (valid form) (valid channel) (valid user) (unauthorized role)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, VALID CHANNEL, UNAUTHORIZED USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 2,
    "user_id": 4
}
response = session.patch(url=url, headers=privileged_user, json=payload)
message = "{}: Privileged user, modify permission (mod) (valid form) (valid channel) (unauthorized user) (valid role)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, VALID CHANNEL, UNAUTHORIZED USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 2,
    "user_id": 4
}
response = session.patch(url=url, headers=unprivileged_user, json=payload)
message = "{}: Unprivileged user, modify permission (mod) (valid form) (valid channel) (unauthorized user) (valid role)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## PRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, UNAUTHORIZED CHANNEL, VALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 2,
    "user_id": 4
}
response = session.patch(url=url, headers=privileged_user, json=payload)
message = "{}: Privileged user, modify permission (mod) (valid form) (unauthorized channel) (valid user) (valid role)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))

## UNPRIVILEGED USER: MOD: CREATE PERMISSIONS: VALID FORM, UNAUTHORIZED CHANNEL, VALID USER, VALID ROLE
url = f"{BASE_URL}/permissions/modify"
payload = {
    "channel_id": 100000000000000000,
    "role_id": 2,
    "user_id": 4
}
response = session.patch(url=url, headers=unprivileged_user, json=payload)
message = "{}: Unprivileged user, modify permission (mod) (valid form) (unauthorized channel) (valid user) (valid role)"
if response.status_code != 403:
    print(message.format(FAILED))
else:
    print(message.format(SUCCESS))
