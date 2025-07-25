#!/usr/bin/env python3
"""
代码质量检查脚本

这个脚本会运行各种代码质量检查工具，确保代码符合项目规范。
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

    except FileNotFoundError:
        print(f"⚠️  工具未找到，跳过 {description}")
        return True
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


def main():
    """主函数"""
    print("🚀 Signal Protocol 代码质量检查")
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

    # 3. 代码格式检查 (如果安装了 black)
    checks.append(run_command(
        ["python", "-m", "black", "--check", "--diff", "signal_protocol", "tests"],
        "代码格式检查 (Black)"
    ))

    # 4. 代码风格检查 (如果安装了 flake8)
    checks.append(run_command(
        ["python", "-m", "flake8", "signal_protocol", "tests"],
        "代码风格检查 (Flake8)"
    ))

    # 5. 类型检查 (如果安装了 mypy)
    checks.append(run_command(
        ["python", "-m", "mypy", "signal_protocol"],
        "类型检查 (MyPy)"
    ))

    # 6. 运行测试
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
        print("🎉 所有检查都通过了！代码质量良好。")
        sys.exit(0)
    else:
        print("❌ 有些检查未通过，请修复后重新运行。")
        sys.exit(1)


if __name__ == "__main__":
    main()
