import logging
import time

import requests

from config import settings

# Configure logging
logging.basicConfig(
    level=settings.logging_level, format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_date_format(date_str: str) -> bool:
    """
    Validates that the date string is in the format YYYYMMDD.
    """
    try:
        time.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False


def validate_pharm_class_epc(pharm_class_epc: str) -> bool:
    """
    Validates that the pharm_class_epc is a non-empty string.
    """
    if not isinstance(pharm_class_epc, str) or not pharm_class_epc:
        return False
    return True


def make_request(url: str) -> dict:
    """
    Makes a request to the specified URL and returns the JSON response.
    """
    logging.info(f"Making request to: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise


def adverse_event_report(start_date: str, end_date: str, limit: int = 1) -> dict:
    """
    Retrieves a single adverse event report within a specified date range.
    """
    if not (validate_date_format(start_date) and validate_date_format(end_date)):
        raise ValueError("start_date and end_date must be in YYYYMMDD format")

    url = f"{settings.fda_api_url}?search=receivedate:[{start_date}+TO+{end_date}]&limit={limit}"
    return make_request(url)


def adverse_event_report_with_drug_class(
    start_date: str, end_date: str, pharm_class_epc: str, limit: int = 1
) -> dict:
    """
    Retrieves a single adverse event report for a drug from a specific pharmacologic class.
    """
    if not (validate_date_format(start_date) and validate_date_format(end_date)):
        raise ValueError("start_date and end_date must be in YYYYMMDD format")
    if not validate_pharm_class_epc(pharm_class_epc):
        raise ValueError("pharm_class_epc must be a non-empty string")

    url = f'{settings.fda_api_url}?search=patient.drug.openfda.pharm_class_epc:"{pharm_class_epc}"&limit={limit}'
    return make_request(url)


def count_patient_reactions(
    start_date: str, end_date: str, pharm_class_epc: str
) -> dict:
    """
    Returns a count of the most frequently reported patient reactions for a given drug class.
    """
    if not (validate_date_format(start_date) and validate_date_format(end_date)):
        raise ValueError("start_date and end_date must be in YYYYMMDD format")
    if not validate_pharm_class_epc(pharm_class_epc):
        raise ValueError("pharm_class_epc must be a non-empty string")

    url = f'{settings.fda_api_url}?search=patient.drug.openfda.pharm_class_epc:"{pharm_class_epc}"&count=patient.reaction.reactionmeddrapt.exact'
    return make_request(url)


def adverse_event_report_by_drug_name(drug_name: str, limit: int = 1):
    """
    Retrieves a single adverse event report for a specific drug name.
    """
    url = (
        f"{settings.fda_api_url}?"
        f"search=patient.drug.medicinalproduct:{drug_name}&limit={limit}"
    )
    return make_request(url)
