# SPEC Tool Catalogue
## Comprehensive Reference for Internal and MCP Tools

**Version:** 1.0  
**Last Updated:** 2025-11-02  
**Purpose:** Authoritative reference of available tools for creating and executing SPECs

---

## Table of Contents

1. [Internal Tools](#internal-tools)
2. [MCP Tools - Currently Integrated](#mcp-tools---currently-integrated)
3. [Recommended MCP Tools - Not Yet Integrated](#recommended-mcp-tools---not-yet-integrated)
4. [Tool Selection Guidelines](#tool-selection-guidelines)
5. [Integration Roadmap](#integration-roadmap)

---

## Internal Tools

These are built-in tools available in the Cursor/Claude development environment.

### File Operations

| Tool | Purpose | Use in SPEC Creation | Key Capabilities |
|------|---------|---------------------|------------------|
| `read_file` | Read file contents | Access existing SPECs, constitutions, parameters | Line-range reading, image support |
| `write` | Create/overwrite files | Generate new SPEC files | Full file creation |
| `search_replace` | Edit files precisely | Update SPEC parameters, modify constitutions | Exact string replacement, replace-all mode |
| `delete_file` | Remove files | Clean up temporary files, deprecated SPECs | Safe deletion with graceful failure |
| `list_dir` | Directory listing | Navigate SPEC structure, discover projects | Glob pattern filtering |
| `glob_file_search` | Pattern-based file search | Find SPECs by pattern (e.g., all `project_constitution.toml`) | Recursive search, modification time sorting |

**SPEC Use Cases:**
- Reading project constitutions to understand context
- Generating new SPEC files from templates
- Updating TOML parameters based on DNA interviews
- Discovering existing SPECs in a project

### Codebase Intelligence

| Tool | Purpose | Use in SPEC Creation | Key Capabilities |
|------|---------|---------------------|------------------|
| `codebase_search` | Semantic code search | Find implementations, understand architecture | Meaning-based search, targeted directories |
| `grep` | Text pattern matching | Find exact strings, symbols, configurations | Regex support, context lines, multiline mode |
| `read_lints` | Read linter errors | Validate SPEC quality, check compliance | File/directory-specific diagnostics |

**SPEC Use Cases:**
- Finding existing implementations to reference in SPECs
- Locating configuration patterns across projects
- Validating SPEC files against linting rules
- Understanding codebase context for persona creation

### Execution & Testing

| Tool | Purpose | Use in SPEC Creation | Key Capabilities |
|------|---------|---------------------|------------------|
| `run_terminal_cmd` | Execute shell commands | Run tests, validate environments, execute workflows | Background execution, PowerShell support |
| `edit_notebook` | Modify Jupyter notebooks | Create analysis SPECs, document workflows | Cell-level editing, multiple languages |

**SPEC Use Cases:**
- Running validation scripts for SPEC parameters
- Executing DNA interview processes
- Testing SPEC compliance with constitutions
- Creating interactive SPEC documentation

### Task Management

| Tool | Purpose | Use in SPEC Creation | Key Capabilities |
|------|---------|---------------------|------------------|
| `todo_write` | Create task lists | Track multi-step SPEC creation workflows | Status tracking, parallel updates |

**SPEC Use Cases:**
- Breaking down complex SPEC creation into tasks
- Tracking progress through DNA interview stages
- Managing SPEC validation checkpoints

### Memory & Knowledge

| Tool | Purpose | Use in SPEC Creation | Key Capabilities |
|------|---------|---------------------|------------------|
| `update_memory` | Store persistent knowledge | Remember user preferences, project patterns | Create, update, delete memories |

**SPEC Use Cases:**
- Storing user's SPEC creation preferences
- Remembering project-specific patterns
- Maintaining context across sessions

---

## MCP Tools - Currently Integrated

These MCP servers are already configured and available in your environment.

### Development & Version Control

#### GitHub MCP Server
**Status:** Integrated  
**Provider:** GitHub  
**Category:** Version Control, Project Management

**Capabilities:**
- Repository management (create, fork, search)
- Issue tracking (create, update, list, comment)
- Pull request workflows (create, review, merge, update)
- Branch management (create, list, switch)
- File operations (read, create, update)
- Commit history and details
- Code scanning and security alerts
- Search across code, issues, users, repositories

**SPEC Use Cases:**
- Creating repositories for new SPEC projects
- Tracking SPEC development issues
- Automating SPEC review workflows through PRs
- Managing SPEC versions across branches
- Documenting SPEC changes in issues
- Searching for similar SPEC implementations

**Key Functions:**
- `mcp_github_create_repository` - Create new repo for SPEC project
- `mcp_github_create_issue` - Track SPEC development tasks
- `mcp_github_create_pull_request` - SPEC review workflow
- `mcp_github_create_or_update_file` - Commit SPEC files
- `mcp_github_search_repositories` - Find similar SPEC projects
- `mcp_github_search_code` - Find SPEC patterns in code

**Best Practices:**
- Use branches for SPEC iterations (e.g., `spec/transaction-processing-v2`)
- Tag SPEC releases with semantic versioning
- Use issues to track SPEC refinements
- Document SPEC decisions in PR descriptions

---

### Deployment & Infrastructure

#### Render MCP Server
**Status:** Integrated  
**Provider:** Render  
**Category:** Deployment, Infrastructure, Monitoring

**Capabilities:**
- Web service deployment (create, update, configure)
- Static site hosting
- PostgreSQL database management
- Key-value store (Redis) management
- Environment variable management
- Log streaming and analysis
- Performance metrics (CPU, memory, bandwidth)
- Deploy management and history

**SPEC Use Cases:**
- Deploying SPEC execution environments
- Hosting SPEC documentation sites
- Managing databases for SPEC state tracking
- Monitoring SPEC execution performance
- Analysing SPEC execution logs
- Configuring runtime environments for SPECs

**Key Functions:**
- `mcp_render_create_web_service` - Deploy SPEC executor
- `mcp_render_create_static_site` - Host SPEC docs
- `mcp_render_create_postgres` - State persistence
- `mcp_render_list_logs` - Debug SPEC executions
- `mcp_render_get_metrics` - Performance analysis
- `mcp_render_update_environment_variables` - Configure SPECs

**Best Practices:**
- Use environment variables for SPEC configuration
- Monitor CPU/memory to optimise SPEC complexity
- Stream logs during SPEC execution for debugging
- Create separate services for different SPEC domains

#### Insforge MCP Server
**Status:** Integrated  
**Provider:** Insforge  
**Category:** Backend-as-a-Service, Database, Edge Functions

**Capabilities:**
- Database schema management
- Raw SQL execution
- Bulk data import/export (CSV, JSON)
- Storage bucket management
- Edge function deployment (Deno runtime)
- Container log monitoring
- Backend metadata indexing

**SPEC Use Cases:**
- Storing SPEC execution history in databases
- Managing SPEC templates and configurations
- Deploying SPEC validation as edge functions
- Tracking SPEC metrics in structured storage
- Importing/exporting SPEC data
- Debugging SPEC runtime issues via logs

**Key Functions:**
- `mcp_insforge_get-backend-metadata` - Understand available resources
- `mcp_insforge_run-raw-sql` - Query SPEC execution data
- `mcp_insforge_bulk-upsert` - Import SPEC templates
- `mcp_insforge_create-function` - Deploy SPEC validators
- `mcp_insforge_get-container-logs` - Debug SPEC issues
- `mcp_insforge_get-table-schema` - Design SPEC data models

**Best Practices:**
- Store SPEC execution logs in structured tables
- Use edge functions for SPEC validation logic
- Track SPEC metrics (success rate, execution time)
- Version SPEC templates with metadata

---

### Research & Machine Learning

#### Hugging Face Hub MCP (via Docker)
**Status:** Integrated  
**Provider:** Hugging Face  
**Category:** ML Models, Datasets, Documentation

**Capabilities:**
- Model search and discovery (by task, author, tags)
- Dataset search and exploration
- Research paper search
- Repository details (models, datasets, spaces)
- Documentation search and retrieval
- Gradio app integration (Flux image generation)

**SPEC Use Cases:**
- Finding ML models relevant to SPEC domain
- Accessing datasets for SPEC validation
- Researching papers to inform SPEC design
- Discovering pre-built tools for SPEC execution
- Generating visualisations for SPEC documentation

**Key Functions:**
- `mcp_MCP_DOCKER_model_search` - Find models for SPECs
- `mcp_MCP_DOCKER_dataset_search` - Discover datasets
- `mcp_MCP_DOCKER_paper_search` - Research context
- `mcp_MCP_DOCKER_hf_doc_search` - Find documentation
- `mcp_MCP_DOCKER_hub_repo_details` - Evaluate tools
- `mcp_MCP_DOCKER_gr1_flux1_schnell_infer` - Generate images

**Best Practices:**
- Search for models that match SPEC domain tasks
- Validate SPEC assumptions against research papers
- Use datasets to test SPEC edge cases
- Generate diagrams for SPEC documentation

#### Academic Paper Access (via Docker)
**Status:** Integrated  
**Sources:** arXiv, bioRxiv, medRxiv, PubMed, CrossRef, Semantic Scholar, IACR  
**Category:** Research, Documentation

**Capabilities:**
- Search papers across multiple repositories
- Download PDFs from various sources
- Read and extract paper text
- Access paper metadata

**SPEC Use Cases:**
- Researching methodologies for SPEC design
- Finding best practices in workflow orchestration
- Understanding domain-specific patterns
- Citing research in SPEC documentation

**Key Functions:**
- `mcp_MCP_DOCKER_download_arxiv` - Get CS/AI papers
- `mcp_MCP_DOCKER_download_semantic` - Multi-source access
- `mcp_MCP_DOCKER_read_arxiv_paper` - Extract paper content
- `mcp_MCP_DOCKER_get_crossref_paper_by_doi` - Metadata lookup

**Best Practices:**
- Reference papers when designing novel SPEC patterns
- Extract methodologies from research
- Build evidence base for SPEC decisions

---

### Web Intelligence

#### Tavily MCP Server
**Status:** Integrated  
**Provider:** Tavily  
**Category:** Web Search, Content Extraction, Site Mapping

**Capabilities:**
- Real-time web search (general, news, finance)
- Deep content extraction from URLs
- Website crawling (multi-page)
- Site structure mapping
- Advanced filtering (domains, dates, countries)
- Image and description extraction

**SPEC Use Cases:**
- Researching latest practices for SPEC domains
- Extracting documentation from vendor sites
- Mapping project architecture across web resources
- Gathering competitive intelligence for SPEC design
- Staying current with industry standards
- Discovering tools and frameworks

**Key Functions:**
- `mcp_tavily-remote-mcp_tavily_search` - Research SPEC domains
- `mcp_tavily-remote-mcp_tavily_extract` - Get full documentation
- `mcp_tavily-remote-mcp_tavily_crawl` - Multi-page analysis
- `mcp_tavily-remote-mcp_tavily_map` - Understand site structure

**Best Practices:**
- Use advanced search for specific technologies
- Extract full docs rather than truncated results
- Map vendor documentation sites for comprehensive coverage
- Filter by recent dates for current best practices

---

### Media Processing

#### YouTube Transcript MCP (via Docker)
**Status:** Integrated  
**Category:** Media Analysis, Documentation

**Capabilities:**
- Video transcript extraction
- Timed transcript with timestamps
- Video metadata retrieval
- Multi-language support

**SPEC Use Cases:**
- Extracting knowledge from conference talks
- Analysing tutorial content for SPEC guidance
- Documenting verbal requirements from stakeholders
- Learning new technologies for SPEC implementation

**Key Functions:**
- `mcp_MCP_DOCKER_get_transcript` - Full text extraction
- `mcp_MCP_DOCKER_get_timed_transcript` - With timestamps
- `mcp_MCP_DOCKER_get_video_info` - Metadata

**Best Practices:**
- Extract transcripts from technical conference talks
- Reference timestamp ranges for specific concepts
- Verify information across multiple sources

#### Document Processing MCP (via Docker)
**Status:** Integrated  
**Category:** OCR, Document Conversion

**Capabilities:**
- Document transcription (OCR)
- Text extraction from images/PDFs
- Status checking for long-running jobs

**SPEC Use Cases:**
- Converting legacy documentation to SPEC format
- Extracting requirements from scanned documents
- Processing handwritten notes into SPEC outlines

**Key Functions:**
- `mcp_MCP_DOCKER_check_status` - Monitor processing
- `mcp_MCP_DOCKER_get_text` - Retrieve results

---

### Documentation

#### Context7 MCP (via Docker)
**Status:** Integrated  
**Provider:** Upstash  
**Category:** Documentation, Library References

**Capabilities:**
- Real-time library documentation
- Version-specific docs
- Topic-focused retrieval
- Multi-framework support

**SPEC Use Cases:**
- Ensuring SPECs use current API patterns
- Referencing accurate framework usage
- Avoiding deprecated patterns in SPECs
- Validating SPEC code examples

**Key Functions:**
- `mcp_MCP_DOCKER_resolve-library-id` - Find correct library
- `mcp_MCP_DOCKER_get-library-docs` - Retrieve documentation

**Best Practices:**
- Always check current documentation before SPEC creation
- Include version requirements in SPEC constitutions
- Reference specific doc sections in SPEC steps

---

## Recommended MCP Tools - Not Yet Integrated

Based on research, these tools would significantly enhance SPEC creation and execution capabilities.

### High Priority

#### 1. Playwright MCP
**Provider:** Microsoft  
**Category:** Browser Automation, Testing  
**Priority:** HIGH

**Capabilities:**
- Accessibility tree-based web automation
- Cross-browser testing
- Natural language test generation
- Screenshot and trace capture
- Network interception

**Why Add:**
- Essential for SPECs involving web testing
- More reliable than Puppeteer for complex interactions
- Built-in accessibility checking aligns with quality SPECs
- Natural language test generation fits SPEC philosophy

**Use Cases:**
- E-commerce SPEC testing (like scarf boutique project)
- Automated UI validation SPECs
- Cross-browser compliance checking
- Accessibility audit SPECs

**Integration Effort:** Medium (official Microsoft tool)

---

#### 2. Sequential Thinking MCP
**Provider:** Community  
**Category:** Reasoning, Long-Running Tasks  
**Priority:** HIGH

**Capabilities:**
- Extended reasoning chains
- Persistent thought process
- Step-by-step problem decomposition
- Memory across reasoning steps

**Why Add:**
- Critical for complex SPEC generation
- Aligns with SPEC's structured thinking approach
- Enables better DNA interview conversations
- Supports multi-step SPEC validation

**Use Cases:**
- Complex SPEC design (highly complex constitutions)
- DNA interview dialogue management
- Multi-phase SPEC refinement
- Constitutional compliance reasoning

**Integration Effort:** Medium

---

#### 3. Filesystem MCP
**Provider:** Community  
**Category:** File Management  
**Priority:** HIGH

**Capabilities:**
- Advanced file operations
- Directory watching
- Batch file operations
- Symlink management

**Why Add:**
- Enhanced SPEC template management
- Batch SPEC generation workflows
- Monitor SPEC directories for changes
- Organise large SPEC projects

**Use Cases:**
- Generating multiple SPECs from templates
- Organising SPEC hierarchies
- Watching for SPEC updates
- Managing SPEC archives

**Integration Effort:** Low

---

#### 4. PostgreSQL MCP
**Provider:** Community  
**Category:** Database  
**Priority:** MEDIUM-HIGH

**Capabilities:**
- Direct database querying
- Schema inspection
- Read-only safe operations
- Natural language SQL generation

**Why Add:**
- Store SPEC execution history
- Track SPEC performance metrics
- Query SPEC patterns across projects
- Analyse SPEC success rates

**Use Cases:**
- SPEC analytics and reporting
- Historical SPEC performance analysis
- Finding similar SPECs by query
- Compliance tracking

**Integration Effort:** Medium

---

#### 5. Notion MCP
**Provider:** Notion  
**Category:** Documentation, Knowledge Management  
**Priority:** MEDIUM

**Capabilities:**
- Page and database access
- Task management
- Real-time workspace integration
- Structured data retrieval

**Why Add:**
- Manage SPEC documentation in Notion
- Track SPEC development tasks
- Create SPEC knowledge bases
- Team collaboration on SPEC design

**Use Cases:**
- SPEC project management
- Team SPEC review workflows
- SPEC template library
- Stakeholder SPEC documentation

**Integration Effort:** Medium

---

### Medium Priority

#### 6. Azure DevOps MCP
**Provider:** Microsoft  
**Category:** Project Management, CI/CD  
**Priority:** MEDIUM

**Capabilities:**
- Work item management
- Build pipeline integration
- Repository operations
- Test plan management

**Why Add:**
- Enterprise SPEC project tracking
- SPEC CI/CD integration
- Automated SPEC validation pipelines
- Work item-driven SPEC creation

**Use Cases:**
- Enterprise SPEC governance
- Automated SPEC deployment
- SPEC testing pipelines
- Team SPEC coordination

**Integration Effort:** Medium

---

#### 7. n8n MCP
**Provider:** n8n  
**Category:** Workflow Automation  
**Priority:** MEDIUM

**Capabilities:**
- Workflow orchestration
- Multi-system integration
- Trigger management
- Low-code automation

**Why Add:**
- Orchestrate complex SPEC execution
- Integrate SPECs with external systems
- Automate SPEC deployment workflows
- Connect SPECs to business processes

**Use Cases:**
- Multi-step SPEC orchestration
- SPEC-triggered workflows
- External system integration
- Business process automation

**Integration Effort:** Medium-High

---

#### 8. Linear MCP
**Provider:** Linear  
**Category:** Project Management  
**Priority:** MEDIUM

**Capabilities:**
- Issue tracking
- Project management
- Team coordination
- Cycle planning

**Why Add:**
- Modern SPEC project tracking
- Better UX than traditional tools
- Fast SPEC task management
- Developer-friendly workflows

**Use Cases:**
- Agile SPEC development
- Sprint-based SPEC delivery
- Team SPEC coordination
- SPEC backlog management

**Integration Effort:** Medium

---

#### 9. Slack MCP
**Provider:** Slack  
**Category:** Communication  
**Priority:** MEDIUM

**Capabilities:**
- Message posting
- Channel management
- User notifications
- File sharing

**Why Add:**
- SPEC execution notifications
- Team alerts on SPEC completion
- Collaborative SPEC review
- Real-time SPEC status updates

**Use Cases:**
- SPEC completion alerts
- Team SPEC notifications
- Collaborative SPEC debugging
- SPEC approval workflows

**Integration Effort:** Low-Medium

---

#### 10. Jira MCP
**Provider:** Atlassian  
**Category:** Project Management  
**Priority:** MEDIUM

**Capabilities:**
- Issue management
- Sprint planning
- Workflow automation
- Reporting

**Why Add:**
- Enterprise SPEC tracking
- Integrate with existing Jira workflows
- SPEC epic and story management
- Custom SPEC workflows

**Use Cases:**
- Enterprise SPEC governance
- Agile SPEC delivery
- SPEC dependency tracking
- Compliance reporting

**Integration Effort:** Medium

---

### Lower Priority (Specialised)

#### 11. Puppeteer MCP
**Provider:** Community  
**Category:** Browser Automation  
**Priority:** LOW (Playwright preferred)

**Why Consider:**
- Node.js native
- Good for simple scraping
- Headless Chrome control

**Use Cases:**
- Simple web scraping SPECs
- PDF generation from web content
- Basic automation tasks

---

#### 12. Selenium MCP
**Provider:** Community  
**Category:** Browser Automation, Testing  
**Priority:** LOW (Playwright preferred)

**Why Consider:**
- Legacy test migration
- Multi-language support
- Established ecosystem

**Use Cases:**
- Migrating legacy tests to SPECs
- Multi-platform testing

---

#### 13. MarkItDown MCP
**Provider:** Microsoft  
**Category:** Document Conversion  
**Priority:** LOW

**Capabilities:**
- Multi-format to Markdown
- Structure preservation
- AI-optimised output

**Why Consider:**
- Converting docs to SPEC format
- Standardising SPEC documentation
- Legacy doc migration

**Use Cases:**
- Converting requirements docs
- Standardising SPEC format
- Documentation migration

**Integration Effort:** Low

---

#### 14. Sentry MCP
**Provider:** Sentry  
**Category:** Error Tracking  
**Priority:** LOW (specialised)

**Capabilities:**
- Error monitoring
- Performance tracking
- Issue management
- Release tracking

**Why Consider:**
- Track SPEC execution errors
- Monitor SPEC performance
- Production SPEC monitoring

**Use Cases:**
- Production SPEC monitoring
- Error pattern analysis
- Performance optimisation

---

#### 15. Time API MCP
**Provider:** Community  
**Category:** Utilities  
**Priority:** LOW

**Capabilities:**
- Time zone management
- Date calculations
- Scheduling utilities

**Why Consider:**
- SPECs with time dependencies
- Scheduling workflows
- Time-based validations

**Use Cases:**
- Scheduled SPEC execution
- Time-based testing
- Timezone-aware SPECs

---

## Tool Selection Guidelines

### For SPEC Authors

When selecting tools for a SPEC, consider:

1. **Match Tool to Task Domain**
   - E-commerce → Playwright, GitHub, Render
   - Data processing → PostgreSQL, Filesystem, Hugging Face
   - Research → Tavily, Academic Papers, Hugging Face
   - Documentation → Context7, MarkItDown, Notion

2. **Consider Backup Methods**
   - Always specify alternative tools in constitutions
   - Example: Playwright → Puppeteer → Manual testing
   - Example: PostgreSQL → SQLite → File-based storage

3. **Respect Constraints**
   - Check project constitution for prohibited tools
   - Verify tool availability in execution environment
   - Consider rate limits and quotas

4. **Progressive Enhancement**
   - Start with internal tools
   - Add MCP tools for enhanced capabilities
   - Document tool dependencies in SPEC parameters

### For SPEC Executors

When executing SPECs with tools:

1. **Read Tool Documentation**
   - Use Context7 for current API patterns
   - Check Hugging Face docs for ML tools
   - Verify parameters before execution

2. **Handle Tool Failures**
   - Follow backup method hierarchy
   - Log tool failures in progress.json
   - Escalate if no backups available

3. **Optimise Tool Usage**
   - Cache documentation lookups
   - Batch file operations
   - Use parallel operations where safe

4. **Monitor Performance**
   - Track tool execution time
   - Monitor rate limits
   - Analyse tool success rates

### For Integration Planning

When adding new MCP tools:

1. **Assess Value**
   - How many SPECs would benefit?
   - Does it fill a gap in current capabilities?
   - Is maintenance effort justified?

2. **Check Compatibility**
   - Works with current environment (Cursor, PowerShell)
   - No conflicts with existing tools
   - Proper authentication support

3. **Plan Migration**
   - Update tool catalogue
   - Document in project constitutions
   - Train team on new capabilities
   - Update SPEC templates

4. **Validate Integration**
   - Test with sample SPECs
   - Verify error handling
   - Document common patterns
   - Create usage examples

---

## Integration Roadmap

### Phase 1: Essential (Q1 2025)
**Goal:** Core functionality for SPEC creation and execution

- [x] GitHub MCP - Repository and project management
- [x] Render MCP - Deployment and hosting
- [x] Tavily MCP - Research and intelligence
- [x] Hugging Face MCP - ML and research
- [ ] **Playwright MCP** - Web automation and testing
- [ ] **Sequential Thinking MCP** - Complex reasoning
- [ ] **Filesystem MCP** - Enhanced file operations

### Phase 2: Enhanced Capabilities (Q2 2025)
**Goal:** Advanced SPEC management and analytics

- [ ] **PostgreSQL MCP** - SPEC analytics and history
- [ ] **Notion MCP** - Documentation and collaboration
- [ ] **Linear/Jira MCP** - Project tracking (choose one)
- [ ] **Slack MCP** - Team notifications

### Phase 3: Enterprise & Specialised (Q3-Q4 2025)
**Goal:** Enterprise features and domain-specific tools

- [ ] **Azure DevOps MCP** - Enterprise project management
- [ ] **n8n MCP** - Workflow orchestration
- [ ] **Sentry MCP** - Production monitoring
- [ ] Domain-specific tools as needed

### Integration Criteria Checklist

Before integrating a new MCP tool:

- [ ] Documented use cases for SPEC system
- [ ] Alignment with project constitution requirements
- [ ] No conflicts with existing tools
- [ ] Authentication configured
- [ ] Error handling patterns documented
- [ ] Backup methods identified
- [ ] Team training plan
- [ ] Usage examples created
- [ ] Tool catalogue updated
- [ ] SPEC templates updated (if needed)

---

## Usage Patterns by SPEC Type

### Simple SPECs (1-3 tasks, 3-8 steps)
**Primary Tools:** Internal tools, GitHub, Tavily
**Why:** Minimal dependencies, fast execution, easy to reason about

### Moderate SPECs (3-5 tasks, 8-15 steps)
**Primary Tools:** Internal + GitHub + Render + Tavily + Context7
**Why:** Balance of capability and complexity

### Complex SPECs (4-5 tasks, 15-25 steps)
**Primary Tools:** Full MCP suite, Sequential Thinking, PostgreSQL
**Why:** Need advanced reasoning, state tracking, orchestration

### Research-Heavy SPECs
**Primary Tools:** Tavily, Hugging Face, Academic Papers, Context7
**Why:** Access to current knowledge and research

### Deployment SPECs
**Primary Tools:** GitHub, Render, Insforge, Playwright (testing)
**Why:** CI/CD pipeline integration

### Data Processing SPECs
**Primary Tools:** PostgreSQL, Filesystem, Hugging Face, Insforge
**Why:** Database operations, bulk data handling

---

## Appendix: Tool Comparison Matrices

### Browser Automation Tools

| Feature | Playwright | Puppeteer | Selenium |
|---------|-----------|-----------|----------|
| Accessibility tree | Yes | No | No |
| Multi-browser | Yes | Chrome only | Yes |
| Natural language | Yes | No | No |
| Integration priority | HIGH | LOW | LOW |
| Best for | Modern SPECs | Simple tasks | Legacy |

### Project Management Tools

| Feature | Linear | Jira | Azure DevOps |
|---------|--------|------|--------------|
| Modern UX | Excellent | Fair | Good |
| Enterprise features | Good | Excellent | Excellent |
| Integration effort | Medium | Medium | Medium |
| Best for | Startups | Enterprise | Microsoft shops |

### Database Tools

| Feature | PostgreSQL | SQLite | Supabase |
|---------|-----------|--------|----------|
| Scalability | High | Low | High |
| Complexity | Medium | Low | Low |
| Integration effort | Medium | Low | Low |
| Best for | Enterprise | Local/simple | Modern apps |

---

## Document Maintenance

**Review Schedule:** Quarterly  
**Owner:** SPEC System Architect  
**Last Review:** 2025-11-02

### Changelog

**v1.0 (2025-11-02)**
- Initial catalogue creation
- Documented all integrated tools
- Researched recommended tools
- Created integration roadmap

---

**End of Tool Catalogue**

