#!/usr/bin/env python3
"""
基础代码质量检查脚本

这个脚本只运行不依赖外部工具的检查，适合在没有安装开发依赖的环境中使用。
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """运行命令并返回结果"""
    print(f"\n🔍 {description}")
    print(f"运行命令: {' '.join(cmd)}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode == 0:
            print(f"✅ {description} - 通过")
            return True
        else:
            print(f"❌ {description} - 失败 (返回码: {result.returncode})")
            return False

    except Exception as e:
        print(f"❌ 运行 {description} 时出错: {e}")
        return False


def check_project_structure():
    """检查项目结构是否符合规范"""
    print("\n📁 检查项目结构")
    print("-" * 50)

    required_files = [
        "signal_protocol/__init__.py",
        "signal_protocol/keys/__init__.py",
        "signal_protocol/keys/pre_keys/__init__.py",
        "tests/__init__.py",
        "tests/signal_protocol/__init__.py",
        "tests/signal_protocol/keys/__init__.py",
        "tests/signal_protocol/keys/pre_keys/__init__.py",
        "docs/DEVELOPMENT_GUIDELINES.md",
        "README.md",
        "run_tests.py"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ 缺少以下必需文件:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ 项目结构检查通过")
        return True


def check_init_files():
    """检查 __init__.py 文件是否为空或只包含注释"""
    print("\n📦 检查 __init__.py 文件 (应该为空或只包含注释)")
    print("-" * 50)

    init_files = list(Path(".").rglob("__init__.py"))
    violations = []

    for init_file in init_files:
        # 跳过一些特殊目录
        if any(part in str(init_file) for part in ['.venv', '__pycache__', '.git']):
            continue

        try:
            content = init_file.read_text().strip()
            # 移除注释行和空行
            lines = [line.strip() for line in content.split('\n')
                     if line.strip() and not line.strip().startswith('#')]

            if lines:
                violations.append((init_file, lines))
                print(f"❌ {init_file} 包含非注释代码:")
                for line in lines[:3]:  # 只显示前3行
                    print(f"    {line}")
                if len(lines) > 3:
                    print(f"    ... (还有 {len(lines) - 3} 行)")
            else:
                print(f"✅ {init_file} - 符合规范 (空或只有注释)")
        except Exception as e:
            print(f"❌ 读取 {init_file} 时出错: {e}")
            return False

    if violations:
        print(f"\n❌ 发现 {len(violations)} 个不符合规范的 __init__.py 文件")
        print("建议: 保持 __init__.py 文件为空或只包含注释，使用具体的导入路径")
        return False
    else:
        print("\n✅ 所有 __init__.py 文件都符合规范")
        return True


def check_import_style():
    """检查导入风格是否符合规范"""
    print("\n📥 检查导入风格")
    print("-" * 50)

    python_files = list(Path("signal_protocol").rglob("*.py")) + \
        list(Path("tests").rglob("*.py"))
    violations = []

    for py_file in python_files:
        if '__pycache__' in str(py_file):
            continue

        try:
            content = py_file.read_text()
            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                line = line.strip()
                # 检查是否有从 __init__.py 导入的情况
                if 'from signal_protocol.keys import' in line and not line.startswith('#'):
                    violations.append((py_file, i, line, "避免从 keys 包直接导入，使用具体模块路径"))
                elif 'from signal_protocol import' in line and not line.startswith('#'):
                    violations.append((py_file, i, line, "避免从根包导入，使用具体模块路径"))
                elif 'import *' in line and not line.startswith('#'):
                    violations.append((py_file, i, line, "禁止使用通配符导入"))

        except Exception as e:
            print(f"❌ 读取 {py_file} 时出错: {e}")

    if violations:
        print(f"❌ 发现 {len(violations)} 个导入风格问题:")
        for file_path, line_num, line, reason in violations[:5]:  # 只显示前5个
            print(f"  {file_path}:{line_num} - {reason}")
            print(f"    {line}")
        if len(violations) > 5:
            print(f"  ... 还有 {len(violations) - 5} 个问题")
        return False
    else:
        print("✅ 导入风格检查通过")
        return True


def check_module_tests():
    """检查模块是否包含 if __name__ == '__main__' 测试部分"""
    print("\n🧪 检查模块测试部分 (if __name__ == '__main__')")
    print("-" * 50)

    # 只检查源码模块，不包括测试文件和 __init__.py
    source_files = []
    for py_file in Path("signal_protocol").rglob("*.py"):
        if '__pycache__' in str(py_file) or py_file.name == '__init__.py':
            continue
        source_files.append(py_file)

    missing_tests = []
    has_tests = []

    for py_file in source_files:
        try:
            content = py_file.read_text()

            # 检查是否包含 if __name__ == "__main__" 或 if __name__ == '__main__'
            if 'if __name__ ==' in content and ('__main__' in content):
                has_tests.append(py_file)
                print(f"✅ {py_file} - 包含模块测试")
            else:
                missing_tests.append(py_file)
                print(f"⚠️  {py_file} - 缺少模块测试")

        except Exception as e:
            print(f"❌ 读取 {py_file} 时出错: {e}")
            return False

    print(f"\n📊 模块测试统计:")
    print(f"  包含测试: {len(has_tests)}/{len(source_files)}")
    print(f"  缺少测试: {len(missing_tests)}/{len(source_files)}")

    if missing_tests:
        print(f"\n💡 建议为以下模块添加 if __name__ == '__main__' 测试:")
        for py_file in missing_tests:
            print(f"  - {py_file}")
        print("\n这些测试可以包含:")
        print("  • 基本功能验证")
        print("  • 使用示例")
        print("  • 快速调试代码")

        # 不将缺少模块测试视为错误，只是建议
        print("\n✅ 模块测试检查完成 (建议性检查)")
        return True
    else:
        print("\n✅ 所有模块都包含测试部分")
        return True


def main():
    """主函数"""
    print("🚀 Signal Protocol 基础代码质量检查")
    print("=" * 60)

    # 确保在项目根目录
    if not Path("signal_protocol").exists():
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)

    checks = []

    # 1. 项目结构检查
    checks.append(check_project_structure())

    # 2. __init__.py 文件检查
    checks.append(check_init_files())

    # 3. 导入风格检查
    checks.append(check_import_style())

    # 4. 模块测试检查 (建议性)
    checks.append(check_module_tests())

    # 5. 运行测试
    checks.append(run_command(
        ["python", "run_tests.py"],
        "单元测试"
    ))

    # 总结
    print("\n" + "=" * 60)
    print("📊 检查结果总结")
    print("=" * 60)

    passed = sum(checks)
    total = len(checks)

    print(f"通过: {passed}/{total}")

    if passed == total:
        print("🎉 所有基础检查都通过了！")
        print("\n📋 检查项目:")
        print("  ✓ 项目结构规范")
        print("  ✓ __init__.py 文件规范 (空文件)")
        print("  ✓ 导入风格规范")
        print("  ✓ 模块测试建议 (if __name__ == '__main__')")
        print("  ✓ 单元测试执行")
        print("\n💡 提示: 运行 'make install-dev' 安装开发工具后可以进行更全面的检查")
        sys.exit(0)
    else:
        print("❌ 有些检查未通过，请修复后重新运行。")
        sys.exit(1)


if __name__ == "__main__":
    main()
