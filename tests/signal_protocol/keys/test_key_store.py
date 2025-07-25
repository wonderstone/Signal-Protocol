import os
import tempfile
import unittest
from signal_protocol.keys.pre_keys.base_pre_key import (
    generate_pre_key_pair,
    generate_pre_keys
)
from signal_protocol.keys.pre_keys.signed_pre_key import generate_signed_pre_key_pair
from signal_protocol.keys.identity_key import generate_identity_key_pair
from signal_protocol.keys.key_store import (
    KeyStore,
    create_key_store
)


class TestPreKeyStorage(unittest.TestCase):
    def setUp(self):
        """Set up a temporary file for testing"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.storage_path = self.temp_file.name
        self.key_store = create_key_store(self.storage_path)

    def tearDown(self):
        """Clean up the temporary file"""
        if os.path.exists(self.storage_path):
            os.unlink(self.storage_path)

    def test_save_and_load_pre_key_pair(self):
        """Test saving and loading a pre-key pair"""
        # Generate and save a pre-key pair
        pre_key_pair = generate_pre_key_pair(1)
        self.key_store.save_pre_key_pair(pre_key_pair)

        # Load the pre-key pair
        loaded_pre_key_pair = self.key_store.load_pre_key_pair(1)

        # Check that the keys match
        self.assertIsNotNone(loaded_pre_key_pair)
        self.assertEqual(
            pre_key_pair.key_id,
            loaded_pre_key_pair.key_id
        )
        self.assertEqual(
            pre_key_pair.public_key_bytes,
            loaded_pre_key_pair.public_key_bytes
        )
        self.assertEqual(
            pre_key_pair.private_key_bytes,
            loaded_pre_key_pair.private_key_bytes
        )

    def test_save_and_load_multiple_pre_key_pairs(self):
        """Test saving and loading multiple pre-key pairs"""
        # Generate and save multiple pre-key pairs
        pre_key_pairs = generate_pre_keys(10, 5)
        self.key_store.save_pre_key_pairs(pre_key_pairs)

        # Load all pre-key pairs
        loaded_pre_key_pairs = self.key_store.load_pre_key_pairs()

        # Check that we have the correct number
        self.assertEqual(len(loaded_pre_key_pairs), 5)

        # Check that the keys match
        for original, loaded in zip(pre_key_pairs, loaded_pre_key_pairs):
            self.assertEqual(
                original.key_id,
                loaded.key_id
            )
            self.assertEqual(
                original.public_key_bytes,
                loaded.public_key_bytes
            )
            self.assertEqual(
                original.private_key_bytes,
                loaded.private_key_bytes
            )

    def test_remove_pre_key_pair(self):
        """Test removing a pre-key pair"""
        # Generate and save a pre-key pair
        pre_key_pair = generate_pre_key_pair(1)
        self.key_store.save_pre_key_pair(pre_key_pair)

        # Remove the pre-key pair
        result = self.key_store.remove_pre_key_pair(1)

        # Check that the removal was successful
        self.assertTrue(result)

        # Try to load the removed pre-key pair
        loaded_pre_key_pair = self.key_store.load_pre_key_pair(1)

        # Check that the pre-key pair was removed
        self.assertIsNone(loaded_pre_key_pair)

    def test_save_and_load_signed_pre_key_pair(self):
        """Test saving and loading a signed pre-key pair"""
        # Generate keys
        identity_key_pair = generate_identity_key_pair()

        # Generate and save a signed pre-key pair
        signed_pre_key_pair = generate_signed_pre_key_pair(
            identity_key_pair, 1)
        self.key_store.save_signed_pre_key_pair(signed_pre_key_pair)

        # Load the signed pre-key pair
        loaded_signed_pre_key_pair = self.key_store.load_signed_pre_key_pair(1)

        # Check that the keys match
        self.assertIsNotNone(loaded_signed_pre_key_pair)
        self.assertEqual(
            signed_pre_key_pair.key_id,
            loaded_signed_pre_key_pair.key_id
        )
        self.assertEqual(
            signed_pre_key_pair.public_key_bytes,
            loaded_signed_pre_key_pair.public_key_bytes
        )
        self.assertEqual(
            signed_pre_key_pair.private_key_bytes,
            loaded_signed_pre_key_pair.private_key_bytes
        )
        self.assertEqual(
            signed_pre_key_pair.timestamp,
            loaded_signed_pre_key_pair.timestamp
        )


if __name__ == '__main__':
    unittest.main()
