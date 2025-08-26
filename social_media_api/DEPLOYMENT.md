# Deployment Guide

## Prerequisites
- Python 3.13+
- PostgreSQL
- Nginx
- AWS Account (for S3)
- Domain Name (optional but recommended)

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/Bertrand1738/Alx_DjangoLearnLab.git
cd social_media_api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Environment Variables:
- Copy `.env.template` to `.env`
- Fill in all required environment variables

## Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE your_db_name;
CREATE USER your_db_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
```

2. Run migrations:
```bash
python manage.py migrate
```

## AWS S3 Setup

1. Create an S3 bucket:
   - Go to AWS Console > S3
   - Create a new bucket
   - Configure CORS settings
   - Set proper bucket policy

2. Create IAM user:
   - Create user with programmatic access
   - Attach S3FullAccess policy
   - Save access keys for .env file

## Server Setup

1. Install system dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

2. Configure Nginx:
- Copy `nginx.conf` to `/etc/nginx/sites-available/`
- Create symlink: `sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled/`
- Test and restart Nginx

3. Set up Gunicorn:
- Copy `gunicorn.conf.py` to project directory
- Create systemd service file for Gunicorn
- Start and enable the service

## SSL/TLS Setup

1. Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
```

2. Obtain SSL certificate:
```bash
sudo certbot --nginx -d your-domain.com
```

## Deployment Steps

1. Collect static files:
```bash
python manage.py collectstatic --no-input
```

2. Set up the production environment:
```bash
export DJANGO_SETTINGS_MODULE=social_media_api.production_settings
```

3. Start the application:
```bash
sudo systemctl start gunicorn
sudo systemctl start nginx
```

## Monitoring and Maintenance

1. Check logs:
- Nginx logs: `/var/log/nginx/`
- Gunicorn logs: `/var/log/gunicorn/`
- Application logs: `/var/log/django/`

2. Regular Maintenance:
- Update packages: `pip install -r requirements.txt`
- Database backups
- Monitor error reports
- Check server resources

## Troubleshooting

Common issues and solutions:
1. Static files not loading:
   - Check S3 bucket permissions
   - Verify AWS credentials
   - Run collectstatic again

2. 502 Bad Gateway:
   - Check Gunicorn status
   - Verify socket permissions
   - Check error logs

3. Database connection issues:
   - Verify PostgreSQL is running
   - Check database credentials
   - Confirm firewall settings

## Security Checklist

- [ ] DEBUG = False in production
- [ ] Secret key is properly secured
- [ ] Database credentials are secure
- [ ] SSL/TLS is properly configured
- [ ] Security headers are enabled
- [ ] File permissions are correct
- [ ] Firewall is configured
- [ ] Regular security updates
