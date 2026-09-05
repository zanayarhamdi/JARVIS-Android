# Contributing to JARVIS-Android

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make changes
5. Add/update tests
6. Submit pull request

## Code Style

- Python 3.7+ compatible
- Type hints for all functions
- Docstrings for all classes and public methods
- logging for debugging
- Follow existing patterns

## Areas for Contribution

### High Priority
- Android integration layer
- Tool implementations (filesystem, shell, etc.)
- Voice input/output integration
- Web search implementation
- Package manager integration

### Medium Priority
- Improved NLU patterns
- More skill examples
- Performance optimization
- Additional test coverage
- Documentation improvements

### Nice to Have
- GUI/web interface
- Multi-language support
- Advanced ML-based NLU
- Cloud sync capability
- Plugin marketplace

## Testing

All contributions must include:
- Unit tests for new functions
- Integration tests for new features
- Update existing tests if behavior changes

```bash
./run_tests.sh
```

## Pull Request Process

1. Update code
2. Add tests
3. Run tests (all must pass)
4. Update documentation
5. Create pull request with:
   - Clear description
   - Reference to issues
   - Testing notes

## Development Workflow

```bash
# Setup
bash install.sh

# Development
python3 main.py  # Run JARVIS

# Testing
bash run_tests.sh

# Backup before changes
bash backup.sh

# Debug/logging
# Check data/logs/ for detailed logs
```

## Code Guidelines

### Example: Adding a New Tool

```python
from tools.tool_base import BaseTool, PermissionLevel, RiskLevel

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Does something useful",
            permission_level=PermissionLevel.MEDIUM,
            risk_level=RiskLevel.LOW
        )
        self.parameters = {
            'param1': {'type': str, 'required': True},
            'param2': {'type': int, 'required': False}
        }
    
    def execute(self, param1: str, param2: int = None) -> Dict[str, Any]:
        """Execute the tool"""
        try:
            # Do work
            result = ...
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_result(self, result: Dict[str, Any]) -> bool:
        """Verify the result is valid"""
        return result.get('success', False)
```

### Example: Adding a New Skill

```python
from skills.skill_base import Skill

class MySkill(Skill):
    def __init__(self):
        super().__init__(
            name="my_skill",
            description="Learn to do something",
            version="1.0.0",
            author="Your Name"
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute skill"""
        # Implementation
        return {'success': True, 'result': ...}
    
    def learn_from_execution(self, inputs: Dict, output: Any) -> bool:
        """Learn from execution"""
        # Learn patterns
        return True
```

## Reporting Bugs

Include:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (Python version, OS, etc.)
- Logs from data/logs/

## Suggesting Features

Include:
- Use case description
- Why it's useful
- Proposed implementation (if known)
- Examples

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
