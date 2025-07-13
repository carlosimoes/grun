import pytest
from multi_tool_agent import openfda_tool
from unittest.mock import patch
import requests

def test_validate_date_format():
    assert openfda_tool.validate_date_format("20230101")
    assert not openfda_tool.validate_date_format("2023-01-01")
    assert not openfda_tool.validate_date_format("12345678")
    assert not openfda_tool.validate_date_format("1234567")

@patch('multi_tool_agent.openfda_tool.requests.get')
def test_adverse_event_report(mock_get):
    # Mock the requests.get method to return a sample response
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = lambda: {"results": [{"test": "data"}]}
    mock_get.return_value = mock_response

    report = openfda_tool.adverse_event_report(receivedate_start="20230101", receivedate_end="20230102")
    assert report == {"results": [{"test": "data"}]}

@patch('multi_tool_agent.openfda_tool.requests.get')
def test_adverse_event_report_with_drug_class(mock_get):
    # Mock the requests.get method to return a sample response
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = lambda: {"results": [{"test": "data"}]}
    mock_get.return_value = mock_response

    report = openfda_tool.adverse_event_report_with_drug_class(receivedate_start="20230101", receivedate_end="20230102", pharm_class_epc="test")
    assert report == {"results": [{"test": "data"}]}

@patch('multi_tool_agent.openfda_tool.requests.get')
def test_count_patient_reactions(mock_get):
    # Mock the requests.get method to return a sample response
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = lambda: {"results": [{"test": "data"}]}
    mock_get.return_value = mock_response

    report = openfda_tool.count_patient_reactions(receivedate_start="20230101", receivedate_end="20230102", pharm_class_epc="test")
    assert report == {"results": [{"test": "data"}]}

@patch('multi_tool_agent.openfda_tool.requests.get')
def test_adverse_event_report_by_drug_name(mock_get):
    # Mock the requests.get method to return a sample response
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = lambda: {"results": [{"test": "data"}]}
    mock_get.return_value = mock_response

    report = openfda_tool.adverse_event_report_by_drug_name(drug_name="test")
    assert report == {"results": [{"test": "data"}]}

@patch('multi_tool_agent.openfda_tool.requests.get')
def test_get_adverse_events(mock_get):
    # Mock the requests.get method to return a sample response
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = lambda: {"results": [{"test": "data"}]}
    mock_get.return_value = mock_response

    report = openfda_tool.get_adverse_events(drug_name="test")
    assert report == {"results": [{"test": "data"}]}

def test_adverse_event_report_invalid_date_format():
    with pytest.raises(ValueError) as excinfo:
        openfda_tool.adverse_event_report(receivedate_start="2023-01-01", receivedate_end="2023-01-02")
    assert "receivedate_start and receivedate_end must be in YYYYMMDD format" in str(excinfo.value)

def test_adverse_event_report_with_drug_class_invalid_pharm_class_epc():
    with pytest.raises(ValueError) as excinfo:
        openfda_tool.adverse_event_report_with_drug_class(receivedate_start="20230101", receivedate_end="20230102", pharm_class_epc="")
    assert "pharm_class_epc must be a non-empty string" in str(excinfo.value)

def test_count_patient_reactions_invalid_pharm_class_epc():
    with pytest.raises(ValueError) as excinfo:
        openfda_tool.count_patient_reactions(receivedate_start="20230101", receivedate_end="20230102", pharm_class_epc="")
    assert "pharm_class_epc must be a non-empty string" in str(excinfo.value)