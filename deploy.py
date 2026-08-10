#!/usr/bin/python3
import os
import subprocess
import sys
from copy import deepcopy
from genericpath import isdir

import config


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import yaml
except ImportError as e:
    print("pyyaml not found - installing")
    install("pyyaml")
    import yaml

if os.geteuid() != 0:
    print("Script must be run as root, try using sudo...")
    sys.exit()

services = {}
args = {
    "environment_name": config.envName,
    "workspaceID": config.workspaceID,
    "workspaceKey": config.workspaceKey,
    "table": None,
}


def runcmd(cmd):  # Wrapper to make running commands quicker
    runcmd = subprocess.run(cmd.split(" "))
    return runcmd.returncode


for collector in config.collectors:
    args["table"] = None
    if os.path.isdir(f"./{collector['name']}"):  # Confirm collector exists
        if "table" in collector:  # If custom table is defined for collector
            args["table"] = collector["table"]
        else:
            args["table"] = collector["name"]
            if collector["proto"] == "tcp":
                ports = [f"{collector['port']}:514"]
            else:  # If syslog is UDP
                ports = [f"{collector['port']}:514/udp"]
            service = {
                "build": {"context": f"./{collector['name']}", "args": deepcopy(args)},
                "image": f"{collector['name']}_sentinel",
                "restart": "always",
                "ports": ports,
            }
            if collector["name"] in services:
                services[f"{collector['name']}_2"] = service
            else:
                services[collector["name"]] = service
    else:
        print(f"Collector not found: {collector['name']}, please check configuration")

yml = yaml.dump({"services": services})

with open("docker-compose.yml", "w") as f:
    f.write(yml)

if runcmd("docker compose down --remove-orphans") == 0:
    print(f"Stopped existing containers")
else:
    print("Stop Failed")

if runcmd("docker compose build") == 0:
    print(f"Build Successful - {len(services)} collectors built")
else:
    print("Build Failed")

if runcmd("docker compose up -d") == 0:
    print(f"Execution Successful - {len(services)} collectors running")
else:
    print("Execution Failed")
