import os
import sys
import unittest

# Add the project root to the path so we can import signal_protocol
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from signal_protocol.keys import (
    generate_identity_key_pair
)
from signal_protocol.sessions import (
    SessionRecord
)
from signal_protocol.messages import (
    encrypt_message,
    decrypt_message,
    SignalMessage
)
from signal_protocol.keys.identity_key import IdentityKey
from signal_protocol.sessions.key_derivation import derive_root_key_and_chain_key


class TestMessageEncryptionDecryption(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Generate identity keys for both parties
        self.alice_identity_key_pair = generate_identity_key_pair()
        self.bob_identity_key_pair = generate_identity_key_pair()
        
        # Simulate a shared secret
        self.shared_secret = os.urandom(32)
        
        # Create a common root key for both parties
        self.initial_root_key = os.urandom(32)
        
        # Derive chain keys for both parties from the same root key and shared secret
        alice_root_key, alice_chain_key = derive_root_key_and_chain_key(self.shared_secret, self.initial_root_key)
        bob_root_key, bob_chain_key = derive_root_key_and_chain_key(self.shared_secret, self.initial_root_key)
        
        # Create session records with active chains
        self.alice_session = SessionRecord(
            session_id="alice-to-bob-session-1",
            remote_identity_key=IdentityKey(self.bob_identity_key_pair.public_key_bytes),
            local_identity_key=IdentityKey(self.alice_identity_key_pair.public_key_bytes),
            root_key=alice_root_key,
            chain_key_send=alice_chain_key,  # Active sending chain
            chain_key_receive=bob_chain_key  # Bob's chain key for receiving
        )
        
        self.bob_session = SessionRecord(
            session_id="bob-to-alice-session-1",
            remote_identity_key=IdentityKey(self.alice_identity_key_pair.public_key_bytes),
            local_identity_key=IdentityKey(self.bob_identity_key_pair.public_key_bytes),
            root_key=bob_root_key,
            chain_key_send=bob_chain_key,  # Active sending chain
            chain_key_receive=alice_chain_key  # Alice's chain key for receiving
        )
    
    def test_message_encryption_decryption(self):
        """Test that messages can be encrypted and decrypted correctly"""
        # Message to encrypt
        plaintext = b"Hello Bob, this is a secret message from Alice!"
        
        # Alice encrypts the message
        encrypted_message = encrypt_message(plaintext, self.alice_session, self.alice_identity_key_pair)
        
        # Bob decrypts the message
        decrypted_plaintext = decrypt_message(encrypted_message, self.bob_session, self.bob_identity_key_pair)
        
        # Verify that the decrypted message matches the original
        self.assertEqual(plaintext, decrypted_plaintext)
    
    def test_message_encryption_with_empty_plaintext(self):
        """Test encryption and decryption with empty plaintext"""
        # Message to encrypt
        plaintext = b""
        
        # Alice encrypts the message
        encrypted_message = encrypt_message(plaintext, self.alice_session, self.alice_identity_key_pair)
        
        # Bob decrypts the message
        decrypted_plaintext = decrypt_message(encrypted_message, self.bob_session, self.bob_identity_key_pair)
        
        # Verify that the decrypted message matches the original
        self.assertEqual(plaintext, decrypted_plaintext)
    
    def test_message_encryption_with_long_plaintext(self):
        """Test encryption and decryption with long plaintext"""
        # Message to encrypt
        plaintext = b"A" * 1000  # 1000 bytes of 'A'
        
        # Alice encrypts the message
        encrypted_message = encrypt_message(plaintext, self.alice_session, self.alice_identity_key_pair)
        
        # Bob decrypts the message
        decrypted_plaintext = decrypt_message(encrypted_message, self.bob_session, self.bob_identity_key_pair)
        
        # Verify that the decrypted message matches the original
        self.assertEqual(plaintext, decrypted_plaintext)
    
    def test_signal_message_serialization(self):
        """Test that SignalMessage can be serialized and deserialized"""
        # Create a SignalMessage
        message = SignalMessage(
            message_version=3,
            ciphertext=b"test_ciphertext",
            sender_ratchet_key=self.alice_identity_key_pair.public_key_bytes,
            counter=1,
            previous_counter=0,
            mac=b"test_mac"
        )
        
        # Serialize the message
        serialized = message.serialize()
        
        # Deserialize the message
        deserialized = SignalMessage.deserialize(serialized)
        
        # Verify that the deserialized message matches the original
        self.assertEqual(message.message_version, deserialized.message_version)
        self.assertEqual(message.ciphertext, deserialized.ciphertext)
        self.assertEqual(message.sender_ratchet_key, deserialized.sender_ratchet_key)
        self.assertEqual(message.counter, deserialized.counter)
        self.assertEqual(message.previous_counter, deserialized.previous_counter)
        self.assertEqual(message.mac, deserialized.mac)
    
    def test_session_counter_updates(self):
        """Test that session counters are updated correctly"""
        # Get initial counter values
        initial_send_counter = self.alice_session.send_chain_counter
        initial_receive_counter = self.bob_session.receive_chain_counter
        
        # Message to encrypt
        plaintext = b"Test message"
        
        # Alice encrypts the message
        encrypted_message = encrypt_message(plaintext, self.alice_session, self.alice_identity_key_pair)
        
        # Bob decrypts the message
        decrypt_message(encrypted_message, self.bob_session, self.bob_identity_key_pair)
        
        # Verify that counters have been updated
        self.assertEqual(initial_send_counter + 1, self.alice_session.send_chain_counter)
        self.assertEqual(initial_receive_counter + 1, self.bob_session.receive_chain_counter)


if __name__ == '__main__':
    unittest.main()