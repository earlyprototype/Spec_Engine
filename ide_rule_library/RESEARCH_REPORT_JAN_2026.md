# Modern LLM-Assisted IDE & CLI Tools Research Report
**Date:** 7 January 2026  
**Purpose:** Comprehensive survey of AI coding tools and their rule integration systems

---

## Executive Summary

As of January 2026, the AI coding assistant market has exploded with **41% of global code now written or assisted by AI tools**. The market size has reached USD 20-30 billion with projected CAGR of 18-60% through 2030. A Stack Overflow survey shows **65% of developers use AI coding tools at least weekly**.

---

## 1. Modern LLM-Assisted IDEs (January 2026)

### A. Full IDEs with Native AI Integration

#### **Google Antigravity** (Released November 2025)
- **Type:** AI-native IDE (VSCode fork)
- **Key Feature:** "Agent-first" paradigm - autonomous AI agents handle complex tasks
- **Models:** Gemini 3, Claude Sonnet 4.5, Claude Opus 4.5
- **Unique:** Editor and Manager views for controlling multiple AI agents
- **Artifacts:** Generates task lists, implementation plans
- **Built-in:** Browser and terminal
- **Pricing:** Free (public preview)
- **Rule Files:**
  - **Global:** `~/.gemini/GEMINI.md`
  - **Workspace:** `.agent/rules/*.md`
- **Activation Modes:**
  - Always On (applied to every prompt)
  - Glob Pattern (e.g., `**/*.test.ts`)
  - Model Decision (AI determines relevance)
  - Manual (e.g., `@security-rule`)

#### **Cursor**
- **Type:** AI-native IDE (VSCode fork)
- **Key Features:**
  - Full codebase understanding
  - Supermaven-powered completion
  - Composer Mode (multi-file edits)
  - Auto-imports (TypeScript, Python)
- **Impact:** Saves 8-12 hours/week on 50k+ line codebases ($600-900/month value)
- **Pricing:** Free tier / $20/month Pro
- **Rule Files:** 
  - `.cursorrules` (legacy, still supported)
  - `.cursor/rules/**/*.mdc` (new Project Rules system with semantic descriptions, glob patterns, automatic attachment)
- **Best For:** Complex multi-file projects

#### **Windsurf** (by Codeium)
- **Type:** AI-native IDE with enterprise focus
- **Key Features:**
  - Cascade: agentic mode with auto shell command execution
  - Deep multi-file understanding
  - Team collaboration features
  - Cleaner UI than competitors
- **Pricing:** From $15/seat
- **Rule Files:** `.windsurfrules`
- **Best For:** Enterprise teams in regulated industries

#### **Visual Studio 2026 Insiders** (Released September 2025)
- **Type:** Microsoft's flagship IDE with embedded LLMs
- **Key Features:**
  - Adaptive Paste (Copilot rewrites pasted code to local context)
  - Copilot Chat with URL references
  - Third-party API key support (BYO models)
  - Profiler Copilot Agent (analyzes CPU/memory, suggests fixes)
- **Models:** GitHub Copilot integration + custom models
- **Pricing:** Part of Visual Studio licensing
- **Rule System:** Uses GitHub Copilot instruction system

#### **IntelliJ IDEA** (AI added September 2025)
- **Type:** JetBrains IDE with AI integration
- **Key Features:**
  - Native agent "Junie"
  - Claude integration
  - Plugin support for other agents
- **Pricing:** Free limited use / Paid subscription
- **Rule Files:** `.github/copilot-instructions.md` or plugin-specific configs

#### **Eclipse Theia**
- **Type:** Open-source IDE framework (web-based)
- **Key Features:**
  - Theia AI framework for building AI tools
  - Theia Coder: open AI coding assistant
  - Model Context Protocol (MCP) integration
  - Claude Code integration
- **Pricing:** Open source
- **Rule System:** MCP-based configuration

