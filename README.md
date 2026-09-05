# JARVIS-Android

**Autonomous AI Agent System for Android/Termux**

A production-grade, self-improving autonomous agent system designed for Android devices running Termux, featuring:

- **Hybrid Cognitive Architecture** (no external LLM dependency)
- **Natural Language Understanding** with intent classification and entity extraction
- **Advanced Memory System** (short-term, episodic, semantic, user preferences, learned skills)
- **Autonomous Planning & Execution** with multi-step task decomposition
- **Self-Improvement Capabilities** with backup, versioning, and rollback
- **Security Layer** with permission checks, risk assessment, and audit logging
- **Persistent Storage** using SQLite
- **Modular Tool System** for file operations, system commands, code generation, etc.

## Project Structure

```
JARVIS-Android/
├── core/              # Core infrastructure (config, logging)
├── memory/            # Memory systems (short-term, episodic, semantic)
├── brain/             # NLU engine (intent, entities, semantics, context)
├── planner/           # Task planning and execution sequencing
├── agent/             # Agent loop (reasoning, decision making, execution)
├── tools/             # Tool registry and implementations
├── skills/            # Skill management and built-in skills
├── security/          # Permission checks, risk assessment, audit
├── scheduler/         # Task scheduling and event dispatching
├── config/            # Configuration files
├── data/              # Runtime data (database, logs, backups)
├── tests/             # Unit and integration tests
├── main.py            # CLI entry point
└── requirements.txt   # Dependencies
```

## Installation

### Prerequisites
- Python 3.7+
- Termux (for Android) or any Linux-like environment
- SQLite3

### Setup

```bash
# Clone the repository
git clone https://github.com/zanayarhamdi/JARVIS-Android.git
cd JARVIS-Android

# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Start JARVIS

```bash
python3 main.py
```

### Example Interactions

```
You: سلام
JARVIS: سلام، چطور می‌تونم کمکت کنم؟

You: یک فایل Python بساز
JARVIS: چه کاری انجام دهد؟

You: فایل‌های دانلودها رو مرتب کن
JARVIS: [Planning 3 steps]
[Step 1: Analyzing requirements]
[Step 2: Generating code]
[Step 3: Creating file]
کد تولید شد و ذخیره شد.

You: اجراش کن
JARVIS: [Executing script]
اسکریپت اجرا شد. 42 فایل مرتب شد.

You: یک قابلیت جدید برام اضافه کن
JARVIS: بیایید بکاپ بگیریم... ✓
[Analyzing improvement]
[Generating changes]
[Applying changes]
[Running tests]
قابلیت جدید اضافه شد و تست شد.
```

## Core Features

### 1. Memory System
- **Short-Term Memory**: Fast access, limited duration working memory
- **Episodic Memory**: Event history with search and retrieval
- **Semantic Memory**: Knowledge base and concepts
- **User Preferences**: Persistent user settings
- **Learned Skills**: Discovered and learned commands

### 2. NLU Engine
- Intent classification (file operations, system info, code generation, etc.)
- Named entity extraction (files, directories, commands, etc.)
- Semantic parsing with relationships
- Conversation context tracking
- Reference resolution ("that file", "previous command")

### 3. Task Planner
- Multi-step task decomposition
- Action sequencing with dependency resolution
- State machine for task transitions
- Result verification

### 4. Agent Loop
1. **Input Processing** → NLU
2. **Planning** → Task decomposition
3. **Reasoning** → Feasibility analysis
4. **Decision Making** → Risk assessment & confirmation
5. **Execution** → Step-by-step execution
6. **Verification** → Result checking

### 5. Security
- Permission-based access control
- Risk assessment for dangerous operations
- User confirmation for risky actions
- Backup before modifications
- Audit logging

### 6. Self-Improvement
- Code modification with backup
- Syntax validation
- Unit testing
- Rollback on failure
- Change logging

## Configuration

Edit `config/default_config.json` to customize:
- JARVIS personality and behavior
- Memory retention periods
- Tool timeouts
- Voice settings (when enabled)
- Security policies
- Learning parameters

## Database

JARVIS uses SQLite for persistent storage:
- `memory.db` - Contains all memory tables
- Auto-created on first run
- Includes tables for:
  - short_term_memory
  - episodic_memory
  - semantic_memory
  - user_preferences
  - learned_skills
  - command_history
  - task_history
  - backup_log

## Architecture

### Hybrid Cognitive Architecture

Instead of relying on external LLMs, JARVIS uses:

1. **Rule-Based Intent Classification**: Pattern matching with confidence scoring
2. **Semantic Parsing**: Entity extraction and relationship mapping
3. **Memory-Augmented Reasoning**: Previous experience and learned patterns
4. **Deterministic Planning**: Step decomposition and sequencing
5. **State-Based Execution**: Finite state machine for task progression
6. **Pattern Learning**: Learn from repeated user interactions
7. **Skill Learning**: Discover and remember user-defined skills

### No External Dependencies for Core Logic

- ✓ NLU works without external APIs
- ✓ Planning and reasoning are deterministic
- ✓ Memory is local SQLite database
- ✓ All learning happens locally
- ✓ Tool execution is sandboxed and controlled

### Optional: External Brain Provider

Architecture supports plug-in LLM providers (to be implemented):

```python
# Future: Inject language model
agent.set_brain_provider(GoogleLLMProvider())
agent.set_brain_provider(LocalLlamaProvider())
agent.set_brain_provider(AnthropicProvider())
```

## Testing

```bash
python3 -m pytest tests/ -v
```

## Limitations & Android/Termux Notes

### What Works
- File operations (read, write, delete, rename)
- Directory navigation and listing
- System information gathering
- Process management
- Basic shell commands
- Python code generation and execution
- Task scheduling

### What Requires Permissions
- Accessing camera/microphone (Android permission)
- Reading sensors (Android permission)
- Network operations (Termux API)
- Android intents (Termux API)

### What's Limited
- Voice I/O (requires external STT/TTS)
- Wake word detection (requires dedicated model)
- Background services (Termux/Android limitations)
- Real-time system modification (permission/safety)

## Future Roadmap

- [ ] Voice input/output integration
- [ ] Wake word detection
- [ ] Pluggable LLM providers
- [ ] Advanced web scraping
- [ ] Machine learning for pattern recognition
- [ ] Multi-user support
- [ ] Cloud sync (optional)
- [ ] Android UI layer
- [ ] Advanced code debugging
- [ ] Distributed execution

## Performance

- **Startup Time**: ~2-3 seconds
- **NLU Processing**: ~100-200ms per input
- **Memory Queries**: <50ms
- **Task Execution**: Depends on task complexity
- **Database Size**: Grows slowly (~1MB per month typical use)

## Contributing

Contributions welcome! Areas of interest:
- New tool implementations
- Improved NLU models
- Android integration
- Voice integration
- Security enhancements

## License

MIT License - See LICENSE file

## Author

Zanayar Hamdi (zanayarhamdi)

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review examples in the codebase
