import json
import os
from typing import Optional, Dict, Any, List
from .identity_key import IdentityKeyPair, serialize_identity_key_pair, deserialize_identity_key_pair
from .pre_keys.base_pre_key import (
    PreKeyPair,
    generate_pre_key_pair,
    serialize_pre_key_pair,
    deserialize_pre_key_pair
)
from .pre_keys.signed_pre_key import (
    SignedPreKeyPair,
    SignedPreKey,
    serialize_signed_pre_key_pair,
    deserialize_signed_pre_key_pair
)


class KeyStore:
    """Simple file-based key storage mechanism for Signal Protocol keys"""

    def __init__(self, storage_path: str):
        """
        Initialize the key store.

        Args:
            storage_path: Path to the storage file
        """
        self.storage_path = storage_path
        self._ensure_storage_path()

    def _ensure_storage_path(self):
        """Ensure the storage path exists"""
        directory = os.path.dirname(self.storage_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def save_identity_key_pair(self, key_pair: IdentityKeyPair) -> None:
        """
        Save an identity key pair to storage.

        Args:
            key_pair: The identity key pair to save
        """
        # Serialize the key pair
        serialized = serialize_identity_key_pair(key_pair)

        # Load existing data
        data = self._load_data()

        # Update identity key pair
        data['identity_key_pair'] = serialized

        # Save data
        self._save_data(data)

    def load_identity_key_pair(self) -> Optional[IdentityKeyPair]:
        """
        Load the identity key pair from storage.

        Returns:
            IdentityKeyPair: The loaded identity key pair, or None if not found
        """
        # Load existing data
        data = self._load_data()

        # Check if identity key pair exists
        if 'identity_key_pair' not in data:
            return None

        # Deserialize and return the key pair
        return deserialize_identity_key_pair(data['identity_key_pair'])

    def save_pre_key_pair(self, pre_key_pair: PreKeyPair) -> None:
        """
        Save a pre-key pair to storage.

        Args:
            pre_key_pair: The pre-key pair to save
        """
        # Serialize the pre-key pair
        serialized = serialize_pre_key_pair(pre_key_pair)

        # Load existing data
        data = self._load_data()

        # Initialize pre-keys dict if it doesn't exist
        if 'pre_keys' not in data:
            data['pre_keys'] = {}

        # Update pre-key pair
        data['pre_keys'][str(pre_key_pair.key_id)] = serialized

        # Save data
        self._save_data(data)

    def load_pre_key_pair(self, key_id: int) -> Optional[PreKeyPair]:
        """
        Load a pre-key pair from storage.

        Args:
            key_id: The ID of the pre-key to load

        Returns:
            PreKeyPair: The loaded pre-key pair, or None if not found
        """
        # Load existing data
        data = self._load_data()

        # Check if pre-keys exist
        if 'pre_keys' not in data:
            return None

        # Check if the specific pre-key exists
        key_id_str = str(key_id)
        if key_id_str not in data['pre_keys']:
            return None

        # Deserialize and return the pre-key pair
        return deserialize_pre_key_pair(data['pre_keys'][key_id_str])

    def save_pre_key_pairs(self, pre_key_pairs: List[PreKeyPair]) -> None:
        """
        Save multiple pre-key pairs to storage.

        Args:
            pre_key_pairs: List of pre-key pairs to save
        """
        # Load existing data
        data = self._load_data()

        # Initialize pre-keys dict if it doesn't exist
        if 'pre_keys' not in data:
            data['pre_keys'] = {}

        # Update pre-key pairs
        for pre_key_pair in pre_key_pairs:
            serialized = serialize_pre_key_pair(pre_key_pair)
            data['pre_keys'][str(pre_key_pair.key_id)] = serialized

        # Save data
        self._save_data(data)

    def load_pre_key_pairs(self) -> List[PreKeyPair]:
        """
        Load all pre-key pairs from storage.

        Returns:
            List[PreKeyPair]: List of all pre-key pairs
        """
        # Load existing data
        data = self._load_data()

        # Check if pre-keys exist
        if 'pre_keys' not in data:
            return []

        # Deserialize and return all pre-key pairs
        pre_key_pairs = []
        for serialized in data['pre_keys'].values():
            pre_key_pair = deserialize_pre_key_pair(serialized)
            pre_key_pairs.append(pre_key_pair)

        return pre_key_pairs

    def remove_pre_key_pair(self, key_id: int) -> bool:
        """
        Remove a pre-key pair from storage.

        Args:
            key_id: The ID of the pre-key to remove

        Returns:
            bool: True if the pre-key was removed, False if it didn't exist
        """
        # Load existing data
        data = self._load_data()

        # Check if pre-keys exist
        if 'pre_keys' not in data:
            return False

        # Check if the specific pre-key exists
        key_id_str = str(key_id)
        if key_id_str not in data['pre_keys']:
            return False

        # Remove the pre-key
        del data['pre_keys'][key_id_str]

        # Save data
        self._save_data(data)
        return True

    def save_signed_pre_key_pair(self, signed_pre_key_pair: SignedPreKeyPair) -> None:
        """
        Save a signed pre-key pair to storage.

        Args:
            signed_pre_key_pair: The signed pre-key pair to save
        """
        # Serialize the signed pre-key pair
        serialized = serialize_signed_pre_key_pair(signed_pre_key_pair)

        # Load existing data
        data = self._load_data()

        # Initialize signed pre-keys dict if it doesn't exist
        if 'signed_pre_keys' not in data:
            data['signed_pre_keys'] = {}

        # Update signed pre-key pair
        data['signed_pre_keys'][str(signed_pre_key_pair.key_id)] = serialized

        # Save data
        self._save_data(data)

    def load_signed_pre_key_pair(self, key_id: int) -> Optional[SignedPreKeyPair]:
        """
        Load a signed pre-key pair from storage.

        Args:
            key_id: The ID of the signed pre-key to load

        Returns:
            SignedPreKeyPair: The loaded signed pre-key pair, or None if not found
        """
        # Load existing data
        data = self._load_data()

        # Check if signed pre-keys exist
        if 'signed_pre_keys' not in data:
            return None

        # Check if the specific signed pre-key exists
        key_id_str = str(key_id)
        if key_id_str not in data['signed_pre_keys']:
            return None

        # Deserialize and return the signed pre-key pair
        return deserialize_signed_pre_key_pair(data['signed_pre_keys'][key_id_str])

    def load_signed_pre_key_pairs(self) -> List[SignedPreKeyPair]:
        """
        Load all signed pre-key pairs from storage.

        Returns:
            List[SignedPreKeyPair]: List of all signed pre-key pairs
        """
        # Load existing data
        data = self._load_data()

        # Check if signed pre-keys exist
        if 'signed_pre_keys' not in data:
            return []

        # Deserialize and return all signed pre-key pairs
        signed_pre_key_pairs = []
        for serialized in data['signed_pre_keys'].values():
            signed_pre_key_pair = deserialize_signed_pre_key_pair(serialized)
            signed_pre_key_pairs.append(signed_pre_key_pair)

        return signed_pre_key_pairs

    def remove_signed_pre_key_pair(self, key_id: int) -> bool:
        """
        Remove a signed pre-key pair from storage.

        Args:
            key_id: The ID of the signed pre-key to remove

        Returns:
            bool: True if the signed pre-key was removed, False if it didn't exist
        """
        # Load existing data
        data = self._load_data()

        # Check if signed pre-keys exist
        if 'signed_pre_keys' not in data:
            return False

        # Check if the specific signed pre-key exists
        key_id_str = str(key_id)
        if key_id_str not in data['signed_pre_keys']:
            return False

        # Remove the signed pre-key
        del data['signed_pre_keys'][key_id_str]

        # Save data
        self._save_data(data)
        return True

    def _load_data(self) -> Dict[str, Any]:
        """
        Load data from storage.

        Returns:
            dict: The loaded data
        """
        if not os.path.exists(self.storage_path):
            return {}

        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_data(self, data: Dict[str, Any]) -> None:
        """
        Save data to storage.

        Args:
            data: The data to save
        """
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)


