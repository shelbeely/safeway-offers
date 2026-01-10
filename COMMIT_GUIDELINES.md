# 📝 Commit Message Guidelines

Write commit messages that are helpful for both humans and AI agents.

## 🎯 Format - For Humans

**Structure:** `<emoji> <type>: <description>`

**Example:** `✨ feat: Add recipe recommendation tool`

### Emoji Reference

| Emoji | Type | When to Use |
|-------|------|-------------|
| ✨ | `feat` | New feature or capability |
| 🐛 | `fix` | Bug fix |
| 📚 | `docs` | Documentation only changes |
| 🔒 | `security` | Security improvements or fixes |
| 🧪 | `test` | Adding or updating tests |
| ♻️ | `refactor` | Code refactoring (no functionality change) |
| 🎨 | `style` | Formatting, whitespace, code style |
| ⚡ | `perf` | Performance improvements |
| 🚀 | `deploy` | Deployment configuration or scripts |
| 🔧 | `config` | Configuration file changes |
| 🌐 | `i18n` | Internationalization or localization |
| ♿ | `a11y` | Accessibility improvements |
| 🔥 | `remove` | Removing code or files |
| 🚑 | `hotfix` | Critical hotfix |
| 💚 | `ci` | CI/CD pipeline changes |
| 📦 | `deps` | Dependency updates |
| 🏗️ | `build` | Build system changes |
| 👷 | `chore` | Maintenance tasks |

### Real Examples

**Good:**
```
✨ feat: Add weekly meal planning tool
🐛 fix: Handle authentication timeout gracefully
📚 docs: Update README with Fly.io deployment guide
🔒 security: Add input validation for store ID parameter
🧪 test: Add integration tests for recipe recommendations
♻️ refactor: Extract authentication logic into separate module
🚀 deploy: Add Docker Compose configuration
```

**Bad:**
```
Update stuff
Fixed bug
Changes
WIP
asdf
```

### Multi-Line Format

For complex changes, use detailed format:

```
<emoji> <type>: <subject line (max 72 chars)>

<body explaining what changed and why>

<footer with issue references>
```

**Example:**
```
✨ feat: Add budget meal planning feature

Implements meal planning within user-specified budgets:
- Filters recipes by total cost
- Calculates cost per serving
- Suggests ingredient substitutions
- Tracks spending against budget

Closes #42
Related to #38
```

## 📏 Rules - For Humans

1. **Use Present Tense** - "Add feature" not "Added feature"
2. **Be Concise** - Subject line under 72 characters
3. **Start with Emoji** - Makes git history scannable
4. **Capitalize After Colon** - Consistent formatting
5. **No Period** - Subject line doesn't need ending punctuation
6. **Explain Why** - Body should explain motivation, not just what

<details>
<summary><strong>For AI Agents / LLMs</strong></summary>

## Automated Commit Message Generation

### Step 0: Analyze Changes

```bash
# Get list of changed files
changed_files=$(git diff --cached --name-only)

# Determine commit type
if echo "$changed_files" | grep -q "\.md$"; then
    type="docs"
    emoji="📚"
elif echo "$changed_files" | grep -q "test"; then
    type="test"
    emoji="🧪"
elif echo "$changed_files" | grep -q "Dockerfile\|docker-compose\|\.yml$"; then
    type="deploy"
    emoji="🚀"
elif echo "$changed_files" | grep -q "SECURITY\|security"; then
    type="security"
    emoji="🔒"
else
    type="feat"  # Default to feature
    emoji="✨"
fi
```

### Step 1: Generate Subject Line

