import json
import os
from typing import Optional, Dict, Any, List
from .identity_key import IdentityKeyPair, generate_identity_key_pair, serialize_identity_key_pair, deserialize_identity_key_pair
from .pre_keys.base_pre_key import (
    PreKeyPair, 
    generate_pre_key_pair,
    serialize_pre_key_pair,
    deserialize_pre_key_pair
)
from .pre_keys.signed_pre_key import SignedPreKey


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


# Convenience functions for common operations
def create_key_store(storage_path: str) -> KeyStore:
    """
    Create a new key store.
    
    Args:
        storage_path: Path to the storage file
        
    Returns:
        KeyStore: The new key store
    """
    return KeyStore(storage_path)

