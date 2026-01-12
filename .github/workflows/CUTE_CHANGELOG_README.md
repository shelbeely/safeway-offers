# 🎀 Cute Auto-Changelog & Release Notes

Automatically generates adorable, user-friendly release notes from merged PRs!

---

## ✨ Features

### 🎯 What It Does

**Automatically generates:**
- 📋 **Grouped changelog** by type (features, fixes, docs, etc.)
- 💝 **Non-dev friendly section** - Plain English for users
- ⚠️ **Breaking changes section** - Important changes highlighted
- 🎀 **Cute formatting** - Emojis and friendly language
- 📝 **Updated CHANGELOG.md** - Keeps project history

### 🤖 Automation

**Triggers:**
- ✅ When PR is merged to main
- ✅ When version tag is pushed (v*.*.*)
- ✅ Manual workflow dispatch

**Actions:**
1. Parse merged PR titles and labels
2. Group by type (feat/fix/docs/chore/security/etc.)
3. Identify breaking changes
4. Generate user-friendly descriptions
5. Update CHANGELOG.md
6. Create GitHub release (on tags)

---

## 📝 PR Title Format (Required!)

### Format
```
<emoji> <type>: <description>
```

### Examples
```
✨ feat: Add weekly meal planning with budget tracking
🐛 fix: Handle authentication timeout gracefully
📚 docs: Update deployment guide for Cloudflare Workers
🔒 security: Add input validation for store ID
⚡ perf: Optimize product search algorithm
🧪 test: Add integration tests for MCP server
```

### Available Types

| Emoji | Type | Description | In Changelog |
|-------|------|-------------|--------------|
| ✨ | `feat` | New features | ✨ Features |
| 🐛 | `fix` | Bug fixes | 🐛 Bug Fixes |
| 📚 | `docs` | Documentation | 📚 Documentation |
| 🔒 | `security` | Security improvements | 🔒 Security |
| ⚡ | `perf` | Performance improvements | ⚡ Performance |
| 🎨 | `style` | Code style/formatting | 🎨 Style & Refactoring |
| ♻️ | `refactor` | Code refactoring | 🎨 Style & Refactoring |
| 🧪 | `test` | Test additions/changes | 🧪 Tests |
| 🔧 | `chore` | Maintenance tasks | 🔧 Chores |
| 🚀 | `deploy` | Deployment changes | 🔧 Chores |

---

## 🎀 Example Output

### Generated Release Notes
```markdown
# 🎀 What's New & Cute!

**Released:** January 10, 2026

## ⚠️ Breaking Changes (Important!)

_These changes might affect how you use the tool. Please read carefully! 💙_

- **⚠️ feat: Change authentication flow to OAuth 2.0** [#123](https://github.com/user/repo/pull/123) by @developer

## 💝 What Changed for You (Non-Dev Friendly)

_Here's what's different in plain English:_

- 🎯 Add weekly meal planning with budget tracking [#124](https://github.com/user/repo/pull/124)
- 🎯 Now works on your phone with Cloudflare deployment [#125](https://github.com/user/repo/pull/125)
- 🎯 Find cheapest ingredients automatically [#126](https://github.com/user/repo/pull/126)

## ✨ Features

- ✨ feat: Add weekly meal planning with budget tracking [#124](https://github.com/user/repo/pull/124) by @developer
- ✨ feat: Add Cloudflare Workers deployment [#125](https://github.com/user/repo/pull/125) by @developer

## 🐛 Bug Fixes

- 🐛 fix: Handle authentication timeout gracefully [#127](https://github.com/user/repo/pull/127) by @developer

## 📚 Documentation

- 📚 docs: Add deployment comparison guide [#128](https://github.com/user/repo/pull/128) by @developer

---

_Made with 💝 by your friendly grocery assistant bot!_

**Full Changelog**: https://github.com/user/repo/compare/v1.0.0...v1.1.0
```

---

## ⚠️ Breaking Changes Detection

### Automatic Detection
Breaking changes are detected when:
1. PR has `breaking` label
2. PR title contains `⚠️` emoji
3. PR body contains "BREAKING" or "BREAKING CHANGE"

### How to Mark Breaking Changes
```
# Option 1: Add emoji to title
⚠️ feat: Change authentication method

# Option 2: Add "breaking" label to PR

# Option 3: Add to PR description
BREAKING CHANGE: Authentication now requires OAuth 2.0
```

---

## 💝 Non-Dev Friendly Section

### What It Does
Translates technical changes into plain English for users who aren't developers.

