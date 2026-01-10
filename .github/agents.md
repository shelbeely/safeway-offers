# Agent Instructions for safeway-offers Repository

This file provides instructions for AI coding agents (like GitHub Copilot) to maintain and update this repository effectively.

## Project Overview

**Project Name:** Safeway MCP Server  
**Primary Interface:** Model Context Protocol (MCP) Server (`safeway_mcp_server.py`)  
**Purpose:** AI-powered grocery assistant connecting Claude and other AI assistants to Safeway's unofficial mobile API

## Core Architecture

```
safeway_mcp_server.py (Primary - MCP Server)
├── 13 AI-powered tools for grocery management
├── Uses safeway_api.py for API interactions
└── Exposes tools via Model Context Protocol

safeway_api.py (Library)
├── SafewayAPIClient class
├── OAuth authentication
├── API endpoint wrappers
└── Data models (Coupon, Offer)

app.py (Alternative - Web Interface)
└── Flask web dashboard

main.go (Legacy - Go CLI)
└── Original CLI tool (maintained for compatibility)
```

## Documentation Structure

### Primary Documentation (Always Keep Updated)

1. **README.md** - Main entry point
   - Structure: Dual-audience (Humans / AI Agents)
   - Style: Engaging, emoji headers, conversational for humans
   - AI Agent sections: Collapsible `<details>` tags
   - Must include: Quick start, features, setup, examples
   - Update whenever: Tools added/changed, setup process changes

2. **MCP_QUICKSTART.md** - 5-minute setup guide
   - Target: New users wanting fast setup
   - Update whenever: Installation steps change, config format changes

3. **MCP_SERVER_GUIDE.md** - Comprehensive 30,000-word guide
   - All 13 tools documented exhaustively
   - Update whenever: New tools added, tool behavior changes
   - Sections: Installation, all tools with I/O, examples, troubleshooting

### Supporting Documentation

4. **COOKING_GUIDE.md** - Cooking workflows
5. **RECIPE_GUIDE.md** - Recipe features
6. **API_STATUS.md** - API availability information
7. **PROJECT_SUMMARY.md** - Architecture overview

### Configuration Examples

8. **mcp_config_example.json** - Claude Desktop config example
   - Update whenever: Environment variables change, paths change

## When Making Changes

### Adding a New MCP Tool

When adding a new tool to the MCP server:

1. **Code Changes:**
   ```python
   # In safeway_mcp_server.py, add to list_tools():
   Tool(
       name="safeway_new_tool",
       description="Clear description of what it does",
       inputSchema={
           "type": "object",
           "properties": {
               "param_name": {
                   "type": "string",
                   "description": "What this parameter does"
               }
           },
           "required": ["param_name"]
       }
   )
   
   # In call_tool(), add handler:
   elif name == "safeway_new_tool":
       # Implementation
   ```

2. **Documentation Updates (REQUIRED):**
   - README.md:
     - Add to "✨ What It Does" features list
     - Add to "🏗️ How It Works → For AI Agents" tool reference
     - Add example usage in "💬 Real Conversations"
     - Update tool count (currently 13)
   
   - MCP_SERVER_GUIDE.md:
     - Add full tool documentation in "Tool Reference" section
     - Include: Purpose, Inputs, Outputs, Example use case
     - Add to examples section
   
   - MCP_QUICKSTART.md:
     - Add to tool list if relevant for quick start

3. **Testing:**
   - Test tool manually via Claude Desktop
   - Verify JSON schema validation
   - Check error handling

### Modifying Existing Tools

1. **Update the tool definition** in `list_tools()`
2. **Update the handler** in `call_tool()`
3. **Update all relevant documentation:**
   - README.md (if behavior significantly changes)
   - MCP_SERVER_GUIDE.md (always)
   - Examples in COOKING_GUIDE.md or RECIPE_GUIDE.md (if applicable)

### Changing Configuration

If environment variables, paths, or configuration format changes:

1. Update `mcp_config_example.json`
2. Update all setup sections in:
   - README.md (Quick Start sections)
   - MCP_QUICKSTART.md (entire guide)
   - MCP_SERVER_GUIDE.md (Installation section)

### Adding New API Endpoints

When adding support for new Safeway API endpoints:

1. **Code Changes:**
   - Add endpoint URL to `SafewayEndpoints` class in `safeway_api.py`
   - Add client method in `SafewayAPIClient` class
   - Consider adding MCP tool to expose it

2. **Documentation Updates:**
   - API_STATUS.md: Document the new endpoint
   - README.md: Mention in features if user-facing
   - MCP_SERVER_GUIDE.md: Document if exposed via MCP tool