#### **Zed** (by Zed Industries)
- **Type:** Open-source collaborative code editor
- **Key Features:**
  - Real-time collaborative editing
  - AI integrations
  - Vim key bindings (optional)
  - Git support
- **Pricing:** Free editor / Paid AI features
- **Rule System:** Under investigation

---

### B. AI Extensions for Existing IDEs

#### **GitHub Copilot** (Mature, 2026 version)
- **Platform:** VSCode, Visual Studio, JetBrains, Neovim, CLI, GitHub.com
- **Key Features:**
  - Agent Mode (project-wide context)
  - Next Edit Suggestions
  - Multi-model support (Claude 3 Sonnet, Gemini 2.5 Pro, OpenAI)
- **Pricing:**
  - Free: 50 chat requests, 2,000 completions/month
  - Pro: $10/month (unlimited fair use)
  - Business: $19/user/month
- **Rule Files:**
  - **Repository-wide:** `.github/copilot-instructions.md`
  - **Path-specific:** `.github/instructions/**/*.instructions.md` (with YAML frontmatter)
  - **Agent-specific:** `AGENTS.md`
  - **Global:** `~/.config/github-copilot/intellij/global-copilot-instructions.md` (macOS) or `C:\Users\{user}\AppData\Local\github-copilot\intellij\global-copilot-instructions.md` (Windows)
- **Best For:** Teams in Microsoft/GitHub ecosystem

#### **Cline** (VS Code Extension)
- **Platform:** VS Code, Cursor, Windsurf
- **Key Features:**
  - Autonomous code generation
  - Terminal command execution
  - Web automation (browser interaction)
  - Image input support
  - Plan/Act workflow
  - Native support for Cursor/Windsurf rule files
- **Rule Files:**
  - **Native:** `.clinerules/project.md`
  - **Compatible:** `.cursorrules`, `.windsurfrules` work automatically
  - **Migration:** `.cursor/rules/*.mdc` → `.clinerules/`
  - **Custom Instructions:** VS Code Settings → Cline → Custom Instructions
- **Best For:** Developers wanting autonomous coding agent in familiar IDE

#### **Tabnine**
- **Platform:** Multiple IDE integrations
- **Key Features:** AI-driven code completion
- **Pricing:** Varies by tier
- **Rule System:** IDE-specific configuration

#### **Qodo** (formerly Codium)
- **Platform:** Multiple IDE/CI/CD integrations
- **Key Features:**
  - AI code review
  - Pull request integration
  - CI/CD workflow integration
- **Pricing:** Enterprise-focused
- **Rule System:** Git workflow integration

#### **Sourcegraph Cody** (with Amp agent, launched 2025)
- **Platform:** Multiple IDEs
- **Key Features:**
  - Code writing and maintenance (Cody)
  - Complex multi-step tasks (Amp)
- **Rule Files:** `.sourcegraph/**/*.rule.md`

---

## 2. AI Coding CLI Tools (January 2026)

### **Google Gemini CLI**
- **Released:** June 2025 (open source)
- **Models:** Google Gemini AI models
- **Features:**
  - Code explanation
  - Feature writing
  - Debugging
  - Command execution via natural language
  - Local codebase integration
  - Runs locally
- **Rule Files:**
  - **Global:** `~/.gemini/GEMINI.md`
  - **Project:** `GEMINI.md` (project root and subdirectories)
  - **Customizable:** Can change filename via `contextFileName` in `settings.json`
  - **Hierarchical loading:** Project-specific overrides global
  - **Commands:** `/memory refresh` (reload), `/memory show` (display context)

### **OpenAI Codex CLI**
- **Released:** April 2025 (open source)
- **Models:** OpenAI models (GPT-5.2 Codex, GPT-5 Pro)
- **Features:**
  - Code writing/editing on desktop
  - File operations
  - Interactive coding in terminal
  - Code review mode
  - Sandbox execution modes
  - Profile management
