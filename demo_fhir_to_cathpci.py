"""
Demo script showing FHIR to CathPCI conversion with sample data
This demonstrates the functionality without requiring network access
"""

import json
from fhir_to_cathpci_mapper import FHIRToCathPCIMapper


def create_sample_fhir_patient():
    """
    Create a sample FHIR Patient resource
    
    Note: This uses a simple patient ID 'sample-patient-001' for demonstration.
    Real EPIC patient IDs are longer (e.g., 'Tbt3KuCY0B5PSrJvCu2j-PlK.aiHsu2xUjUM8bWpetXoB')
    """
    return {
        "resourceType": "Patient",
        "id": "sample-patient-001",
        "identifier": [
            {
                "type": {
                    "text": "MRN"
                },
                "value": "MRN-123456"
            }
        ],
        "name": [
            {
                "family": "Argonaut",
                "given": ["Jason"]
            }
        ],
        "gender": "male",
        "birthDate": "1963-01-01",
        "address": [
            {
                "line": ["123 Main Street"],
                "city": "Verona",
                "state": "WI",
                "postalCode": "53593",
                "country": "USA"
            }
        ],
        "extension": [
            {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                "extension": [
                    {
                        "url": "ombCategory",
                        "valueCoding": {
                            "system": "urn:oid:2.16.840.1.113883.6.238",
                            "code": "2106-3",
                            "display": "White"
                        }
                    }
                ]
            },
            {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                "extension": [
                    {
                        "url": "ombCategory",
                        "valueCoding": {
                            "system": "urn:oid:2.16.840.1.113883.6.238",
                            "code": "2186-5",
                            "display": "Not Hispanic or Latino"
                        }
                    }
                ]
            }
        ]
    }


def create_sample_fhir_procedure():
    """Create a sample FHIR Procedure resource"""
    return {
        "resourceType": "Procedure",
        "id": "cardiac-cath-001",
        "status": "completed",
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "41976001",
                    "display": "Cardiac catheterization"
                }
            ],
            "text": "Diagnostic Cardiac Catheterization"
        },
        "subject": {
            "reference": "Patient/sample-patient-001"
        },
        "performedDateTime": "2024-01-15T10:30:00Z",
        "reasonCode": [
            {
                "text": "Chest pain, suspected coronary artery disease"
            }
        ],
        "bodySite": [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "368504007",
                        "display": "Right radial artery"
                    }
                ],
                "text": "Right radial artery"
            }
        ]
    }


def create_sample_observations():
    """Create sample FHIR Observation resources"""
    return [
        {
            "resourceType": "Observation",
            "id": "obs-hemoglobin",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "718-7",
                        "display": "Hemoglobin"
                    }
                ],
                "text": "Hemoglobin"
            },
            "valueQuantity": {
                "value": 14.2,
                "unit": "g/dL",
                "system": "http://unitsofmeasure.org",
                "code": "g/dL"
            }
        },
        {
            "resourceType": "Observation",
            "id": "obs-creatinine",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "2160-0",
                        "display": "Creatinine"
                    }
                ],
                "text": "Creatinine"
            },
            "valueQuantity": {
                "value": 1.1,
                "unit": "mg/dL",
                "system": "http://unitsofmeasure.org",
                "code": "mg/dL"
            }
        },
        {
            "resourceType": "Observation",
            "id": "obs-cholesterol",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "2093-3",
                        "display": "Total Cholesterol"
                    }
                ],
                "text": "Total Cholesterol"
            },
            "valueQuantity": {
                "value": 210,
                "unit": "mg/dL",
                "system": "http://unitsofmeasure.org",
                "code": "mg/dL"
            }
        },
        {
            "resourceType": "Observation",
            "id": "obs-ldl",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "13457-7",
                        "display": "LDL Cholesterol"
                    }
                ],
                "text": "LDL"
            },
            "valueQuantity": {
                "value": 130,
                "unit": "mg/dL",
                "system": "http://unitsofmeasure.org",
                "code": "mg/dL"
            }
        },
        {
            "resourceType": "Observation",
            "id": "obs-hdl",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "2085-9",
                        "display": "HDL Cholesterol"
                    }
                ],
                "text": "HDL"
            },
            "valueQuantity": {
                "value": 45,
                "unit": "mg/dL",
                "system": "http://unitsofmeasure.org",
                "code": "mg/dL"
            }
        },
        {
            "resourceType": "Observation",
            "id": "obs-height",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8302-2",
                        "display": "Body Height"
                    }
                ],
                "text": "Height"
            },
            "valueQuantity": {
                "value": 178,
                "unit": "cm",
                "system": "http://unitsofmeasure.org",
                "code": "cm"
            }
        },
        {
            "resourceType": "Observation",
            "id": "obs-weight",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "29463-7",
                        "display": "Body Weight"
                    }
                ],
                "text": "Weight"
            },
            "valueQuantity": {
                "value": 85,
                "unit": "kg",
                "system": "http://unitsofmeasure.org",
                "code": "kg"
            }
        },
        {
            "resourceType": "Observation",
            "id": "obs-systolic-bp",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8480-6",
                        "display": "Systolic Blood Pressure"
                    }
                ],
                "text": "Systolic"
            },
            "valueQuantity": {
                "value": 138,
                "unit": "mmHg",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]"
            }
        },
        {
            "resourceType": "Observation",
            "id": "obs-diastolic-bp",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8462-4",
                        "display": "Diastolic Blood Pressure"
                    }
                ],
                "text": "Diastolic"
            },
            "valueQuantity": {
                "value": 88,
                "unit": "mmHg",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]"
            }
        },
        {
            "resourceType": "Observation",
            "id": "obs-smoking",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "72166-2",
                        "display": "Tobacco smoking status"
                    }
                ],
                "text": "Smoking Status"
            },
            "valueCodeableConcept": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "8517006",
                        "display": "Former smoker"
                    }
                ],
                "text": "Former smoker"
            }
        }
    ]


