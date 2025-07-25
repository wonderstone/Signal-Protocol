# Signal Protocol 实现 🔒

这是一个用于深入学习和理解 Signal Protocol 端到端加密协议的 Python 实现项目。Signal Protocol 是目前最先进的端到端加密通信协议，被广泛应用于 Signal、WhatsApp、Facebook Messenger 等主流通信应用中。

## 🎯 项目目标

- **深度学习**: 通过完整实现理解 Signal Protocol 的核心原理和技术细节
- **模块化设计**: 采用清晰的模块化架构，便于学习和扩展
- **完整测试**: 每个组件都有对应的单元测试，确保实现正确性
- **详细文档**: 提供详细的开发过程文档和技术说明

## 🏗️ 项目架构

```
signal_protocol/
├── keys/                    # 密钥管理模块
│   ├── base_key.py         # 基础密钥类和 Curve25519 实现
│   ├── identity_key.py     # 身份密钥和 XEdDSA 签名
│   ├── key_store.py        # 密钥存储和管理
│   └── pre_keys/           # 预密钥子系统
│       ├── base_pre_key.py     # 基础预密钥
│       ├── signed_pre_key.py   # 签名预密钥
│       ├── one_time_pre_key.py # 一次性预密钥
│       └── pre_key_bundle.py   # 预密钥包
├── sessions/               # 会话管理模块 (计划中)
├── messages/               # 消息加密/解密模块 (计划中)
└── tests/                  # 完整的测试套件
```

## ✨ 当前实现功能

### 🔑 密钥管理系统

#### 核心密钥基础设施
- **Curve25519 密钥生成**: 实现了标准的 Curve25519 ECDH 密钥对生成
- **密钥钳制 (Key Clamping)**: 正确实现 Curve25519 私钥的位操作要求
- **多种实现对比**: 提供 PyNaCl 官方实现和手动实现的性能对比

#### 身份密钥 (Identity Keys)
- **IdentityKeyPair**: 长期身份密钥对，用于身份验证
- **XEdDSA 签名**: Ed25519 兼容签名，使用 Curve25519 密钥
- **密钥序列化**: 支持密钥的持久化存储和恢复
- **Ed25519 验证密钥**: 自动生成对应的 Ed25519 验证密钥

#### 预密钥系统 (Pre-Keys)
- **基础预密钥 (PreKey)**: 用于初始密钥交换的临时密钥
- **签名预密钥 (SignedPreKey)**: 带有身份密钥签名的预密钥，提供前向安全性
- **一次性预密钥 (OneTimePreKey)**: 用于确保完美前向安全性的单次使用密钥
- **预密钥包 (PreKeyBundle)**: 完整的密钥交换信息包

#### 密钥存储 (Key Storage)
- **持久化存储**: 基于文件的密钥存储系统
- **安全序列化**: 安全的密钥序列化和反序列化
- **密钥管理**: 支持密钥的保存、加载、删除等操作

## 🔧 技术栈

- **Python 3.11+**: 现代 Python 特性和类型提示
- **PyNaCl**: 高性能的 NaCl/libsodium 加密库
- **Cryptography**: 用于高级加密操作
- **时间戳管理**: 毫秒级时间戳用于密钥生命周期管理

## 🚀 快速开始

### 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd Signal-Protocol

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或者 .venv\\Scripts\\activate  # Windows

# 安装依赖
pip install pynacl cryptography
```

### 基础使用示例

```python
from signal_protocol.keys.identity_key import generate_identity_key_pair
from signal_protocol.keys.pre_keys.base_pre_key import generate_pre_key_pair
from signal_protocol.keys.pre_keys.signed_pre_key import generate_signed_pre_key_pair
from signal_protocol.keys.pre_keys.pre_key_bundle import create_pre_key_bundle

# 1. 生成身份密钥对
identity_key_pair = generate_identity_key_pair()
print(f"身份密钥生成完成")

# 2. 生成预密钥
pre_key_pair = generate_pre_key_pair(key_id=1)
print(f"预密钥 ID: {pre_key_pair.key_id}")

# 3. 生成签名预密钥
signed_pre_key_pair = generate_signed_pre_key_pair(identity_key_pair, key_id=1)
print(f"签名预密钥时间戳: {signed_pre_key_pair.timestamp}")

# 4. 创建预密钥包 (用于密钥交换)
pre_key_bundle = create_pre_key_bundle(
    registration_id=12345,
    device_id=1,
    pre_key_pair=pre_key_pair,
    signed_pre_key_pair=signed_pre_key_pair,
    signed_pre_key_signature=signature,
    identity_key_pair=identity_key_pair
)
print("预密钥包创建完成")
```

### 运行测试

```bash
# 运行所有测试
python -m unittest discover tests/ -v

# 运行特定测试
python -m unittest tests.test_identity_key -v
python -m unittest tests.test_pre_key -v
```

### 模块执行和调试

```bash
# 直接运行模块进行测试
python -m signal_protocol.keys.pre_keys.base_pre_key
python -m signal_protocol.keys.pre_keys.signed_pre_key
python -m signal_protocol.keys.pre_keys.one_time_pre_key

# 抑制运行时警告（推荐用于调试）
python -W ignore::RuntimeWarning -m signal_protocol.keys.pre_keys.base_pre_key
```

## 🧪 开发和测试

### VS Code 调试支持

项目包含完整的 VS Code 调试配置：

1. **Python: Current File** - 调试当前打开的文件
2. **Python Module: Auto-detect Current File** - 自动检测并调试当前文件对应的模块
3. **Python: pytest** - 运行和调试测试

### 测试覆盖范围

- ✅ **身份密钥测试**: 密钥生成、XEdDSA 签名验证、序列化
- ✅ **预密钥测试**: 各类预密钥的生成、签名、验证
- ✅ **密钥存储测试**: 持久化存储和恢复功能
- ✅ **密钥包测试**: 预密钥包的创建和验证

## 📚 学习资源

### Signal Protocol 核心概念

1. **X3DH (Extended Triple Diffie-Hellman)**: 初始密钥协商协议
2. **Double Ratchet**: 消息加密和前向安全性算法
3. **XEdDSA**: Ed25519 兼容签名使用 Curve25519 密钥
4. **前向安全性**: 历史消息在密钥泄露后仍然安全

### 技术细节

- **Curve25519**: 现代椭圆曲线加密标准
- **Ed25519**: 高性能数字签名算法
- **HKDF**: 基于 HMAC 的密钥派生函数
- **AES-CTR**: 流式加密模式

## 🔍 代码质量

- **类型提示**: 完整的 Python 类型标注
- **文档字符串**: 详细的 API 文档
- **模块化设计**: 清晰的职责分离
- **测试驱动**: 高测试覆盖率

## 🛠️ 开发工具集成

- **VS Code**: 完整的调试和开发支持
- **Git**: 版本控制和开发历史
- **虚拟环境**: 隔离的依赖管理
- **命令行工具**: 支持各种开发任务

## 📋 待实现功能

查看 [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md) 了解详细的开发进度和计划。

## 🤝 贡献指南

这是一个学习项目，欢迎：
- 提出问题和建议
- 改进代码实现
- 增加测试用例
- 完善文档

## 📄 许可证

本项目仅用于学习和研究目的。

## 🙏 致谢

感谢 Signal Foundation 和开源社区为端到端加密通信做出的贡献。

---

**注意**: 这是一个学习实现，不应在生产环境中使用。如需在实际项目中使用 Signal Protocol，请使用官方的 libsignal 库。