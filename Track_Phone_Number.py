import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium

def validate_phone_number(number):
    """Validate phone number format and return parsed object or None"""
    try:
        parsed = phonenumbers.parse(number)
        return parsed if phonenumbers.is_valid_number(parsed) else None
    except phonenumbers.NumberParseException:
        return None

def track_location():
    print("\n📱 Phone Number Location Tracker")
    print("-------------------------------\n")
    
    while True:
        number = input("Enter phone number with country code (e.g., +919876543210): ").strip()
        
        # Input validation
        if not number.startswith('+'):
            print("\n❌ Error: Number must start with '+' (e.g., +91 for India)")
            continue
            
        phone_obj = validate_phone_number(number)
        if not phone_obj:
            print("\n❌ Error: Invalid phone number. Please check:")
            print("- Correct country code (e.g., +1 for US, +91 for India)")
            print("- Full number without spaces/dashes (e.g., +919876543210)")
            continue
        
        # Get basic info
        location = geocoder.description_for_number(phone_obj, "en") or "Unknown location"
        provider = carrier.name_for_number(phone_obj, "en") or "Unknown carrier"
        
        print(f"\n🔍 Results for {number}:")
        print(f"📍 Location: {location}")
        print(f"📡 Carrier: {provider}")
        
        # Geocoding with OpenCage
        try:
            # Define the geocoder here
            geocoder_service = OpenCageGeocode("Enter API Key")
            results = geocoder_service.geocode(location)
            
            if not results or len(results) == 0:
                print("\n⚠️ Precise coordinates not available")
                break
                
            lat, lng = results[0]['geometry']['lat'], results[0]['geometry']['lng']
            print(f"\n🌎 Coordinates: {lat:.4f}, {lng:.4f}")
            
            # Generate map
            m = folium.Map(location=[lat, lng], zoom_start=12)
            folium.Marker(
                [lat, lng],
                popup=f"<b>{location}</b><br>{phone_obj.national_number}",
                tooltip="Click for details"
            ).add_to(m)
            
            filename = f"location_{number[1:]}.html"
            m.save(filename)
            print(f"\n✅ Map saved as: {filename}")
            print("Open this file in your browser to view the location")
            
        except Exception as e:
            print(f"\n⚠️ Geocoding error: {str(e)}")
        
        break  # Remove this line if you want to track multiple numbers

if __name__ == "__main__":
    track_location()
