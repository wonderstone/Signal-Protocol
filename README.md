# Signal Protocol Implementation

This project implements the Signal Protocol for secure messaging.

## Installation

Before running the code, install the required dependencies:

```bash
pip install pynacl cryptography
```

## Identity Key Setup

The first step in implementing the Signal Protocol is setting up identity keys. This has been completed and includes:

1. Generating Curve25519 identity key pairs for ECDH key exchange
2. Implementing XEdDSA signatures (Ed25519-compatible signatures using Curve25519 keys)
3. Storing and retrieving identity keys with Ed25519 verify keys
4. Serializing keys for persistence

## Pre-Key Setup

The second step in implementing the Signal Protocol is setting up pre-keys. This has been completed and includes:

1. Generating Curve25519 pre-key pairs for ECDH key exchange
2. Generating signed pre-key pairs with XEdDSA signatures
3. Creating pre-key bundles for initial communication
4. Storing and managing pre-keys and signed pre-keys
5. Proper signature verification using Ed25519 verify keys

## Session Management

The third step in implementing the Signal Protocol is setting up session management. This has been completed and includes:

1. Session record creation and management
2. Session storage and retrieval
3. Key derivation functions (HKDF)
4. Root key and chain key management

## Message Encryption/Decryption

The fourth step in implementing the Signal Protocol is setting up message encryption and decryption. This has been completed and includes:

1. Signal message structure definition
2. Message encryption with AES-CTR
3. Message decryption with AES-CTR
4. Message authentication codes (MAC) calculation and verification

## Running Tests

To run the identity key tests:

```bash
python -m unittest tests/test_identity_key.py
```

To run the pre-key tests:

```bash
python -m unittest tests/test_pre_key.py
```

To run the message encryption/decryption tests:

```bash
python -m unittest tests/test_message_encryption.py
```

## Running Examples

To run the session management example:

```bash
python examples/session_management_example.py
```

To run the message encryption/decryption example:

```bash
python examples/message_encryption_example.py
```

## VSCode Debugging

The project includes comprehensive VSCode debugging configurations for all modules in the `signal_protocol/keys` directory. See `docs/vscode_debug_guide.md` for detailed instructions on:

1. Setting up breakpoints in key modules
2. Debugging test cases
3. Step-by-step debugging of XEdDSA signatures
4. Troubleshooting common issues

## Key Features

- **XEdDSA Signatures**: Ed25519-compatible signatures using Curve25519 keys
- **Comprehensive Testing**: All modules include unit tests with 100% pass rate
- **VSCode Integration**: Full debugging support for development
- **Modular Design**: Clean separation of concerns across key management components