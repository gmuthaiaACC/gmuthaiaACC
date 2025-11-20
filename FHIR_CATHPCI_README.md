# EPIC FHIR to CathPCI Data Extractor

This project provides a Python-based solution to connect to EPIC EMR's free FHIR resources and extract data from the sample dataset, converting it to CathPCI (Cardiac Catheterization and Percutaneous Coronary Intervention) registry format.

## Overview

The tool consists of three main components:

1. **EPIC FHIR Client** (`epic_fhir_client.py`) - Connects to EPIC's public FHIR sandbox and retrieves patient data
2. **FHIR to CathPCI Mapper** (`fhir_to_cathpci_mapper.py`) - Converts FHIR resources to CathPCI data format
3. **Data Extractor** (`cathpci_extractor.py`) - Main orchestrator that ties everything together

## Features

- ✅ Connects to EPIC's free FHIR sandbox (no authentication required for demo)
- ✅ Extracts patient demographics, procedures, observations, conditions, and medications
- ✅ Maps FHIR resources to CathPCI registry data elements including:
  - Patient demographics (name, DOB, gender, race, ethnicity)
  - Risk factors (diabetes, hypertension, smoking status)
  - Lab values (hemoglobin, creatinine, cholesterol, LDL, HDL)
  - Vital signs (height, weight, BMI, blood pressure)
  - Procedure details (type, date, indication, access site)
- ✅ Saves output in JSON format for further processing

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/gmuthaiaACC/gmuthaiaACC.git
cd gmuthaiaACC
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the extractor with sample patient data:

```bash
python cathpci_extractor.py
```

This will attempt to extract data from EPIC's public sandbox using sample patient IDs and save the output to the `output/` directory.

### Using in Your Code

```python
from cathpci_extractor import FHIRToCathPCIExtractor

# Initialize the extractor
extractor = FHIRToCathPCIExtractor(output_dir="output")

# Extract and convert data for a specific patient
patient_id = "Tbt3KuCY0B5PSrJvCu2j-PlK.aiHsu2xUjUM8bWpetXoB"
cathpci_data = extractor.extract_and_convert(patient_id)

# Access the converted data
print(f"Patient: {cathpci_data['demographics']['name']}")
print(f"Procedures: {len(cathpci_data['procedures'])}")

# Extract data for multiple patients
patient_ids = ["patient1", "patient2", "patient3"]
all_data = extractor.extract_multiple_patients(patient_ids)
```

### Using Individual Components

#### EPIC FHIR Client

```python
from epic_fhir_client import EPICFHIRClient

client = EPICFHIRClient()

# Get patient data
patient = client.get_patient("patient_id")

# Search for patients
patients = client.search_patients(name="Smith")

# Get procedures
procedures = client.get_procedures("patient_id")

# Get observations (lab values, vitals)
observations = client.get_observations("patient_id")
```

#### FHIR to CathPCI Mapper

```python
from fhir_to_cathpci_mapper import FHIRToCathPCIMapper

mapper = FHIRToCathPCIMapper()

# Map patient demographics
demographics = mapper.map_patient_demographics(patient_resource)

# Map procedure to CathPCI format
cathpci_procedure = mapper.map_procedure_to_cathpci(
    procedure_resource,
    observations,
    conditions
)
```

## EPIC FHIR Sandbox

This tool connects to EPIC's public FHIR R4 sandbox at:
```
https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4
```

The sandbox provides sample patient data without requiring authentication. For production use with real EPIC implementations, you would need:
- OAuth 2.0 authentication
- Client credentials registered with EPIC
- Appropriate permissions and scopes

## CathPCI Data Elements

The mapper extracts and converts the following CathPCI data elements:

### Demographics
- Patient ID
- Medical Record Number
- Date of Birth
- Gender
- Race
- Ethnicity
- Name
- Address

### Risk Factors
- Diabetes
- Hypertension
- Smoking Status
- Family History of CAD

### Lab Values
- Hemoglobin
- Creatinine
- Total Cholesterol
- LDL
- HDL

### Vital Signs
- Height
- Weight
- BMI
- Systolic Blood Pressure
- Diastolic Blood Pressure

### Procedure Details
- Procedure ID
- Procedure Date
- Procedure Type
- Status
- Indication
- Access Site
- Lesion Location

## Output Format

The tool generates JSON output with the following structure:

```json
{
  "demographics": {
    "patient_id": "...",
    "medical_record_number": "...",
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "name": "John Doe",
    ...
  },
  "procedures": [
    {
      "procedure_id": "...",
      "procedure_date": "2024-01-01",
      "procedure_type": "Cardiac Catheterization",
      "diabetes": true,
      "hypertension": false,
      "hemoglobin": 14.5,
      ...
    }
  ],
  "raw_fhir_data": {
    "patient_id": "...",
    "procedure_count": 1,
    "observation_count": 25,
    "condition_count": 3
  }
}
```

## Extending the Tool

### Adding New FHIR Resources

To extract additional FHIR resources, add methods to `epic_fhir_client.py`:

```python
def get_diagnostic_reports(self, patient_id: str) -> List[Dict]:
    url = f"{self.base_url}/DiagnosticReport"
    params = {'patient': patient_id}
    # ... implementation
```

### Adding CathPCI Data Elements

To map additional CathPCI data elements, add methods to `fhir_to_cathpci_mapper.py`:

```python
def _extract_new_element(self, resource: Dict) -> Any:
    # Custom extraction logic
    pass
```

## Troubleshooting

### Connection Issues
- Ensure you have internet connectivity
- Check that EPIC's FHIR sandbox is accessible
- Verify the base URL is correct

### Patient Not Found
- EPIC's sandbox patient IDs may change
- Use sample patient IDs from EPIC's documentation
- Check EPIC's developer portal for current test patient IDs

### Missing Data
- Not all FHIR resources may have complete data
- The mapper handles missing data gracefully with default values
- Check the raw FHIR response for available data

## References

- [EPIC FHIR Documentation](https://fhir.epic.com/)
- [FHIR R4 Specification](https://www.hl7.org/fhir/R4/)
- [CathPCI Registry](https://www.ncdr.com/registries/cathpci-registry)

## License

This project is provided as-is for educational and development purposes.

## Author

Ganesan Muthiah
- Email: gmuthaia@live.com
- LinkedIn: [linkedin.com/in/ganesanmuthiah](https://www.linkedin.com/in/ganesanmuthiah/)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
