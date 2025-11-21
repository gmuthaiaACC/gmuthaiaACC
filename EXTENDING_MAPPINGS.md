# Extending CathPCI Data Mappings

This guide shows you how to add additional CathPCI data elements to the FHIR to CathPCI mapper.

## Understanding the Current Implementation

The current implementation maps **31 CathPCI data elements** as a foundational starting point:

### Currently Mapped Elements

**Demographics (8 elements):**
- patient_id, medical_record_number, date_of_birth, gender, race, ethnicity, name, address

**Risk Factors (4 elements):**
- diabetes, hypertension, smoking_status, family_history_cad

**Lab Values (5 elements):**
- hemoglobin, creatinine, total_cholesterol, ldl, hdl

**Vital Signs (5 elements):**
- height, weight, bmi, systolic_bp, diastolic_bp

**Procedure Details (7 elements):**
- procedure_id, procedure_date, procedure_type, procedure_status, indication, access_site, lesion_location

**Note:** The CathPCI Registry contains 1000+ data elements. This implementation provides the most commonly used elements to get you started.

## Why Only Core Elements?

The initial implementation focuses on core elements because:

1. **FHIR Data Availability**: Not all CathPCI elements have direct FHIR equivalents
2. **Complexity**: Some elements require complex clinical logic or multiple FHIR resources
3. **Extensibility**: The architecture allows easy addition of new elements as needed
4. **EPIC Sandbox Limitations**: The free EPIC sandbox has limited sample data

## How to Add New CathPCI Data Elements

### Step 1: Identify the Data Element

Check `cathpci_data_dictionary.py` for available elements:

```python
from cathpci_data_dictionary import get_unmapped_elements, LOINC_CODES, SNOMED_CODES

# See what's available to add
unmapped = get_unmapped_elements()
print(unmapped)
```

### Step 2: Find the FHIR Source

Determine which FHIR resource contains the data:

| CathPCI Element | FHIR Resource | FHIR Field |
|-----------------|---------------|------------|
| Prior MI | Condition | code.coding (SNOMED: 22298006) |
| HbA1c | Observation | valueQuantity (LOINC: 4548-4) |
| Heart Rate | Observation | valueQuantity (LOINC: 8867-4) |
| Stent Type | Device | type |
| Contrast Volume | Procedure | used |

### Step 3: Add Extraction Method

Add a new method to `fhir_to_cathpci_mapper.py`:

```python
def _extract_prior_mi(self, conditions: List[Dict]) -> bool:
    """Extract prior myocardial infarction from conditions"""
    for condition in conditions:
        code = condition.get('code', {})
        for coding in code.get('coding', []):
            # SNOMED code for MI: 22298006
            if coding.get('code') == '22298006':
                return True
    return False
```

### Step 4: Add to Mapping

Update the `map_procedure_to_cathpci` method:

```python
def map_procedure_to_cathpci(self, procedure: Dict, observations: List[Dict], 
                              conditions: List[Dict]) -> Dict[str, Any]:
    cathpci_record = {
        # ... existing mappings ...
        
        # Add your new element
        'prior_mi': self._extract_prior_mi(conditions),
    }
    return cathpci_record
```

## Complete Example: Adding HbA1c

Here's a complete example of adding Hemoglobin A1c:

### 1. Add to `cathpci_data_dictionary.py` (Already there!)

```python
CATHPCI_LAB_VALUES = {
    # ...existing...
    'hba1c': 'Hemoglobin A1c (%)',  # Uncomment this line
}

LOINC_CODES = {
    # ...existing...
    'hba1c': '4548-4',  # Already defined
}
```

### 2. Add extraction method to `fhir_to_cathpci_mapper.py`

```python
def _extract_hba1c(self, observations: List[Dict]) -> Optional[float]:
    """Extract HbA1c from observations"""
    return self._extract_lab_value(observations, 'hba1c')
```

### 3. Add to mapping in `map_procedure_to_cathpci`

```python
# In the Lab Values section
'hba1c': self._extract_hba1c(observations),
```

That's it! The generic `_extract_lab_value` method handles the LOINC code matching.

## Complete Example: Adding Prior PCI

For a condition/history element:

### 1. Add extraction method

