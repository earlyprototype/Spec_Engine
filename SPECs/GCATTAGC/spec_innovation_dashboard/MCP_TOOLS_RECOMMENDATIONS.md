# MCP Tools Recommendations - Innovation Consultancy Dashboard

**Project:** Innovation Consultancy Dashboard  
**DNA Code:** GCATTAGC  
**Date:** 2025-11-03  
**Analyzed From:** `__SPEC_Engine/_tools/mcp_tools_catalog.yaml`

---

## Executive Summary

Based on analysis of 269 MCP servers (2900+ tools), I've identified **REQUIRED**, **RECOMMENDED**, and **OPTIONAL** tools for your Innovation Consultancy Dashboard project.

**Quick Stats:**
- **REQUIRED:** 3 tools (critical for core functionality)
- **RECOMMENDED:** 7 tools (significantly improve development speed)
- **OPTIONAL:** 8 tools (enhance features, nice-to-have)

---

## REQUIRED Tools (Must Install)

### 1. **filesystem** (Category: Cloud & Infrastructure)
**Priority:** CRITICAL  
**Install:** `npm install @modelcontextprotocol/server-filesystem`

**Why Required:**
- Read/write project files (React components, config files)
- Create directory structures
- Edit code files during development
- Essential for all file operations

**Tools Provided:**
- `create_directory`, `read_file`, `write_file`
- `edit_file`, `list_directory`, `directory_tree`
- `search_files`, `get_file_info`

**Used In:**
- All SPEClets (file creation, editing, reading)
- SPEClet 0: Creating React components, config files
- SPEClets 1-5: Stage module development

---

### 2. **github** (Category: Cloud & Infrastructure)
**Priority:** CRITICAL  
**Install:** `npm install @modelcontextprotocol/server-github`

**Why Required:**
- Version control for all code
- Deployment via GitHub Pages/Vercel integration
- Collaboration and backup
- CI/CD integration

**Tools Provided:**
- `create_repository`, `create_or_update_file`
- `get_file_contents`, `create_branch`
- `create_pull_request`, `create_issue`

**Used In:**
- Project initialization
- Continuous deployment
- Code management across SPEClets

---

### 3. **fetch** (Category: Cloud & Infrastructure)
**Priority:** CRITICAL  
**Install:** Built-in MCP server

**Why Required:**
- API calls to Insforge backend
- External API integrations (LLM APIs for synthesis)
- HTTP requests for all external services

**Tools Provided:**
- `fetch` - Universal HTTP client

**Used In:**
- SPEClet 0: Insforge API integration
- SPEClets 1-5: AI synthesis API calls
- SPEClet 6: Export/reporting functionality

---

## RECOMMENDED Tools (Strongly Suggested)

### 4. **postgres** or **SQLite** (Category: Databases)
**Priority:** HIGH  
**Install:** `npm install @modelcontextprotocol/server-postgres`  
**Alternative:** `npm install @modelcontextprotocol/server-sqlite`

**Why Recommended:**
- Direct database management (if not using Insforge exclusively)
- Schema inspection and debugging
- Data migration support
- Query testing during development

**Tools Provided:**
- `query`, `create_table`, `describe_table`
- `list_tables`, `execute_query`
- `get_connection_string`, `describe_table_schema`

**Used In:**
- SPEClet 0: Database schema creation
- Debugging data issues
- Migration scripts

**Note:** May be redundant if Insforge handles all database operations.

---

### 5. **playwright** (Category: Cloud & Infrastructure)
**Priority:** HIGH  
**Install:** `npm install @modelcontextprotocol/server-playwright`

**Why Recommended:**
- End-to-end testing of web application
- Automated browser testing
- Visual regression testing
- Mobile responsiveness verification

**Tools Provided:**
- `browser_navigate`, `browser_click`, `browser_fill_form`
- `browser_screenshot`, `browser_evaluate`
- `browser_network_requests`, `browser_console_messages`

**Used In:**
- SPEClet 0: Testing authentication flow
- SPEClets 1-5: Testing stage modules
- SPEClet 6: End-to-end workflow verification

---

### 6. **git** (Category: Cloud & Infrastructure)
**Priority:** MEDIUM  
**Install:** `npm install @modelcontextprotocol/server-git`

**Why Recommended:**
- Local git operations
- Branch management
- Commit workflow automation
- Status checking

