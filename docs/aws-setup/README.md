# AWS Setup for GitHub Actions

This directory contains setup scripts and documentation for configuring GitHub Actions to deploy to AWS.

## Quick Start

### Option 1: Use Existing Role (Recommended if you already have one)

```bash
cd docs/aws-setup
./use-existing-role.sh arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME YOUR_GITHUB_USERNAME VillaEcommerceSdk
```

**Example:**
```bash
./use-existing-role.sh arn:aws:iam::394922924679:role/deploy-github-action-wallet2 thanakijwanavit VillaEcommerceSdk
```

### Option 2: Create New Role

```bash
cd docs/aws-setup
./setup-aws-oidc.sh YOUR_GITHUB_USERNAME VillaEcommerceSdk
```

Then add the Role ARN to GitHub Secrets:
- Repository → Settings → Secrets → Actions
- Add secret: `AWS_ROLE_ARN` = (Role ARN from script output)

## Files

- **SETUP.md** - Main setup guide (OIDC, no access keys)
- **use-existing-role.sh** - Configure existing IAM role for GitHub Actions ⭐
- **setup-aws-oidc.sh** - Create new IAM role and setup OIDC
- **fix-oidc-trust.sh** - Quick fix for OIDC trust policy issues
- **TROUBLESHOOTING.md** - Troubleshooting guide for OIDC errors
- **AWS_SETUP.md** - Detailed OIDC setup documentation
- **AWS_IAM_SETUP.md** - IAM access keys setup (alternative)
- **QUICK_SETUP.md** - Quick reference

## Troubleshooting

If you get "Not authorized to perform sts:AssumeRoleWithWebIdentity":

```bash
cd docs/aws-setup
./fix-oidc-trust.sh YOUR_GITHUB_USERNAME VillaEcommerceSdk
```

This will update the trust policy with the correct repository name. See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for detailed help.

## Recommended: Use OIDC

Use `setup-aws-oidc.sh` for the secure, keyless setup. No access keys needed!