```python
def generate_commit_subject(changed_files, changes_summary):
    """Generate commit subject following guidelines"""
    
    # Determine type and emoji
    if any('.md' in f for f in changed_files):
        if 'SECURITY' in changes_summary:
            emoji, type_name = '🔒', 'security'
        else:
            emoji, type_name = '📚', 'docs'
    elif 'test' in changes_summary.lower():
        emoji, type_name = '🧪', 'test'
    elif any('fix' in c.lower() for c in changes_summary):
        emoji, type_name = '🐛', 'fix'
    elif 'deploy' in changes_summary.lower():
        emoji, type_name = '🚀', 'deploy'
    else:
        emoji, type_name = '✨', 'feat'
    
    # Generate description (max 60 chars for prefix room)
    description = extract_key_change(changes_summary)
    description = description[:60] if len(description) > 60 else description
    
    return f"{emoji} {type_name}: {description}"

def extract_key_change(summary):
    """Extract the most important change from summary"""
    # Remove common words
    important_words = [w for w in summary.split() 
                      if w.lower() not in ['the', 'a', 'an', 'to', 'for', 'with']]
    
    # Focus on action verbs
    if important_words:
        action = important_words[0]
        if action.lower() in ['add', 'adding', 'added']:
            action = 'Add'
        elif action.lower() in ['fix', 'fixing', 'fixed']:
            action = 'Fix'
        elif action.lower() in ['update', 'updating', 'updated']:
            action = 'Update'
        
        return action + ' ' + ' '.join(important_words[1:])
    
    return summary
```

### Step 2: Validate Format

```bash
# Validate commit message format
validate_commit_message() {
    local message="$1"
    
    # Check for emoji at start
    if ! echo "$message" | grep -q "^[[:emoji:]]"; then
        echo "❌ Missing emoji at start"
        return 1
    fi
    
    # Check for type
    if ! echo "$message" | grep -qE "^.+ (feat|fix|docs|security|test|refactor|style|perf|deploy|config|i18n|a11y|remove|hotfix|ci|deps|build|chore):"; then
        echo "❌ Invalid or missing type"
        return 1
    fi
    
    # Check length
    subject=$(echo "$message" | head -n1)
    if [ ${#subject} -gt 72 ]; then
        echo "⚠️  Subject line too long (${#subject} > 72)"
        return 1
    fi
    
    echo "✅ Commit message format valid"
    return 0
}
```

### Step 3: Generate Body (if needed)

```python
def generate_commit_body(detailed_changes):
    """Generate detailed commit body"""
    
    body_parts = []
    
    # Group changes by type
    if detailed_changes['added']:
        body_parts.append("Added:\n" + "\n".join(f"- {c}" for c in detailed_changes['added']))
    
    if detailed_changes['changed']:
        body_parts.append("Changed:\n" + "\n".join(f"- {c}" for c in detailed_changes['changed']))
    
    if detailed_changes['fixed']:
        body_parts.append("Fixed:\n" + "\n".join(f"- {c}" for c in detailed_changes['fixed']))
    
    if detailed_changes['removed']:
        body_parts.append("Removed:\n" + "\n".join(f"- {c}" for c in detailed_changes['removed']))
    
    return "\n\n".join(body_parts)
```

### Step 4: Example Automation

```bash
#!/bin/bash
# Auto-generate commit message based on changes

# Get changed files
files=$(git diff --cached --name-only)
stats=$(git diff --cached --stat)

# Determine type
if echo "$files" | grep -q "test"; then
    emoji="🧪"
    type="test"
    action="Add"
elif echo "$files" | grep -q "\.md$"; then
    emoji="📚"
    type="docs"
    action="Update"
elif echo "$files" | grep -q "security\|SECURITY"; then
    emoji="🔒"
    type="security"
    action="Improve"
else
    emoji="✨"
    type="feat"
    action="Add"
fi

# Extract main file changed
main_file=$(echo "$files" | head -n1 | sed 's/.*\///' | sed 's/\..*//')

# Generate message
message="$emoji $type: $action $main_file functionality"

echo "Generated commit message:"
echo "$message"
echo ""
echo "Use this message? (y/n)"
read -r response

if [[ "$response" == "y" ]]; then
    git commit -m "$message"
else
    echo "Edit your commit message:"
    git commit
fi
```

