import requests 
username = input("Username: ") 
password = input("Password: ") 
if username == "admin" and password == "1234": 
    print("Authentication Successful") 
 
    role = "Admin" 
elif username == "user" and password == "1111": 
    print("Authentication Successful") 
    role = "User" 
else: 
    print("Authentication Failed") 
    exit() 
operation = input("Enter operation: ") 
if operation == "read": 
    print("Authorization Successful") 
    print("Operation Allowed") 
elif operation == "write": 
    print("Authorization Successful") 
    print("Operation Allowed") 
else: 
    print("Authorization Failed") 
    print("Operation Not Allowed") 
# Secure HTTPS communication 
url = "https://api.thingspeak.com/update" 
data = { 
    "api_key": "UJZK95RDT96K21W1", 
    "field1": 25 
} 
response = requests.get(url, params=data) 
print("Secure Data Transmission Response:", response.text)