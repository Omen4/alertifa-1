#!/usr/bin/env python3
import os
import sys
import subprocess
import pickle
import platform
from pathlib import Path


target_os = platform.system()
package_name = Path(__file__).parts[-2]
package_path = Path(__file__).parent
build_prefix = sys.argv[1]

build = {
    "path": str(package_path.resolve()),
    "tag": f"{build_prefix}{package_name}:latest",
    "nocache": False,
    "forcerm": True,
}
if target_os == "Linux":
    build.update({"buildargs": {"--network": "host"}})

image_name = f"{build_prefix}{package_name}:latest"
host_logs = package_path.parent / "logs" / package_name
run = {
    "image": image_name,
    "detach": False,
    "volumes": {
        str(host_logs.resolve()): {
            'bind': "/logs", 'mode': 'rw'
        }
    }
}
if target_os == "Linux":
    run.update({"network_mode": "host"})
else:
    run.update({"ports": {"9000/tcp": 9000}})

bin_src = package_path.parent / ".bin.pckl"
with bin_src.open("wb") as file:
    pickle.dump({"build": build, "run": run}, file)
