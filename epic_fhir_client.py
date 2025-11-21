"""
EPIC FHIR Client Module
Connects to EPIC's free FHIR sandbox to extract patient data
"""

import requests
from typing import Dict, List, Optional
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EPICFHIRClient:
    """Client to interact with EPIC's free FHIR sandbox"""
    
    # EPIC's public FHIR sandbox endpoint (no authentication required for demo data)
    BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize EPIC FHIR client
        
        Args:
            base_url: Optional custom FHIR endpoint URL. Defaults to EPIC's public sandbox.
        """
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/fhir+json',
            'Content-Type': 'application/fhir+json'
        })
    
    def get_patient(self, patient_id: str) -> Optional[Dict]:
        """
        Retrieve a patient resource by ID
        
        Args:
            patient_id: FHIR patient ID
            
        Returns:
            Patient resource as dictionary or None if not found
        """
        url = f"{self.base_url}/Patient/{patient_id}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching patient {patient_id}: {e}")
            return None
    
    def search_patients(self, **kwargs) -> List[Dict]:
        """
        Search for patients with given criteria
        
        Args:
            **kwargs: Search parameters (e.g., name, birthdate, identifier)
            
        Returns:
            List of patient resources
        """
        url = f"{self.base_url}/Patient"
        try:
            response = self.session.get(url, params=kwargs)
            response.raise_for_status()
            bundle = response.json()
            
            patients = []
            if bundle.get('entry'):
                patients = [entry['resource'] for entry in bundle['entry'] 
                           if entry.get('resource', {}).get('resourceType') == 'Patient']
            return patients
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching patients: {e}")
            return []
    
    def get_procedures(self, patient_id: str) -> List[Dict]:
        """
        Retrieve procedures for a patient
        
        Args:
            patient_id: FHIR patient ID
            
        Returns:
            List of procedure resources
        """
        url = f"{self.base_url}/Procedure"
        params = {'patient': patient_id}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            bundle = response.json()
            
            procedures = []
            if bundle.get('entry'):
                procedures = [entry['resource'] for entry in bundle['entry']
                            if entry.get('resource', {}).get('resourceType') == 'Procedure']
            return procedures
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching procedures for patient {patient_id}: {e}")
            return []
    
    def get_observations(self, patient_id: str, category: Optional[str] = None) -> List[Dict]:
        """
        Retrieve observations for a patient
        
        Args:
            patient_id: FHIR patient ID
            category: Optional observation category filter (e.g., 'vital-signs', 'laboratory')
            
        Returns:
            List of observation resources
        """
        url = f"{self.base_url}/Observation"
        params = {'patient': patient_id}
        if category:
            params['category'] = category
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            bundle = response.json()
            
            observations = []
            if bundle.get('entry'):
                observations = [entry['resource'] for entry in bundle['entry']
                              if entry.get('resource', {}).get('resourceType') == 'Observation']
            return observations
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching observations for patient {patient_id}: {e}")
            return []
    
    def get_conditions(self, patient_id: str) -> List[Dict]:
        """
        Retrieve conditions for a patient
        
        Args:
            patient_id: FHIR patient ID
            
        Returns:
            List of condition resources
        """
        url = f"{self.base_url}/Condition"
        params = {'patient': patient_id}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            bundle = response.json()
            
            conditions = []
            if bundle.get('entry'):
                conditions = [entry['resource'] for entry in bundle['entry']
                            if entry.get('resource', {}).get('resourceType') == 'Condition']
            return conditions
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching conditions for patient {patient_id}: {e}")
            return []
    
    def get_medication_requests(self, patient_id: str) -> List[Dict]:
        """
        Retrieve medication requests for a patient
        
        Args:
            patient_id: FHIR patient ID
            
        Returns:
            List of medication request resources
        """
        url = f"{self.base_url}/MedicationRequest"
        params = {'patient': patient_id}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            bundle = response.json()
            
            medications = []
            if bundle.get('entry'):
                medications = [entry['resource'] for entry in bundle['entry']
                             if entry.get('resource', {}).get('resourceType') == 'MedicationRequest']
            return medications
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching medications for patient {patient_id}: {e}")
            return []
