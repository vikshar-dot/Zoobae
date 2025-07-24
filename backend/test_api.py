import requests
import json

# API Configuration
BASE_URL = "http://localhost:8000"
EMAIL = "hello@vikas.com"
PASSWORD = "helloworld"

def test_register():
    """Test user registration"""
    print("Testing registration...")
    data = {
        "email": "test2@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Register response: {response.status_code}")
    if response.status_code == 200:
        print(f"User created: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_login():
    """Test user login"""
    print("\nTesting login...")
    data = {
        "username": EMAIL,
        "password": PASSWORD
    }
    response = requests.post(f"{BASE_URL}/login", data=data)
    print(f"Login response: {response.status_code}")
    if response.status_code == 200:
        print(f"Login successful: {response.json()}")
        return response.json()
    return None

def test_create_profile(token):
    """Test profile creation"""
    print("\nTesting profile creation...")
    headers = {"Authorization": f"Bearer {token}"}
    
    profile_data = {
        "name": "Test User",
        "pronouns": "They/Them",
        "verification_status": "unverified",
        "essential_details": [
            {"key": "age", "value": "25", "is_visible": True},
            {"key": "height", "value": "5'8\"", "is_visible": True},
            {"key": "home", "value": "New York, NY", "is_visible": True}
        ],
        "prompts": [
            {"question": "I'm looking for someone who...", "answer": "can make me laugh", "order": 1},
            {"question": "My ideal first date is...", "answer": "trying a new restaurant", "order": 2}
        ],
        "photos": []
    }
    
    response = requests.post(f"{BASE_URL}/profile", json=profile_data, headers=headers)
    print(f"Profile creation response: {response.status_code}")
    if response.status_code == 200:
        print(f"Profile created: {response.json()}")
    elif response.status_code == 422:
        print(f"Validation error: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_get_profile(token):
    """Test getting profile"""
    print("\nTesting get profile...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    print(f"Get profile response: {response.status_code}")
    if response.status_code == 200:
        print(f"Profile retrieved: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_api():
    print("Starting API tests...")
    
    # Test login
    print("\nTesting login...")
    login_data = {
        "username": EMAIL,
        "password": PASSWORD
    }
    login_response = requests.post(f"{BASE_URL}/login", data=login_data)
    print(f"Login response: {login_response.status_code}")
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        print(f"Login successful: {login_data}")
        access_token = login_data["access_token"]
        
        # Set up headers with auth token
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Test get profile
        print("\nTesting get profile...")
        profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
        print(f"Get profile response: {profile_response.status_code}")
        if profile_response.status_code == 200:
            profile = profile_response.json()
            print(f"Profile retrieved: {profile}")
        
        # Test get photos
        print("\nTesting get photos...")
        photos_response = requests.get(f"{BASE_URL}/profile/photos", headers=headers)
        print(f"Get photos response: {photos_response.status_code}")
        if photos_response.status_code == 200:
            photos = photos_response.json()
            print(f"Photos retrieved: {photos}")
        else:
            print(f"Photos error: {photos_response.text}")
    
    print("\nAPI tests completed!")

if __name__ == "__main__":
    test_api() 