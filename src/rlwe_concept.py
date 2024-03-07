import numpy as np


class RingLWECrypto:
    def __init__(self, n, q):
        self.n = n  # Polynomial degree
        self.q = q  # Modulus
        self.secret_key = self._generate_secret_key()

    def _generate_secret_key(self):
        """Generates a more complex secret key for the Ring-LWE encryption."""
        # Example: Using a combination of random polynomials
        key_part1 = np.random.randint(0, self.q, self.n)
        key_part2 = np.random.randint(0, self.q, self.n)
        secret_key = (key_part1 + key_part2) % self.q
        return secret_key

    def _add_noise(self, message):
        """Introduces more complex noise to the message."""
        if message.shape[0] < self.n:
            padding_length = self.n - message.shape[0]
            padded_message = np.pad(message, ((0, padding_length), (0, 0)), 'constant', constant_values=0)
        else:
            padded_message = message
        noise = np.random.randint(-self.q // 150, self.q // 150 + 1, padded_message.shape)
        noisy_message = (padded_message + noise) % self.q
        return noisy_message

    def _polynomial_multiplication(self, a, b):
        """Performs polynomial multiplication under the given modulus."""
        return np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)).real.astype(int) % self.q

    def encrypt(self, message):
        """Encrypts a message using the Ring-LWE scheme with enhanced complexity."""
        a = np.random.randint(0, self.q, self.n)
        encoded_message = self._add_noise(message)
        encrypted_message = self._polynomial_multiplication(a, self.secret_key) + encoded_message
        return a, encrypted_message % self.q

    def decrypt(self, a, encrypted_message):
        """Decrypts an encrypted message using the Ring-LWE scheme."""
        # Decrypt the message
        s_times_a = self._polynomial_multiplication(a, self.secret_key)
        decoded_message = (encrypted_message - s_times_a + self.q) % self.q

        # Correct the decoded message assuming values were initially between 0 and 255
        decoded_message = np.where(decoded_message < 256, decoded_message, decoded_message - self.q)

        return decoded_message

