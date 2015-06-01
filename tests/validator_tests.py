from nose.tools import *
import tempfile
import xml.etree.ElementTree as ET

from validator import validator

v = 0

def setup():
    global v
    v = validator.Validate(tempfile.TemporaryFile())

def teardown():
    v = 0

# Validate footer tests
def test_validate_footer_ok():
    assert v.validate_footer("F|test|20150601_203200|4", 4, "test", "20150601_203200") == True

def test_validate_footer_prefix():
    assert v.validate_footer("B|test|20150601_203200|4", 4, "test", "20150601_203200") == False

def test_validate_footer_interface():
    assert v.validate_footer("F|badtest|20150601_203200|4", 4, "test", "20150601_203200") == False

def test_validate_footer_nlines():
    assert v.validate_footer("F|test|20150601_203200|0", 4, "test", "20150601_203200") == False

def test_validate_footer_datetime():
    assert v.validate_footer("F|test|20150601_203200|4", 4, "test", "20150201_033200") == False

def test_validate_footer_empty():
    assert v.validate_footer("", 4, "test", "20150601_203200") == False

# Validate header
def test_validate_header_ok():
    fields = ET.fromstring("<fields><field><name>test_field</name><length>10</length><type>string</type></field></fields>")
    assert v.validate_header("H|test_field", fields) == True

def test_validate_header_prefix():
    assert v.validate_header("B|test_field", None) == False

def test_validate_header_extra_field():
    fields = ET.fromstring("<fields><field><name>test_field</name><length>10</length><type>string</type></field></fields>")
    assert v.validate_header("H|test_field|extra_field", fields) == False

def test_validate_header_fields():
    fields = ET.fromstring("<fields><field><name>test_field</name><length>10</length><type>string</type></field></fields>")
    assert v.validate_header("H|", fields) == False

# Validate line
def test_validate_line_ok():
    fields = ET.fromstring("<fields><field><name>test_field</name><length>10</length><type>string</type></field></fields>")
    v.validator_setup(fields)
    assert v.validate_line("B|0123456789", 1, fields) == True

def test_validate_line_prefix():
    assert v.validate_line("H|0123456789", 1, None) == False

def test_validate_field_exists():
    fields = ET.fromstring("<fields><field><name>test_field</name><length>10</length><type>string</type></field></fields>")
    v.validator_setup(fields)
    assert v.validate_line("B", 1, fields) == False

def test_validate_field_exists():
    fields = ET.fromstring("<fields><field><name>test_field</name><length>10</length><type>string</type></field></fields>")
    v.validator_setup(fields)
    assert v.validate_line("B|12345678910", 1, fields) == False

# Validate file
def test_validate_file_ok():
    assert v.validate_file("tests/test_config/config.xml", "tests/test_data/full_customer_gb_20150528_224302.dat") == True

def test_validate_file_nodata():
    assert v.validate_file("tests/test_config/config.xml", "tests/test_data/full_nonexistant_gb_20150528_225900.dat") == False
