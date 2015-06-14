# File-Validator:
*Framework to test delimeted files against a configuration.*

The purpose of file-validator is to provide a configurable way of validating
delimited files such as those in CSV format. The expected file format is 
defined within an XML configuration file, and intends to validate the following
features:

* Correct header fields exist.
* Correct footer fields exist.
* Correct filename format.
* Correct maximum length of fields. 
* Field type checking.

## Example usage

The `validate_file.py` script can be used to validate a particular file in the following way:

```
validate_file.py --config config.xml --file data_gb_20110220_183732.psv
```

where `config.xml` is the XML configuration file defining the expected format of the data file and `data_gb_20110220_183732.psv` is the data file to be validated.

### config.xml
```
<?xml version="1.0"?>
<interfaces>
  <interface>
    <fileName>
      <name>(data)_([a-z]{2})_(\d{8}_\d{6})\.psv</name>
      <fileInterface>1</fileInterface>
      <subGroup>2</subGroup>
      <dateTimeGroup>3</dateTimeGroup>
    </fileName>
    <group>data</group>
    <fields>
      <field>
        <name>name</name>
        <length>100</length>
      </field>
      <field>
        <name>party</name>
        <length>100</length>
      </field>
      <field>
        <name>term_start_date</name>
        <length>8</length>
      </field>
      <field>
        <name>term_end_date</name>
        <length>8</length>
      </field>
    </fields>
  </interface>
</interfaces>
```

### data_gb_20110220_183732.psv
```
H|name|party|term_start_date|term_end_date
B|Gordon Brown|Labour|20070627|20100511
B|Tony Blair|Labour|19970502|20070627
B|John Major|Conservative|19901128|19970502
F|data|20110220_183732|5
```
