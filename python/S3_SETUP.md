# S3 Bucket Setup Guide for Villa Ecommerce SDK

## Bucket Naming Recommendations

### Best Practices for Bucket Names

S3 bucket names must follow these rules:
- **3-63 characters long**
- **Lowercase letters, numbers, hyphens, and periods only**
- **Must start and end with a letter or number**
- **Must be globally unique** across all AWS accounts

### Recommended Naming Patterns

For the Villa Ecommerce SDK cache, consider these naming patterns:

1. **Descriptive and Environment-Specific:**
   ```
   villa-ecommerce-sdk-cache-prod
   villa-ecommerce-sdk-cache-dev
   villa-ecommerce-sdk-cache-staging
   ```

2. **With Organization Prefix:**
   ```
   your-org-villa-sdk-cache
   company-villa-cache-prod
   ```

3. **Simple and Clear:**
   ```
   villa-sdk-cache
   villa-market-cache
   villa-api-cache
   ```

4. **With Region Identifier (if using multiple regions):**
   ```
   villa-sdk-cache-us-east-1
   villa-sdk-cache-eu-west-1
   ```

### Example Bucket Names

- `villa-ecommerce-sdk-cache` ✅ (Recommended)
- `villa-market-api-cache-prod` ✅
- `mycompany-villa-sdk-cache` ✅
- `villa-sdk-cache-dev` ✅

## S3 Bucket Policy Configuration

### Step 1: Create the Bucket

```bash
aws s3 mb s3://villa-ecommerce-sdk-cache --region us-east-1
```

### Step 2: Configure Bucket Policy

The bucket policy below allows the SDK to read and write cache files. Replace `YOUR_ACCOUNT_ID` and `YOUR_IAM_ROLE_OR_USER` with your actual values.

#### Option A: IAM User/Role-Based Policy (Recommended)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSDKCacheAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:user/YOUR_IAM_USER"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::villa-ecommerce-sdk-cache/*",
        "arn:aws:s3:::villa-ecommerce-sdk-cache"
      ]
    }
  ]
}
```

#### Option B: IAM Role-Based Policy (for EC2/Lambda)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSDKCacheAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_IAM_ROLE"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::villa-ecommerce-sdk-cache/*",
        "arn:aws:s3:::villa-ecommerce-sdk-cache"
      ]
    }
  ]
}
```

#### Option C: Public Read, Authenticated Write (Less Secure)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::villa-ecommerce-sdk-cache/*"
    },
    {
      "Sid": "AuthenticatedWrite",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:user/YOUR_IAM_USER"
      },
      "Action": [
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::villa-ecommerce-sdk-cache/*"
    }
  ]
}
```

### Step 3: Apply the Policy

#### Using AWS CLI:

```bash
aws s3api put-bucket-policy \
  --bucket villa-ecommerce-sdk-cache \
  --policy file://bucket-policy.json
```

#### Using AWS Console:

1. Go to S3 Console → Your Bucket → Permissions
2. Scroll to "Bucket policy"
3. Click "Edit" and paste the JSON policy
4. Replace placeholders with your actual values
5. Save changes

### Step 4: Configure IAM User/Role Permissions

Your IAM user or role also needs permissions. Attach this policy to your IAM user/role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "s3:HeadObject"
      ],
      "Resource": [
        "arn:aws:s3:::villa-ecommerce-sdk-cache",
        "arn:aws:s3:::villa-ecommerce-sdk-cache/*"
      ]
    }
  ]
}
```

### Step 5: Enable Versioning (Optional but Recommended)

Versioning helps protect against accidental deletion:

```bash
aws s3api put-bucket-versioning \
  --bucket villa-ecommerce-sdk-cache \
  --versioning-configuration Status=Enabled
```

### Step 6: Configure Lifecycle Rules (Optional)

To automatically delete old cache files after a certain period:

```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket villa-ecommerce-sdk-cache \
  --lifecycle-configuration file://lifecycle-config.json
```

Example `lifecycle-config.json`:

```json
{
  "Rules": [
    {
      "Id": "DeleteOldCacheFiles",
      "Status": "Enabled",
      "Prefix": "villa-sdk/",
      "Expiration": {
        "Days": 30
      }
    }
  ]
}
```

## Testing the Setup

After configuring your bucket, test it with:

```python
from villa_ecommerce_sdk import VillaClient

# Initialize with your bucket name
client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")

# This will test cache read/write
products_df = client.get_product_list(branch=1000)
print(f"Fetched {len(products_df)} products")
```

## Security Best Practices

1. **Never make the bucket public** unless absolutely necessary
2. **Use IAM roles** instead of IAM users when possible (for EC2, Lambda, etc.)
3. **Enable bucket encryption**:
   ```bash
   aws s3api put-bucket-encryption \
     --bucket villa-ecommerce-sdk-cache \
     --server-side-encryption-configuration '{
       "Rules": [{
         "ApplyServerSideEncryptionByDefault": {
           "SSEAlgorithm": "AES256"
         }
       }]
     }'
   ```
4. **Enable access logging** to monitor usage
5. **Use least privilege principle** - only grant necessary permissions
6. **Consider using bucket policies** with IP restrictions if accessing from fixed locations

## Troubleshooting

### Error: Access Denied
- Check IAM user/role has correct permissions
- Verify bucket policy allows your principal
- Ensure AWS credentials are configured correctly

### Error: Bucket Not Found
- Verify bucket name is correct (case-sensitive)
- Check you're in the correct AWS region
- Ensure bucket exists in your AWS account

### Error: Invalid Bucket Name
- Bucket name must be globally unique
- Use only lowercase letters, numbers, hyphens, and periods
- Must be 3-63 characters long

## Cost Considerations

S3 pricing is very low for cache storage:
- **Storage**: ~$0.023 per GB/month
- **PUT requests**: $0.005 per 1,000 requests
- **GET requests**: $0.0004 per 1,000 requests

For typical usage (thousands of cache operations per month), costs should be under $1/month.

