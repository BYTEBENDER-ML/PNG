# 🚀 Deployment Guide

This guide will help you deploy the Engagement Chatbot to various platforms. Choose the deployment method that best suits your needs.

## 📋 Prerequisites

Before deploying, ensure you have:

- Python 3.11 or higher
- Git installed
- Required platform-specific tools (see individual sections)

## 🛠️ Quick Setup

1. **Clone or download the project**
2. **Make the deployment script executable:**
   ```bash
   chmod +x deploy.sh
   ```

## 🎯 Deployment Options

### 1. Local Development

**Best for:** Development and testing

```bash
# Run the deployment script
./deploy.sh local

# Or manually:
pip install -r requirements.txt
python app.py
```

**Access:** http://localhost:5000

### 2. Docker Deployment

**Best for:** Containerized environments, Kubernetes, cloud platforms

```bash
# Build and run with Docker
./deploy.sh docker

# Or manually:
docker build -t engagement-chatbot .
docker run -p 5000:5000 engagement-chatbot
```

**Access:** http://localhost:5000

### 3. Docker Compose

**Best for:** Local development with additional services

```bash
# Run with Docker Compose
./deploy.sh docker-compose

# Or manually:
docker-compose up -d
```

**Access:** http://localhost:5000

### 4. Heroku Deployment

**Best for:** Quick cloud deployment, free tier available

#### Prerequisites:
- Heroku CLI installed
- Heroku account

#### Deploy:
```bash
# Deploy to Heroku
./deploy.sh heroku

# Or manually:
heroku create your-app-name
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set DEBUG=False
git push heroku main
```

**Access:** https://your-app-name.herokuapp.com

### 5. Railway Deployment

**Best for:** Modern cloud deployment, easy setup

#### Prerequisites:
- Railway CLI installed
- Railway account

#### Deploy:
```bash
# Deploy to Railway
./deploy.sh railway

# Or manually:
railway login
railway init
railway up
```

**Access:** Provided by Railway dashboard

### 6. Render Deployment

**Best for:** Free tier deployment, easy GitHub integration

1. **Fork this repository to your GitHub account**
2. **Go to [Render](https://render.com) and create an account**
3. **Click "New Web Service"**
4. **Connect your GitHub repository**
5. **Configure the service:**
   - **Name:** engagement-chatbot
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. **Add environment variables:**
   - `SECRET_KEY`: Generate a random key
   - `DEBUG`: False
7. **Deploy**

### 7. Vercel Deployment

**Best for:** Serverless deployment, global CDN

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Follow the prompts and deploy**

### 8. Google Cloud Run

**Best for:** Scalable container deployment

1. **Install Google Cloud CLI**
2. **Build and deploy:**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/engagement-chatbot
   gcloud run deploy --image gcr.io/YOUR_PROJECT_ID/engagement-chatbot --platform managed
   ```

## 🔧 Environment Variables

Configure these environment variables for production:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Flask secret key | Auto-generated | Yes |
| `DATABASE_PATH` | SQLite database path | `engagement_data.db` | No |
| `DEBUG` | Debug mode | `False` | No |
| `SESSION_COOKIE_SECURE` | Secure cookies | `False` | No |
| `PORT` | Application port | `5000` | No |

## 📊 Health Checks

The application includes health check endpoints:

- **Health Check:** `GET /health`
- **API Status:** `GET /api/status`

## 🔒 Security Considerations

### Production Security Checklist:

- [ ] Change default `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Enable `SESSION_COOKIE_SECURE=True` (for HTTPS)
- [ ] Configure proper CORS headers
- [ ] Use HTTPS in production
- [ ] Set up proper logging
- [ ] Configure database backups
- [ ] Set up monitoring and alerts

### Environment Variables for Security:

```bash
# Production settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

## 📈 Monitoring and Logging

### Built-in Monitoring:

The application includes:
- Health check endpoints
- Request logging
- Error tracking
- Session monitoring

### External Monitoring:

Consider adding:
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Uptime monitoring
- Database monitoring

## 🔄 Database Management

### SQLite (Default):
- File-based database
- Good for small to medium applications
- Backup by copying the database file

### PostgreSQL (Recommended for production):
1. **Update requirements.txt:**
   ```
   psycopg2-binary==2.9.7
   ```

2. **Update database configuration in chatbot.py**

3. **Set environment variable:**
   ```bash
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

## 🚨 Troubleshooting

### Common Issues:

1. **Port already in use:**
   ```bash
   # Change port
   export PORT=8000
   python app.py
   ```

2. **Database permission errors:**
   ```bash
   # Ensure write permissions
   chmod 755 data/
   ```

3. **Docker build fails:**
   ```bash
   # Clean and rebuild
   docker system prune -a
   docker build --no-cache -t engagement-chatbot .
   ```

4. **Heroku deployment fails:**
   ```bash
   # Check logs
   heroku logs --tail
   
   # Ensure all files are committed
   git add .
   git commit -m "Update deployment"
   git push heroku main
   ```

### Debug Mode:

For troubleshooting, enable debug mode:
```bash
export DEBUG=True
python app.py
```

## 📞 Support

If you encounter issues:

1. **Check the logs:**
   ```bash
   # Local
   python app.py
   
   # Docker
   docker logs container_name
   
   # Heroku
   heroku logs --tail
   ```

2. **Verify environment variables:**
   ```bash
   # Check current environment
   python -c "import os; print(os.environ.get('SECRET_KEY', 'Not set'))"
   ```

3. **Test the application:**
   ```bash
   # Run tests
   ./deploy.sh test
   ```

## 🎉 Success!

Once deployed, your engagement chatbot will be available at the provided URL. The application includes:

- ✅ Real-time engagement monitoring
- ✅ Smart intervention system
- ✅ Break management
- ✅ Usage analytics
- ✅ REST API endpoints
- ✅ Health monitoring
- ✅ Error handling

## 🔄 Updates and Maintenance

### Updating the Application:

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Redeploy:**
   ```bash
   # For Docker
   docker-compose down
   docker-compose up -d --build
   
   # For Heroku
   git push heroku main
   
   # For Railway
   railway up
   ```

### Database Migrations:

The application automatically handles database schema changes. For major updates:

1. **Backup existing data**
2. **Deploy new version**
3. **Verify data integrity**

---

**Happy Deploying! 🚀**

For more information, check the main [README.md](README.md) file.
