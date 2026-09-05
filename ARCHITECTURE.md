# JARVIS-Android Architecture

## System Overview

JARVIS is a hybrid cognitive architecture designed to operate completely independently without relying on external LLMs or cloud services. The system uses a combination of deterministic reasoning, pattern matching, memory retrieval, and learning mechanisms.

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INPUT / VOICE                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    NLU ENGINE (Brain)                        │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │   Intent     │   Entity     │    Semantic Parser       │ │
│  │ Classifier   │  Extractor   │    & Context Tracker    │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   TASK PLANNER                               │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │  Decompose   │  Sequence    │    State Machine        │ │
│  │  Tasks       │  Actions     │    & Verification       │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  REASONING ENGINE                            │
│  ┌──────────────┬──────────────────────────────────────────┐ │
│  │  Feasibility │  Risk Analysis │  Confidence Scoring    │ │
│  │  Analysis    │  Memory Lookup │  Decision Support      │ │
│  └──────────────┴──────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                 DECISION MAKER                               │
│  ┌──────────────┬──────────────────────────────────────────┐ │
│  │ Permission   │  Risk Assessment │  User Confirmation   │ │
│  │ Checking     │  & Backup Plan   │  Request             │ │
│  └──────────────┴──────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                    YES│
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              TASK EXECUTOR & TOOL SYSTEM                    │
│  ┌──────────┬──────────┬──────────┬──────────────────────┐ │
│  │ Shell    │ File Ops │ Python   │ Code Generation      │ │
│  │ Commands │ Tools    │ Execution│ & Self-Modification  │ │
│  └──────────┴──────────┴──────────┴──────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  VERIFIER & LOGGER                           │
│  ┌──────────────┬──────────────────────────────────────────┐ │
│  │ Result Check │  Memory Update │  Audit Logging         │ │
│  │ & Validation │  & Learning    │  & Task Recording      │ │
│  └──────────────┴──────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              RESPONSE FORMATTING & OUTPUT                    │
│           (Text, Voice, Notifications, etc)                 │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. NLU Engine (brain/)

**Purpose**: Convert natural language to structured understanding

**Components**:
- **Intent Classifier**: Maps input to intent categories
  - Patterns: Regex + keyword matching
  - Scoring: Weighted pattern + keyword matching
  - Confidence: 0-1 score
  - Supports: file_operation, system_info, code_generation, self_improvement, learning, execution, conversation

- **Entity Extractor**: Identifies relevant entities
  - Extracts: filepaths, filenames, directories, numbers, emails, URLs, commands
  - Intent-specific: Operation type, source, destination for file ops
  - Description, language for code generation

- **Semantic Parser**: Understands relationships
  - Extracts: Subject, object, relationships
  - Detects: Tense (past/present/future)
  - Modifiers and qualifiers

- **Context Tracker**: Maintains conversation context
  - History: Last 10 interactions
  - Current task state
  - Reference resolution ("that file", "previous command")

### 2. Memory System (memory/)

**Persistence Layer**: SQLite database (data/memory.db)

**Components**:

- **Short-Term Memory**: Fast working memory
  - TTL-based expiration
  - In-memory cache + database backup
  - Max 100 entries by default
  - Use: Current task state, recent values

- **Episodic Memory**: Event history
  - Stores: What happened, when, context, importance
  - Retention: 90 days (configurable)
  - Search: By type, keyword, time range
  - Use: Learning from past actions, pattern recognition

- **Semantic Memory**: Knowledge base
  - Stores: Concepts, definitions, relationships
  - Categories: Organized knowledge
  - Search: By keyword, category
  - Use: General knowledge, learned concepts

- **User Preferences**: Settings & preferences
  - Persistent user configuration
  - Type-aware storage (bool, int, float, json)
  - Use: Personalization, user-specific behavior

- **Learned Skills**: Discovered capabilities
  - Stores: Skill name, description, implementation
  - Confidence scoring: Success/failure ratio
  - Use: Reuse learned patterns, improve efficiency

### 3. Planner (planner/)

**Purpose**: Decompose complex tasks into executable steps

**Components**:

- **Task Planner**: Break down tasks
  - Analyzes intent and entities
  - Generates step-by-step plan
  - Different strategies for different intent types
  - Each step has: ID, action, parameters, verification flag

- **Action Sequencer**: Order steps correctly
  - Topological sort based on dependencies
  - Ensures prerequisites complete before dependents
  - Identifies parallelizable steps

- **State Machine**: Track task progression
  - States: PENDING → RUNNING → COMPLETED/FAILED
  - Transitions: FAILED → PENDING (retry), PAUSED → RUNNING
  - Prevents invalid state transitions

- **Verifier**: Check execution results
  - Validates: Success/failure of each step
  - Captures: Output, errors, side effects
  - Calculates: Confidence in result

### 4. Agent Core (agent/)

**Purpose**: Orchestrate reasoning, decision, and execution

**Components**:

- **Reasoning Engine**: Analyze feasibility
  - Checks: Is plan feasible?
  - Identifies: Risky steps, assumptions, dependencies
  - Memory lookup: Similar past actions
  - Confidence scoring: 0-1 based on risks

- **Decision Maker**: Make execution decision
  - Policy: Execute if feasible and confident
  - Requires confirmation: For risky operations
  - Selects backup strategy: For high-risk tasks

