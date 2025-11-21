"""
CathPCI Mapping Status Utility

This script shows which CathPCI data elements are currently mapped
and which are available to add.
"""

from cathpci_data_dictionary import (
    get_mapped_elements,
    get_unmapped_elements,
    CATHPCI_DATA_DICTIONARY,
    list_all_data_elements
)


def print_section_header(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_mapping_summary():
    """Print summary of mapped vs unmapped elements"""
    mapped = get_mapped_elements()
    all_elements = list_all_data_elements()
    
    total_available = sum(len(elements) for elements in all_elements.values())
    total_mapped = len(mapped)
    
    print_section_header("CathPCI Mapping Status Summary")
    
    print(f"Currently Mapped:     {total_mapped:3d} elements")
    print(f"Available to Add:     {total_available - total_mapped:3d} elements")
    print(f"Total in Dictionary:  {total_available:3d} elements")
    print(f"\nMapping Coverage:     {(total_mapped/total_available)*100:.1f}%")
    
    print("\n" + "-"*70)
    print("Note: The CathPCI Registry contains 1000+ total data elements.")
    print("This dictionary focuses on commonly used elements.")
    print("-"*70)


def print_mapped_elements():
    """Print all currently mapped elements by category"""
    print_section_header("Currently Mapped Elements (31)")
    
    mapped = set(get_mapped_elements())
    
    for category, elements in CATHPCI_DATA_DICTIONARY.items():
        mapped_in_category = [elem for elem in elements.keys() if elem in mapped]
        
        if mapped_in_category:
            print(f"\n{category.upper().replace('_', ' ')}:")
            for elem in mapped_in_category:
                description = elements[elem]
                print(f"  ✓ {elem:30s} - {description}")


def print_unmapped_elements():
    """Print all unmapped elements available to add"""
    unmapped = get_unmapped_elements()
    
    if not unmapped:
        print("\nAll elements in the dictionary are mapped!")
        return
    
    print_section_header("Available Elements to Add")
    
    for category, elements in unmapped.items():
        print(f"\n{category.upper().replace('_', ' ')}:")
        category_dict = CATHPCI_DATA_DICTIONARY[category]
        for elem in elements:
            description = category_dict[elem]
            print(f"  ○ {elem:30s} - {description}")


def print_loinc_snomed_reference():
    """Print LOINC and SNOMED code reference"""
    from cathpci_data_dictionary import LOINC_CODES, SNOMED_CODES
    
    print_section_header("LOINC Codes Reference")
    print("Use these codes when mapping FHIR Observations:\n")
    for name, code in sorted(LOINC_CODES.items()):
        print(f"  {name:25s} : {code}")
    
    print_section_header("SNOMED Codes Reference")
    print("Use these codes when mapping FHIR Conditions:\n")
    for name, code in sorted(SNOMED_CODES.items()):
        print(f"  {name:35s} : {code}")


def main():
    """Main function to display mapping status"""
    print("\n" + "="*70)
    print("  EPIC FHIR to CathPCI Mapper - Data Element Coverage")
    print("="*70)
    
    # Print summary
    print_mapping_summary()
    
    # Print mapped elements
    print_mapped_elements()
    
    # Print unmapped elements
    print_unmapped_elements()
    
    # Print code references
    print_loinc_snomed_reference()
    
    # Print help
    print_section_header("How to Add More Elements")
    print("1. Review the 'Available Elements to Add' section above")
    print("2. See EXTENDING_MAPPINGS.md for detailed instructions")
    print("3. Edit fhir_to_cathpci_mapper.py to add new extraction methods")
    print("4. Test your changes with demo_fhir_to_cathpci.py")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
