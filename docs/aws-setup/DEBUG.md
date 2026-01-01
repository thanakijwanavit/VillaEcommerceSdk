# Debugging OIDC Authentication Issues

If you're still getting "Not authorized to perform sts:AssumeRoleWithWebIdentity" after setting everything up correctly, try these steps:

## Step 1: Verify GitHub Secret

Make sure the secret `AWS_ROLE_ARN` in GitHub matches **exactly**:

```
arn:aws:iam::394922924679:role/deploy-github-action-wallet2
```

**Common mistakes:**
- Extra spaces before/after
- Missing `arn:aws:iam::` prefix
- Wrong account ID
- Wrong role name

## Step 2: Check CloudTrail Logs

View recent authentication attempts:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRoleWithWebIdentity \
  --max-results 10 \
  --region ap-southeast-1 \
  --query 'Events[*].CloudTrailEvent' \
  --output json | jq -r '.[] | {time: .eventTime, error: .errorMessage, sub: .requestParameters.webIdentityToken}'
```

This will show you:
- What repository GitHub is claiming to be from
- The exact error message
- When it happened

## Step 3: Try Permissive Policy (Testing Only)

Temporarily allow ANY GitHub repository to test:

```bash
cd docs/aws-setup
./fix-trust-permissive.sh deploy-github-action-wallet2
```

**⚠️ WARNING**: This allows any GitHub repo. Use only for testing!

If this works, the issue is with the repository name matching. If it still fails, the issue is elsewhere.

## Step 4: Verify Repository Name

The repository name in the trust policy must match **exactly**:

- Check your GitHub repository URL: `https://github.com/thanakijwanavit/VillaEcommerceSdk`
- Username: `thanakijwanavit` (case-sensitive)
- Repo name: `VillaEcommerceSdk` (case-sensitive)
- Format in trust policy: `repo:thanakijwanavit/VillaEcommerceSdk:*`

## Step 5: Check Workflow Permissions

Make sure your workflow has the `id-token: write` permission:

```yaml
permissions:
  id-token: write
  contents: read
```

## Step 6: Verify OIDC Provider Thumbprint

The OIDC provider thumbprint might need updating:

```bash
# Get latest thumbprint
THUMBPRINT=$(echo | openssl s_client -servername token.actions.githubusercontent.com -showcerts -connect token.actions.githubusercontent.com:443 2>/dev/null | openssl x509 -fingerprint -noout -sha1 | tr ':' ' ' | awk '{print $2}')
echo "Latest thumbprint: $THUMBPRINT"

# Current thumbprint in use: 6938fd4d98bab03faadb97b34396831e3780aea1
```

If they don't match, you may need to delete and recreate the OIDC provider (but this is rare).

## Step 7: Check IAM Role Permissions

Verify the role has the necessary permissions:

```bash
aws iam list-attached-role-policies --role-name deploy-github-action-wallet2
aws iam list-role-policies --role-name deploy-github-action-wallet2
```

The role needs permissions for:
- CloudFormation operations
- S3 operations
- IAM operations (to create policies)

## Step 8: Test with AWS CLI

Test assuming the role manually (this won't work from your machine, but shows the command):

```bash
# This will fail from your local machine, but shows what GitHub Actions is trying
aws sts assume-role-with-web-identity \
  --role-arn arn:aws:iam::394922924679:role/deploy-github-action-wallet2 \
  --role-session-name test-session \
  --web-identity-token "test-token"
```

## Common Issues

### Issue: Repository name case mismatch

**Symptom**: Everything looks correct but still fails

**Solution**: GitHub repository names are case-sensitive. Double-check:
- GitHub URL: `https://github.com/thanakijwanavit/VillaEcommerceSdk`
- Trust policy: `repo:thanakijwanavit/VillaEcommerceSdk:*`

### Issue: GitHub Secret has extra characters

**Symptom**: Role ARN looks correct but fails

**Solution**: Copy the ARN exactly, no spaces:
```
arn:aws:iam::394922924679:role/deploy-github-action-wallet2
```

### Issue: Workflow doesn't have id-token permission

**Symptom**: OIDC token not generated

**Solution**: Add to workflow:
```yaml
permissions:
  id-token: write
  contents: read
```

## Still Not Working?

1. Check the exact error message in GitHub Actions logs
2. Look at CloudTrail logs for the specific failure
3. Try the permissive policy to isolate the issue
4. Verify the GitHub repository name matches exactly (case-sensitive)

