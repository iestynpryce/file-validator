#!/usr/bin/env python3

import argparse
import validator.validator as vv

parser = argparse.ArgumentParser()
parser.add_argument('--config', help="configuration file for file validator", required=True)
parser.add_argument('--file', help="file to validate", required=True)
args = parser.parse_args()

v = vv.Validate("validator.pickle",diefast=False)
v.validate_file(args.config, args.file)
