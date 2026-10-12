import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def analyze_phone_number(phone_string):
    try:
        # Parse the raw string into a phone number object
        parsed_number = phonenumbers.parse(phone_string)
        
        # 1. Validation checks
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        
        if not is_possible:
            return {"error": "Invalid phone number format."}
            
        # 2. Extract structural and carrier metadata
        formatted_international = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
        
        region_description = geocoder.description_for_number(parsed_number, "en")
        carrier_name = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)
        
        number_type = phonenumbers.number_type(parsed_number)
        type_mapping = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
            phonenumbers.PhoneNumberType.VOIP: "VoIP"
        }
        line_type = type_mapping.get(number_type, "Other / Unknown")

        return {
            "formatted": formatted_international,
            "valid": is_valid,
            "region": region_description or "Unknown Region",
            "carrier": carrier_name or "Unknown Carrier",
            "line_type": line_type,
            "time_zones": list(time_zones)
        }
        
    except phonenumbers.NumberParseException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Pulls the number from environment variable or defaults to your target number
    target = os.getenv("TARGET_PHONE", "+2349163349757")
    print(f"Analyzing target number: {target}\n")
    result = analyze_phone_number(target)
    
    print("--- Phone Number Metadata ---")
    for key, value in result.items():
        print(f"{key.capitalize()}: {value}")