- **Task Executor**: Run plan steps
  - Sequential execution with tool integration
  - Captures: Output, errors, timing
  - Logs: All execution to memory

### 5. Tool System (tools/)

**Purpose**: Abstracted interface for system operations

**Base Tool Class**:
```python
class BaseTool:
    - execute(**kwargs) → result
    - verify_result(result) → bool
    - get_metadata() → tool info
```

**Built-in Tools** (to be implemented):
- ShellTool: Execute shell commands
- FileSystemTool: File operations
- ProcessTool: Process management
- PythonTool: Python code execution
- AndroidTool: Android intents
- NetworkTool: HTTP requests
- CodeTool: Code generation/analysis

### 6. Security Layer (security/)

**Components**:

- **Permission Checker**: Access control
  - Roles: user, admin
  - Permissions: Read, write, delete, execute, network, system
  - Enforcement: Before tool execution

- **Risk Assessor**: Danger level
  - Levels: SAFE, LOW, MEDIUM, HIGH, CRITICAL
  - Rules: Mapped to actions
  - Determines: Need for confirmation/backup

- **Confirmation Manager**: User approval
  - Stores: Pending confirmations
  - Tracks: Response status
  - Options: Custom confirmation prompts

- **Audit Log**: Security tracking
  - Logs: Every action, actor, resource, status
  - Query: By action, actor, time
  - Use: Security review, accountability

- **Sandbox**: Code execution safety
  - Validates: Code for dangerous operations
  - Restricts: Imports, dangerous functions
  - Executes: With timeout, capture output

### 7. Learning System (skills/)

**Purpose**: Discover, learn, and reuse patterns

**Components**:
- **Skill Manager**: Registry of learned skills
- **Pattern Learner**: Find recurring patterns
- **Command Learner**: Learn user-defined shortcuts
- **Feedback Integration**: Learn from success/failure

## Data Flow Example: File Organization

```
User: "جارویس، فایل‌های دانلودها رو مرتب کن"

1. NLU:
   - Intent: file_operation
   - Entities: {directory: 'downloads'}
   - Context: Previous interactions

2. Planning:
   - Step 1: List directory contents
   - Step 2: Categorize files
   - Step 3: Create directories
   - Step 4: Move files
   - Step 5: Verify result

3. Reasoning:
   - Feasible: YES
   - Risks: File move could be dangerous
   - Confidence: 0.85
   - Similar past actions: 3 found

4. Decision:
   - Execute: YES
   - Requires confirmation: YES (high-risk)
   - Backup: YES

5. User Confirmation:
   "Are you sure? This will move files."
   User: "yes"

6. Execution:
   - Create backup
   - Execute each step
   - Capture output
   - Verify success

7. Learning:
   - Store episodic event
   - Update learned skills
   - Record success
   - Update confidence

8. Response:
   "Files organized. 42 files categorized and moved."
```

## Hybrid Cognitive Architecture Details

### Why No External LLM?

1. **Privacy**: All data stays local
2. **Reliability**: No network dependency
3. **Customization**: Tailored for Android/Termux
4. **Efficiency**: Fast inference without API latency
5. **Cost**: No API fees
6. **Transparency**: Clear decision logic

### How Does It Understand Language?

1. **Pattern Matching**: Regex + keyword patterns
   - Trade-off: Less flexible but deterministic
   - Coverage: 80+ common patterns
   - Fallback: Asks for clarification

2. **Memory Augmentation**: Retrieve similar past interactions
   - Improves: Understanding context and intent
   - Provides: Examples of similar requests
   - Enables: Learning from experience

3. **Semantic Relationships**: Parse object-action relationships
   - Identifies: Subject, verb, object
   - Maps: To actionable parameters
   - Enables: Multi-step task inference

4. **Context Awareness**: Track conversation state
   - Resolves: References ("that file")
   - Continues: Multi-turn conversations
   - Adapts: To user preferences

5. **Feedback Loops**: Learn from results
   - Success: Increase pattern confidence
   - Failure: Add error handling
   - User feedback: Adjust understanding

### Future: Pluggable Brain Provider

Architecture allows swapping NLU without rewriting:

```python
# Current: Hybrid approach
agent.brain = HybridNLU()

# Future: Local LLM
agent.brain = LlamaProvider(model='llama2-13b')

# Future: Cloud LLM
agent.brain = AnthropicProvider(api_key='...')
```

## Performance Characteristics

- **Startup**: 2-3 seconds
- **NLU Processing**: 100-200ms
- **Memory Query**: <50ms
- **Task Execution**: Variable (depends on task)
- **Database Size**: ~1MB per month
- **Memory Usage**: 50-100MB typical

## Security Properties

- **No privilege escalation**: Only user permissions
- **Audit trail**: Every action logged
- **Backup safety**: Automatic backups before risky ops
- **Rollback capability**: Easy recovery from mistakes
- **Sandboxed execution**: Code runs in restricted environment
- **Confirmation gates**: Dangerous operations need approval

## Extension Points

1. **New Tools**: Inherit from BaseTool
2. **New Intents**: Add to IntentClassifier patterns
3. **New Skills**: Register with SkillManager
4. **Custom Extraction**: Extend EntityExtractor
5. **New Memory Types**: Add to database schema
6. **Event Handlers**: Subscribe to EventDispatcher
