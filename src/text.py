from rlwe_concept import RingLWECrypto


def text_to_numbers(text, max_length):
    """Convert text to a list of numbers based on Unicode values."""
    return [ord(char) for char in text][:max_length]


def numbers_to_text(numbers):
    """Convert a list of numbers back to text, ensuring numbers are integers."""
    return ''.join(chr(int(number) % 1200) for number in numbers if number != 0)


# Example usage with the RingLWECrypto class
crypto = RingLWECrypto(n=256, q=7681)  # Assuming this class is already defined

# Convert text to numbers
text = "Hello, World!"
max_length = 256  # Ensure this matches the 'n' parameter of your Ring-LWE scheme
message = text_to_numbers(text, max_length)

# Encrypt the message
a, encrypted_message = crypto.encrypt(message)

# Decrypt the message
decrypted_message = crypto.decrypt(a, encrypted_message)

# Convert numbers back to text
decrypted_text = numbers_to_text(decrypted_message)

print("Original Text:", text)
print("Decrypted Text:", decrypted_text)