### Reference Table for AI Selection

```python
COMMIT_TYPE_MAP = {
    # File patterns -> (emoji, type, default_action)
    r'\.md$': ('📚', 'docs', 'Update'),
    r'test.*\.py$': ('🧪', 'test', 'Add'),
    r'SECURITY': ('🔒', 'security', 'Improve'),
    r'Dockerfile|docker-compose': ('🚀', 'deploy', 'Update'),
    r'\.yml$|\.yaml$': ('🔧', 'config', 'Update'),
    r'requirements\.txt|package\.json': ('📦', 'deps', 'Update'),
    r'\.github/workflows': ('💚', 'ci', 'Update'),
    # Default
    r'.*': ('✨', 'feat', 'Add')
}

def select_commit_type(files):
    """Select appropriate commit type based on files"""
    import re
    
    for pattern, (emoji, type_name, action) in COMMIT_TYPE_MAP.items():
        if any(re.search(pattern, f) for f in files):
            return emoji, type_name, action
    
    return '✨', 'feat', 'Add'
```

</details>

## 🔍 Verification - For Humans

Before committing, ask yourself:

1. ✅ Does the emoji match the change type?
2. ✅ Is the subject line under 72 characters?
3. ✅ Does it explain WHAT changed?
4. ✅ Does the body (if present) explain WHY?
5. ✅ Will this be clear in 6 months?
6. ✅ Could someone revert this based on the message alone?

## 🛠️ Tools - For Humans

### Git Hooks

Add to `.git/hooks/commit-msg`:

```bash
#!/bin/bash
# Validate commit message format

commit_msg=$(cat "$1")

# Check for emoji
if ! echo "$commit_msg" | grep -qP "^[\p{Emoji}]"; then
    echo "❌ Commit message must start with an emoji"
    echo "See COMMIT_GUIDELINES.md for reference"
    exit 1
fi

# Check for type
if ! echo "$commit_msg" | grep -qE " (feat|fix|docs|security|test|refactor|style|perf|deploy|config|i18n|a11y|remove|hotfix|ci|deps|build|chore):"; then
    echo "❌ Commit message must include a type"
    echo "See COMMIT_GUIDELINES.md for reference"
    exit 1
fi

exit 0
```

### VS Code Extension

Install: **Conventional Commits** extension for guided commit messages.

### Command Line Alias

Add to `.bashrc` or `.zshrc`:

```bash
alias gc='git commit -m'
alias gcf='git commit -m "✨ feat: "'
alias gcd='git commit -m "📚 docs: "'
alias gcb='git commit -m "🐛 fix: "'
alias gcs='git commit -m "🔒 security: "'
```

## 📚 Why These Guidelines? - For Humans

**Benefits:**

1. **Visual Scanning** - Emojis make git history easy to scan
2. **Consistent Format** - Everyone follows same pattern
3. **Better Changelogs** - Auto-generate from commit messages
4. **Easier Rollbacks** - Clear what each commit does
5. **Team Communication** - Commit messages document decisions
6. **AI-Friendly** - Tools can parse and automate based on commits

## 🌟 Examples by Scenario - For Humans

**Adding a new feature:**
```
✨ feat: Add ingredient substitution suggestions
```

**Fixing a bug:**
```
🐛 fix: Prevent crash when API returns empty response
```

**Updating documentation:**
```
📚 docs: Add troubleshooting section for authentication errors
```

**Security improvement:**
```
🔒 security: Add rate limiting to prevent API abuse
```

**Adding tests:**
```
🧪 test: Add unit tests for recipe recommendation logic
```

**Refactoring code:**
```
♻️ refactor: Simplify offer loading logic
```

**Deployment configuration:**
```
🚀 deploy: Add health check endpoint for Kubernetes
```

**Performance optimization:**
```
⚡ perf: Cache authentication tokens to reduce API calls
```

---

Made with 💙 for developers who appreciate good commit messages.