- **Rule Files:**
  - **Config:** `~/.codex/config.toml` (TOML format)
  - **Project guidelines:** `AGENTS.md`
  - **Profiles:** Named config sets in config.toml
- **Config Options:**
  - Model selection
  - Approval policy (untrusted, on-failure, on-request, never)
  - Sandbox mode (read-only, workspace-write, danger-full-access)
  - Reasoning effort (minimal, low, medium, high, xhigh)
  - Shell environment policy
  - Custom model providers

### **Google Jules Tools**
- **Type:** Lightweight CLI for Jules coding agent
- **Features:**
  - Code generation
  - Bug fixing
  - Testing from terminal
- **Rule System:** Under investigation

### **Anthropic Claude Code**
- **Type:** Agentic coding tool
- **Features:**
  - Codebase understanding
  - Routine task assistance
  - Complex code explanation
  - Git workflow management (natural language)
  - Works in terminal, IDEs, or GitHub repos
- **Rule Files:** `CLAUDE.md`, `.claude/settings.json`

### **Aider** (Established tool, 2026 version)
- **Type:** Terminal-based AI coding assistant
- **Features:**
  - Natural language commands
  - Multiple model support
  - Environment variable configuration
  - YAML config support
  - Coding conventions management
- **Rule Files:**
  - **Config:** `.aider.conf.yml`
  - **Ignore:** `.aiderignore`
  - **Conventions:** `CONVENTIONS.md` (referenced in config)
  - **Environment:** `.env` (API keys)
- **Example Config:**
```yaml
model: gpt-4o
auto-commits: true
dark-mode: true
conventions_file: CONVENTIONS.md
```
- **Best For:** Terminal-focused developers

### **Forgecode**
- **Type:** AI-powered shell
- **Features:**
  - Integrates with existing CLI tools
  - Code generation, refactoring, deployment
  - Multi-model support
  - Self-hosted or cloud options
  - Enterprise governance
  - ZSH integration with `:` sentinel
- **Rule Files:**
  - **Environment:** `.env` (API keys, provider config)
  - **Project guidelines:** `AGENTS.md`
- **Config Options:**
  - Multiple API providers (FORGE_KEY, OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY)
  - Custom API endpoints
  - Retry logic configuration
  - ZSH syntax highlighting integration

---

## 3. Rule Integration Systems Summary

### Rule File Formats by Tool

