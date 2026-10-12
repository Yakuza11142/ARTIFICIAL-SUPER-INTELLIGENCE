import os
import requests
import phonenumbers
from phonenumbers import carrier, geocoder

def analyze_number_with_abstract_api(phone_string):
    results = {}
    
    try:
        # 1. Offline Baseline Analysis
        parsed_number = phonenumbers.parse(phone_string)
        results["formatted"] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        results["valid_format"] = phonenumbers.is_valid_number(parsed_number)
        results["baseline_region"] = geocoder.description_for_number(parsed_number, "en") or "Nigeria"
        
        # 2. AbstractAPI Phone Validation Integration
        api_key = os.getenv("FREE_LOOKUP_API_KEY")
        
        if api_key:
            api_url = f"https://phonevalidation.abstractapi.com/v1/?api_key={api_key}&phone={phone_string}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results["number_is_active"] = data.get("valid", "Unknown")
                results["line_type"] = data.get("type", "Unknown")
                results["carrier"] = data.get("carrier", "Unknown")
                results["country"] = data.get("country", {}).get("name", "Unknown")
                # Pulls whatever region/location string the API registers
                results["api_location"] = data.get("location", "Not Provided by API")
            else:
                results["api_error"] = f"API request failed with status code {response.status_code}"
        else:
            results["api_status"] = "API Key not provided."
            results["carrier"] = carrier.name_for_number(parsed_number, "en") or "MTN Nigeria"
            results["line_type"] = "Mobile"
            results["api_location"] = "Requires API Key"
            
    except Exception as e:
        results["error"] = str(e)
        
    return results

if __name__ == "__main__":
    target = os.getenv("TARGET_PHONE", "+2349163349757")
    print(f"=== Running Tracking Analysis for: {target} ===\n")
    
    analysis_data = analyze_number_with_abstract_api(target)
    
    for key, value in analysis_data.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")
        
    print("\n[Note]: api_location shows regional prefix data, not real-time live city GPS coordinates.")
