"""
CathPCI Data Dictionary and Mapping Configuration

This file defines the CathPCI data elements and provides a template
for extending the FHIR to CathPCI mapping.

The CathPCI Registry has 1000+ data elements. This implementation provides
a foundational set of commonly used elements. You can extend this dictionary
to add more elements as needed.

Reference: https://www.ncdr.com/registries/cathpci-registry/data-collection
"""

from typing import Dict, List

# CathPCI Data Element Categories and Examples
# You can extend these dictionaries to add more data elements

CATHPCI_DEMOGRAPHICS = {
    # Currently Mapped
    'patient_id': 'Unique patient identifier',
    'medical_record_number': 'Hospital MRN',
    'date_of_birth': 'Patient date of birth (YYYY-MM-DD)',
    'gender': 'Patient gender (M/F/O/U)',
    'race': 'Patient race',
    'ethnicity': 'Patient ethnicity',
    'name': 'Patient full name',
    'address': 'Patient address (street, city, state, zip, country)',
    
    # Available to Add
    'insurance_type': 'Primary insurance type',
    'zip_code': 'Patient ZIP code',
    'telephone': 'Patient telephone number',
    'marital_status': 'Marital status',
    'living_situation': 'Current living situation',
}

CATHPCI_RISK_FACTORS = {
    # Currently Mapped
    'diabetes': 'Diabetes mellitus (boolean)',
    'hypertension': 'Hypertension (boolean)',
    'smoking_status': 'Smoking status (current/former/never)',
    'family_history_cad': 'Family history of CAD (boolean)',
    
    # Available to Add
    'prior_mi': 'Prior myocardial infarction (boolean)',
    'prior_pci': 'Prior PCI (boolean)',
    'prior_cabg': 'Prior CABG (boolean)',
    'peripheral_arterial_disease': 'PAD diagnosis (boolean)',
    'cerebrovascular_disease': 'CVD diagnosis (boolean)',
    'chronic_lung_disease': 'Chronic lung disease (boolean)',
    'dyslipidemia': 'Dyslipidemia (boolean)',
    'renal_failure_dialysis': 'Renal failure on dialysis (boolean)',
}

CATHPCI_LAB_VALUES = {
    # Currently Mapped
    'hemoglobin': 'Hemoglobin (g/dL)',
    'creatinine': 'Creatinine (mg/dL)',
    'total_cholesterol': 'Total cholesterol (mg/dL)',
    'ldl': 'LDL cholesterol (mg/dL)',
    'hdl': 'HDL cholesterol (mg/dL)',
    
    # Available to Add
    'triglycerides': 'Triglycerides (mg/dL)',
    'glucose': 'Glucose (mg/dL)',
    'hba1c': 'Hemoglobin A1c (%)',
    'platelet_count': 'Platelet count (x1000/μL)',
    'inr': 'International normalized ratio',
    'bnp': 'B-type natriuretic peptide (pg/mL)',
    'troponin': 'Troponin I or T',
    'egfr': 'Estimated GFR (mL/min/1.73m²)',
}

CATHPCI_VITAL_SIGNS = {
    # Currently Mapped
    'height': 'Height (cm)',
    'weight': 'Weight (kg)',
    'bmi': 'Body mass index',
    'systolic_bp': 'Systolic blood pressure (mmHg)',
    'diastolic_bp': 'Diastolic blood pressure (mmHg)',
    
    # Available to Add
    'heart_rate': 'Heart rate (bpm)',
    'respiratory_rate': 'Respiratory rate (breaths/min)',
    'oxygen_saturation': 'O2 saturation (%)',
    'temperature': 'Temperature (°C or °F)',
}

CATHPCI_PROCEDURE_DETAILS = {
    # Currently Mapped
    'procedure_id': 'Unique procedure identifier',
    'procedure_date': 'Procedure date and time',
    'procedure_type': 'Type of procedure',
    'procedure_status': 'Procedure status (completed/cancelled)',
    'indication': 'Indication for procedure',
    'access_site': 'Vascular access site',
    'lesion_location': 'Lesion location (coronary artery)',
    
    # Available to Add
    'operator_id': 'Primary operator identifier',
    'facility_id': 'Performing facility identifier',
    'urgency': 'Procedure urgency (elective/urgent/emergent/salvage)',
    'cardiac_arrest_within_24h': 'Cardiac arrest within 24h (boolean)',
    'cardiogenic_shock': 'Cardiogenic shock at start (boolean)',
    'contrast_volume': 'Total contrast volume (mL)',
    'fluoroscopy_time': 'Total fluoroscopy time (minutes)',
    'procedure_time': 'Total procedure time (minutes)',
    'number_vessels_diseased': 'Number of diseased vessels (0-3)',
    'left_main_disease': 'Left main disease >50% (boolean)',
    'stent_type': 'Type of stent used (BMS/DES)',
    'number_stents': 'Number of stents placed',
    'ivus_used': 'IVUS used (boolean)',
    'ffr_used': 'FFR used (boolean)',
}

