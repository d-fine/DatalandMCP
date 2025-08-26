# AWS Deployment with GitHub Actions

This document explains how to set up automated deployment to AWS using GitHub Actions.

## Required GitHub Secrets

Configure the following secrets in your GitHub repository settings (`Settings > Secrets and variables > Actions`):

### AWS Configuration
- `AWS_ACCESS_KEY_ID` - AWS access key ID for your deployment user
- `AWS_SECRET_ACCESS_KEY` - AWS secret access key for your deployment user  
- `AWS_REGION` - AWS region where your EC2 instance is located (e.g., `us-east-1`)

### EC2 Instance Configuration
- `EC2_HOST` - Public IP address or domain name of your EC2 instance
- `EC2_USER` - SSH username for your EC2 instance (usually `ubuntu` for Ubuntu AMI)
- `EC2_SSH_PRIVATE_KEY` - Private SSH key content (entire key including headers)

### Application Configuration
- `DATALAND_API_KEY` - Your Dataland API key

## Setting Up AWS EC2 Instance

1. **Launch EC2 Instance**:
   - Recommended: `t3.large` (8GB RAM, 2 vCPUs)
   - OS: Ubuntu 22.04 LTS
   - Storage: 20-30 GB gp3
   - Security Group: Allow SSH (22), HTTP (8000), and Custom (8080)

2. **Create SSH Key Pair**:
   ```bash
   # Generate new key pair locally
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/datalandmcp-deploy
   
   # Copy public key to EC2 instance
   ssh-copy-id -i ~/.ssh/datalandmcp-deploy.pub ubuntu@YOUR_EC2_IP
   ```

3. **Add private key to GitHub Secrets**:
   Copy the entire content of your private key file to the `EC2_SSH_PRIVATE_KEY` secret:
   ```bash
   cat ~/.ssh/datalandmcp-deploy
   ```

## Deployment Triggers

The deployment workflow runs:

### Automatic Triggers
- **Push to main branch** - Automatically deploys to production
- **Excludes**: Documentation changes (*.md files, docs/ folder)

### Manual Triggers
- **workflow_dispatch** - Manual deployment via GitHub Actions UI
- **Options**:
  - `environment`: Choose between `production` or `staging`
  - `purge_volume`: Option to purge Open Web UI volume (⚠️ removes all user data)

## Using the Deployment

### Manual Deployment
1. Go to `Actions` tab in your GitHub repository
2. Select `Deploy to AWS` workflow
3. Click `Run workflow`
4. Choose options:
   - **Environment**: production/staging
   - **Purge volume**: Check if you want to reset Open Web UI data

### Monitoring Deployment
- The workflow includes health checks for both services
- Displays deployment summary with service URLs
- Provides clear success/failure notifications

## Post-Deployment Access

After successful deployment, access your services:
- **Open Web UI**: `http://YOUR_EC2_IP:8080`
- **MCP Server Docs**: `http://YOUR_EC2_IP:8000/DatalandMCP/docs`

## Troubleshooting

### Common Issues

1. **SSH Connection Failed**:
   - Verify EC2 security group allows SSH from GitHub Actions IPs
   - Check private key format in GitHub secret
   - Ensure EC2 instance is running

2. **Docker Installation Failed**:
   - The workflow auto-installs Docker if missing
   - Check EC2 instance has sufficient permissions

3. **Health Checks Failed**:
   - Services may need more time to start
   - Check EC2 instance resources (memory/CPU)
   - Verify Dataland API key is valid

4. **Volume Issues**:
   - Use `purge_volume: true` to reset Open Web UI data
   - Check available disk space on EC2 instance

### Debug Commands

SSH into your EC2 instance to debug:
```bash
# Check container status
cd /opt/datalandmcp
docker compose ps

# View logs
docker compose logs dataland-mcp-server
docker compose logs open-webui

# Check disk space
df -h

# Check system resources
free -h
top
```

## Security Notes

- Never commit secrets to your repository
- Use GitHub Environments for additional protection
- Regularly rotate AWS access keys and SSH keys
- Consider using AWS IAM roles instead of access keys
- Monitor AWS CloudTrail for deployment activities