def create_key_store(storage_path: str) -> KeyStore:
    """
    Create a new key store.

    Args:
        storage_path: Path to the storage file

    Returns:
        KeyStore: The new key store
    """
    return KeyStore(storage_path)


if __name__ == '__main__':
    # Test key store functionality
    import tempfile
    import os
    from .identity_key import generate_identity_key_pair
    from .pre_keys.base_pre_key import generate_pre_keys
    from .pre_keys.signed_pre_key import generate_signed_pre_key_pair

    print("🗄️ Testing KeyStore functionality...")

    # Create a temporary storage file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
        storage_path = tmp_file.name

    try:
        # Create a key store
        key_store = create_key_store(storage_path)
        print(f"✅ Created key store at: {storage_path}")

        # Test 1: Identity Key Pair operations
        print("\n🔑 Testing Identity Key Pair operations...")

        # Generate and save identity key pair
        identity_key_pair = generate_identity_key_pair()
        key_store.save_identity_key_pair(identity_key_pair)
        print("✅ Saved identity key pair")

        # Load identity key pair
        loaded_identity_key_pair = key_store.load_identity_key_pair()
        assert loaded_identity_key_pair is not None, "Should load identity key pair"
        assert loaded_identity_key_pair.public_key_bytes == identity_key_pair.public_key_bytes
        assert loaded_identity_key_pair.private_key_bytes == identity_key_pair.private_key_bytes
        print("✅ Loaded and verified identity key pair")

        # Test 2: Pre-Key Pair operations
        print("\n🔐 Testing Pre-Key Pair operations...")

        # Generate and save multiple pre-key pairs
        pre_key_pairs = generate_pre_keys(1, 5)
        key_store.save_pre_key_pairs(pre_key_pairs)
        print(f"✅ Saved {len(pre_key_pairs)} pre-key pairs")

        # Load all pre-key pairs
        loaded_pre_key_pairs = key_store.load_pre_key_pairs()
        assert len(loaded_pre_key_pairs) == len(
            pre_key_pairs), "Should load all pre-key pairs"
        print(f"✅ Loaded {len(loaded_pre_key_pairs)} pre-key pairs")

        # Load specific pre-key pair
        specific_pre_key = key_store.load_pre_key_pair(3)
        assert specific_pre_key is not None, "Should load specific pre-key pair"
        assert specific_pre_key.key_id == 3, "Should have correct key ID"
        print("✅ Loaded specific pre-key pair")

        # Remove a pre-key pair
        removed = key_store.remove_pre_key_pair(2)
        assert removed, "Should successfully remove pre-key pair"

        # Verify removal
        removed_key = key_store.load_pre_key_pair(2)
        assert removed_key is None, "Removed pre-key should not be found"
        print("✅ Removed pre-key pair successfully")

        # Test 3: Signed Pre-Key Pair operations
        print("\n📝 Testing Signed Pre-Key Pair operations...")

        # Generate and save signed pre-key pair
        signed_pre_key_pair = generate_signed_pre_key_pair(
            identity_key_pair, 100)
        key_store.save_signed_pre_key_pair(signed_pre_key_pair)
        print("✅ Saved signed pre-key pair")

        # Load signed pre-key pair
        loaded_signed_pre_key = key_store.load_signed_pre_key_pair(100)
        assert loaded_signed_pre_key is not None, "Should load signed pre-key pair"
        assert loaded_signed_pre_key.key_id == 100, "Should have correct key ID"
        assert loaded_signed_pre_key.timestamp == signed_pre_key_pair.timestamp
        print("✅ Loaded and verified signed pre-key pair")

        # Load all signed pre-key pairs
        all_signed_pre_keys = key_store.load_signed_pre_key_pairs()
        assert len(
            all_signed_pre_keys) == 1, "Should have one signed pre-key pair"
        print("✅ Loaded all signed pre-key pairs")

        # Remove signed pre-key pair
        removed_signed = key_store.remove_signed_pre_key_pair(100)
        assert removed_signed, "Should successfully remove signed pre-key pair"

        # Verify removal
        removed_signed_key = key_store.load_signed_pre_key_pair(100)
        assert removed_signed_key is None, "Removed signed pre-key should not be found"
        print("✅ Removed signed pre-key pair successfully")

        # Test 4: Persistence verification
        print("\n💾 Testing persistence...")

        # Create a new key store instance with the same storage path
        key_store2 = KeyStore(storage_path)

        # Verify identity key pair persists
        persisted_identity_key = key_store2.load_identity_key_pair()
        assert persisted_identity_key is not None, "Identity key should persist"
        assert persisted_identity_key.public_key_bytes == identity_key_pair.public_key_bytes
        print("✅ Identity key pair persisted correctly")

        # Verify remaining pre-key pairs persist (should be 4 after removal)
        persisted_pre_keys = key_store2.load_pre_key_pairs()
        assert len(
            persisted_pre_keys) == 4, "Should have 4 pre-key pairs after removal"
        print("✅ Pre-key pairs persisted correctly")

        # Test 5: Edge cases
        print("\n🔍 Testing edge cases...")

        # Load non-existent pre-key
        non_existent_pre_key = key_store.load_pre_key_pair(999)
        assert non_existent_pre_key is None, "Non-existent pre-key should return None"

        # Remove non-existent pre-key
        remove_non_existent = key_store.remove_pre_key_pair(999)
        assert not remove_non_existent, "Removing non-existent pre-key should return False"

        # Load non-existent signed pre-key
        non_existent_signed = key_store.load_signed_pre_key_pair(999)
        assert non_existent_signed is None, "Non-existent signed pre-key should return None"

        # Remove non-existent signed pre-key
        remove_non_existent_signed = key_store.remove_signed_pre_key_pair(999)
        assert not remove_non_existent_signed, "Removing non-existent signed pre-key should return False"
        print("✅ Edge cases handled correctly")

        # Test 6: Storage file verification
        print("\n📁 Testing storage file structure...")

        # Verify the storage file exists and has correct structure
        assert os.path.exists(storage_path), "Storage file should exist"

        with open(storage_path, 'r') as f:
            stored_data = json.load(f)

        assert 'identity_key_pair' in stored_data, "Should have identity_key_pair"
        assert 'pre_keys' in stored_data, "Should have pre_keys"
        assert 'signed_pre_keys' in stored_data, "Should have signed_pre_keys (even if empty)"
        print("✅ Storage file structure is correct")

        print("\n🎉 All KeyStore tests passed!")
        print("=" * 60)
        print("KeyStore Features Tested:")
        print("  ✓ Identity key pair save/load operations")
        print("  ✓ Pre-key pair batch and individual operations")
        print("  ✓ Pre-key pair removal and verification")
        print("  ✓ Signed pre-key pair operations")
        print("  ✓ Data persistence across instances")
        print("  ✓ Edge case handling")
        print("  ✓ Storage file structure validation")
        print("=" * 60)

    finally:
        # Clean up temporary file
        if os.path.exists(storage_path):
            os.unlink(storage_path)
            print(f"🧹 Cleaned up temporary storage file")
