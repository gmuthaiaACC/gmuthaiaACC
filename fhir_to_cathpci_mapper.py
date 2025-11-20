"""
FHIR to CathPCI Data Mapper
Converts FHIR resources to CathPCI registry format
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class FHIRToCathPCIMapper:
    """Maps FHIR resources to CathPCI data elements"""
    
    def __init__(self):
        """Initialize the mapper with CathPCI data element mappings"""
        pass
    
    def map_patient_demographics(self, patient: Dict) -> Dict[str, Any]:
        """
        Map FHIR Patient resource to CathPCI demographics
        
        Args:
            patient: FHIR Patient resource
            
        Returns:
            Dictionary with CathPCI demographic fields
        """
        demographics = {
            'patient_id': patient.get('id', ''),
            'medical_record_number': self._extract_mrn(patient),
            'date_of_birth': self._extract_birthdate(patient),
            'gender': self._map_gender(patient.get('gender', '')),
            'race': self._extract_race(patient),
            'ethnicity': self._extract_ethnicity(patient),
            'name': self._extract_name(patient),
            'address': self._extract_address(patient)
        }
        return demographics
    
    def map_procedure_to_cathpci(self, procedure: Dict, observations: List[Dict], 
                                  conditions: List[Dict]) -> Dict[str, Any]:
        """
        Map FHIR Procedure with related resources to CathPCI procedure record
        
        Args:
            procedure: FHIR Procedure resource
            observations: List of related FHIR Observation resources
            conditions: List of FHIR Condition resources
            
        Returns:
            Dictionary with CathPCI procedure fields
        """
        cathpci_record = {
            # Procedure Identification
            'procedure_id': procedure.get('id', ''),
            'procedure_date': self._extract_procedure_date(procedure),
            'procedure_type': self._map_procedure_type(procedure),
            'procedure_status': procedure.get('status', ''),
            
            # Patient Risk Factors (from conditions and observations)
            'diabetes': self._has_condition(conditions, 'diabetes'),
            'hypertension': self._has_condition(conditions, 'hypertension'),
            'smoking_status': self._extract_smoking_status(observations),
            'family_history_cad': self._has_condition(conditions, 'family history'),
            
            # Lab Values (from observations)
            'hemoglobin': self._extract_lab_value(observations, 'hemoglobin'),
            'creatinine': self._extract_lab_value(observations, 'creatinine'),
            'total_cholesterol': self._extract_lab_value(observations, 'cholesterol'),
            'ldl': self._extract_lab_value(observations, 'ldl'),
            'hdl': self._extract_lab_value(observations, 'hdl'),
            
            # Vital Signs
            'height': self._extract_vital_sign(observations, 'height'),
            'weight': self._extract_vital_sign(observations, 'weight'),
            'bmi': self._calculate_bmi(observations),
            'systolic_bp': self._extract_vital_sign(observations, 'systolic'),
            'diastolic_bp': self._extract_vital_sign(observations, 'diastolic'),
            
            # Procedure Details
            'indication': self._extract_indication(procedure),
            'access_site': self._extract_access_site(procedure),
            'lesion_location': self._extract_lesion_location(procedure),
        }
        return cathpci_record
    
    def _extract_mrn(self, patient: Dict) -> str:
        """Extract Medical Record Number from patient identifiers"""
        identifiers = patient.get('identifier', [])
        for identifier in identifiers:
            if identifier.get('type', {}).get('text', '').lower() == 'mrn':
                return identifier.get('value', '')
        return identifiers[0].get('value', '') if identifiers else ''
    
    def _extract_birthdate(self, patient: Dict) -> str:
        """Extract birth date from patient"""
        return patient.get('birthDate', '')
    
    def _map_gender(self, fhir_gender: str) -> str:
        """Map FHIR gender to CathPCI gender codes"""
        gender_map = {
            'male': 'M',
            'female': 'F',
            'other': 'O',
            'unknown': 'U'
        }
        return gender_map.get(fhir_gender.lower(), 'U')
    
    def _extract_race(self, patient: Dict) -> str:
        """Extract race from patient extension"""
        extensions = patient.get('extension', [])
        for ext in extensions:
            if 'us-core-race' in ext.get('url', ''):
                if ext.get('extension'):
                    for sub_ext in ext['extension']:
                        if sub_ext.get('valueCoding'):
                            return sub_ext['valueCoding'].get('display', '')
        return 'Unknown'
    
    def _extract_ethnicity(self, patient: Dict) -> str:
        """Extract ethnicity from patient extension"""
        extensions = patient.get('extension', [])
        for ext in extensions:
            if 'us-core-ethnicity' in ext.get('url', ''):
                if ext.get('extension'):
                    for sub_ext in ext['extension']:
                        if sub_ext.get('valueCoding'):
                            return sub_ext['valueCoding'].get('display', '')
        return 'Unknown'
    
    def _extract_name(self, patient: Dict) -> str:
        """Extract formatted name from patient"""
        names = patient.get('name', [])
        if names:
            name = names[0]
            family = name.get('family', '')
            given = ' '.join(name.get('given', []))
            return f"{given} {family}".strip()
        return ''
    
    def _extract_address(self, patient: Dict) -> Dict[str, str]:
        """Extract address from patient"""
        addresses = patient.get('address', [])
        if addresses:
            addr = addresses[0]
            return {
                'street': ', '.join(addr.get('line', [])),
                'city': addr.get('city', ''),
                'state': addr.get('state', ''),
                'postal_code': addr.get('postalCode', ''),
                'country': addr.get('country', '')
            }
        return {}
    
    def _extract_procedure_date(self, procedure: Dict) -> str:
        """Extract procedure date/time"""
        return procedure.get('performedDateTime', '') or \
               procedure.get('performedPeriod', {}).get('start', '')
    
    def _map_procedure_type(self, procedure: Dict) -> str:
        """Map FHIR procedure code to CathPCI procedure type"""
        code = procedure.get('code', {})
        coding = code.get('coding', [])
        if coding:
            return coding[0].get('display', '')
        return code.get('text', '')
    
    def _has_condition(self, conditions: List[Dict], condition_name: str) -> bool:
        """Check if patient has a specific condition"""
        for condition in conditions:
            code = condition.get('code', {})
            text = code.get('text', '').lower()
            for coding in code.get('coding', []):
                display = coding.get('display', '').lower()
                if condition_name.lower() in text or condition_name.lower() in display:
                    return True
        return False
    
    def _extract_smoking_status(self, observations: List[Dict]) -> str:
        """Extract smoking status from observations"""
        for obs in observations:
            code = obs.get('code', {})
            for coding in code.get('coding', []):
                if 'smoking' in coding.get('display', '').lower():
                    value = obs.get('valueCodeableConcept', {})
                    return value.get('text', '') or \
                           value.get('coding', [{}])[0].get('display', '')
        return 'Unknown'
    
    def _extract_lab_value(self, observations: List[Dict], lab_name: str) -> Optional[float]:
        """Extract lab value from observations"""
        for obs in observations:
            code = obs.get('code', {})
            text = code.get('text', '').lower()
            for coding in code.get('coding', []):
                display = coding.get('display', '').lower()
                if lab_name.lower() in text or lab_name.lower() in display:
                    value = obs.get('valueQuantity', {})
                    return value.get('value')
        return None
    
    def _extract_vital_sign(self, observations: List[Dict], vital_name: str) -> Optional[float]:
        """Extract vital sign value from observations"""
        return self._extract_lab_value(observations, vital_name)
    
    def _calculate_bmi(self, observations: List[Dict]) -> Optional[float]:
        """Calculate BMI from height and weight observations"""
        height = self._extract_vital_sign(observations, 'height')
        weight = self._extract_vital_sign(observations, 'weight')
        
        if height and weight:
            # Assuming height in cm and weight in kg
            height_m = height / 100 if height > 3 else height  # Convert cm to m if needed
            bmi = weight / (height_m ** 2)
            return round(bmi, 2)
        return None
    
    def _extract_indication(self, procedure: Dict) -> str:
        """Extract procedure indication"""
        reason_code = procedure.get('reasonCode', [])
        if reason_code:
            return reason_code[0].get('text', '') or \
                   reason_code[0].get('coding', [{}])[0].get('display', '')
        return ''
    
    def _extract_access_site(self, procedure: Dict) -> str:
        """Extract access site from procedure"""
        body_site = procedure.get('bodySite', [])
        if body_site:
            return body_site[0].get('text', '') or \
                   body_site[0].get('coding', [{}])[0].get('display', '')
        return ''
    
    def _extract_lesion_location(self, procedure: Dict) -> str:
        """Extract lesion location from procedure"""
        # This would typically come from procedure notes or specific extensions
        # For now, extracting from procedure code or body site
        return self._extract_access_site(procedure)
