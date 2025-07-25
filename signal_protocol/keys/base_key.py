"""Base classes and utilities for Signal Protocol keys"""

import os
import nacl.bindings
import nacl.public

from abc import ABC


class BaseKey(ABC):
    """Abstract base class for all key types in the Signal Protocol"""

    def __init__(self, public_key: bytes):
        """
        Initialize a base key.

        Args:
            public_key: 32-byte public key
        """
        if len(public_key) != 32:
            raise ValueError("Public key must be 32 bytes")
        self.public_key = public_key

    @property
    def public_key_bytes(self) -> bytes:
        """Get the public key as bytes"""
        return self.public_key


class BaseKeyPair(ABC):
    """Abstract base class for all key pair types in the Signal Protocol"""

    def __init__(self, public_key: bytes, private_key: bytes):
        """
        Initialize a base key pair.

        Args:
            public_key: 32-byte public key
            private_key: 32-byte private key
        """
        if len(public_key) != 32:
            raise ValueError("Public key must be 32 bytes")
        if len(private_key) != 32:
            raise ValueError("Private key must be 32 bytes")

        self.public_key = public_key
        self.private_key = private_key

    @property
    def public_key_bytes(self) -> bytes:
        """Get the public key as bytes"""
        return self.public_key

    @property
    def private_key_bytes(self) -> bytes:
        """Get the private key as bytes"""
        return self.private_key


def clamp_curve25519_private_key(key: bytes) -> bytes:
    """
    Clamp a Curve25519 private key as per the specification.

    Args:
        key: 32-byte private key

    Returns:
        bytes: Clamped 32-byte private key
    """
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes")

    # Convert to bytearray for easy manipulation
    key_array = bytearray(key)

    # Apply Curve25519 clamping:
    # - Clear the lowest 3 bits of the first byte
    # - Clear the highest bit and set the second highest bit of the last byte
    key_array[0] &= 0xF8  # Clear lowest 3 bits
    key_array[31] &= 0x7F  # Clear highest bit
    key_array[31] |= 0x40  # Set second highest bit

    return bytes(key_array)


def generate_key_pair() -> tuple[bytes, bytes]:
    """
    Generate a new Curve25519 key pair using PyNaCl (official implementation).
    This is now the default and recommended method.

    Returns:
        tuple: (public_key, private_key) as bytes
    """
    # Use PyNaCl's official implementation
    private_key_obj = nacl.public.PrivateKey.generate()

    # Extract raw bytes - PyNaCl uses encode() method
    private_key = private_key_obj.encode()  # Returns 32 bytes
    public_key = private_key_obj.public_key.encode()  # Returns 32 bytes

    # Ensure private key is properly clamped for Curve25519
    private_key = clamp_curve25519_private_key(private_key)

    # Regenerate public key from clamped private key to ensure consistency
    public_key = nacl.bindings.crypto_scalarmult_base(private_key)

    return public_key, private_key


def generate_key_pair_manual() -> tuple[bytes, bytes]:
    """
    Generate a new Curve25519 key pair using manual implementation.
    This is kept for comparison and educational purposes.

    Returns:
        tuple: (public_key, private_key) as bytes
    """
    # Generate a random 32-byte private key
    private_key = os.urandom(32)

    # Clamp the private key as required by Curve25519
    private_key = clamp_curve25519_private_key(private_key)

    # Derive the public key from the private key
    public_key = nacl.bindings.crypto_scalarmult_base(private_key)

    return public_key, private_key


def generate_key_pair_from_seed(seed: bytes) -> tuple[bytes, bytes]:
    """
    Generate a Curve25519 key pair from a deterministic seed.
    Useful for testing and reproducible key generation.

    Args:
        seed: 32-byte seed for deterministic generation

    Returns:
        tuple: (public_key, private_key) as bytes
    """
    if len(seed) != 32:
        raise ValueError("Seed must be 32 bytes")

    # Use the seed as private key base, then clamp it
    private_key = clamp_curve25519_private_key(seed)

    # Derive public key
    public_key = nacl.bindings.crypto_scalarmult_base(private_key)

    return public_key, private_key


def compare_key_generation_methods() -> dict:
    """
    Compare different key generation methods to ensure consistency.

    Returns:
        dict: Comparison results and statistics
    """
    results = {
        'total_tests': 100,
        'manual_vs_nacl_matches': 0,
        'key_length_valid': 0,
        'clamping_consistent': 0,
        'sample_keys': {}
    }

    # Test multiple generations
    for i in range(results['total_tests']):
        # Generate using both methods
        nacl_pub, nacl_priv = generate_key_pair()
        manual_pub, manual_priv = generate_key_pair_manual()

        # Check key lengths
        if (len(nacl_pub) == 32 and len(nacl_priv) == 32 and
                len(manual_pub) == 32 and len(manual_priv) == 32):
            results['key_length_valid'] += 1

        # Check if both methods produce properly clamped keys
        nacl_clamped = clamp_curve25519_private_key(nacl_priv)
        manual_clamped = clamp_curve25519_private_key(manual_priv)

        if nacl_clamped == nacl_priv and manual_clamped == manual_priv:
            results['clamping_consistent'] += 1

    # Generate a deterministic test
    test_seed = b'0' * 32
    seed_pub, seed_priv = generate_key_pair_from_seed(test_seed)

    results['sample_keys'] = {
        'nacl_method': {
            'public': generate_key_pair()[0].hex()[:32] + '...',
            'private': generate_key_pair()[1].hex()[:32] + '...'
        },
        'manual_method': {
            'public': generate_key_pair_manual()[0].hex()[:32] + '...',
            'private': generate_key_pair_manual()[1].hex()[:32] + '...'
        },
        'deterministic_seed': {
            'public': seed_pub.hex(),
            'private': seed_priv.hex()
        }
    }

    return results


