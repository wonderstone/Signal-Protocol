import os
import tempfile
import unittest
from signal_protocol.keys import (
    IdentityKeyPair,
    IdentityKey,
    generate_identity_key_pair,
    serialize_identity_key_pair,
    deserialize_identity_key_pair,
    KeyStore,
    create_key_store
)


class TestIdentityKey(unittest.TestCase):
    def test_identity_key_pair_creation(self):
        """Test creating an identity key pair with valid keys"""
        # Generate a key pair
        key_pair = generate_identity_key_pair()
        
        # Check that both keys are 32 bytes
        self.assertEqual(len(key_pair.public_key_bytes), 32)
        self.assertEqual(len(key_pair.private_key_bytes), 32)
        
        # Check that we can access the keys
        public_key = key_pair.public_key_bytes
        private_key = key_pair.private_key_bytes
        self.assertIsInstance(public_key, bytes)
        self.assertIsInstance(private_key, bytes)
    
    def test_identity_key_creation(self):
        """Test creating an identity key with valid public key"""
        # Generate a key pair to get a valid public key
        key_pair = generate_identity_key_pair()
        public_key = key_pair.public_key_bytes
        
        # Create an identity key
        identity_key = IdentityKey(public_key)
        
        # Check that the public key is 32 bytes
        self.assertEqual(len(identity_key.public_key_bytes), 32)
        self.assertEqual(identity_key.public_key_bytes, public_key)
    
    def test_invalid_key_sizes(self):
        """Test that invalid key sizes raise ValueError"""
        # Test IdentityKeyPair with invalid public key size
        with self.assertRaises(ValueError):
            IdentityKeyPair(b"too_short", os.urandom(32))
        
        # Test IdentityKeyPair with invalid private key size
        with self.assertRaises(ValueError):
            IdentityKeyPair(os.urandom(32), b"too_short")
        
        # Test IdentityKey with invalid public key size
        with self.assertRaises(ValueError):
            IdentityKey(b"too_short")
    
    def test_key_serialization(self):
        """Test serializing and deserializing identity key pairs"""
        # Generate a key pair
        original_key_pair = generate_identity_key_pair()
        
        # Serialize the key pair
        serialized = serialize_identity_key_pair(original_key_pair)
        
        # Check that the serialized data has the expected keys
        self.assertIn('public_key', serialized)
        self.assertIn('private_key', serialized)
        
        # Check that the keys are hex strings
        self.assertIsInstance(serialized['public_key'], str)
        self.assertIsInstance(serialized['private_key'], str)
        
        # Deserialize the key pair
        deserialized_key_pair = deserialize_identity_key_pair(serialized)
        
        # Check that the keys match the original
        self.assertEqual(
            original_key_pair.public_key_bytes,
            deserialized_key_pair.public_key_bytes
        )
        self.assertEqual(
            original_key_pair.private_key_bytes,
            deserialized_key_pair.private_key_bytes
        )


class TestKeyStore(unittest.TestCase):
    def setUp(self):
        """Set up a temporary file for testing"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.storage_path = self.temp_file.name
    
    def tearDown(self):
        """Clean up the temporary file"""
        if os.path.exists(self.storage_path):
            os.unlink(self.storage_path)
    
    def test_key_store_creation(self):
        """Test creating a key store"""
        key_store = create_key_store(self.storage_path)
        self.assertIsInstance(key_store, KeyStore)
        self.assertEqual(key_store.storage_path, self.storage_path)
    
    def test_save_and_load_identity_key_pair(self):
        """Test saving and loading an identity key pair"""
        # Create a key store
        key_store = create_key_store(self.storage_path)
        
        # Generate and save a key pair
        key_pair = generate_identity_key_pair()
        key_store.save_identity_key_pair(key_pair)
        
        # Load the key pair
        loaded_key_pair = key_store.load_identity_key_pair()
        
        # Check that the keys match
        self.assertIsNotNone(loaded_key_pair)
        self.assertEqual(
            key_pair.public_key_bytes,
            loaded_key_pair.public_key_bytes
        )
        self.assertEqual(
            key_pair.private_key_bytes,
            loaded_key_pair.private_key_bytes
        )
    
    def test_load_nonexistent_key_pair(self):
        """Test loading a key pair when none exists"""
        # Create a key store
        key_store = create_key_store(self.storage_path)
        
        # Try to load a key pair when none exists
        loaded_key_pair = key_store.load_identity_key_pair()
        
        # Check that None is returned
        self.assertIsNone(loaded_key_pair)


if __name__ == '__main__':
    unittest.main()