def create_sample_conditions():
    """Create sample FHIR Condition resources"""
    return [
        {
            "resourceType": "Condition",
            "id": "condition-diabetes",
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "44054006",
                        "display": "Diabetes mellitus type 2"
                    }
                ],
                "text": "Type 2 Diabetes"
            },
            "subject": {
                "reference": "Patient/sample-patient-001"
            }
        },
        {
            "resourceType": "Condition",
            "id": "condition-hypertension",
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "38341003",
                        "display": "Hypertension"
                    }
                ],
                "text": "Hypertension"
            },
            "subject": {
                "reference": "Patient/sample-patient-001"
            }
        },
        {
            "resourceType": "Condition",
            "id": "condition-family-history",
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "266894000",
                        "display": "Family history of coronary artery disease"
                    }
                ],
                "text": "Family history of CAD"
            },
            "subject": {
                "reference": "Patient/sample-patient-001"
            }
        }
    ]


def main():
    """Demonstrate FHIR to CathPCI conversion"""
    print("="*70)
    print("FHIR to CathPCI Conversion Demo")
    print("="*70)
    
    # Create sample FHIR data
    print("\n1. Creating sample FHIR resources...")
    patient = create_sample_fhir_patient()
    procedure = create_sample_fhir_procedure()
    observations = create_sample_observations()
    conditions = create_sample_conditions()
    
    print(f"   ✓ Patient: {patient['name'][0]['given'][0]} {patient['name'][0]['family']}")
    print(f"   ✓ Procedure: {procedure['code']['text']}")
    print(f"   ✓ Observations: {len(observations)}")
    print(f"   ✓ Conditions: {len(conditions)}")
    
    # Convert to CathPCI
    print("\n2. Converting to CathPCI format...")
    mapper = FHIRToCathPCIMapper()
    
    demographics = mapper.map_patient_demographics(patient)
    cathpci_procedure = mapper.map_procedure_to_cathpci(
        procedure, observations, conditions
    )
    
    # Create complete record
    cathpci_data = {
        "demographics": demographics,
        "procedures": [cathpci_procedure],
        "raw_fhir_data": {
            "patient_id": patient.get('id'),
            "procedure_count": 1,
            "observation_count": len(observations),
            "condition_count": len(conditions)
        }
    }
    
    # Display results
    print("\n3. CathPCI Data Extract:")
    print("-"*70)
    print("\nDEMOGRAPHICS:")
    print(f"   Patient ID: {demographics['patient_id']}")
    print(f"   Name: {demographics['name']}")
    print(f"   DOB: {demographics['date_of_birth']}")
    print(f"   Gender: {demographics['gender']}")
    print(f"   Race: {demographics['race']}")
    print(f"   MRN: {demographics['medical_record_number']}")
    
    print("\nPROCEDURE:")
    print(f"   Type: {cathpci_procedure['procedure_type']}")
    print(f"   Date: {cathpci_procedure['procedure_date']}")
    print(f"   Status: {cathpci_procedure['procedure_status']}")
    print(f"   Indication: {cathpci_procedure['indication']}")
    print(f"   Access Site: {cathpci_procedure['access_site']}")
    
    print("\nRISK FACTORS:")
    print(f"   Diabetes: {cathpci_procedure['diabetes']}")
    print(f"   Hypertension: {cathpci_procedure['hypertension']}")
    print(f"   Smoking: {cathpci_procedure['smoking_status']}")
    print(f"   Family History CAD: {cathpci_procedure['family_history_cad']}")
    
    print("\nLAB VALUES:")
    print(f"   Hemoglobin: {cathpci_procedure['hemoglobin']} g/dL")
    print(f"   Creatinine: {cathpci_procedure['creatinine']} mg/dL")
    print(f"   Total Cholesterol: {cathpci_procedure['total_cholesterol']} mg/dL")
    print(f"   LDL: {cathpci_procedure['ldl']} mg/dL")
    print(f"   HDL: {cathpci_procedure['hdl']} mg/dL")
    
    print("\nVITAL SIGNS:")
    print(f"   Height: {cathpci_procedure['height']} cm")
    print(f"   Weight: {cathpci_procedure['weight']} kg")
    print(f"   BMI: {cathpci_procedure['bmi']}")
    print(f"   Blood Pressure: {cathpci_procedure['systolic_bp']}/{cathpci_procedure['diastolic_bp']} mmHg")
    
    # Save output
    print("\n4. Saving output...")
    output_file = "demo_cathpci_output.json"
    with open(output_file, 'w') as f:
        json.dump(cathpci_data, f, indent=2)
    print(f"   ✓ Output saved to: {output_file}")
    
    print("\n" + "="*70)
    print("Demo completed successfully!")
    print("="*70)
    
    return cathpci_data


if __name__ == "__main__":
    main()