```python
def _extract_prior_pci(self, procedures: List[Dict]) -> bool:
    """
    Check if patient has prior PCI
    
    This would require fetching historical procedures, not just current one.
    In practice, you'd search for procedures with date < current procedure date.
    """
    # This is a simplified example
    # In production, you'd need to:
    # 1. Fetch all procedures for patient
    # 2. Filter by procedure type (PCI/catheterization)
    # 3. Check if any occurred before current procedure
    return False  # Placeholder
```

### 2. Add to mapper

```python
'prior_pci': self._extract_prior_pci(procedures),
```

## Complete Example: Adding Medications

For medication data:

### 1. Fetch medications in extractor

Update `cathpci_extractor.py` to pass medications to mapper:

```python
# In extract_patient_data method
medications = self.client.get_medication_requests(patient_id)

# In convert_to_cathpci method
cathpci_proc = self.mapper.map_procedure_to_cathpci(
    procedure, observations, conditions, medications  # Add medications
)
```

### 2. Update mapper signature

```python
def map_procedure_to_cathpci(self, procedure: Dict, observations: List[Dict], 
                              conditions: List[Dict], 
                              medications: List[Dict] = None) -> Dict[str, Any]:
    if medications is None:
        medications = []
    
    cathpci_record = {
        # ... existing ...
        'aspirin_pre_procedure': self._has_medication(medications, 'aspirin'),
        'statin': self._has_medication(medications, 'statin'),
    }
```

### 3. Add helper method

```python
def _has_medication(self, medications: List[Dict], med_name: str) -> bool:
    """Check if patient has specific medication"""
    for med in medications:
        code = med.get('medicationCodeableConcept', {})
        text = code.get('text', '').lower()
        for coding in code.get('coding', []):
            display = coding.get('display', '').lower()
            if med_name.lower() in text or med_name.lower() in display:
                return True
    return False
```

## Using LOINC and SNOMED Codes

The `cathpci_data_dictionary.py` includes common codes:

```python
from cathpci_data_dictionary import LOINC_CODES, SNOMED_CODES

# Get LOINC code for a lab
loinc_hba1c = LOINC_CODES['hba1c']  # '4548-4'

# Get SNOMED code for a condition
snomed_mi = SNOMED_CODES['myocardial_infarction']  # '22298006'
```

Use these in your extraction methods to match FHIR coding systems.

## Testing Your Changes

After adding new elements:

1. **Update demo data** in `demo_fhir_to_cathpci.py`:
```python
def create_sample_observations():
    return [
        # ... existing observations ...
        {
            "resourceType": "Observation",
            "id": "obs-hba1c",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "4548-4",
                    "display": "Hemoglobin A1c"
                }]
            },
            "valueQuantity": {
                "value": 7.2,
                "unit": "%"
            }
        }
    ]
```

2. **Run the demo**:
```bash
python demo_fhir_to_cathpci.py
```

3. **Verify output** contains your new element

## Quick Reference: Common Patterns

### Adding a Lab Value (from Observation)
```python
'new_lab': self._extract_lab_value(observations, 'lab_name')
```

### Adding a Vital Sign (from Observation)
```python
'new_vital': self._extract_vital_sign(observations, 'vital_name')
```

### Adding a Condition (from Condition)
```python
'new_condition': self._has_condition(conditions, 'condition_name')
```

### Adding a Demographic (from Patient)
```python
'new_demographic': patient.get('field_name', 'default_value')
```

## Need More Help?

1. **Review the code**: Look at existing methods in `fhir_to_cathpci_mapper.py`
2. **Check FHIR docs**: https://www.hl7.org/fhir/R4/
3. **Check CathPCI docs**: https://www.ncdr.com/registries/cathpci-registry
4. **Check EPIC docs**: https://fhir.epic.com/

## Summary

The mapper currently includes **31 core elements** out of 1000+ possible CathPCI elements. This is by design to:
- Provide a solid foundation
- Demonstrate the mapping pattern
- Allow easy extension based on your needs

You can extend it by:
1. Identifying the element in `cathpci_data_dictionary.py`
2. Finding the FHIR source
3. Adding an extraction method
4. Adding to the mapping

The architecture is designed for easy extension - add only the elements you need!
