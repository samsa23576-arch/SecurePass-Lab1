import requests

print("--- 1. TESTING PART A (GENERATION) ---")
url_gen = 'http://127.0.0.1:5000/generate?length=12'
response_gen = requests.get(url_gen)
print(response_gen.json())

print("\n--- 2. TESTING PART B & C (VALIDATION & DATABASE) ---")
# Ask the user to type a password instead of hardcoding it
my_test_password = input("Enter a password to validate on the server: ")

url_val = 'http://127.0.0.1:5000/validate'
data = {"password": my_test_password}
response_val = requests.post(url_val, json=data)
print(response_val.json())