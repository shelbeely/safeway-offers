# 🤖 Composite GitHub Actions

Reusable composite actions for the PantryPilot project. These actions reduce duplication across workflows and make CI/CD configuration cleaner and more maintainable.

---

## 📋 Available Actions

### 1. 🐍 Setup Python Environment
**Path:** `.github/actions/setup-python`

Sets up Python with pip caching and installs common dependencies.

**Usage:**
```yaml
- uses: ./.github/actions/setup-python
  with:
    python-version: '3.11'  # Optional, default: '3.11'
    cache-dependencies: 'true'  # Optional, default: 'true'
```

**What it does:**
- Installs specified Python version
- Upgrades pip, setuptools, wheel
- Caches pip dependencies
- Installs requirements.txt if present

---

### 2. 🧪 Run Tests
**Path:** `.github/actions/run-tests`

Runs pytest with coverage reporting and uploads to Codecov.

**Usage:**
```yaml
- uses: ./.github/actions/run-tests
  with:
    python-version: '3.11'  # Required
    upload-coverage: 'true'  # Optional, default: 'true'
    codecov-token: ${{ secrets.CODECOV_TOKEN }}  # Optional

- name: Get coverage
  run: echo "Coverage is ${{ steps.test.outputs.coverage }}%"
```

**Outputs:**
- `coverage`: Coverage percentage as string (e.g., "85.3")

**What it does:**
- Installs pytest and related tools
- Runs pytest with coverage
- Uploads coverage to Codecov (if token provided)
- Uploads coverage artifacts (XML and HTML reports)

---

### 3. 🎨 Code Quality Checks
**Path:** `.github/actions/code-quality`

Runs Black, Flake8, MyPy, and Bandit for Python code quality.

**Usage:**
```yaml
- uses: ./.github/actions/code-quality
  with:
    check-formatting: 'true'  # Optional, default: 'true'
    check-linting: 'true'  # Optional, default: 'true'
    check-types: 'true'  # Optional, default: 'true'
    check-security: 'true'  # Optional, default: 'true'
```

**What it does:**
- Black: Checks code formatting
- Flake8: Lints for style and errors
- MyPy: Type checking
- Bandit: Security vulnerability scanning
- Uploads Bandit report as artifact

---

### 4. 🐳 Docker Build
**Path:** `.github/actions/docker-build`

Builds and optionally pushes Docker images with caching.

**Usage:**
```yaml
- uses: ./.github/actions/docker-build
  with:
    dockerfile: './deployment/docker/Dockerfile'  # Optional
    image-name: 'safeway-mcp'  # Required
    image-tag: 'latest'  # Optional, default: 'latest'
    push: 'false'  # Optional, default: 'false'
    registry-username: ${{ secrets.DOCKER_USERNAME }}  # Optional
    registry-password: ${{ secrets.DOCKER_PASSWORD }}  # Optional
```

**Outputs:**
- `image`: Full image ID

**What it does:**
- Sets up Docker Buildx
- Logs into Docker Hub (if push enabled and credentials provided)
- Builds Docker image with layer caching
- Pushes to registry (if enabled)
- Shows image size

---

### 5. 📝 Generate Changelog
**Path:** `.github/actions/generate-changelog`

Generates formatted changelog from git commit messages using emoji commit format.

**Usage:**
```yaml
- uses: ./.github/actions/generate-changelog
  with:
    previous-tag: 'v1.0.0'  # Optional, auto-detects if omitted
    output-file: 'CHANGELOG.md'  # Optional, default: 'CHANGELOG.md'

- name: Use changelog
  run: echo "${{ steps.changelog.outputs.changelog }}"
```

**Outputs:**
- `changelog`: Full changelog content as string

**What it does:**
- Detects previous tag automatically (or uses provided)
- Groups commits by emoji/type:
  - ✨ Features
  - 🐛 Bug Fixes
  - 📚 Documentation
  - 🔒 Security
  - 🧪 Tests
  - 🎨 Other Changes
- Generates formatted markdown
- Outputs to file and as step output

---

### 6. 📢 Notify
**Path:** `./.github/actions/notify`

Sends notifications to Slack, Discord, or GitHub.

