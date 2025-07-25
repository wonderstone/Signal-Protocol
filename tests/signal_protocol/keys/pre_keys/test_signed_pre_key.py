import unittest
from signal_protocol.keys.pre_keys.signed_pre_key import (
    SignedPreKeyPair,
    SignedPreKey,
    generate_signed_pre_key_pair,
    sign_signed_pre_key,
    verify_signed_pre_key_signature,
    serialize_signed_pre_key_pair,
    deserialize_signed_pre_key_pair
)
from signal_protocol.keys.identity_key import (
    IdentityKeyPair,
    generate_identity_key_pair,
    xeddsa_sign,
    xeddsa_verify
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


if __name__ == '__main__':
    unittest.main()
