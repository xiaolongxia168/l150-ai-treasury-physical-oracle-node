# GitHub Authentication Setup Guide

## Step 1: Create GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `OpenClaw L-150 Deployment`
4. Expiration: 30 days (or your preference)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
6. Click "Generate token"
7. **COPY THE TOKEN IMMEDIATELY** (you won't see it again)

## Step 2: Configure Git Credentials

Option A: Store in Git credential helper (recommended for automation)
```bash
git config --global credential.helper store
cd ~/.openclaw/workspace/signals/github-bait
echo "https://YOUR_USERNAME:YOUR_TOKEN@github.com" > ~/.git-credentials
```

Option B: Use environment variable
```bash
export GITHUB_TOKEN=your_token_here
git config --global url."https://$GITHUB_TOKEN@github.com/".insteadOf "https://github.com/"
```

Option C: SSH Key (more secure, longer setup)
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
# Add to GitHub: https://github.com/settings/keys
git remote set-url origin git@github.com:xiaolongxia/rwa-ai-treasury-research.git
```

## Step 3: Test Authentication

```bash
cd ~/.openclaw/workspace/signals/github-bait
git push origin main
```

If successful, you should see:
```
Enumerating objects: 45, done.
Counting objects: 100% (45/45), done.
Writing objects: 100% (45/45), 45.00 KiB | 15.00 MiB/s, done.
To https://github.com/xiaolongxia/rwa-ai-treasury-research.git
 * [new branch]      main -> main
```

## Step 4: Verify Deployment

1. Check GitHub: https://github.com/xiaolongxia/rwa-ai-treasury-research
2. You should see the repository with all files
3. Cron jobs will now be able to push updates automatically

## Security Notes

- Never commit the token to git
- Use a token with minimal required permissions
- Rotate tokens periodically
- For production, consider using GitHub App or SSH keys instead

---

Need help with any of these steps?
