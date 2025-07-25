# Signal Protocol 包开发规范总结

> **创建日期**: 2025年7月25日  
> **目的**: 总结我们在开发过程中确立的包组织和测试规范

## 🎯 核心开发理念

### 1. 简洁性优先 (Simplicity First)
- **空 `__init__.py`**: 所有包的 `__init__.py` 文件保持为空或只包含注释
- **明确导入**: 使用完整的模块路径，避免隐式导入
- **职责单一**: 每个模块专注于单一功能

### 2. 可维护性 (Maintainability)
- **结构镜像**: 测试结构完全镜像源码结构
- **一对一映射**: 每个源码模块对应一个测试模块
- **清晰依赖**: 依赖关系一目了然，避免循环导入

### 3. 扩展性 (Scalability)
- **模块化设计**: 新功能可以自然地融入现有结构
- **层次清晰**: 包结构反映功能层次关系
- **工具支持**: 提供自动化检查工具确保规范遵守

---

## 📁 包结构设计原则

### 源码包结构
```
signal_protocol/
├── __init__.py                    # 空文件
├── keys/                          # 密钥管理模块
│   ├── __init__.py               # 空文件
│   ├── identity_key.py           # 身份密钥
│   ├── key_store.py              # 密钥存储
│   └── pre_keys/                 # 预密钥子模块
│       ├── __init__.py           # 空文件
│       ├── base_pre_key.py       # 基础预密钥
│       ├── signed_pre_key.py     # 签名预密钥
│       ├── one_time_pre_key.py   # 一次性预密钥
│       └── pre_key_bundle.py     # 预密钥包
├── sessions/                      # 会话管理 (未来)
└── messages/                      # 消息处理 (未来)
```

### 测试包结构 (完全镜像)
```
tests/
├── __init__.py                    # 空文件
└── signal_protocol/               # 镜像源码结构
    ├── __init__.py               # 空文件
    └── keys/
        ├── __init__.py           # 空文件
        ├── test_identity_key.py  # 对应 identity_key.py
        ├── test_key_store.py     # 对应 key_store.py
        └── pre_keys/
            ├── __init__.py       # 空文件
            ├── test_base_pre_key.py      # 对应 base_pre_key.py
            ├── test_signed_pre_key.py    # 对应 signed_pre_key.py
            └── test_pre_key_bundle.py    # 对应 pre_key_bundle.py
```

---

## 🔧 关键规范

### 1. __init__.py 文件规范 ⭐
```python
# ✅ 正确的 __init__.py 内容
# Empty __init__.py file for signal_protocol.keys package

# ❌ 禁止的内容
from .identity_key import generate_identity_key_pair  # 禁止重新导出
from . import identity_key                            # 禁止子模块导入
__all__ = ['identity_key']                           # 禁止 __all__ 定义
```

### 2. 导入规范
```python
# ✅ 正确的导入方式
from signal_protocol.keys.identity_key import generate_identity_key_pair
from signal_protocol.keys.pre_keys.base_pre_key import PreKeyPair

# ❌ 禁止的导入方式
from signal_protocol.keys import generate_identity_key_pair  # 避免从包导入
from signal_protocol import keys                             # 避免导入整个包
from signal_protocol.keys import *                          # 禁止通配符导入
```

### 3. 测试文件组织
```python
# 文件: tests/signal_protocol/keys/test_identity_key.py
import unittest
from signal_protocol.keys.identity_key import (  # 使用完整路径
    IdentityKeyPair,
    generate_identity_key_pair
)

class TestIdentityKey(unittest.TestCase):
    """测试身份密钥基础功能"""

    def test_identity_key_creation(self):
        """测试身份密钥创建"""
        pass

if __name__ == '__main__':
    unittest.main()
```

### 4. 模块测试规范 ⭐ 推荐实践
每个源码模块都应该包含`if __name__ == "__main__"`测试部分：

```python
# 文件: signal_protocol/keys/identity_key.py

# ... 模块的主要代码 ...

if __name__ == "__main__":
    """
    模块的简要测试和演示。

    运行方式: python -m signal_protocol.keys.identity_key
    """
    print("🔑 Testing identity key functionality...")

    # 基本功能测试
    key_pair = generate_identity_key_pair()
    print(f"✅ Generated key pair: {key_pair.public_key_bytes.hex()[:16]}...")

    # 功能验证
    test_message = b"Hello, Signal Protocol!"
    signature = xeddsa_sign(key_pair, test_message)
    is_valid = xeddsa_verify(key_pair.ed25519_verify_key_bytes, test_message, signature)

    assert is_valid, "Signature should be valid"
    print("✅ XEdDSA signing and verification works!")

    print("🎉 All tests passed!")
```

#### 模块测试的好处
- **快速验证**: 直接运行模块验证功能
- **使用示例**: 展示模块的核心用法
- **开发调试**: 便于开发时快速测试
- **活文档**: 作为可执行的使用文档

---

## 🛠️ 开发工具

### 1. 测试运行器
```bash
# 运行所有测试
python run_tests.py

# 使用 Make 命令
make test
```

### 2. 代码质量检查
```bash
# 基础检查 (不需要外部工具)
python scripts/basic_check.py
make check

# 完整检查 (需要开发工具)
python scripts/check_code_quality.py
make quality-check
```

### 3. 开发环境设置
```bash
# 安装开发依赖
make install-dev

# 初始化开发环境
make setup
```

---

## ✅ 自动化检查

我们的自动化检查包括：

### 1. 项目结构检查
- 验证必需文件存在
- 检查目录结构完整性

### 2. __init__.py 规范检查
- 确保所有 `__init__.py` 文件为空或只包含注释
- 检测违反规范的导入

### 3. 导入风格检查
- 检测从包级别的导入
- 发现通配符导入
- 验证使用完整模块路径

### 4. 模块测试检查
- 检查每个模块是否包含 `if __name__ == "__main__"` 测试
- 统计模块测试覆盖率
- 提供改进建议

### 5. 测试完整性
- 运行所有单元测试
- 验证测试覆盖率

---

## 🎯 遵循这些规范的好处

### 1. 避免常见问题
- **循环导入**: 空的 `__init__.py` 避免复杂的导入依赖
- **隐式依赖**: 明确的导入路径使依赖关系清晰
- **命名冲突**: 完整路径避免名称空间污染

### 2. 提高可维护性
- **易于重构**: 移动模块时不需要更新 `__init__.py`
- **清晰结构**: 测试结构镜像源码，易于定位
- **一致性**: 统一的规范减少认知负担

### 3. 便于团队协作
- **明确规范**: 详细的文档和自动化检查
- **工具支持**: 自动化工具确保规范遵守
- **渐进式**: 可以逐步添加新功能而不破坏现有结构

---

## 📚 相关文档

- [完整开发规范](./DEVELOPMENT_GUIDELINES.md) - 详细的开发指南
- [项目README](../README.md) - 项目概述和使用说明
- [开发状态](../DEVELOPMENT_STATUS.md) - 当前开发进度

---

## 🔄 持续改进

这些规范是基于我们的实际开发经验总结的，会随着项目的发展而不断完善：

1. **定期审查**: 每个开发阶段结束后审查规范的有效性
2. **工具改进**: 持续改进自动化检查工具
3. **文档更新**: 及时更新文档以反映最新的最佳实践

**记住**: 规范的目的是提高开发效率和代码质量，而不是限制创新。在特殊情况下可以灵活处理，但需要在代码审查中说明原因。
