import os
import unittest
from signal_protocol.keys.pre_keys.base_pre_key import (
    PreKeyPair,
    PreKey,
    generate_pre_key_pair,
    generate_pre_keys,
    serialize_pre_key_pair,
    deserialize_pre_key_pair
)


class TestPreKey(unittest.TestCase):
    def test_pre_key_pair_creation(self):
        """Test creating a pre-key pair with valid keys"""
        # Generate a pre-key pair
        pre_key_pair = generate_pre_key_pair(1)

        # Check that both keys are 32 bytes
        self.assertEqual(len(pre_key_pair.public_key_bytes), 32)
        self.assertEqual(len(pre_key_pair.private_key_bytes), 32)

        # Check that the key ID is correct
        self.assertEqual(pre_key_pair.key_id, 1)

        # Check that we can access the keys
        public_key = pre_key_pair.public_key_bytes
        private_key = pre_key_pair.private_key_bytes
        self.assertIsInstance(public_key, bytes)
        self.assertIsInstance(private_key, bytes)

    def test_pre_key_creation(self):
        """Test creating a pre-key with valid public key"""
        # Generate a pre-key pair to get a valid public key
        pre_key_pair = generate_pre_key_pair(1)
        public_key = pre_key_pair.public_key_bytes

        # Create a pre-key
        pre_key = PreKey(1, public_key)

        # Check that the public key is 32 bytes
        self.assertEqual(len(pre_key.public_key_bytes), 32)
        self.assertEqual(pre_key.public_key_bytes, public_key)
        self.assertEqual(pre_key.key_id, 1)

    def test_invalid_key_sizes(self):
        """Test that invalid key sizes raise ValueError"""
        # Test PreKeyPair with invalid public key size
        with self.assertRaises(ValueError):
            PreKeyPair(1, b"too_short", os.urandom(32))

        # Test PreKeyPair with invalid private key size
        with self.assertRaises(ValueError):
            PreKeyPair(1, os.urandom(32), b"too_short")

        # Test PreKey with invalid public key size
        with self.assertRaises(ValueError):
            PreKey(1, b"too_short")

    def test_generate_multiple_pre_keys(self):
        """Test generating multiple pre-keys"""
        # Generate multiple pre-keys
        pre_keys = generate_pre_keys(10, 5)

        # Check that we have the correct number
        self.assertEqual(len(pre_keys), 5)

        # Check that the key IDs are correct
        for i, pre_key in enumerate(pre_keys):
            self.assertEqual(pre_key.key_id, 10 + i)

    def test_pre_key_serialization(self):
        """Test serializing and deserializing pre-key pairs"""
        # Generate a pre-key pair
        original_pre_key_pair = generate_pre_key_pair(1)

        # Serialize the pre-key pair
        serialized = serialize_pre_key_pair(original_pre_key_pair)

        # Check that the serialized data has the expected keys
        self.assertIn('key_id', serialized)
        self.assertIn('public_key', serialized)
        self.assertIn('private_key', serialized)

        # Check that the keys are hex strings
        self.assertIsInstance(serialized['public_key'], str)
        self.assertIsInstance(serialized['private_key'], str)
        self.assertIsInstance(serialized['key_id'], int)

        # Deserialize the pre-key pair
        deserialized_pre_key_pair = deserialize_pre_key_pair(serialized)

        # Check that the keys match the original
        self.assertEqual(
            original_pre_key_pair.key_id,
            deserialized_pre_key_pair.key_id
        )
        self.assertEqual(
            original_pre_key_pair.public_key_bytes,
            deserialized_pre_key_pair.public_key_bytes
        )
        self.assertEqual(
            original_pre_key_pair.private_key_bytes,
            deserialized_pre_key_pair.private_key_bytes
        )


if __name__ == '__main__':
    unittest.main()