**Tools Provided:**
- `git_status`, `git_commit`, `git_add`
- `git_create_branch`, `git_diff`, `git_log`

**Used In:**
- Development workflow across all SPEClets
- Version tracking

---

### 7. **puppeteer** (Category: Cloud & Infrastructure)
**Priority:** MEDIUM  
**Install:** `npm install @modelcontextprotocol/server-puppeteer`

**Why Recommended:**
- Alternative to Playwright for browser automation
- Screenshot generation for documentation
- PDF export functionality (SPEClet 6)

**Tools Provided:**
- `puppeteer_navigate`, `puppeteer_screenshot`
- `puppeteer_click`, `puppeteer_evaluate`

**Used In:**
- SPEClet 6: Report generation (PDF export)
- Testing and documentation

---

### 8. **notion** (Category: Other Tools - Productivity)
**Priority:** LOW-MEDIUM  
**Install:** `npm install @modelcontextprotocol/server-notion`

**Why Recommended:**
- Alternative data storage for consultants
- Export integration for reports
- Collaboration features

**Tools Provided:**
- `API-create-a-database`, `API-post-page`
- `API-post-database-query`, `API-patch-page`

**Used In:**
- SPEClet 6: Export to Notion (optional feature)

---

### 9. **slack** (Category: Communication)
**Priority:** LOW  
**Install:** `npm install @modelcontextprotocol/server-slack`

**Why Recommended:**
- Team notifications
- Project updates
- Integration for consultant teams

**Tools Provided:**
- `slack_post_message`, `slack_list_channels`
- `slack_get_channel_history`

**Used In:**
- SPEClet 6: Optional notification integration

---

### 10. **obsidian** (Category: Other Tools - Knowledge Management)
**Priority:** LOW  
**Install:** `npm install @modelcontextprotocol/server-obsidian`

**Why Recommended:**
- Local knowledge base for consultants
- Note-taking integration
- Markdown export compatibility

**Tools Provided:**
- `obsidian_create_note`, `obsidian_search`
- `obsidian_get_file_contents`

**Used In:**
- SPEClet 6: Alternative export format

---

## OPTIONAL Tools (Nice-to-Have)

### 11. **mongodb** (Category: Databases)
**Priority:** OPTIONAL  
**Why:** Alternative database if moving away from Insforge
**Used In:** Backend architecture changes

### 12. **redis** (Category: Databases)
**Priority:** OPTIONAL  
**Why:** Session caching, performance optimization
**Used In:** SPEClet 0 optimization (future)

### 13. **confluence** (Category: Other Tools - Documentation)
**Priority:** OPTIONAL  
**Why:** Enterprise knowledge base integration
**Used In:** SPEClet 6 (enterprise client export)

### 14. **stripe** (Category: Other Tools - Payments)
**Priority:** OPTIONAL  
**Why:** If monetizing the platform
**Used In:** Future business model

### 15. **linear** (Category: Other Tools - Project Management)
**Priority:** OPTIONAL  
**Why:** Project management for consultant teams
**Used In:** Optional integration

### 16. **airtable** (Category: Other Tools - Productivity)
**Priority:** OPTIONAL  
**Why:** Alternative data storage/CRM features
**Used In:** Client management features

### 17. **zapier/n8n** (Not in catalog but relevant)
**Priority:** OPTIONAL  
**Why:** Workflow automation
**Used In:** SPEClet 6 (automation integrations)

### 18. **figma** (Not in catalog but relevant)
**Priority:** OPTIONAL  
**Why:** Design system integration
**Used In:** UI/UX design workflow

---

## Tools Specifically for AI Synthesis

For your AI-powered synthesis features (critical functionality), you'll need:

### LLM API Integration

**NOT in MCP catalog - Manual integration required:**
- **OpenAI API** (recommended - GPT-4 for synthesis)
- **Anthropic API** (Claude for reasoning)
- **Local LLM** (Ollama for privacy/cost)

**Implementation Approach:**
Use **fetch** MCP tool to call:
- `https://api.openai.com/v1/chat/completions` (OpenAI)
- `https://api.anthropic.com/v1/messages` (Anthropic)
- Local endpoint for Ollama

**Used In:**
- SPEClets 1-5: Stage-specific synthesis
- SPEClet 6: Cross-stage synthesis

