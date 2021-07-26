#!/usr/bin/env python3

from base64 import b64decode
from binascii import Error
from sys import stderr, stdin

import yaml


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str',
                                       data,
                                       style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def decode_kv(pair):
    for key, value in pair.items():
        if isinstance(value, str):
            try:
                secret_decoded = b64decode(value, validate=True).decode()
            except (Error, UnicodeDecodeError):
                pass
            else:
                pair[key] = secret_decoded
        else:
            decode_kv(value)


def main():
    yaml.add_representer(str, str_presenter)

    yaml_file = yaml.safe_load(stdin)

    if yaml_file["kind"] == "Secret":
        print("# Kubernetes secret found: decode data key contents only",
              file=stderr)
        decode_kv(yaml_file["data"])
        yaml_file["stringData"] = yaml_file["data"]
        del yaml_file["data"]
    else:
        print("# Common yaml found: try to decode every string value",
              file=stderr)
        decode_kv(yaml_file)

    print(yaml.dump(yaml_file, default_flow_style=False))


if __name__ == "__main__":
    main()