### Selection Criteria
Includes PRs that have:
- `user-facing` label
- `enhancement` label
- Are in "Features" or "Bug Fixes" categories

### Simplification
- Removes technical prefixes: `✨ feat:`, `🐛 fix:`, etc.
- Shows only user-impactful changes
- Limits to top 10 most recent
- Uses friendly language

---

## 🔧 Configuration

### Required Secrets
None! Uses `GITHUB_TOKEN` automatically.

### Optional: Add Labels
Enhance changelog grouping by adding these labels to PRs:
- `user-facing` - Appears in non-dev section
- `breaking` - Highlighted in breaking changes
- `enhancement` - Included in non-dev section
- `skip-changelog` - Skips PR in changelog

### Customize Categories
Edit `.github/workflows/cute-release-notes.yml`:
```python
categories = {
    '✨ Your Category': [],
    '🎨 Another Category': [],
}

emoji_map = {
    '🎉': '✨ Your Category',
    'party': '✨ Your Category',
}
```

---

## 📊 Workflow Details

### Files Modified
- `CHANGELOG.md` - Prepends new release notes
- `RELEASE_NOTES.md` - Temporary file for each release
- GitHub Release - Created for version tags

### Artifacts Uploaded
- `cute-release-notes` - Contains RELEASE_NOTES.md and updated CHANGELOG.md

### Commit Message
```
📝 docs: Update CHANGELOG.md with cute release notes

Auto-generated from merged PRs
```

---

## 🎯 Benefits

### For Humans
- 😊 **Readable changelogs** - Emojis and clear language
- 💝 **Non-technical section** - Users understand what changed
- ⚠️ **Breaking changes clear** - Important updates highlighted
- 🎀 **Cute and friendly** - Makes releases fun!

### For AI Agents
- 🤖 **Structured format** - Easy to parse
- 📊 **Categorized changes** - Grouped by type
- 🔍 **Metadata preserved** - PR numbers, authors, labels
- 🛠️ **Automation-ready** - No manual work needed

---

## 🚀 Usage

### Merge a PR
1. Title your PR correctly: `✨ feat: Add awesome feature`
2. Merge to main
3. Changelog automatically updates! 🎉

### Create a Release
1. Push a version tag: `git tag v1.1.0 && git push --tags`
2. Workflow runs automatically
3. GitHub release created with cute notes! 🎀

### Manual Trigger
1. Go to Actions → 🎀 Cute Release Notes
2. Click "Run workflow"
3. Select branch
4. Generated notes appear as artifact

---

## 📝 PR Title Checker

### Automatic Validation
PR title format is validated automatically on:
- PR opened
- PR edited
- PR synchronized (new commits)
- PR reopened

### Helpful Comments
If title format is wrong, bot comments with:
- ✅ Correct format examples
- 📋 Available types
- 💡 Why it matters
- 🎯 How to fix

### Skip Validation
Add these labels to skip:
- `skip-changelog`
- `bot`

---

## 🎨 Examples from Real World

### Before (Manual Release Notes)
```
## Version 1.1.0

- PR #123
- Fixed bug
- Added stuff
- Updated docs
```

### After (Cute Auto-Changelog)
```
# 🎀 What's New & Cute!

**Released:** January 10, 2026

## 💝 What Changed for You

- 🎯 Now you can plan a whole week of meals with budget tracking!
- 🎯 Works on your phone thanks to Cloudflare deployment
- 🎯 Finds the cheapest ingredients automatically

## ✨ Features

- ✨ feat: Add weekly meal planning [#124] by @chef-bot
- ✨ feat: Add Cloudflare Workers deployment [#125] by @deploy-bot

---

_Made with 💝 by your friendly grocery assistant bot!_
```

---

## 📚 Following Established Guidelines

All generated content follows project guidelines:
- ✅ **Emoji headers** for visual scanning
- ✅ **Dual-audience** - Technical AND user-friendly sections
- ✅ **Clear structure** - Easy to skim
- ✅ **Example-driven** - Real PR links
- ✅ **Cute personality** - Friendly bot messages

---

## 🤝 Contributing

### Add New Category
1. Edit `cute-release-notes.yml`
2. Add to `categories` dict
3. Add emoji mapping
4. Test with workflow dispatch

### Change Detection Logic
Edit the Python script in `cute-release-notes.yml` to customize:
- Breaking change detection
- Non-dev change selection
- Title simplification rules

### Customize Cute Messages
Edit footer and headers in the Python script:
```python
changelog.append("_Made with 💝 by YOUR MESSAGE!_")
```

---

## 📄 License

Same as project license. Uses GitHub API for automation.
