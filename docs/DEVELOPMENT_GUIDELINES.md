# Signal Protocol 开发规范与代码风格指南

> **版本**: 1.0  
> **最后更新**: 2025年7月25日  
> **适用范围**: Signal Protocol Python 实现项目

## 📋 目录

1. [项目结构规范](#项目结构规范)
2. [包和模块组织](#包和模块组织)
3. [测试组织规范](#测试组织规范)
4. [代码风格指南](#代码风格指南)
5. [导入规范](#导入规范)
6. [文档规范](#文档规范)
7. [Git 提交规范](#git-提交规范)
8. [调试和开发工具](#调试和开发工具)

---

## 📁 项目结构规范

### 核心原则
- **模块化设计**: 每个功能模块独立，职责单一
- **层次清晰**: 包结构反映功能层次关系
- **易于扩展**: 新功能可以自然地融入现有结构

### 标准项目结构
```
Signal-Protocol/
├── signal_protocol/           # 主包
│   ├── __init__.py           # 空文件，保持简洁
│   ├── keys/                 # 密钥管理模块
│   │   ├── __init__.py       # 空文件
│   │   ├── identity_key.py   # 身份密钥
│   │   ├── key_store.py      # 密钥存储
│   │   └── pre_keys/         # 预密钥子模块
│   │       ├── __init__.py   # 空文件
│   │       ├── base_pre_key.py
│   │       ├── signed_pre_key.py
│   │       ├── one_time_pre_key.py
│   │       └── pre_key_bundle.py
│   ├── sessions/             # 会话管理模块 (未来)
│   └── messages/             # 消息处理模块 (未来)
├── tests/                    # 测试包
│   ├── __init__.py           # 空文件
│   └── signal_protocol/      # 镜像源码结构
│       ├── __init__.py       # 空文件
│       └── keys/
│           ├── __init__.py   # 空文件
│           ├── test_identity_key.py
│           ├── test_key_store.py
│           └── pre_keys/
│               ├── __init__.py
│               ├── test_base_pre_key.py
│               ├── test_signed_pre_key.py
│               └── test_pre_key_bundle.py
├── examples/                 # 使用示例
├── docs/                     # 文档
├── .vscode/                  # VSCode 配置
└── run_tests.py             # 测试运行器
```

---

## 📦 包和模块组织

### __init__.py 文件规范 ⭐ 重要规则
- **严格保持空文件**: 所有 `__init__.py` 文件必须为空或只包含注释
- **禁止任何导入**: 不在 `__init__.py` 中进行任何模块导入或重新导出
- **明确导入路径**: 始终使用完整的模块路径进行导入
- **便于维护**: 空的 `__init__.py` 使模块结构更清晰，避免循环导入问题

#### 为什么要保持 __init__.py 为空？
1. **避免循环导入**: 复杂的导入容易造成循环依赖
2. **明确依赖关系**: 强制使用具体路径，使依赖关系一目了然
3. **便于重构**: 移动模块时不需要更新 `__init__.py` 文件
4. **减少意外**: 避免因为 `__init__.py` 中的代码导致的意外副作用

### 模块命名规范
- **使用小写字母**: 模块名使用小写字母和下划线
- **描述性命名**: 模块名应该清楚地描述其功能
- **避免缩写**: 除非是广泛认知的缩写，否则使用完整单词

### 导入示例
```python
# ✅ 正确的导入方式 - 使用完整的模块路径
from signal_protocol.keys.identity_key import generate_identity_key_pair
from signal_protocol.keys.pre_keys.base_pre_key import PreKeyPair
from signal_protocol.keys.pre_keys.signed_pre_key import SignedPreKeyPair

# ❌ 禁止的导入方式
from signal_protocol.keys import *  # 禁止通配符导入
from signal_protocol.keys import generate_identity_key_pair  # 禁止从 __init__.py 导入
from signal_protocol import keys  # 避免导入整个子包
```

### __init__.py 文件内容示例
```python
# ✅ 正确的 __init__.py 内容
# Empty __init__.py file for signal_protocol.keys package

# ❌ 禁止的 __init__.py 内容
from .identity_key import generate_identity_key_pair  # 禁止重新导出
from . import identity_key  # 禁止子模块导入
__all__ = ['identity_key']  # 禁止 __all__ 定义
```

---

## 🧪 测试组织规范

### 测试结构原则
- **镜像源码结构**: 测试目录结构完全镜像源码结构
- **一对一映射**: 每个源码模块对应一个测试模块
- **功能分离**: 不同功能的测试分离到不同文件

### 测试文件命名
- **前缀规范**: 测试文件以 `test_` 开头
- **对应关系**: `test_module_name.py` 对应 `module_name.py`
- **描述性**: 测试类名使用 `TestClassName` 格式

### 测试类组织
```python
# 示例: tests/signal_protocol/keys/test_identity_key.py
import unittest
from signal_protocol.keys.identity_key import (
    IdentityKeyPair,
    generate_identity_key_pair
)

class TestIdentityKey(unittest.TestCase):
    """测试身份密钥基础功能"""
    
    def test_identity_key_creation(self):
        """测试身份密钥创建"""
        pass
    
    def test_invalid_key_sizes(self):
        """测试无效密钥大小的处理"""
        pass

class TestIdentityKeyPair(unittest.TestCase):
    """测试身份密钥对功能"""
    pass

if __name__ == '__main__':
    unittest.main()
```

### 测试运行规范
- **使用测试运行器**: 通过 `run_tests.py` 运行所有测试
- **环境隔离**: 每个测试使用独立的临时环境
- **清理资源**: 测试后清理临时文件和资源

---

## 🎨 代码风格指南

### 基本原则
- **遵循 PEP 8**: Python 官方代码风格指南
- **一致性**: 整个项目保持一致的代码风格
- **可读性**: 代码应该易于理解和维护

### 命名规范
```python
# 类名: PascalCase
class IdentityKeyPair:
    pass

# 函数名和变量名: snake_case
def generate_identity_key_pair():
    key_pair_data = {}
    return key_pair_data

# 常量: UPPER_SNAKE_CASE
MAX_KEY_SIZE = 32
DEFAULT_KEY_ID = 1

# 私有成员: 前缀下划线
class KeyStore:
    def __init__(self):
        self._storage_path = None
        self.__private_data = {}
```

### 函数和方法规范
```python
def function_name(param1: type, param2: type = default) -> return_type:
    """
    函数的简短描述。
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述，有默认值
        
    Returns:
        return_type: 返回值的描述
        
    Raises:
        ValueError: 在什么情况下抛出此异常
    """
    # 函数实现
    pass
```

### 类定义规范
```python
class ClassName:
    """
    类的简短描述。

    这个类用于...的详细描述。

    Attributes:
        attribute_name: 属性描述
    """

    def __init__(self, param: type):
        """
        初始化方法。

        Args:
            param: 参数描述
        """
        self.attribute_name = param

    def method_name(self) -> type:
        """方法描述"""
        pass
```

### 模块测试规范 ⭐ 推荐实践
每个模块都应该在文件末尾包含一个简要的测试部分，用于验证模块的基本功能：

```python
if __name__ == "__main__":
    """
    模块的简要测试和演示。

    这部分代码只在直接运行模块时执行，用于：
    1. 验证模块的基本功能
    2. 提供使用示例
    3. 快速调试和开发
    """
    # 基本功能测试
    print("Testing module functionality...")

    # 示例：测试密钥生成
    key_pair = generate_identity_key_pair()
    print(f"Generated key pair with public key: {key_pair.public_key_bytes.hex()[:16]}...")

    # 示例：测试序列化
    serialized = serialize_identity_key_pair(key_pair)
    deserialized = deserialize_identity_key_pair(serialized)

    # 验证结果
    assert key_pair.public_key_bytes == deserialized.public_key_bytes
    print("✅ Basic functionality test passed!")
```

#### 模块测试的好处
1. **快速验证**: 直接运行模块即可验证基本功能
2. **使用示例**: 为其他开发者提供使用示例
3. **开发调试**: 在开发过程中快速测试新功能
4. **文档补充**: 作为活文档展示模块的核心功能

---

## 📥 导入规范

### 导入顺序
1. **标准库导入**
2. **第三方库导入**
3. **本地模块导入**

### 导入格式
```python
# 1. 标准库
import os
import sys
import unittest
from typing import List, Optional

# 2. 第三方库
import nacl.signing
from cryptography.hazmat.primitives import hashes

# 3. 本地模块 (按层次顺序)
from signal_protocol.keys.identity_key import IdentityKeyPair
from signal_protocol.keys.pre_keys.base_pre_key import PreKeyPair
from signal_protocol.keys.key_store import KeyStore
```

### 导入最佳实践
- **具体导入**: 明确导入需要的类和函数
- **避免循环导入**: 合理设计模块依赖关系
- **相对导入**: 在包内部可以使用相对导入，但要谨慎

---

## 📚 文档规范

### 文档字符串 (Docstring)
- **使用三重引号**: `"""` 格式
- **Google 风格**: 使用 Google 风格的文档字符串
- **完整描述**: 包含参数、返回值、异常说明

### 注释规范
```python
# 单行注释：解释代码的目的
def complex_function():
    # 这里解释复杂逻辑的原因
    result = some_complex_operation()
    
    # 多行注释用于解释
    # 复杂的算法或业务逻辑
    return result
```

### README 和文档
- **保持更新**: 文档与代码同步更新
- **示例代码**: 提供可运行的示例
- **安装说明**: 清晰的安装和使用说明

---

## 🔧 调试和开发工具

### VSCode 配置
- **调试配置**: 为每个模块提供调试配置
- **设置统一**: 团队使用统一的编辑器设置
- **扩展推荐**: 推荐必要的 VSCode 扩展

### 开发环境
```python
# 推荐的开发依赖
dependencies = [
    "pynacl>=1.5.0",      # 密码学库
    "cryptography>=3.0",   # 高级密码学功能
    "unittest",            # 测试框架 (内置)
]

dev_dependencies = [
    "black",               # 代码格式化
    "flake8",             # 代码检查
    "mypy",               # 类型检查
]
```

---

## 📝 Git 提交规范

### 提交消息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型 (type)
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例
```
feat(keys): implement XEdDSA signature system

- Add xeddsa_sign and xeddsa_verify functions
- Update IdentityKeyPair to support Ed25519 verify keys
- Fix signed pre-key verification issues

Closes #123
```

---

## ✅ 检查清单

### 新功能开发
- [ ] 遵循项目结构规范
- [ ] 编写对应的测试
- [ ] 添加完整的文档字符串
- [ ] 添加模块级别的 `if __name__ == "__main__"` 测试
- [ ] 更新相关文档
- [ ] 运行所有测试确保通过
- [ ] 检查代码风格

### 代码审查
- [ ] 代码逻辑正确
- [ ] 测试覆盖充分
- [ ] 文档完整准确
- [ ] 符合代码风格
- [ ] 没有安全问题

---

---

## 📚 相关文档

- [包开发规范总结](./PACKAGE_DEVELOPMENT_SUMMARY.md) - 包开发规范总结
- [模块测试模板](./MODULE_TEST_TEMPLATE.md) - 模块测试编写指南和模板
- [项目README](../README.md) - 项目概述和使用说明
- [开发状态](../DEVELOPMENT_STATUS.md) - 当前开发进度

---

## 🎯 总结

这份开发规范旨在确保 Signal Protocol 项目的代码质量、可维护性和团队协作效率。所有开发者都应该遵循这些规范，并在发现问题时及时更新这份文档。

### 🌟 核心规范要点

1. **空 `__init__.py`**: 保持所有包的 `__init__.py` 文件为空
2. **完整导入路径**: 使用具体的模块路径进行导入
3. **测试结构镜像**: 测试目录完全镜像源码结构
4. **模块测试**: 每个模块包含 `if __name__ == "__main__"` 测试部分
5. **自动化检查**: 使用工具确保规范遵守

**记住**: 规范是为了提高效率，而不是限制创新。在特殊情况下，可以灵活处理，但需要在代码审查中说明原因。