**Usage:**
```yaml
- uses: ./.github/actions/notify
  with:
    service: 'slack'  # Required: slack, discord, or github
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}  # Required for slack/discord
    message: 'Build succeeded! ✅'  # Required
    status: 'success'  # Optional: success, failure, warning
```

**What it does:**
- Slack: Posts formatted message with color based on status
- Discord: Posts simple text message
- GitHub: Comments on PR (if triggered by PR event)

---

## 🎯 Benefits

### For Humans
- 😊 **Cleaner workflows** - Less duplication, easier to read
- 🔧 **Easy maintenance** - Update once, applies everywhere
- 📖 **Self-documenting** - Action names describe what they do
- 🚀 **Faster development** - Copy-paste usage examples

### For AI Agents
- 🤖 **Reusable components** - DRY principle in CI/CD
- 📊 **Consistent behavior** - Same action = same results
- 🔍 **Easier analysis** - Single source of truth
- 🛠️ **Tool-friendly** - Well-defined inputs/outputs

---

## 📚 Examples

### Complete CI Workflow Using Composite Actions
```yaml
name: 🧪 CI Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: ./.github/actions/setup-python
        with:
          python-version: '3.11'
      
      - uses: ./.github/actions/code-quality
      
      - uses: ./.github/actions/run-tests
        with:
          python-version: '3.11'
          codecov-token: ${{ secrets.CODECOV_TOKEN }}
      
      - uses: ./.github/actions/notify
        if: failure()
        with:
          service: 'slack'
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          message: 'CI failed on ${{ github.ref }}'
          status: 'failure'
```

### Release Workflow Using Composite Actions
```yaml
name: 🚀 Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - uses: ./.github/actions/generate-changelog
        id: changelog
      
      - uses: ./.github/actions/docker-build
        with:
          image-name: 'myorg/safeway-mcp'
          image-tag: ${{ github.ref_name }}
          push: 'true'
          registry-username: ${{ secrets.DOCKER_USERNAME }}
          registry-password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          body: ${{ steps.changelog.outputs.changelog }}
```

---

## 🔧 Development

### Creating a New Composite Action

1. **Create directory structure:**
   ```bash
   mkdir -p .github/actions/my-action
   ```

2. **Create action.yml:**
   ```yaml
   name: My Action
   description: Does something useful
   
   inputs:
     my-input:
       description: 'Input description'
       required: true
   
   outputs:
     my-output:
       description: 'Output description'
       value: ${{ steps.step-id.outputs.value }}
   
   runs:
     using: composite
     steps:
       - name: Do something
         id: step-id
         shell: bash
         run: echo "value=result" >> $GITHUB_OUTPUT
   ```

3. **Use in workflow:**
   ```yaml
   - uses: ./.github/actions/my-action
     with:
       my-input: 'test'
   ```

### Best Practices

✅ **Use emoji** in action names for visual scanning
✅ **Add descriptions** to all inputs and outputs
✅ **Provide defaults** for optional inputs
✅ **Use shell: bash** for cross-platform compatibility
✅ **Upload artifacts** for debugging
✅ **Handle errors** gracefully with `|| true` or `continue-on-error`
✅ **Document usage** with examples
✅ **Keep actions focused** - one responsibility per action

---

## 📝 Following Established Guidelines

All composite actions follow project guidelines:

- ✅ **Emoji headers** for visual scanning
- ✅ **Clear descriptions** of purpose
- ✅ **Example-driven** documentation
- ✅ **Error handling** built-in
- ✅ **Artifact uploads** for debugging
- ✅ **Consistent naming** conventions

---

## 🤖 For AI Agents

### Action Discovery
All composite actions are in `.github/actions/*/action.yml`.

### Usage Pattern
```yaml
- uses: ./.github/actions/<action-name>
  with:
    input-name: 'value'
```

### Available Actions
- `setup-python` - Python environment setup
- `run-tests` - Test execution with coverage
- `code-quality` - Code quality checks
- `docker-build` - Docker image building
- `generate-changelog` - Changelog generation
- `notify` - Notifications (Slack/Discord/GitHub)

### Creating Workflows
1. Use composite actions for common tasks
2. Combine multiple actions for complete workflows
3. Add notifications for important events
4. Upload artifacts for debugging

---

## 📄 License

Same as project license. See main LICENSE file.
