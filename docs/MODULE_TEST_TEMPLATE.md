# 模块测试模板

> **用途**: 为新模块添加 `if __name__ == "__main__"` 测试的模板和指南

## 📋 基本模板

```python
# your_module.py

# ... 模块的主要代码 ...

if __name__ == "__main__":
    """
    模块的简要测试和演示。
    
    这部分代码只在直接运行模块时执行：
    python -m signal_protocol.path.to.your_module
    """
    print("🧪 Testing [模块名] functionality...")
    
    # 1. 基本功能测试
    print("\n📝 Basic functionality tests:")
    
    # 在这里添加基本功能测试
    # 例如：创建对象、调用主要函数等
    
    # 2. 边界条件测试
    print("\n🔍 Edge case tests:")
    
    # 在这里添加边界条件测试
    # 例如：无效输入、空值处理等
    
    # 3. 集成测试
    print("\n🔗 Integration tests:")
    
    # 在这里添加与其他模块的集成测试
    
    print("\n🎉 All [模块名] tests passed!")
```

## 🎯 具体示例

### 1. 密钥生成模块示例

```python
# signal_protocol/keys/example_key.py

def generate_example_key():
    """生成示例密钥"""
    return os.urandom(32)

def validate_key(key: bytes) -> bool:
    """验证密钥格式"""
    return len(key) == 32

if __name__ == "__main__":
    """测试示例密钥模块"""
    print("🔑 Testing example key functionality...")
    
    # 1. 基本功能测试
    print("\n📝 Basic functionality tests:")
    key = generate_example_key()
    print(f"✅ Generated key: {key.hex()[:16]}...")
    assert len(key) == 32, "Key should be 32 bytes"
    
    # 2. 验证功能测试
    print("\n🔍 Validation tests:")
    assert validate_key(key), "Generated key should be valid"
    assert not validate_key(b"short"), "Short key should be invalid"
    print("✅ Key validation works correctly")
    
    # 3. 多次生成测试
    print("\n🔄 Multiple generation tests:")
    keys = [generate_example_key() for _ in range(5)]
    assert len(set(key.hex() for key in keys)) == 5, "Keys should be unique"
    print("✅ Multiple key generation produces unique keys")
    
    print("\n🎉 All example key tests passed!")
```

### 2. 数据处理模块示例

```python
# signal_protocol/utils/data_processor.py

def process_data(data: bytes) -> bytes:
    """处理数据"""
    return data.upper() if isinstance(data, str) else data

def serialize_data(data: dict) -> str:
    """序列化数据"""
    import json
    return json.dumps(data)

if __name__ == "__main__":
    """测试数据处理模块"""
    print("📊 Testing data processor functionality...")
    
    # 1. 数据处理测试
    print("\n📝 Data processing tests:")
    test_str = "hello world"
    processed = process_data(test_str)
    print(f"✅ Processed '{test_str}' -> '{processed}'")
    
    test_bytes = b"binary data"
    processed_bytes = process_data(test_bytes)
    assert processed_bytes == test_bytes, "Bytes should remain unchanged"
    print("✅ Bytes processing works correctly")
    
    # 2. 序列化测试
    print("\n💾 Serialization tests:")
    test_data = {"key": "value", "number": 42}
    serialized = serialize_data(test_data)
    print(f"✅ Serialized data: {serialized}")
    
    # 验证可以反序列化
    import json
    deserialized = json.loads(serialized)
    assert deserialized == test_data, "Deserialized data should match original"
    print("✅ Serialization round-trip works")
    
    print("\n🎉 All data processor tests passed!")
```

## 📝 编写指南

### 1. 测试内容建议

#### 必须包含
- **基本功能验证**: 测试模块的核心功能
- **参数验证**: 测试不同类型的输入参数
- **错误处理**: 测试异常情况的处理

#### 推荐包含
- **边界条件**: 测试极限情况
- **性能检查**: 简单的性能验证
- **集成测试**: 与其他模块的交互

#### 可选包含
- **使用示例**: 展示典型用法
- **调试信息**: 输出有助于调试的信息
- **基准测试**: 简单的性能基准

### 2. 输出格式建议

```python
# 使用表情符号和清晰的分组
print("🧪 Testing module functionality...")
print("\n📝 Basic tests:")
print("✅ Test passed")
print("❌ Test failed")
print("\n🎉 All tests passed!")
```

### 3. 断言使用

```python
# 使用有意义的断言消息
assert condition, "Clear error message explaining what went wrong"

# 对于复杂验证，使用 try-except
try:
    result = some_function()
    assert result is not None, "Function should return a value"
    print("✅ Function works correctly")
except Exception as e:
    print(f"❌ Function failed: {e}")
    raise
```

## 🔧 运行方式

### 1. 直接运行模块
```bash
# 运行特定模块的测试
python -m signal_protocol.keys.identity_key

# 或者直接运行文件
python signal_protocol/keys/identity_key.py
```

### 2. 批量运行模块测试
```bash
# 使用我们的检查脚本
python scripts/basic_check.py

# 或者使用 Make 命令
make check
```

## ✅ 最佳实践

1. **保持简洁**: 测试应该快速运行，专注于核心功能
2. **清晰输出**: 使用清晰的输出格式，便于理解测试结果
3. **有意义的断言**: 断言失败时应该提供有用的错误信息
4. **独立性**: 测试不应该依赖外部文件或网络
5. **文档性**: 测试代码本身就是使用文档

## 🎯 检查清单

为新模块添加测试时，确保：

- [ ] 包含 `if __name__ == "__main__":` 块
- [ ] 添加模块功能的基本测试
- [ ] 使用清晰的输出格式
- [ ] 包含有意义的断言
- [ ] 测试可以独立运行
- [ ] 输出结果易于理解
- [ ] 测试覆盖主要功能路径

---

**记住**: 模块测试的目的是提供快速反馈和使用示例，不需要像单元测试那样全面，但应该覆盖核心功能。
