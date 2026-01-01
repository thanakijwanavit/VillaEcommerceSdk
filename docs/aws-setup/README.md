# AWS Setup for GitHub Actions

This directory contains setup scripts and documentation for configuring GitHub Actions to deploy to AWS.

## Quick Start

```bash
cd docs/aws-setup
./setup-aws-oidc.sh YOUR_GITHUB_USERNAME VillaEcommerceSdk
```

Then add the Role ARN to GitHub Secrets:
- Repository → Settings → Secrets → Actions
- Add secret: `AWS_ROLE_ARN` = (Role ARN from script output)

## Files

- **SETUP.md** - Main setup guide (OIDC, no access keys)
- **setup-aws-oidc.sh** - Automated OIDC setup script
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

