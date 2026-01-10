# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 🔒 For Security Issues

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security issues through one of these methods:

1. **GitHub Security Advisories** (Preferred)
   - Navigate to the repository's Security tab
   - Click "Report a vulnerability"
   - Fill out the form with details

2. **Email**
   - Send to: security@safeway-mcp-project.example
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

### Security Measures

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

### Known Security Considerations

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

### Security Best Practices

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

### Bug Bounty

We currently do not offer a bug bounty program, but we greatly appreciate security research and responsible disclosure.

### Acknowledgments

We thank all security researchers who responsibly disclose vulnerabilities to help keep our users safe.