---

## Installation Priority Matrix

### Phase 1: Before SPEClet 0 Execution
```bash
# CRITICAL - Install immediately
npm install @modelcontextprotocol/server-filesystem
npm install @modelcontextprotocol/server-github
# fetch is built-in
```

### Phase 2: During SPEClet 0 Development
```bash
# RECOMMENDED for testing
npm install @modelcontextprotocol/server-playwright
npm install @modelcontextprotocol/server-git
```

### Phase 3: Before SPEClets 1-5 (Stage Modules)
```bash
# OPTIONAL but helpful
npm install @modelcontextprotocol/server-puppeteer  # For PDF export
```

### Phase 4: Before SPEClet 6 (Integration)
```bash
# OPTIONAL integrations
npm install @modelcontextprotocol/server-slack  # If using notifications
npm install @modelcontextprotocol/server-notion  # If exporting to Notion
```

---

## Configuration Guide

### After Installing MCP Tools

**1. Update MCP Client Config**

Location varies by OS:
- **Windows:** `%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
- **macOS:** `~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
- **Linux:** `~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`

**2. Add MCP Servers**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/workspace"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<your-token>"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"]
    }
  }
}
```

**3. Restart MCP Client**

Restart your IDE/cursor to load new MCP servers.

**4. Test Tools**

Verify tools are accessible:
```
List available MCP tools
```

---

## Database Decision: Insforge vs. Postgres

### Option A: Full Insforge (Recommended for MVP)
**MCP Tools Needed:**
- ✅ `fetch` (for Insforge API calls)
- ❌ No `postgres` tool needed

**Pros:**
- Faster development (BaaS handles everything)
- Less infrastructure management
- Built-in authentication
- Rapid prototyping

**Cons:**
- Vendor lock-in
- Less control over schema
- May need migration later

### Option B: Custom Postgres Backend
**MCP Tools Needed:**
- ✅ `postgres` (direct database access)
- ✅ `fetch` (for custom API)

**Pros:**
- Full control
- No vendor lock-in
- Flexible schema

**Cons:**
- More development time
- Manual authentication setup
- Infrastructure management

**Recommendation:** Start with Option A (Insforge), use `postgres` tool later if migrating.

---

## Cost Considerations

### Free Tier MCP Tools
- ✅ filesystem (free)
- ✅ github (free with personal account)
- ✅ git (free)
- ✅ fetch (free)
- ✅ playwright (free)
- ✅ puppeteer (free)

### Paid/API Key Required
- ⚠️ Insforge (check pricing)
- ⚠️ OpenAI API (for AI synthesis)
- ⚠️ Anthropic API (alternative AI)
- ⚠️ Slack (free tier limited)
- ⚠️ Notion (free tier available)

---

## Next Steps

1. **Install REQUIRED tools immediately:**
   ```bash
   npm install @modelcontextprotocol/server-filesystem
   npm install @modelcontextprotocol/server-github
   ```

2. **Configure MCP client** (see Configuration Guide above)

3. **Restart Cursor/IDE**

4. **Begin SPEClet 0 execution** with tools available

5. **Install RECOMMENDED tools** as needed during development

6. **Add OPTIONAL tools** based on feature requirements

---

## Summary Table

| Tool | Category | Priority | Install Before | Used In |
|------|----------|----------|----------------|---------|
| filesystem | Infrastructure | **REQUIRED** | SPEClet 0 | All SPEClets |
| github | Infrastructure | **REQUIRED** | SPEClet 0 | All SPEClets |
| fetch | Infrastructure | **REQUIRED** | SPEClet 0 | All SPEClets |
| playwright | Testing | RECOMMENDED | SPEClet 0 | Testing |
| git | Version Control | RECOMMENDED | SPEClet 0 | All SPEClets |
| postgres | Database | RECOMMENDED | SPEClet 0 | Backend (if not Insforge) |
| puppeteer | Automation | RECOMMENDED | SPEClet 6 | PDF Export |
| slack | Communication | Optional | SPEClet 6 | Notifications |
| notion | Productivity | Optional | SPEClet 6 | Export |
| obsidian | Knowledge Mgmt | Optional | SPEClet 6 | Export |

---

**Ready to install! Start with the 3 REQUIRED tools before beginning SPEClet 0 execution.**


