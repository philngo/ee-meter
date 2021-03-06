from eemeter.config.yaml_parser import load

import pytest

def test_sequential_meter():
    meter_yaml = """
        !obj:eemeter.meter.SequentialMeter {
            sequence: [
                !obj:eemeter.meter.DummyMeter {},
            ]
        }"""

    meter = load(meter_yaml)

    result = meter.evaluate(value=10)

    assert result["result"] == 10

def test_input_output_mappings():
    meter_yaml = """
        !obj:eemeter.meter.SequentialMeter {
            sequence: [
                !obj:eemeter.meter.DummyMeter {
                    input_mapping: {"value_one":"value"},
                    output_mapping: {"result":"result_one"}
                },
                !obj:eemeter.meter.DummyMeter {
                    input_mapping: {"value_two":"value"},
                    output_mapping: {"result":"result_two"}
                },
            ]
        }"""

    meter = load(meter_yaml)

    result = meter.evaluate(value_one=10,value_two=100)

    assert result["result_one"] == 10
    assert result["result_two"] == 100

def test_incorrect_input_mappings():
    meter_yaml = """ !obj:eemeter.meter.SequentialMeter {
            sequence: [
                !obj:eemeter.meter.DummyMeter {
                    input_mapping: {"value_one":"value"},
                    output_mapping: {"result":"value"}
                },
                !obj:eemeter.meter.DummyMeter {
                    input_mapping: {"value_two":"value"},
                    output_mapping: {"result":"value_one"}
                },
            ]
        }"""

    meter = load(meter_yaml)

    with pytest.raises(ValueError):
        result = meter.evaluate(value_one=10,value_two=100)

def test_incorrect_output_mappings():
    meter_yaml = """ !obj:eemeter.meter.SequentialMeter {
            sequence: [
                !obj:eemeter.meter.DummyMeter {
                    input_mapping: {"value_one":"value"},
                    output_mapping: {"result":"value_one"}
                },
                !obj:eemeter.meter.DummyMeter {
                    input_mapping: {"value_two":"value"},
                    output_mapping: {"result":"value_one"}
                },
            ]
        }"""

    meter = load(meter_yaml)

    with pytest.raises(ValueError):
        result = meter.evaluate(value_one=10,value_two=100)

def test_conditional_meter():
    meter_yaml="""
        !obj:eemeter.meter.ConditionalMeter {
            condition_parameter: "electricity_present",
            success: !obj:eemeter.meter.DummyMeter {
                input_mapping: {"success":"value"},
            },
            failure: !obj:eemeter.meter.DummyMeter {
                input_mapping: {"failure":"value"},
            },
        }
        """
    meter = load(meter_yaml)
    assert meter.evaluate(electricity_present=True,success="success",failure="failure")["result"] == "success"
    assert meter.evaluate(electricity_present=False,success="success",failure="failure")["result"] == "failure"

def test_conditional_meter_without_params():
    meter_yaml="""
        !obj:eemeter.meter.ConditionalMeter {
            condition_parameter: "electricity_present",
        }
        """
    meter = load(meter_yaml)
    assert isinstance(meter.evaluate(electricity_present=True),dict)
    assert isinstance(meter.evaluate(electricity_present=False),dict)

def test_debug_meter():

    meter_yaml="""
        !obj:eemeter.meter.DebugMeter {
        }
        """
    meter = load(meter_yaml)