CATHPCI_MEDICATIONS = {
    # Available to Add
    'aspirin_pre_procedure': 'Aspirin within 24h pre-procedure (boolean)',
    'p2y12_inhibitor_pre_procedure': 'P2Y12 inhibitor pre-procedure (boolean)',
    'beta_blocker': 'Beta blocker at discharge (boolean)',
    'ace_inhibitor': 'ACE inhibitor at discharge (boolean)',
    'arb': 'ARB at discharge (boolean)',
    'statin': 'Statin at discharge (boolean)',
}

CATHPCI_OUTCOMES = {
    # Available to Add
    'in_hospital_mortality': 'In-hospital mortality (boolean)',
    'stroke': 'Stroke during hospitalization (boolean)',
    'bleeding_complication': 'Bleeding complication (boolean)',
    'vascular_complication': 'Vascular complication (boolean)',
    'acute_kidney_injury': 'Acute kidney injury (boolean)',
    'length_of_stay': 'Hospital length of stay (days)',
}

# Complete CathPCI Data Dictionary
# Combine all categories for reference
CATHPCI_DATA_DICTIONARY = {
    'demographics': CATHPCI_DEMOGRAPHICS,
    'risk_factors': CATHPCI_RISK_FACTORS,
    'lab_values': CATHPCI_LAB_VALUES,
    'vital_signs': CATHPCI_VITAL_SIGNS,
    'procedure_details': CATHPCI_PROCEDURE_DETAILS,
    'medications': CATHPCI_MEDICATIONS,
    'outcomes': CATHPCI_OUTCOMES,
}

# LOINC codes for common lab values (helpful for FHIR mapping)
LOINC_CODES = {
    'hemoglobin': '718-7',
    'creatinine': '2160-0',
    'total_cholesterol': '2093-3',
    'ldl': '13457-7',
    'hdl': '2085-9',
    'triglycerides': '2571-8',
    'glucose': '2345-7',
    'hba1c': '4548-4',
    'platelet_count': '777-3',
    'troponin_i': '10839-9',
    'troponin_t': '6598-7',
    'bnp': '30934-4',
    'height': '8302-2',
    'weight': '29463-7',
    'bmi': '39156-5',
    'systolic_bp': '8480-6',
    'diastolic_bp': '8462-4',
    'heart_rate': '8867-4',
    'respiratory_rate': '9279-1',
    'oxygen_saturation': '2708-6',
}

# SNOMED codes for common conditions (helpful for FHIR mapping)
SNOMED_CODES = {
    'diabetes_type_2': '44054006',
    'diabetes_type_1': '46635009',
    'hypertension': '38341003',
    'myocardial_infarction': '22298006',
    'coronary_artery_disease': '53741008',
    'heart_failure': '84114007',
    'atrial_fibrillation': '49436004',
    'peripheral_arterial_disease': '399957001',
    'cerebrovascular_disease': '62914000',
    'chronic_kidney_disease': '709044004',
    'copd': '13645005',
}


def get_data_element_info(category: str, element: str) -> str:
    """
    Get information about a specific CathPCI data element
    
    Args:
        category: Category name (e.g., 'demographics', 'risk_factors')
        element: Element name (e.g., 'patient_id', 'diabetes')
        
    Returns:
        Description of the data element
    """
    if category in CATHPCI_DATA_DICTIONARY:
        return CATHPCI_DATA_DICTIONARY[category].get(element, 'Unknown element')
    return 'Unknown category'


def list_all_data_elements() -> Dict[str, List[str]]:
    """
    List all CathPCI data elements by category
    
    Returns:
        Dictionary of categories with their data elements
    """
    result = {}
    for category, elements in CATHPCI_DATA_DICTIONARY.items():
        result[category] = list(elements.keys())
    return result


def get_mapped_elements() -> List[str]:
    """
    Get list of currently mapped data elements
    
    Returns:
        List of element names that are currently mapped
    """
    mapped = []
    
    # Demographics
    mapped.extend(['patient_id', 'medical_record_number', 'date_of_birth', 
                   'gender', 'race', 'ethnicity', 'name', 'address'])
    
    # Risk factors
    mapped.extend(['diabetes', 'hypertension', 'smoking_status', 'family_history_cad'])
    
    # Lab values
    mapped.extend(['hemoglobin', 'creatinine', 'total_cholesterol', 'ldl', 'hdl'])
    
    # Vital signs
    mapped.extend(['height', 'weight', 'bmi', 'systolic_bp', 'diastolic_bp'])
    
    # Procedure details
    mapped.extend(['procedure_id', 'procedure_date', 'procedure_type', 
                   'procedure_status', 'indication', 'access_site', 'lesion_location'])
    
    return mapped


def get_unmapped_elements() -> Dict[str, List[str]]:
    """
    Get list of data elements that are not yet mapped
    
    Returns:
        Dictionary of categories with unmapped elements
    """
    mapped = set(get_mapped_elements())
    unmapped = {}
    
    for category, elements in CATHPCI_DATA_DICTIONARY.items():
        unmapped_in_category = [elem for elem in elements.keys() if elem not in mapped]
        if unmapped_in_category:
            unmapped[category] = unmapped_in_category
    
    return unmapped
