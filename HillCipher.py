import sys
import numpy as np

# Function to read only the lowercase alphabetic letters from the input file
def read_plaintext(input_file):
  
  # Opens the plaintext file
    with open(input_file, 'r') as plaintxt:
      
      # replace new line w space, removes non-alphabet characters, coverts to lowercase
        data = plaintxt.read().replace('\n', '')
        data = ''.join(e for e in data if e.isalpha()) 
        data = data.lower()
      
    return data

# Pads plaintext with 'x'
def padPlaintext(plaintext, n):
    pad_len = (n - len(plaintext) % n) % n
    return plaintext + 'x' * pad_len
  
# Hill encryption algorithm
def hill_cipher_encrypt(plaintext, key_matrix):

    # Get size of key
    n = key_matrix.shape[0]

    # Create ints to represent plaintext & append values to list
    plaintext_ints = []
    for char in plaintext:
        if char.isalpha():
            plaintext_ints.append(ord(char) - ord('a'))

    # Convert the list of integers to a matrix
    plaintext_matrix = np.array(plaintext_ints).reshape(-1, n).T

    # Multiply plaintext matrix by the key matrix
    ciphertext_matrix = np.dot(key_matrix, plaintext_matrix) % 26

    # Convert ciphertext matrix to a string
    ciphertext = ''
    for row in ciphertext_matrix.T:
        for char_int in row:
            ciphertext += chr(char_int + ord('a'))

    return ciphertext


# Function to output ciphertext 
def outputCiphertext(ciphertext):
    print("\nCiphertext:")
  # print 80 char per line
    for i in range(0, len(ciphertext), 80):
        print(ciphertext[i:i+80])
      
# Main- tells user how to exec
if len(sys.argv) != 3:
    print("\nTo execute, input your key file and plaintext file.\n")
    print("like this -> Python pa01.py [keyfile.txt] [plaintext.txt]\n")
    exit(1)

# Reads key file
with open(sys.argv[1], 'r') as file: #takes first arg as key
    n = int(file.readline())
    key_matrix = []
    for line in file:
        row = line.split()
        row_int = [int(i) % 26 for i in row]
        key_matrix.append(row_int)
    key_matrix = np.array(key_matrix)

# Reads input file
plaintext = read_plaintext(sys.argv[2])

# Encrypts plaintext using Hill cipher and key matrix
ciphertext = hill_cipher_encrypt(plaintext, key_matrix)

# Output key matrix
print("\nKey matrix:")
for row in key_matrix:
    row_str = " ".join(str(x) for x in row)
    print(row_str)

# Outputs plaintext and ciphertext
print("\nPlaintext:")
print(plaintext)
outputCiphertext(ciphertext)
