# HTTPS Deployment Configuration Guide

This document provides comprehensive instructions for configuring HTTPS and secure redirects in production environments.

## Table of Contents
1. [SSL Certificate Setup](#ssl-certificate-setup)
2. [Web Server Configuration](#web-server-configuration)
3. [Django Settings Verification](#django-settings-verification)
4. [Testing and Validation](#testing-and-validation)
5. [Monitoring and Maintenance](#monitoring-and-maintenance)

## SSL Certificate Setup

### Option 1: Let's Encrypt (Free SSL Certificate)

1. **Install Certbot**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install certbot python3-certbot-nginx
   
   # CentOS/RHEL
   sudo yum install certbot python3-certbot-nginx
   
   # macOS
   brew install certbot
   ```

2. **Obtain SSL Certificate**:
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. **Set up automatic renewal**:
   ```bash
   sudo crontab -e
   # Add this line:
   0 2 * * * /usr/bin/certbot renew --quiet
   ```

### Option 2: Commercial SSL Certificate

1. Generate a Certificate Signing Request (CSR)
2. Purchase SSL certificate from a trusted CA
3. Install the certificate on your web server

## Web Server Configuration

### Nginx Configuration

Create or update your Nginx configuration file (`/etc/nginx/sites-available/libraryproject`):

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Certificate Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL Security Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';" always;

    # Django Application Configuration
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /path/to/your/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/your/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Apache Configuration

Create or update your Apache virtual host configuration:

```apache
# HTTP to HTTPS redirect
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS Virtual Host
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/yourdomain.com/chain.pem
    
    # SSL Security
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder on
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # Django Application
    WSGIDaemonProcess libraryproject python-path=/path/to/LibraryProject
    WSGIProcessGroup libraryproject
    WSGIScriptAlias / /path/to/LibraryProject/LibraryProject/wsgi.py
    
    <Directory /path/to/LibraryProject/LibraryProject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    # Static files
    Alias /static /path/to/staticfiles
    <Directory /path/to/staticfiles>
        Require all granted
    </Directory>
    
    # Media files
    Alias /media /path/to/media
    <Directory /path/to/media>
        Require all granted
    </Directory>
</VirtualHost>
```

## Django Settings Verification

### Production Environment Variables

Create a `.env` file for production settings:

```bash
# .env file (keep this secure and out of version control)
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-connection-string
```

### Settings Configuration Checklist

Verify these settings in your production `settings.py`:

- [ ] `DEBUG = False`
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SECURE_HSTS_SECONDS = 31536000`
- [ ] `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- [ ] `SECURE_HSTS_PRELOAD = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `ALLOWED_HOSTS` contains your domain names
- [ ] `SECRET_KEY` uses environment variable

## Testing and Validation

### 1. SSL Certificate Validation

```bash
# Test SSL certificate
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Check certificate expiration
echo | openssl s_client -connect yourdomain.com:443 2>/dev/null | openssl x509 -noout -dates
```

### 2. HTTPS Redirect Testing

```bash
# Test HTTP to HTTPS redirect
curl -I http://yourdomain.com
# Should return 301/302 redirect to https://

# Test HTTPS response
curl -I https://yourdomain.com
# Should return 200 OK
```

### 3. Security Headers Testing

```bash
# Check security headers
curl -I https://yourdomain.com
# Look for: Strict-Transport-Security, X-Frame-Options, etc.
```

### 4. Online Security Testing Tools

- [SSL Labs SSL Test](https://www.ssllabs.com/ssltest/)
- [Security Headers](https://securityheaders.com/)
- [HSTS Preload](https://hstspreload.org/)

### 5. Django Security Test

Run our custom security test:

```bash
python manage.py test_security
```

## Monitoring and Maintenance

### 1. SSL Certificate Monitoring

Set up monitoring for SSL certificate expiration:

```bash
#!/bin/bash
# ssl_check.sh - Check SSL certificate expiration
DOMAIN="yourdomain.com"
DAYS_THRESHOLD=30

EXPIRY_DATE=$(echo | openssl s_client -connect $DOMAIN:443 -servername $DOMAIN 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
CURRENT_EPOCH=$(date +%s)
DAYS_LEFT=$(( ($EXPIRY_EPOCH - $CURRENT_EPOCH) / 86400 ))

if [ $DAYS_LEFT -lt $DAYS_THRESHOLD ]; then
    echo "SSL certificate for $DOMAIN expires in $DAYS_LEFT days!"
    # Send alert email or notification
fi
```

### 2. Security Log Monitoring

Monitor Django security logs:

```bash
# Monitor security.log
tail -f /path/to/LibraryProject/security.log

# Set up log rotation
sudo logrotate -d /etc/logrotate.d/libraryproject
```

### 3. Regular Security Updates

Create a maintenance schedule:

- Weekly: Review security logs
- Monthly: Update dependencies (`pip list --outdated`)
- Quarterly: Security audit and penetration testing
- Annually: SSL certificate renewal (if not automated)

## Troubleshooting

### Common Issues

1. **Mixed Content Warnings**:
   - Ensure all resources (CSS, JS, images) use HTTPS or relative URLs
   - Update `STATIC_URL` and `MEDIA_URL` to use HTTPS

2. **HSTS Issues**:
   - Clear browser HSTS cache: chrome://net-internals/#hsts
   - Test with different browsers/incognito mode

3. **Reverse Proxy Issues**:
   - Verify `SECURE_PROXY_SSL_HEADER` setting
   - Check proxy headers configuration

4. **Certificate Issues**:
   - Verify certificate chain completeness
   - Check certificate permissions and ownership

## Security Best Practices

1. **Regular Updates**:
   - Keep Django and dependencies updated
   - Monitor security advisories

2. **Environment Separation**:
   - Use different settings for development/staging/production
   - Never commit secrets to version control

3. **Access Control**:
   - Restrict server access with firewalls
   - Use strong passwords and SSH keys
   - Implement fail2ban for brute force protection

4. **Backup Strategy**:
   - Regular database backups
   - SSL certificate backups
   - Application code backups

## Deployment Checklist

Before going live:

- [ ] SSL certificate installed and tested
- [ ] Django HTTPS settings configured
- [ ] Web server HTTPS redirect configured
- [ ] Security headers implemented
- [ ] HSTS policy configured
- [ ] Security testing completed
- [ ] Monitoring and alerts set up
- [ ] Backup strategy implemented
- [ ] Documentation updated

## Support and Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
