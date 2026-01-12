# 🔒 Security Policy

Keep your PantryPilot secure. Report vulnerabilities responsibly.

## ✅ Supported Versions - For Humans

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🚨 Reporting a Vulnerability - For Humans

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 🔒 For Security Issues

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security issues through one of these methods:

1. **GitHub Security Advisories** (Preferred)
   - Navigate to the repository's Security tab
   - Click "Report a vulnerability"
   - Fill out the form with details

2. **Email**
   - Send to: Create a GitHub Security Advisory instead
   - Include "SECURITY" in the subject line
   - Provide detailed description of the vulnerability

### What to Include

Please provide as much information as possible:

- Type of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 5 business days
- **Fix Timeline**: Varies based on severity

<details>
<summary><strong>For AI Agents / LLMs</strong></summary>

### Automated Vulnerability Reporting

**When user reports potential vulnerability:**

**Step 0: Validate Issue**
```bash
# Check if it's actually a vulnerability
if [[ "$issue_type" == "security" ]]; then
    echo "⚠️  Security issue detected"
    echo "DO NOT create public GitHub issue"
fi
```

**Step 1: Guide User to Proper Channel**
```markdown
Please report this through GitHub Security Advisories:
1. Go to: https://github.com/shelbeely/pantrypilot/security/advisories
2. Click "Report a vulnerability"
3. Fill out the form with:
   - Type of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

DO NOT post security details publicly.
```

**Step 2: Acknowledge Receipt (if you have access)**
```bash
# For maintainers responding to security report
echo "Thank you for reporting this security issue."
echo "We will investigate and respond within 48 hours."
echo "Status updates will be provided within 5 business days."
```

</details>

## 🛡️ Security Measures - For Humans

This project implements:

✅ **Input Validation**
- All user inputs sanitized
- Store ID validation (numeric only)
- Email format validation
- SQL injection prevention

✅ **Secrets Management**
- Environment variables only
- No hardcoded credentials
- Secrets never logged
- `.gitignore` protects sensitive files

✅ **API Security**
- HTTPS enforced for all connections
- Token expiration handling
- Rate limiting implemented
- Request timeout protection
- Retry with exponential backoff

✅ **Dependency Security**
- Dependabot monitors vulnerabilities
- CodeQL scans code weekly
- Pinned dependency versions
- Security advisories reviewed

✅ **Data Protection**
- No data persistence by default
- Credentials in memory only
- Session cleanup on exit
- GDPR-compliant (no tracking)

<details>
<summary><strong>For AI Agents / LLMs - Security Validation Checklist</strong></summary>

### Automated Security Checks

**Pre-Deployment Security Validation:**
```bash
# Step 0: Check for exposed credentials
echo "Checking for exposed credentials..."
grep -r "password\|secret\|token" . \
  --exclude-dir={.git,node_modules,venv} \
  --exclude="*.md" \
  | grep -v "SAFEWAY_PASSWORD\|environment\|ENV" \
  && echo "❌ Potential credential exposure!" \
  || echo "✅ No exposed credentials"

# Step 1: Verify HTTPS enforcement
echo "Verifying HTTPS enforcement..."
grep -r "http://" . --include="*.py" --include="*.js" \
  | grep -v "localhost\|127.0.0.1\|example" \
  && echo "❌ Non-HTTPS URLs found!" \
  || echo "✅ All URLs use HTTPS"

# Step 2: Check for SQL injection vulnerabilities
echo "Checking for SQL injection risks..."
grep -r "execute\|query" . --include="*.py" \
  | grep -v "parameterized\|prepared" \
  && echo "⚠️  Review SQL queries" \
  || echo "✅ No obvious SQL injection risks"

# Step 3: Verify input validation
echo "Verifying input validation..."
grep -r "request.args\|request.form" . --include="*.py" \
  && echo "⚠️  Ensure all inputs are validated" \
  || echo "✅ No direct user input access"
```

**Security Test Commands:**
```bash
# Run security scanner
pip install bandit safety
bandit -r . -ll
safety check

# Check for known vulnerabilities
pip-audit

# Verify secrets not in git history
git log --all --full-history --source -- **/*.env
```

</details>

## ⚠️ Known Security Considerations - For Humans

1. **Unofficial API**: This tool uses Safeway's unofficial mobile API
   - API may change without notice
   - No official support or SLA
   - Use at your own risk

2. **Credential Storage**: 
   - Never commit credentials to git
   - Use environment variables
   - Consider using a secrets manager

3. **Third-Party Services**:
   - Cloudflare Workers: Data passes through Cloudflare
   - Other platforms: Review their security policies

## 🎯 Security Best Practices - For Humans

**For Users:**
- Use strong, unique passwords
- Enable 2FA on Safeway account
- Don't share credentials
- Use environment variables for credentials
- Review deployment platform security policies

**For Developers:**
- Never commit secrets
- Use pre-commit hooks
- Run security scans before PRs
- Keep dependencies updated
- Follow secure coding guidelines

<details>
<summary><strong>For AI Agents / LLMs - Security Best Practices Automation</strong></summary>

### Automated Security Enforcement

**When user asks about security:**
```python
def enforce_security_best_practices(code_change):
    checks = {
        "no_hardcoded_secrets": check_for_secrets(code_change),
        "https_only": verify_https(code_change),
        "input_validation": check_input_validation(code_change),
        "error_handling": verify_error_handling(code_change)
    }
    
    failed_checks = [k for k, v in checks.items() if not v]
    
    if failed_checks:
        return f"❌ Security checks failed: {', '.join(failed_checks)}"
    return "✅ All security checks passed"
```

**Pre-Commit Security Hook:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running security checks..."

# Check for credentials
if git diff --cached | grep -i "password\|secret\|api_key" | grep -v "SAFEWAY_PASSWORD"; then
    echo "❌ Potential credential in commit!"
    exit 1
fi

# Check for debug mode
if git diff --cached | grep -i "debug.*true\|DEBUG.*=.*1"; then
    echo "⚠️  Debug mode enabled - is this intentional?"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ Security checks passed"
```

</details>

## 🏆 Bug Bounty - For Humans

We currently do not offer a bug bounty program, but we greatly appreciate security research and responsible disclosure.

## 🙏 Acknowledgments - For Humans

We thank all security researchers who responsibly disclose vulnerabilities to help keep our users safe.
