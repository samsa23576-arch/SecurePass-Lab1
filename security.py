import bcrypt
import hashlib    
import requests   

# --- STEP 1: BCRYPT HASHER ---
def hash_password(plain_password):
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

# --- STEP 2 & 3: THE FREE API CHECK ---
def check_hibp(password):
    # STEP 2: Prep the password (SHA-1 & Splitting for k-anonymity)
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    # STEP 3: The API Call (Send ONLY the first 5 characters)
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    # Check if our 'suffix' is hiding inside the API's response text
    if suffix in response.text:
        return True  # Found! The password is breached.
    return False     # Not found! The password is safe.

# --- TEST IT ALL TOGETHER ---
if __name__ == "__main__":
    print("--- SECUREPASS: PART B TESTING ---")
    
    # We will test a famously hacked password
    test_pw = "password123"
    print(f"\nTesting password: '{test_pw}'")
    
    # 1. Test the API
    is_breached = check_hibp(test_pw)
    if is_breached:
         print("[!] HIBP Check: FAILED (This password has been breached!)")
    else:
         print("[+] HIBP Check: PASSED (Safe)")

    # 2. Test the Hasher
    secure_hash = hash_password(test_pw)
    print(f"[+] Database Hash generated: {secure_hash}")