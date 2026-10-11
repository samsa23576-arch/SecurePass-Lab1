import secrets
import string
import ctypes 

# Load the C library right at the start
try:
    c_lib = ctypes.CDLL("./version.so") # Use .dll if testing on Windows
    version_number = c_lib.get_security_version()
except:
    version_number = 1 

# --- FUNCTION 1: PASSWORD GENERATOR ---
def generate_password(length=12):
    # Combine all possible characters
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
    all_chars = letters + digits + symbols
    
    # Securely pick random characters one by one
    password = ""
    for _ in range(length):
        password += secrets.choice(all_chars)
    return password

# --- FUNCTION 2: POLICY CHECKER ---
def check_policy(password):
    fails = []
    
    # Check all 5 rules
    if len(password) < 8:
        fails.append("Too short (needs 8+ chars)")
    if not any(c.isupper() for c in password):
        fails.append("Missing uppercase letter")
    if not any(c.islower() for c in password):
        fails.append("Missing lowercase letter")
    if not any(c.isdigit() for c in password):
        fails.append("Missing number")
    
    special_chars = set(string.punctuation)
    if not any(c in special_chars for c in password):
        fails.append("Missing special character")
        
    # If the fails list is empty, it passed all rules!
    passed = (len(fails) == 0)
    return passed, fails

# --- TEST IT ALL TOGETHER ---
if __name__ == "__main__":
    print(f"--- SECUREPASS (Security Version: {version_number}) ---\n")
    
    # 1. Ask the user to type a password
    my_test_password = input("Enter a password to test (e.g., 'sameer'): ")
    
    # 2. Check the typed password
    print(f"\nTesting your password: '{my_test_password}'")
    passed, errors = check_policy(my_test_password)
    
    print(f"Passed Policy? {passed}")
    if not passed:
        print(f"Errors: {errors}\n")
    else:
        print("Perfect! No errors.\n")
        
    # 3. Test the Generator to show it still works
    print("Generating a brand new 16-character password for you...")
    new_pw = generate_password(16)
    print(f"Generated Password: {new_pw}")
    
    passed, errors = check_policy(new_pw)
    print(f"Does the generated password pass the policy? {passed}")