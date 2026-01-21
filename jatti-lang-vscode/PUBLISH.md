# 🚀 Publish Your Extension to VS Code Marketplace

## Step 1: Install vsce
```powershell
npm install -g vsce
```

## Step 2: Create Publisher Account
1. Go to: https://marketplace.visualstudio.com/manage
2. Sign in with Microsoft account
3. Click "Create publisher"
4. Enter publisher name (e.g., "jatti-lang", "singh-dev")

## Step 3: Generate Personal Access Token
1. Go to: https://dev.azure.com/
2. Click your profile → Personal access tokens
3. Create new token:
   - Name: "Jatti Publishing"
   - Scopes: Check "Publish"
4. **Copy and save the token** (shown only once!)

## Step 4: Login to vsce
```powershell
cd "c:\Users\Mr.Singh\Desktop\jatti-lang - Copy\jatti-lang-vscode"
vsce login your-publisher-name
# Paste your token when prompted
```

## Step 5: Package the Extension
```powershell
vsce package
# Creates: jatti-lang-0.1.0.vsix
```

## Step 6: Publish!
```powershell
vsce publish
```

**Wait 5-10 minutes** for it to appear in marketplace.

## Step 7: Verify
1. Go to: https://marketplace.visualstudio.com/
2. Search: "Jatti Language"
3. You should see your extension!

---

## Commands Reference

```powershell
# Install vsce (one time)
npm install -g vsce

# Login (one time)
vsce login your-publisher-name

# Package locally
vsce package

# Publish to marketplace
vsce publish

# Show all versions
vsce ls your-publisher-name.jatti-lang
```

---

**Your extension is ready to publish!** 🎉
