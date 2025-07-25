# Signal Protocol 项目 Makefile
# 提供常用的开发任务快捷命令

.PHONY: help test test-verbose clean format lint type-check quality-check install-dev setup

# 默认目标
help:
	@echo "Signal Protocol 开发工具"
	@echo "========================"
	@echo ""
	@echo "可用命令:"
	@echo "  test           - 运行所有测试"
	@echo "  test-verbose   - 运行测试 (详细输出)"
	@echo "  check          - 基础代码质量检查 (不需要外部工具)"
	@echo "  format         - 格式化代码 (black)"
	@echo "  lint           - 代码风格检查 (flake8)"
	@echo "  type-check     - 类型检查 (mypy)"
	@echo "  quality-check  - 运行所有代码质量检查"
	@echo "  clean          - 清理临时文件"
	@echo "  install-dev    - 安装开发依赖"
	@echo "  setup          - 初始化开发环境"
	@echo ""

# 运行测试
test:
	@echo "🧪 运行测试..."
	python run_tests.py

test-verbose:
	@echo "🧪 运行测试 (详细输出)..."
	python run_tests.py -v

# 基础代码质量检查 (不需要外部工具)
check:
	@echo "🔍 基础代码质量检查..."
	python scripts/basic_check.py

# 代码格式化
format:
	@echo "🎨 格式化代码..."
	python -m black signal_protocol tests scripts

# 代码风格检查
lint:
	@echo "🔍 代码风格检查..."
	python -m flake8 signal_protocol tests scripts

# 类型检查
type-check:
	@echo "🔍 类型检查..."
	python -m mypy signal_protocol

# 完整的代码质量检查
quality-check:
	@echo "🚀 运行完整的代码质量检查..."
	python scripts/check_code_quality.py

# 清理临时文件
clean:
	@echo "🧹 清理临时文件..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/

# 安装开发依赖
install-dev:
	@echo "📦 安装开发依赖..."
	pip install black flake8 mypy pytest

# 初始化开发环境
setup: install-dev
	@echo "🔧 初始化开发环境..."
	@echo "✅ 开发环境设置完成！"
	@echo ""
	@echo "下一步:"
	@echo "1. 运行 'make test' 确保所有测试通过"
	@echo "2. 运行 'make quality-check' 检查代码质量"
	@echo "3. 查看 docs/DEVELOPMENT_GUIDELINES.md 了解开发规范"

# 快速开发检查 (在提交前运行)
pre-commit: format lint type-check test
	@echo "✅ 预提交检查完成！"
