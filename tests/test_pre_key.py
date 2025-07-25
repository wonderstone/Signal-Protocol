import os
import tempfile
import unittest
from signal_protocol.keys.pre_keys.base_pre_key import (
    PreKeyPair,
    PreKey,
    generate_pre_key_pair,
    generate_pre_keys,
    serialize_pre_key_pair,
    deserialize_pre_key_pair
)
from signal_protocol.keys.pre_keys.signed_pre_key import (
    SignedPreKeyPair,
    SignedPreKey,
    generate_signed_pre_key_pair,
    sign_signed_pre_key,
    verify_signed_pre_key_signature,
    serialize_signed_pre_key_pair,
    deserialize_signed_pre_key_pair
)
from signal_protocol.keys.pre_keys.pre_key_bundle import (
    PreKeyBundle,
    create_pre_key_bundle
)
from signal_protocol.keys.identity_key import (
    IdentityKeyPair,
    generate_identity_key_pair,
    xeddsa_sign,
    xeddsa_verify
)
from signal_protocol.keys.key_store import (
    KeyStore,
    create_key_store
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


class TestSignedPreKey(unittest.TestCase):
    def test_signed_pre_key_pair_creation(self):
        """Test creating a signed pre-key pair"""
        # Generate an identity key pair
        identity_key_pair = generate_identity_key_pair()

        # Generate a signed pre-key pair
        signed_pre_key_pair = generate_signed_pre_key_pair(
            identity_key_pair, 1)

        # Check that both keys are 32 bytes
        self.assertEqual(len(signed_pre_key_pair.public_key_bytes), 32)
        self.assertEqual(len(signed_pre_key_pair.private_key_bytes), 32)

        # Check that the key ID is correct
        self.assertEqual(signed_pre_key_pair.key_id, 1)

        # Check that we have a timestamp
        self.assertIsInstance(signed_pre_key_pair.timestamp, int)

    def test_sign_and_verify_signed_pre_key(self):
        """Test signing and verifying a signed pre-key using XEdDSA"""
        # Generate an identity key pair
        identity_key_pair = generate_identity_key_pair()

        # Generate a signed pre-key pair
        signed_pre_key_pair = generate_signed_pre_key_pair(
            identity_key_pair, 1)

        # Sign the signed pre-key using XEdDSA
        signature = sign_signed_pre_key(identity_key_pair, signed_pre_key_pair)

        # Verify the signature using XEdDSA
        is_valid = verify_signed_pre_key_signature(
            identity_key_pair,
            signed_pre_key_pair.public_key_bytes,
            signature
        )

        # Check that the signature is valid
        self.assertTrue(is_valid)

        # Test that signature verification fails with wrong public key
        wrong_identity = generate_identity_key_pair()
        is_invalid = verify_signed_pre_key_signature(
            wrong_identity,
            signed_pre_key_pair.public_key_bytes,
            signature
        )
        self.assertFalse(is_invalid)

        # Test that signature verification fails with wrong message
        wrong_pre_key = generate_signed_pre_key_pair(identity_key_pair, 2)
        is_invalid = verify_signed_pre_key_signature(
            identity_key_pair,
            wrong_pre_key.public_key_bytes,
            signature
        )
        self.assertFalse(is_invalid)

    def test_xeddsa_direct(self):
        """Test XEdDSA signing and verification directly"""
        # Generate an identity key pair
        identity_key_pair = generate_identity_key_pair()

        # Test message
        message = b"Hello, XEdDSA!"

        # Sign the message
        signature = xeddsa_sign(identity_key_pair, message)

        # Verify the signature
        is_valid = xeddsa_verify(
            identity_key_pair.ed25519_verify_key_bytes,
            message,
            signature
        )

        # Check that the signature is valid
        self.assertTrue(is_valid)

        # Test with wrong message
        wrong_message = b"Wrong message"
        is_invalid = xeddsa_verify(
            identity_key_pair.ed25519_verify_key_bytes,
            wrong_message,
            signature
        )
        self.assertFalse(is_invalid)

    def test_signed_pre_key_serialization(self):
        """Test serializing and deserializing signed pre-key pairs"""
        # Generate an identity key pair
        identity_key_pair = generate_identity_key_pair()

        # Generate a signed pre-key pair
        original_signed_pre_key_pair = generate_signed_pre_key_pair(
            identity_key_pair, 1)

        # Serialize the signed pre-key pair
        serialized = serialize_signed_pre_key_pair(
            original_signed_pre_key_pair)

        # Check that the serialized data has the expected keys
        self.assertIn('key_id', serialized)
        self.assertIn('public_key', serialized)
        self.assertIn('private_key', serialized)
        self.assertIn('timestamp', serialized)

        # Check that the keys are hex strings
        self.assertIsInstance(serialized['public_key'], str)
        self.assertIsInstance(serialized['private_key'], str)
        self.assertIsInstance(serialized['key_id'], int)
        self.assertIsInstance(serialized['timestamp'], int)

        # Deserialize the signed pre-key pair
        deserialized_signed_pre_key_pair = deserialize_signed_pre_key_pair(
            serialized)

        # Check that the keys match the original
        self.assertEqual(
            original_signed_pre_key_pair.key_id,
            deserialized_signed_pre_key_pair.key_id
        )
        self.assertEqual(
            original_signed_pre_key_pair.public_key_bytes,
            deserialized_signed_pre_key_pair.public_key_bytes
        )
        self.assertEqual(
            original_signed_pre_key_pair.private_key_bytes,
            deserialized_signed_pre_key_pair.private_key_bytes
        )
        self.assertEqual(
            original_signed_pre_key_pair.timestamp,
            deserialized_signed_pre_key_pair.timestamp
        )


class TestPreKeyBundle(unittest.TestCase):
    def test_pre_key_bundle_creation(self):
        """Test creating a pre-key bundle"""
        # Generate keys
        identity_key_pair = generate_identity_key_pair()
        pre_key_pair = generate_pre_key_pair(1)
        signed_pre_key_pair = generate_signed_pre_key_pair(
            identity_key_pair, 2)
        signature = sign_signed_pre_key(identity_key_pair, signed_pre_key_pair)

        # Create a pre-key bundle
        pre_key_bundle = create_pre_key_bundle(
            registration_id=123,
            device_id=1,
            pre_key_pair=pre_key_pair,
            signed_pre_key_pair=signed_pre_key_pair,
            signed_pre_key_signature=signature,
            identity_key_pair=identity_key_pair
        )

        # Check the bundle properties
        self.assertEqual(pre_key_bundle.registration_id, 123)
        self.assertEqual(pre_key_bundle.device_id, 1)
        self.assertIsNotNone(pre_key_bundle.pre_key)
        self.assertIsNotNone(pre_key_bundle.pre_key_id)
        self.assertIsNotNone(pre_key_bundle.signed_pre_key)
        self.assertIsNotNone(pre_key_bundle.signed_pre_key_id)
        self.assertIsNotNone(pre_key_bundle.signed_pre_key_signature)
        self.assertIsNotNone(pre_key_bundle.identity_key)

        # Check that the bundle has a pre-key
        self.assertTrue(pre_key_bundle.has_pre_key())

    def test_pre_key_bundle_without_pre_key(self):
        """Test creating a pre-key bundle without a pre-key"""
        # Generate keys
        identity_key_pair = generate_identity_key_pair()
        signed_pre_key_pair = generate_signed_pre_key_pair(
            identity_key_pair, 2)
        signature = sign_signed_pre_key(identity_key_pair, signed_pre_key_pair)

        # Create a pre-key bundle without a pre-key
        pre_key_bundle = create_pre_key_bundle(
            registration_id=123,
            device_id=1,
            pre_key_pair=None,
            signed_pre_key_pair=signed_pre_key_pair,
            signed_pre_key_signature=signature,
            identity_key_pair=identity_key_pair
        )

        # Check that the bundle doesn't have a pre-key
        self.assertFalse(pre_key_bundle.has_pre_key())


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
