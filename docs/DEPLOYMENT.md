# Deployment Guide

This guide provides step-by-step instructions for deploying the Expense Tracker application to various platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Deployment](#local-development-deployment)
- [Azure Web App Deployment](#azure-web-app-deployment)
- [Docker Deployment](#docker-deployment)
- [Heroku Deployment](#heroku-deployment)
- [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
- [Production Considerations](#production-considerations)

## Prerequisites

Before deploying, ensure you have:
- Python 3.7 or higher installed
- Git installed
- Access to the deployment platform (Azure, Heroku, AWS, etc.)
- Basic knowledge of command line operations

## Local Development Deployment

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/expense-tracker.git
   cd expense-tracker
   ```

2. **Create and activate virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   # or
   ./run.sh
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Environment Variables

For production deployments, set these environment variables:

```bash
export FLASK_APP=app.py
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export DATABASE_URL=sqlite:///expenses.db  # or your database URL
```

## Azure Web App Deployment

### Method 1: GitHub Actions (Automated)

This repository includes a pre-configured GitHub Actions workflow for automatic deployment.

**Setup Steps:**

1. **Create Azure Web App**
   ```bash
   az webapp create \
     --resource-group <resource-group-name> \
     --plan <app-service-plan-name> \
     --name <webapp-name> \
     --runtime "PYTHON|3.9"
   ```

2. **Configure GitHub Secrets**
   
   In your GitHub repository, go to Settings > Secrets and add:
   
   - `AZURE_CREDENTIALS`: Azure service principal credentials (JSON format)
     ```json
     {
       "clientId": "<client-id>",
       "clientSecret": "<client-secret>",
       "subscriptionId": "<subscription-id>",
       "tenantId": "<tenant-id>"
     }
     ```
   - `AZURE_WEBAPP_NAME`: Your Azure Web App name
   - `AZURE_RESOURCE_GROUP`: Your Azure resource group name

3. **Push to main/master branch**
   
   The workflow will automatically:
   - Run tests
   - Build the application
   - Deploy to Azure
   - Initialize the database

### Method 2: Azure CLI (Manual)

1. **Login to Azure**
   ```bash
   az login
   ```

2. **Create resource group**
   ```bash
   az group create --name expense-tracker-rg --location eastus
   ```

3. **Create App Service plan**
   ```bash
   az appservice plan create \
     --name expense-tracker-plan \
     --resource-group expense-tracker-rg \
     --sku B1 \
     --is-linux
   ```

4. **Create Web App**
   ```bash
   az webapp create \
     --resource-group expense-tracker-rg \
     --plan expense-tracker-plan \
     --name expense-tracker-app \
     --runtime "PYTHON|3.9"
   ```

5. **Deploy using deployment script**
   ```bash
   ./azure_deploy.sh
   ```

6. **Configure startup command**
   ```bash
   az webapp config set \
     --resource-group expense-tracker-rg \
     --name expense-tracker-app \
     --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
   ```

### Method 3: Azure Portal (GUI)

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Create a new Web App
3. Configure:
   - Runtime: Python 3.9
   - Operating System: Linux
   - Region: Choose nearest
4. Go to Deployment Center
5. Connect to your GitHub repository
6. Select the main/master branch
7. Azure will automatically build and deploy

## Docker Deployment

### Create Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Build and Run

```bash
# Build the image
docker build -t expense-tracker .

# Run the container
docker run -d -p 5000:5000 --name expense-tracker-app expense-tracker

# Access at http://localhost:5000
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./expenses.db:/app/expenses.db
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
```

Run with:
```bash
docker-compose up -d
```

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Create Procfile**
   ```
   web: gunicorn app:app
   ```

2. **Create runtime.txt**
   ```
   python-3.9.16
   ```

3. **Login to Heroku**
   ```bash
   heroku login
   ```

4. **Create Heroku app**
   ```bash
   heroku create expense-tracker-app
   ```

5. **Add buildpack**
   ```bash
   heroku buildpacks:set heroku/python
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **Initialize database**
   ```bash
   heroku run python -c "from app import db; db.create_all()"
   ```

8. **Open the app**
   ```bash
   heroku open
   ```

## AWS Elastic Beanstalk

### Prerequisites
- AWS account
- EB CLI installed

### Steps

1. **Initialize EB application**
   ```bash
   eb init -p python-3.9 expense-tracker
   ```

2. **Create environment**
   ```bash
   eb create expense-tracker-env
   ```

3. **Deploy**
   ```bash
   eb deploy
   ```

4. **Open the app**
   ```bash
   eb open
   ```

## Production Considerations

### Security

1. **Change Secret Key**
   ```python
   import secrets
   app.secret_key = secrets.token_hex(32)
   ```

2. **Use Environment Variables**
   ```python
   import os
   app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
   ```

3. **HTTPS Only**
   - Configure SSL certificates
   - Force HTTPS redirects

### Database

1. **Production Database**
   - Replace SQLite with PostgreSQL/MySQL for production
   - Use managed database services (Azure Database, RDS)

2. **Database Configuration**
   ```python
   # For PostgreSQL
   app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
   ```

### Performance

1. **Use Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn --workers 4 --bind 0.0.0.0:8000 app:app
   ```

2. **Enable Caching**
   - Use Redis for session storage
   - Implement view caching

3. **Static File Serving**
   - Use CDN for static assets
   - Configure proper caching headers

### Monitoring

1. **Application Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

2. **Error Tracking**
   - Integrate Sentry or similar service
   - Monitor application errors

3. **Performance Monitoring**
   - Use Azure Application Insights
   - Configure New Relic or DataDog

### Backup

1. **Database Backups**
   ```bash
   # SQLite backup
   cp expenses.db expenses.db.backup
   
   # Automated backups for production databases
   ```

2. **Configuration Backups**
   - Version control all configuration
   - Document environment variables

### Scaling

1. **Horizontal Scaling**
   - Use load balancers
   - Deploy multiple instances

2. **Vertical Scaling**
   - Increase server resources as needed

### Health Checks

Add a health check endpoint:

```python
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200
```

Configure platform health checks to use this endpoint.

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Check Python version compatibility
   - Verify all dependencies are installed
   - Review application logs

2. **Database errors**
   - Ensure database tables are created
   - Check database connection string
   - Verify permissions

3. **Static files not loading**
   - Configure static file serving
   - Check file paths
   - Verify CORS settings if using CDN

### Logs

- **Local**: Check console output
- **Azure**: `az webapp log tail --name <app-name> --resource-group <rg-name>`
- **Heroku**: `heroku logs --tail`
- **Docker**: `docker logs <container-id>`

## Rollback

### Azure
```bash
az webapp deployment slot swap \
  --name <app-name> \
  --resource-group <rg-name> \
  --slot staging
```

### Heroku
```bash
heroku rollback
```

## Continuous Deployment

The repository includes a GitHub Actions workflow (`.github/workflows/cicd.yml`) that:
1. Runs tests on every push
2. Deploys to Azure on push to main/master
3. Validates deployment health

Customize the workflow as needed for your deployment pipeline.

## Support

For deployment issues:
- Check the [troubleshooting section](#troubleshooting)
- Review platform-specific documentation
- Open an issue in the GitHub repository
