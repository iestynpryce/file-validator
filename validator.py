#!/usr/bin/env python

import argparse
from copy import deepcopy
from os.path import basename
import re
import sys
import xml.etree.ElementTree as ET

# Store information about the fields
field_mapping = dict()
field_length  = dict()
field_type    = dict()


def validate_header(header, field_config):
    fields = header.split('|')
    prefix = fields[0]
    if prefix != 'H':
        print("Error: header prefix is '" + prefix + "', 'H' expected.")
        return False

    required_fields = {k.text: True for k in field_config.findall('.//name')}

    for index, field in enumerate(fields[1:], start=1):
        if field in required_fields:
            field_mapping[field] = index
            del(required_fields[field])
        else:
            print("Error: field '" + field + "' found in header, but not in the configuration")
            return False
     
    if len(required_fields) > 0:
        print("Error: header missing the following fields:")
        for k in required_fields.keys():
            print(k)
            return False

    return True


def validate_footer(footer, nlines, interface_id, field_config):
    fields =  footer.split('|')
    prefix = fields[0]
    if prefix != 'F':
        print("Error: footer prefix is '" + prefix + "', 'F' expected.")
        return False
    interface = fields[1]
    if interface != interface_id:
        print("Error: file group is '" + interface + "', '" + interface_id + "' expected.")
        return False
    read_obs = fields[2]
    if int(read_obs) != nlines:
        print("Error:", nlines, "lines read", read_obs, "expected.")
        return False

    return True


def validate_line(line, linenum, field_config):
    fields = line.split('|')
    prefix = fields[0]
    if prefix != 'B':
        print("Error: body prefix is '" + prefix + "', 'B' expected. File line:", format(linenum))
        return False

    for f, i in field_mapping.items():
        # Check if the field even exists
        try:
            field = fields[i]
        except IndexError:
            print("Error: line", linenum, "column", i+1, "- field not found. Field name:", f)
            return False

        # Check if it's within the length limits
        if len(field) > field_length[f]:
            print("Error: line", linenum, "column", i+1, "- field too long.", len(field), ">", field_length[f])
            return False

        # Check the type of the field
        check_type(field, f)

    return True


def check_type(field, field_name):
    return True


def validator_setup(fields):
    for field in fields.findall('field'):
        name = field.find('name').text
        length = int(field.find('length').text)
        ftype = field.find('type').text
        field_length[name] = length
        field_type[name] = ftype


def validate_file(config, filename):
    tree = ET.parse(config)
    root = tree.getroot()

    for interface in root.findall('interface'):
        fields = interface.find('fields')
        validator_setup(fields)
        
        group = interface.find('group').text
        name = interface.find('fileName').find('name').text
        m = re.match(name, basename(filename))
        if m == None:
            print("Error: filename '" + basename(filename) +"' does not match the expected pattern:", name)
            return False

        interface_name = m.group(int(interface.find('fileName').find('fileInterface').text))
        sub_group = m.group(int(interface.find('fileName').find('subGroup').text))
        date_time = m.group(int(interface.find('fileName').find('dateTimeGroup').text))

        with open(filename) as f:
            nlines = 0
            first_line = f.readline().rstrip()
            last_line = f.readline().rstrip()
            ok = validate_header(first_line, fields)
            if  not ok:
               sys.exit(-1)
            nlines += 1
            for line in f:
                nlines +=1
                ok = validate_line(last_line, nlines, fields)
                if not ok:
                   sys.exit(-1)
                last_line = line.rstrip()
            nlines += 1
            ok = validate_footer(last_line, nlines, group,fields)
            if not ok:
               sys.exit(-1)

        print("SUCCESS: validated", basename(filename), "from group:", group + ", subgroup:", sub_group + ", interface:", 
                        interface_name +". Timestamp:", date_time)
        return True

parser = argparse.ArgumentParser()
parser.add_argument('--config', help="configuration file for file validator")
parser.add_argument('--file', help="file to validate")
args = parser.parse_args()

validate_file(args.config, args.file)
