#!/usr/bin/python3
import os
import subprocess
import sys
from copy import deepcopy

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
    sys.exit(1)

VALID_PROTOS = {"tcp", "udp"}

services = {}
used_ports = {}  # host_port -> collector name, to catch clashes
args = {
    "environment_name": config.envName,
    "appId": config.appId, 
    "appSecret": config.appSecret, 
    "tenantId": config.tenantId, 
    "dce": config.dce, 
    "dcrId": config.dcrId,
    "table": None,
}


def runcmd(cmd):  # Wrapper to make running commands quicker
    result = subprocess.run(cmd)
    return result.returncode


for collector in config.collectors:
    args["table"] = None
    if os.path.isdir(f"./{collector['name']}"):  # Confirm collector exists
        # Validate required fields (issue 5).
        if "port" not in collector or "proto" not in collector:
            print(
                f"Collector '{collector['name']}' missing 'port' or 'proto', skipping"
            )
            continue
        if collector["proto"] not in VALID_PROTOS:
            print(
                f"Collector '{collector['name']}' has invalid proto "
                f"'{collector['proto']}' (expected tcp/udp), skipping"
            )
            continue

        # Detect duplicate host-port bindings early (issue 6).
        if collector["port"] in used_ports:
            print(
                f"Port {collector['port']} already used by "
                f"'{used_ports[collector['port']]}'; '{collector['name']}' would clash, skipping"
            )
            continue
        used_ports[collector["port"]] = collector["name"]

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

        # Handle duplicate collector names with an incrementing suffix (issue 4).
        key = collector["name"]
        suffix = 2
        while key in services:
            key = f"{collector['name']}_{suffix}"
            suffix += 1
        services[key] = service
    else:
        print(f"Collector not found: {collector['name']}, please check configuration")

yml = yaml.dump({"services": services})

with open("docker-compose.yml", "w") as f:
    f.write(yml)

if runcmd(["docker", "compose", "down", "--remove-orphans"]) == 0:
    print(f"Stopped existing containers")
else:
    print("Stop Failed")
    sys.exit(1)

if runcmd(["docker", "compose", "build"]) == 0:
    print(f"Build Successful - {len(services)} collectors built")
else:
    print("Build Failed")
    sys.exit(1)

if runcmd(["docker", "compose", "up", "-d"]) == 0:
    print(f"Execution Successful - {len(services)} collectors running")
else:
    print("Execution Failed")
    sys.exit(1)
