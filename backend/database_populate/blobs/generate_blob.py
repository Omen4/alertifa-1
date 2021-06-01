#!/usr/bin/env python3
import pickle
from typing import Any

def prepare_pickle(file: str) -> list[Any]:
    with open(file, "r") as f:
        raw_data = f.read().split("\n")[:-1]

    result = []
    for d in raw_data:
        buffer = []
        for i in d.split(','):
            try:
                buffer.append(int(i))
            except:
                buffer.append(i)
        result.append(buffer)

    return result


with open("test_data_old.pckl", "rb") as f:
    (channels, users, messages, conversations) = pickle.load(f)
    channels = prepare_pickle("channels.csv")
    roles = prepare_pickle("roles.csv")
    permissions = prepare_pickle("permissions.csv")

with open("test_data.pckl", "wb") as f:
    pickle.dump((
        channels, 
        users, 
        messages,
        conversations, 
        roles, 
        permissions
        ), f)