| Tool | Primary Rule Files | Additional Configs | Notes |
|------|-------------------|-------------------|-------|
| **Cursor** | `.cursorrules` (legacy)<br>`.cursor/rules/**/*.mdc` (new) | - | New system supports semantic descriptions, glob patterns, auto-attachment |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.github/instructions/**/*.instructions.md`<br>`AGENTS.md`<br>Global config | YAML frontmatter for path-specific rules |
| **Claude Code** | `CLAUDE.md` | `.claude/settings.json` | - |
| **Windsurf** | `.windsurfrules` | - | - |
| **Cline** | `.clinerules/project.md` | Custom Instructions in settings<br>Compatible with `.cursorrules`, `.windsurfrules` | Native cross-IDE compatibility |
| **Aider** | `.aider.conf.yml` | `.aiderignore`<br>`CONVENTIONS.md`<br>`.env` | YAML-based config |
| **Sourcegraph Cody** | `.sourcegraph/**/*.rule.md` | - | - |
| **OpenCode** | `.opencode.json` | - | JSON format |
| **Gemini CLI** | `GEMINI.md` | `~/.gemini/GEMINI.md` (global)<br>`settings.json` (custom filename) | Hierarchical loading |
| **OpenAI Codex CLI** | `~/.codex/config.toml` | `AGENTS.md` | TOML format + profiles |
| **Forgecode** | `AGENTS.md` | `.env` | Uses emerging AGENTS.md standard |
| **Google Antigravity** | `.agent/rules/*.md` | `~/.gemini/GEMINI.md` (global) | Multiple activation modes |
| **Generic Conventions** | `AI.md`, `INSTRUCTIONS.md`, `CODING.md` | - | Common in 2026 projects |
| **Centralized Tools** | `.ai/`, `.ai-rulez/` | Tool-specific generators | Single source for multiple AIs |
| **VS Code AI Config** | `.vscode/settings.json` | `.vscode/extensions.json`, `.vscode/launch.json` | Copilot custom instructions |
| **JetBrains AI Config** | `.idea/workspace.xml` | `.idea/misc.xml` | Project-specific AI settings |
| **AIConfig Framework** | `.aiconfig` | - | JSON format, multi-modal |

### Common Rule File Patterns

1. **Markdown-based:** Most tools (`.cursorrules`, `CLAUDE.md`, `GEMINI.md`, `AI.md`, `INSTRUCTIONS.md`, `CODING.md`, `copilot-instructions.md`, `.mdc`)
2. **YAML/JSON/TOML configs:** Aider (`.aider.conf.yml`), OpenCode (`.opencode.json`), Codex CLI (`config.toml`), AIConfig (`.aiconfig`), VS Code (`.vscode/settings.json`)
3. **Hierarchical structures:** Cursor's `.cursor/rules/`, Copilot's `.github/instructions/`, Gemini CLI (global + project), `.ai/`, `.ai-rulez/`, `.agent/rules/`
4. **Cross-compatibility:** Cline natively supports Cursor and Windsurf formats
5. **Emerging standards:** 
   - `AGENTS.md` / `AGENT.md` - Unified standard across OpenAI, GitHub, Forgecode
   - `AI.md` - Generic convention for AI-specific instructions
   - Centralized directories (`.ai/`, `.ai-rulez/`) for multi-tool management

### Generic File Naming Conventions (2026)

Beyond tool-specific formats, several **generic conventions** have emerged:

1. **`AI.md`** - Generic AI instructions file (vendor-neutral)
   - Purpose: AI-specific project instructions
   - Common sections: Project overview, coding standards, architecture details
   - Used when no specific tool preference exists

2. **`AGENT.md` / `AGENTS.md`** - Standardized agent instructions
   - Purpose: Vendor-neutral configuration for all AI agents
   - Initiative: agentdotmd.github.io
   - Goal: Single file for multiple AI tools

3. **`INSTRUCTIONS.md`** - Generic project instructions
   - Purpose: General project guidelines and workflows
   - Can be used by both humans and AI assistants

4. **`CODING.md`** - Coding standards documentation
   - Purpose: Code style guidelines, naming conventions, best practices
   - Often referenced by AI tools for code generation

5. **Centralized Directories:**
   - `.ai/` - Used by dot-ai tool for centralized instructions
   - `.ai-rulez/` - Used by ai-rulez tool for multi-tool config generation

### Rule Management Tools (2026)

#### **rulesync** (PHP-based)
- Synchronizes instruction files across multiple AI assistants
- Supports: `.cursorrules`, `copilot-instructions.md`, `CLAUDE.md`, and more
- Single source of truth approach
- GitHub: `jpcaparas/rulesync`

#### **onlyrules** (TypeScript CLI)
- Generates rule files for multiple AI assistants from single source
- Supports: Claude, Cursor, GitHub Copilot, Gemini, OpenAI Codex, Cline, Junie, Windsurf, Trae
- NPM package: `onlyrules`
- Ideal for maintaining consistency across tools

#### **Ruler**
- Centralized rule management for multiple AI coding agents
- Stores rules in `.ruler/` directory
- Automatic distribution to agent configs
- Agent-specific fine-tuning via `ruler.toml`
- Example config:
```toml
[agents.aider]
enabled = true
output_path_instructions = "AGENTS.md"
output_path_config = ".aider.conf.yml"
```

---

## 4. Security Concerns (2026)

### Rules File Backdoor Attack
- **Threat:** Malicious actors embedding deceptive prompts in rule files
- **Impact:** AI tools generate code with vulnerabilities or backdoors
- **Mitigation:** Regular validation and monitoring of rule files
- **Source:** Security Affairs, Issue 175593

### Code Security Statistics
- **56.4%** of developers report AI-generated code sometimes/frequently introduces security vulnerabilities (Snyk 2023)
- **80%** of developers admit bypassing security policies when using AI tools

---

## 5. Adoption Statistics (2026)

- **41%** of global code written/assisted by AI
- **65%** of developers use AI tools weekly
- **Most Popular Tools:**
  - ChatGPT: 82%
  - GitHub Copilot: 68%

---

## 6. IDE Rule Extraction Strategy for Knowledge Graph

### Recommended Approach

Based on this research, we should extract rule files from:

#### High Priority (Widespread Formats)
1. `.cursorrules` - Most common, works with Cursor and Cline
2. `.github/copilot-instructions.md` - GitHub Copilot (68% adoption)
3. `AGENTS.md` / `AGENT.md` - **Emerging unified standard** used by OpenAI, GitHub Copilot, Forgecode
4. `CLAUDE.md` - Anthropic's format
5. `GEMINI.md` - Google Gemini CLI
6. `AI.md` - Generic AI instructions (common convention 2026)
7. `INSTRUCTIONS.md` - Generic project instructions
8. `.windsurfrules` - Windsurf/Codeium
9. `.cursor/rules/**/*.mdc` - New Cursor project rules

#### Medium Priority (Specialized)
10. `CODING.md` - Coding standards documentation
11. `.vscode/settings.json` - VS Code AI assistant configuration (Copilot instructions)
12. `.idea/workspace.xml` - JetBrains AI configuration
13. `.ai/` directory - Centralized AI instructions (dot-ai tool)
14. `.ai-rulez/` directory - Centralized rules (ai-rulez tool)
15. `.aiconfig` files - AIConfig framework format (JSON)
16. `.aider.conf.yml` + `CONVENTIONS.md` - Terminal developers
17. `.sourcegraph/**/*.rule.md` - Sourcegraph users
18. `.clinerules/project.md` - Cline-specific projects
19. `.agent/rules/*.md` - Google Antigravity workspace rules
20. `~/.codex/config.toml` - OpenAI Codex CLI config

#### Low Priority (Emerging/Niche)
21. `.opencode.json` - OpenCode
22. `.claude/settings.json` - Claude settings
23. `.aiderignore` - Aider exclusions
24. `~/.gemini/GEMINI.md` - Gemini CLI global rules
25. `.env` - Forgecode environment config
26. `.vscode/extensions.json` - VS Code extension recommendations
27. `.vscode/launch.json` - AI-enhanced debugging config
28. `.idea/misc.xml` - JetBrains project-specific AI settings

### File Priority for Scanning

When scanning existing Pattern repositories:

```
Priority 1 (Check first - Most Widespread):
- .cursorrules
- .github/copilot-instructions.md
- AGENTS.md / AGENT.md (emerging unified standard)
- AI.md (generic convention)
- CLAUDE.md
- GEMINI.md
- INSTRUCTIONS.md (generic project instructions)

Priority 2 (Check if P1 not found):
- .cursor/rules/*.mdc
- .windsurfrules
- .agent/rules/*.md (Antigravity)
- CODING.md
- .vscode/settings.json (for Copilot config)
- .ai/ directory (centralized instructions)
- .ai-rulez/ directory

Priority 3 (Check if codebase context suggests):
- .aider.conf.yml + CONVENTIONS.md (if Python/CLI tool)
- .sourcegraph/*.rule.md (if Sourcegraph references)
- .clinerules/project.md (if Cline mentioned)
- ~/.codex/config.toml (if Codex CLI project)
- .aiconfig (AIConfig framework)
- .idea/workspace.xml (JetBrains)
```

---

## 7. Extraction Implementation Notes

### Node Schema for IDERule

```cypher
(r:IDERule {
    id: string,
    source_repo: string,
    
    // File info
    file_path: string,              // e.g., ".cursorrules" or ".cursor/rules/main.mdc"
    file_format: string,            // "cursorrules", "copilot-instructions", "claude-md", etc.
    ide_type: [string],             // ["cursor", "cline"] - multiple possible
    
    // Content
    content: string,                // Actual rule file text
    
    // Analysis (Gemini)
    purpose: string,                // One-sentence summary
    categories: [string],           // ["code_style", "testing", "performance"]
    key_practices: [string],        // Specific practices enforced
    reasoning: string,              // Why valuable
    
    // Metadata
    technologies: [string],         // Tech stack targeted
    project_types: [string],        // ["web_app", "cli_tool"]
    stars: integer,                 // Repo popularity
    
    // Semantic search
    embedding: list<float>,         // 768-dimensional
    
    extracted_date: datetime
})
```

### Links to Existing Patterns

```cypher
(p:Pattern)-[:HAS_IDE_RULES]->(r:IDERule)
```

This allows:
- "Show me IDE rules for this pattern"
- "What patterns use these IDE configuration styles?"
- Pattern-informed SPEC generation → Automatic IDE rule generation

---

## 8. Market Insights

### Regional Adoption
- **North America:** Leading adoption (US tech companies)
- **Europe:** Steady growth (Germany, UK, France)
- **Asia-Pacific:** Rapid adoption (China, India - large dev communities)

### Market Projections
- **2025 Market Size:** USD 20-30 billion
- **CAGR through 2030:** 18-60%
- **2030 Projected Size:** USD 50-100+ billion

---

## Conclusions

1. **Rich Ecosystem:** 10+ major IDEs/tools with native AI integration as of January 2026
2. **Standardizing Formats:** Markdown-based rule files dominating (`.cursorrules`, `.md` variants)
3. **Cross-compatibility:** Tools like Cline bridging different rule formats
4. **Management Tools Emerging:** rulesync, onlyrules, Ruler addressing multi-tool complexity
5. **Security Focus Growing:** Awareness of rule file vulnerabilities increasing
6. **Massive Adoption:** 65% weekly usage among developers

### Recommendation for SPEC Engine

**Implement the isolated `ide_rule_library` module** with focus on:
1. **Top 8 priority formats:** `.cursorrules`, `.github/copilot-instructions.md`, `AGENTS.md`/`AGENT.md`, `AI.md`, `CLAUDE.md`, `GEMINI.md`, `INSTRUCTIONS.md`, `CODING.md`
2. Scan existing 534 Pattern repositories for these files
3. Use semantic search to match rules to project context
4. Synthesize tailored rule files for new SPECs
5. Monitor format evolution (new tools emerging rapidly)
6. **Key trends:**
   - `AGENTS.md`/`AGENT.md` is the emerging unified standard
   - Generic `AI.md` widely adopted as vendor-neutral option
   - Centralized directory approaches (`.ai/`, `.ai-rulez/`) gaining traction
   - IDE-specific configs (`.vscode/settings.json`, `.idea/workspace.xml`) also contain AI instructions

---

**Sources:**
- Wikipedia: Google Antigravity, Eclipse Theia, IntelliJ IDEA, Qodo, Tabnine, Zed, Sourcegraph
- TechCrunch: Gemini CLI, Codex CLI announcements
- GitHub: rulesync, Cline, dot-ai, ai-rulez, context-engineering
- Stack Overflow: Developer survey 2025
- HD Insights Research: Market analysis
- Security Affairs: Rules file backdoor vulnerability
- Official documentation: Cursor, GitHub Copilot, Aider, Claude Code, VS Code, JetBrains
- arXiv.org: Prompt engineering standards, Agent README research
- agentdotmd.github.io: AGENT.md standardization initiative
- AIConfig framework documentation
- Medium: AGENTS.md convention articles
- Dev.to: Prompt engineering best practices

**Last Updated:** 7 January 2026
