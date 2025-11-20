"""
EPIC FHIR to CathPCI Data Extractor
Main script to extract data from EPIC FHIR and convert to CathPCI format
"""

import json
import os
from datetime import datetime
from typing import List, Dict
from epic_fhir_client import EPICFHIRClient
from fhir_to_cathpci_mapper import FHIRToCathPCIMapper


class FHIRToCathPCIExtractor:
    """Extract FHIR data from EPIC and convert to CathPCI format"""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the extractor
        
        Args:
            output_dir: Directory to save output files
        """
        self.client = EPICFHIRClient()
        self.mapper = FHIRToCathPCIMapper()
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def extract_patient_data(self, patient_id: str) -> Dict:
        """
        Extract complete patient data from EPIC FHIR
        
        Args:
            patient_id: FHIR patient ID
            
        Returns:
            Dictionary containing all extracted FHIR resources
        """
        print(f"Extracting data for patient: {patient_id}")
        
        # Fetch all relevant resources
        patient = self.client.get_patient(patient_id)
        if not patient:
            print(f"Patient {patient_id} not found")
            return {}
        
        procedures = self.client.get_procedures(patient_id)
        observations = self.client.get_observations(patient_id)
        conditions = self.client.get_conditions(patient_id)
        medications = self.client.get_medication_requests(patient_id)
        
        print(f"  Found {len(procedures)} procedures")
        print(f"  Found {len(observations)} observations")
        print(f"  Found {len(conditions)} conditions")
        print(f"  Found {len(medications)} medications")
        
        return {
            'patient': patient,
            'procedures': procedures,
            'observations': observations,
            'conditions': conditions,
            'medications': medications
        }
    
    def convert_to_cathpci(self, fhir_data: Dict) -> Dict:
        """
        Convert FHIR data to CathPCI format
        
        Args:
            fhir_data: Dictionary containing FHIR resources
            
        Returns:
            Dictionary with CathPCI formatted data
        """
        patient = fhir_data.get('patient')
        if not patient:
            return {}
        
        # Map patient demographics
        demographics = self.mapper.map_patient_demographics(patient)
        
        # Map procedures
        procedures = fhir_data.get('procedures', [])
        observations = fhir_data.get('observations', [])
        conditions = fhir_data.get('conditions', [])
        
        cathpci_procedures = []
        for procedure in procedures:
            cathpci_proc = self.mapper.map_procedure_to_cathpci(
                procedure, observations, conditions
            )
            cathpci_procedures.append(cathpci_proc)
        
        return {
            'demographics': demographics,
            'procedures': cathpci_procedures,
            'raw_fhir_data': {
                'patient_id': patient.get('id'),
                'procedure_count': len(procedures),
                'observation_count': len(observations),
                'condition_count': len(conditions)
            }
        }
    
    def save_output(self, data: Dict, filename: str = None):
        """
        Save output to JSON file
        
        Args:
            data: Data to save
            filename: Output filename (optional)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cathpci_data_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nData saved to: {filepath}")
        return filepath
    
    def extract_and_convert(self, patient_id: str, save: bool = True) -> Dict:
        """
        Complete workflow: extract FHIR data and convert to CathPCI
        
        Args:
            patient_id: FHIR patient ID
            save: Whether to save output to file
            
        Returns:
            CathPCI formatted data
        """
        # Extract FHIR data
        fhir_data = self.extract_patient_data(patient_id)
        
        if not fhir_data:
            return {}
        
        # Convert to CathPCI
        print("\nConverting to CathPCI format...")
        cathpci_data = self.convert_to_cathpci(fhir_data)
        
        # Save if requested
        if save and cathpci_data:
            self.save_output(cathpci_data)
        
        return cathpci_data
    
    def extract_multiple_patients(self, patient_ids: List[str], save: bool = True) -> List[Dict]:
        """
        Extract and convert data for multiple patients
        
        Args:
            patient_ids: List of FHIR patient IDs
            save: Whether to save output to file
            
        Returns:
            List of CathPCI formatted data for each patient
        """
        all_data = []
        
        for patient_id in patient_ids:
            print(f"\n{'='*60}")
            cathpci_data = self.extract_and_convert(patient_id, save=False)
            if cathpci_data:
                all_data.append(cathpci_data)
        
        # Save combined data
        if save and all_data:
            self.save_output({'patients': all_data}, 'cathpci_data_batch.json')
        
        return all_data


def main():
    """Main execution function"""
    print("EPIC FHIR to CathPCI Data Extractor")
    print("="*60)
    
    # Initialize extractor
    extractor = FHIRToCathPCIExtractor()
    
    # Example EPIC sample patient IDs (these are publicly available test patients)
    # Note: These IDs may need to be updated based on EPIC's current sandbox data
    sample_patient_ids = [
        "Tbt3KuCY0B5PSrJvCu2j-PlK.aiHsu2xUjUM8bWpetXoB",  # Sample patient from EPIC
        "erXuFYUfucBZaryVksYEcMg3",  # Another sample patient
    ]
    
    print("\nAttempting to extract data from EPIC FHIR sandbox...")
    print("Note: Using EPIC's public sandbox - some patient IDs may not be available")
    print("\nIf you have specific patient IDs, you can modify the sample_patient_ids list")
    print(f"or call extractor.extract_and_convert(patient_id) directly\n")
    
    # Try to extract data for sample patients
    for patient_id in sample_patient_ids:
        try:
            print(f"\n{'='*60}")
            print(f"Attempting patient ID: {patient_id}")
            cathpci_data = extractor.extract_and_convert(patient_id)
            
            if cathpci_data and cathpci_data.get('demographics'):
                print("\n✓ Successfully extracted and converted data!")
                print(f"  Patient: {cathpci_data['demographics'].get('name', 'N/A')}")
                print(f"  DOB: {cathpci_data['demographics'].get('date_of_birth', 'N/A')}")
                print(f"  Gender: {cathpci_data['demographics'].get('gender', 'N/A')}")
                print(f"  Procedures: {len(cathpci_data.get('procedures', []))}")
                break  # Success - exit after first successful extraction
            else:
                print("  Patient not found or no data available")
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print("\n" + "="*60)
    print("\nTo use this tool with specific patient IDs:")
    print("  from cathpci_extractor import FHIRToCathPCIExtractor")
    print("  extractor = FHIRToCathPCIExtractor()")
    print("  data = extractor.extract_and_convert('patient_id')")
    print("\nOutput files are saved to the 'output/' directory")


if __name__ == "__main__":
    main()