if __name__ == "__main__":
    """
    测试和比较不同的密钥生成方法
    """
    print("🔑 Curve25519 密钥生成方法对比测试")
    print("=" * 50)

    # 1. 基本功能测试
    print("1️⃣ 基本功能测试:")

    # PyNaCl 官方方法
    nacl_pub, nacl_priv = generate_key_pair()
    print(f"✅ PyNaCl 官方方法:")
    print(f"   公钥长度: {len(nacl_pub)} bytes")
    print(f"   私钥长度: {len(nacl_priv)} bytes")
    print(f"   公钥示例: {nacl_pub.hex()[:32]}...")

    # 手动实现方法
    manual_pub, manual_priv = generate_key_pair_manual()
    print(f"✅ 手动实现方法:")
    print(f"   公钥长度: {len(manual_pub)} bytes")
    print(f"   私钥长度: {len(manual_priv)} bytes")
    print(f"   公钥示例: {manual_pub.hex()[:32]}...")

    # 2. 确定性种子测试
    print(f"\n2️⃣ 确定性种子测试:")
    test_seed = b'Signal Protocol Test Seed 123456'  # Exactly 32 bytes
    assert len(test_seed) == 32, f"Test seed length: {len(test_seed)}"
    seed_pub1, seed_priv1 = generate_key_pair_from_seed(test_seed)
    seed_pub2, seed_priv2 = generate_key_pair_from_seed(test_seed)

    print(f"✅ 种子确定性验证:")
    print(f"   第一次生成: {seed_pub1.hex()[:32]}...")
    print(f"   第二次生成: {seed_pub2.hex()[:32]}...")
    print(
        f"   结果一致: {'是' if seed_pub1 == seed_pub2 and seed_priv1 == seed_priv2 else '否'}")

    # 3. 密钥钳制验证
    print(f"\n3️⃣ 密钥钳制验证:")

    # 检查 PyNaCl 生成的私钥是否已经正确钳制
    nacl_reclamped = clamp_curve25519_private_key(nacl_priv)
    nacl_properly_clamped = nacl_reclamped == nacl_priv
    print(f"✅ PyNaCl 私钥钳制: {'正确' if nacl_properly_clamped else '需要修正'}")

    # 检查手动方法生成的私钥钳制
    manual_reclamped = clamp_curve25519_private_key(manual_priv)
    manual_properly_clamped = manual_reclamped == manual_priv
    print(f"✅ 手动方法私钥钳制: {'正确' if manual_properly_clamped else '需要修正'}")

    # 4. 大规模对比测试
    print(f"\n4️⃣ 大规模对比测试 (100次生成):")
    comparison = compare_key_generation_methods()

    print(f"✅ 测试结果:")
    print(f"   总测试次数: {comparison['total_tests']}")
    print(
        f"   密钥长度正确: {comparison['key_length_valid']}/{comparison['total_tests']}")
    print(
        f"   钳制一致性: {comparison['clamping_consistent']}/{comparison['total_tests']}")

    success_rate = (comparison['key_length_valid'] /
                    comparison['total_tests']) * 100
    clamp_rate = (comparison['clamping_consistent'] /
                  comparison['total_tests']) * 100

    print(f"   成功率: {success_rate:.1f}%")
    print(f"   钳制正确率: {clamp_rate:.1f}%")

    # 5. 性能对比 (简单测试)
    print(f"\n5️⃣ 性能对比测试:")

    import time

    # PyNaCl 方法性能
    start_time = time.time()
    for _ in range(1000):
        generate_key_pair()
    nacl_time = time.time() - start_time

    # 手动方法性能
    start_time = time.time()
    for _ in range(1000):
        generate_key_pair_manual()
    manual_time = time.time() - start_time

    print(f"✅ 1000次生成性能:")
    print(f"   PyNaCl 官方方法: {nacl_time:.4f}秒")
    print(f"   手动实现方法: {manual_time:.4f}秒")
    print(f"   性能比: {manual_time/nacl_time:.2f}x")

    # 6. 推荐总结
    print(f"\n🎯 推荐使用:")
    print(f"   默认推荐: generate_key_pair() (PyNaCl官方)")
    print(f"   确定性生成: generate_key_pair_from_seed()")
    print(f"   教育对比: generate_key_pair_manual()")

    print(f"\n🎉 所有测试完成!")
