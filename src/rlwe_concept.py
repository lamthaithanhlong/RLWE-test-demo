import numpy as np


class RingLWECrypto:
    def __init__(self, n, q, sigma):
        self.n = n  # Polynomial degree
        self.q = q  # Modulus
        self.sigma = sigma # Gaussian rate
        self.secret_key = self._generate_secret_key()

    def _generate_secret_key(self):
        """Generates a more complex secret key for the Ring-LWE encryption."""
        # Example: Using a combination of random polynomials
        key_part1 = np.random.randint(0, self.q, self.n)
        key_part2 = np.random.randint(0, self.q, self.n)
        secret_key = (key_part1 + key_part2) % self.q
        return secret_key

    def _add_noise(self, message):
        """Adds Gaussian noise to a message.

        Args:
            message (np.array): The original message as a numpy array.
            sigma (float): The standard deviation of the Gaussian noise.

        Returns:
            np.array: The message with Gaussian noise added.
        """
        noise = np.random.normal(0, self.sigma, size=message.shape)
        noisy_message = (message + noise) % self.q  # Assume q is the modulus for your Ring-LWE scheme
        return noisy_message

    def _polynomial_multiplication(self, a, b):
        """Performs polynomial multiplication under the given modulus."""
        return np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)).real.astype(int) % self.q

    def encrypt(self, message):
        """
        Encrypts a message using the Ring-LWE scheme, incorporating enhanced complexity
        through polynomial operations and noise addition.

        Parameters:
        - message: The plaintext message to be encrypted, represented as a polynomial.

        Returns:
        - a tuple of (a, encrypted_message), where 'a' is a randomly chosen polynomial
          and 'encrypted_message' is the resulting encrypted message after applying
          the Ring-LWE encryption process.
        """
        # Randomly choose a polynomial 'a' from a uniform distribution over Z_q
        a = np.random.randint(0, self.q, self.n)

        # Encode the message with noise for security enhancement
        encoded_message = self._add_noise(message)

        # Perform polynomial multiplication between 'a' and the secret key,
        # then add the encoded message
        encrypted_message = self._polynomial_multiplication(a, self.secret_key) + encoded_message

        # Ensure the encrypted message is within the field by taking modulo q
        encrypted_message = encrypted_message % self.q

        return a, encrypted_message

    def decrypt(self, a, encrypted_message):
        """Decrypts an encrypted message using the Ring-LWE scheme."""
        # Decrypt the message
        s_times_a = self._polynomial_multiplication(a, self.secret_key)
        decoded_message = (encrypted_message - s_times_a + self.q) % self.q

        # Correct the decoded message assuming values were initially between 0 and 255
        decoded_message = np.where(decoded_message < self.n, decoded_message, decoded_message - self.q)

        return decoded_message

