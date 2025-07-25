import unittest
from signal_protocol.keys.pre_keys.base_pre_key import generate_pre_key_pair
from signal_protocol.keys.pre_keys.signed_pre_key import (
    generate_signed_pre_key_pair,
    sign_signed_pre_key
)
from signal_protocol.keys.pre_keys.pre_key_bundle import (
    PreKeyBundle,
    create_pre_key_bundle
)
from signal_protocol.keys.identity_key import generate_identity_key_pair


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


if __name__ == '__main__':
    unittest.main()