## Documentation Style Guidelines

### For README.md

**Tone:** Engaging, casual, personality-driven  
**Structure:** 
- Use emoji section headers (🛒, ✨, 🚀, etc.)
- Dual-audience: "For Humans" and "For AI Agents" subsections
- AI Agent sections in collapsible `<details>` tags
- Real conversation examples over command syntax
- Benefits over features

**Example Good Pattern:**
```markdown
### ✨ What It Does

- **Auto-Clip All Coupons** - Never miss a deal. Claude loads every available coupon with one command.
```

**Example Bad Pattern:**
```markdown
### Features

- Automated offer management system that programmatically interfaces with...
```

### For MCP_SERVER_GUIDE.md

**Tone:** Technical but accessible  
**Structure:**
- Complete tool reference with all details
- Every tool has: Purpose, Inputs, Outputs, Example
- Troubleshooting section with solutions
- Step-by-step installation for all platforms

### For AI Agent Sections

**Format:**
```markdown
<details>
<summary><h3>For AI Agents / LLMs</h3></summary>

**Step 0:** Pre-setup discovery
- Check OS: `uname -s` or `echo %OS%`
- Check Python: `python3 --version`

**Step 1:** Install dependencies
```bash
pip install -r requirements.txt
```

**Step 2:** Configure
...

</details>
```

**Content:**
- Numbered steps (Step 0, Step 1, etc.)
- Bash command blocks ready to execute
- JSON manipulation examples
- Error handling strategies
- Verification procedures

## Testing Requirements

### Before Committing Changes

1. **Python code:**
   ```bash
   # Verify syntax
   python3 -m py_compile safeway_mcp_server.py
   python3 -m py_compile safeway_api.py
   ```

2. **MCP server:**
   ```bash
   # Test it runs without errors
   export SAFEWAY_USERNAME="test@example.com"
   export SAFEWAY_PASSWORD="testpass"
   export SAFEWAY_STORE_ID="2948"
   python3 safeway_mcp_server.py --help  # Should not crash
   ```

3. **Documentation:**
   - Check all links work
   - Verify code blocks have proper syntax highlighting
   - Ensure examples are up to date

### Integration Testing

Test via Claude Desktop after changes:
1. Update your Claude Desktop config
2. Restart Claude
3. Try: "What Safeway offers are available?"
4. Verify the response uses your updated tool

## Common Maintenance Tasks

### Updating Tool Count

When tools are added/removed, update these locations:
- README.md: "13 AI-powered tools" → update number
- MCP_SERVER_GUIDE.md: Tool count in introduction
- PR descriptions and commit messages

### Keeping Examples Fresh

Every 6 months or when major changes occur:
- Test all example commands in README.md
- Verify conversation examples still work
- Update any outdated screenshots or outputs

### API Changes

If Safeway changes their API:
1. Update `SafewayEndpoints` URLs
2. Update authentication flow if needed
3. Add note to API_STATUS.md with date
4. Test all tools still work
5. Update troubleshooting section if new errors occur

## Code Style

### Python

- Use type hints: `def get_offers() -> List[Offer]:`
- Docstrings for all public functions
- Follow PEP 8
- Use dataclasses for data models
- Async for MCP tool handlers

### Documentation

- Use markdown code blocks with language tags
- Emoji headers for visual scanning
- Lists over paragraphs where possible
- Code examples should be copy-pasteable
- Platform-specific instructions clearly labeled

## Version Control

### Commit Messages

Good:
- "Add safeway_get_nutrition tool with full documentation"
- "Update MCP_SERVER_GUIDE.md with new budget planning examples"
- "Fix authentication error handling in safeway_api.py"

Bad:
- "Update docs"
- "Fix bug"
- "Changes"

### Branch Strategy

- Main branch: stable, documented code
- Feature branches: new tools, major changes
- Always update documentation in same commit as code changes

## Security Considerations

### Never Commit

- Real credentials in examples
- Actual store IDs from users
- Access tokens or session data

### Always Document

- What credentials are needed
- Where they should be stored (environment variables)
- Security implications of unofficial API

## Questions?

If you're an AI agent and encounter:
- **Unclear architecture:** Refer to PROJECT_SUMMARY.md
- **API questions:** Check API_STATUS.md
- **Setup issues:** Read MCP_QUICKSTART.md
- **Style questions:** Follow patterns in existing README.md

## Update History

This agents.md file should be updated when:
- Project architecture changes significantly
- New documentation patterns emerge
- Common issues are discovered
- Tool count changes by more than 2

---

**Remember:** The MCP Server is the core functionality. All changes should prioritize MCP compatibility and documentation quality for both human users and AI agents.
