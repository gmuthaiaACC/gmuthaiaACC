# EPIC FHIR to CathPCI Data Extraction - Quick Start Guide

## What This Tool Does

This tool connects to EPIC EMR's free FHIR (Fast Healthcare Interoperability Resources) sandbox and extracts patient data, converting it to the CathPCI (Cardiac Catheterization and Percutaneous Coronary Intervention) registry format.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. See What's Available

Check the mapping coverage and available CathPCI elements:

```bash
python show_mapping_status.py
```

This shows:
- Currently mapped elements (29)
- Available elements to add (51+)
- LOINC and SNOMED codes for mapping

### 3. Run the Demo

The easiest way to see how the tool works is to run the demo script:

```bash
python demo_fhir_to_cathpci.py
```

This will:
- Create sample FHIR resources (Patient, Procedure, Observations, Conditions)
- Convert them to CathPCI format
- Display the results on screen
- Save output to `demo_cathpci_output.json`

### 3. Connect to EPIC's Real FHIR Sandbox

To extract data from EPIC's actual sandbox:

```bash
python cathpci_extractor.py
```

**Note**: This requires internet access to EPIC's FHIR endpoint. If you're in a restricted network environment, the connection may fail. The demo script works offline.

## Extending the Mappings

The tool currently maps **29 core CathPCI elements** out of 1000+ available. To see what's available and add more:

### Check Mapping Status

```bash
python show_mapping_status.py
```

This displays:
- Currently mapped elements (29)
- Available elements ready to add (51)
- LOINC codes for lab observations
- SNOMED codes for conditions

### Add New Elements

See **[EXTENDING_MAPPINGS.md](EXTENDING_MAPPINGS.md)** for detailed step-by-step instructions on adding:
- Lab values (HbA1c, troponin, BNP, etc.)
- Risk factors (prior MI, prior PCI, PAD, etc.)
- Medications (aspirin, statins, beta blockers, etc.)
- Procedure details (contrast volume, fluoroscopy time, stents, etc.)
- Outcomes (mortality, stroke, bleeding, etc.)

## File Structure

```
.
├── README.md                      # Original GitHub profile README
├── FHIR_CATHPCI_README.md        # Detailed documentation
├── QUICK_START.md                # This file
├── EXTENDING_MAPPINGS.md         # Guide to adding more CathPCI elements
├── requirements.txt              # Python dependencies
├── config.py                     # Configuration (FHIR endpoint, patient IDs)
├── cathpci_data_dictionary.py    # CathPCI data elements catalog (80 elements)
├── epic_fhir_client.py           # FHIR client to connect to EPIC
├── fhir_to_cathpci_mapper.py     # Converter from FHIR to CathPCI format
├── cathpci_extractor.py          # Main extraction tool
├── demo_fhir_to_cathpci.py       # Demo with sample data (works offline)
├── show_mapping_status.py        # Utility to show mapping coverage
└── example_output.json           # Example CathPCI output
```

## Usage Examples

### Example 1: Extract Data for a Specific Patient

```python
from cathpci_extractor import FHIRToCathPCIExtractor

# Initialize the extractor
extractor = FHIRToCathPCIExtractor(output_dir="output")

# Extract and convert data for a specific patient
patient_id = "Tbt3KuCY0B5PSrJvCu2j-PlK.aiHsu2xUjUM8bWpetXoB"
cathpci_data = extractor.extract_and_convert(patient_id)

# Access the data
print(f"Patient: {cathpci_data['demographics']['name']}")
print(f"Procedures: {len(cathpci_data['procedures'])}")
```

### Example 2: Extract Data for Multiple Patients

```python
from cathpci_extractor import FHIRToCathPCIExtractor

extractor = FHIRToCathPCIExtractor()

# Process multiple patients
patient_ids = ["patient1", "patient2", "patient3"]
all_data = extractor.extract_multiple_patients(patient_ids)

print(f"Processed {len(all_data)} patients")
```

### Example 3: Use Individual Components

```python
from epic_fhir_client import EPICFHIRClient
from fhir_to_cathpci_mapper import FHIRToCathPCIMapper

# Create client
client = EPICFHIRClient()

# Get patient data
patient = client.get_patient("patient_id")
procedures = client.get_procedures("patient_id")
observations = client.get_observations("patient_id")
conditions = client.get_conditions("patient_id")

# Convert to CathPCI
mapper = FHIRToCathPCIMapper()
demographics = mapper.map_patient_demographics(patient)
cathpci_proc = mapper.map_procedure_to_cathpci(
    procedures[0], observations, conditions
)
```

## Output Format

The tool generates JSON output with CathPCI data elements:

```json
{
  "demographics": {
    "patient_id": "...",
    "name": "Jason Argonaut",
    "date_of_birth": "1963-01-01",
    "gender": "M",
    "race": "White",
    "ethnicity": "Not Hispanic or Latino"
  },
  "procedures": [
    {
      "procedure_type": "Cardiac catheterization",
      "procedure_date": "2024-01-15T10:30:00Z",
      "diabetes": true,
      "hypertension": true,
      "hemoglobin": 14.2,
      "creatinine": 1.1,
      "bmi": 26.83,
      "systolic_bp": 138,
      "diastolic_bp": 88
    }
  ]
}
```

## CathPCI Data Elements Extracted

### Demographics
- Patient ID, MRN, Name
- Date of Birth, Gender
- Race, Ethnicity, Address

### Risk Factors
- Diabetes, Hypertension
- Smoking Status
- Family History of CAD

### Lab Values
- Hemoglobin, Creatinine
- Total Cholesterol, LDL, HDL

### Vital Signs
- Height, Weight, BMI
- Blood Pressure

### Procedure Details
- Type, Date, Status
- Indication, Access Site

## Configuration

### Update Patient IDs

Edit `config.py` to update patient IDs:

```python
SAMPLE_PATIENT_IDS = [
    "your-patient-id-1",
    "your-patient-id-2",
]
```

### Change FHIR Endpoint

To use a different FHIR endpoint:

```python
from epic_fhir_client import EPICFHIRClient

client = EPICFHIRClient(base_url="https://your-fhir-endpoint.com/R4")
```

## Troubleshooting

### "No address associated with hostname" Error

This means you cannot access EPIC's FHIR endpoint. This is common in restricted network environments. Use the demo script instead:

```bash
python demo_fhir_to_cathpci.py
```

### Patient Not Found

EPIC's sandbox patient IDs can change. Check EPIC's documentation for current test patient IDs:
https://fhir.epic.com/Documentation

### Missing Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

## Next Steps

1. **Review the Demo Output**: Check `demo_cathpci_output.json` to see the expected output format
2. **Read Full Documentation**: See `FHIR_CATHPCI_README.md` for detailed information
3. **Customize Mappings**: Modify `fhir_to_cathpci_mapper.py` to add custom CathPCI data elements
4. **Add Authentication**: For production EPIC systems, implement OAuth 2.0 authentication

## Support

For questions or issues:
- Email: gmuthaia@live.com
- LinkedIn: [linkedin.com/in/ganesanmuthiah](https://www.linkedin.com/in/ganesanmuthiah/)

## References

- [EPIC FHIR Documentation](https://fhir.epic.com/)
- [FHIR R4 Specification](https://www.hl7.org/fhir/R4/)
- [CathPCI Registry](https://www.ncdr.com/registries/cathpci-registry)
