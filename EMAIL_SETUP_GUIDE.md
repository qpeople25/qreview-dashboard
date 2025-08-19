# qReview Email System Setup Guide

## Overview
The qReview platform now includes an automated email system that sends welcome emails with login credentials to new users when they're added via bulk upload.

## Features
- ✅ **Welcome Emails**: Professional HTML emails with login credentials
- ✅ **Secure Passwords**: Automatically generated 12-character secure passwords
- ✅ **Bulk Processing**: Handles multiple users in one upload
- ✅ **Error Handling**: Graceful fallback if emails fail
- ✅ **Professional Templates**: Branded emails with clear instructions

## Quick Setup

### 1. Create Environment File
Create a `.env` file in your project root with these settings:

```bash
# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Sender Information
FROM_EMAIL=noreply@yourcompany.com
FROM_NAME=Your Company Name
```

### 2. Configure Email Settings
1. Login as admin (admin@qpeople.com / admin123)
2. Go to Survey tab → Settings tab
3. Expand "Email Configuration"
4. Enter your SMTP details
5. Click "Test Email Configuration" to verify

## Email Provider Setup

### Gmail Setup
1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Use App Password** in SMTP_PASSWORD (not your regular password)

### Outlook/Office 365 Setup
1. **SMTP Server**: `smtp-mail.outlook.com`
2. **Port**: `587`
3. **Username**: Your full email address
4. **Password**: Your regular password (or app password if 2FA enabled)

### Company Email Setup
1. **Check with IT** for SMTP settings
2. **Common servers**: `smtp.company.com`, `mail.company.com`
3. **Ports**: Usually `587` (TLS) or `465` (SSL)
4. **Authentication**: Usually username/password or domain authentication

## How It Works

### Bulk User Upload Process
1. **Admin uploads CSV** with user details
2. **System generates** secure password for each user
3. **User account created** in database
4. **Welcome email sent** automatically with:
   - Login credentials
   - Organization information
   - Platform access instructions
   - Security recommendations

### Email Template Features
- **Professional HTML design** with qReview branding
- **Clear login instructions** with credentials
- **Security notes** about password changes
- **Direct login button** linking to platform
- **Responsive design** for all devices

## Security Features

### Password Generation
- **12-character passwords** using letters and numbers
- **Cryptographically secure** using Python's secrets module
- **Unique per user** - no shared passwords

### Email Security
- **TLS encryption** for SMTP connections
- **App passwords** recommended over regular passwords
- **No password storage** in plain text emails (sent separately)

## Troubleshooting

### Common Issues

**"Email test failed"**
- Check SMTP credentials
- Verify port and server settings
- Ensure 2FA is properly configured (for Gmail)

**"Failed to send email" during bulk upload**
- Users are still created successfully
- Check email configuration
- Verify SMTP server is accessible

**Emails not received**
- Check spam/junk folders
- Verify recipient email addresses
- Test with admin email first

### Testing Steps
1. **Configure email settings** in admin panel
2. **Test email configuration** button
3. **Create single user** to test email flow
4. **Check email delivery** and formatting
5. **Proceed with bulk upload** once confirmed

## Production Deployment

### Environment Variables
For production, set these environment variables:

```bash
export SMTP_SERVER=smtp.yourcompany.com
export SMTP_PORT=587
export SMTP_USERNAME=noreply@yourcompany.com
export SMTP_PASSWORD=your-secure-password
export FROM_EMAIL=noreply@yourcompany.com
export FROM_NAME=Your Company Name
```

### Email Service Recommendations
- **SendGrid**: Professional email delivery service
- **Mailgun**: Reliable email API
- **AWS SES**: Cost-effective for high volume
- **Company SMTP**: Use existing email infrastructure

### Monitoring
- **Email delivery rates** tracking
- **Bounce handling** for invalid emails
- **Log monitoring** for email failures
- **User feedback** on email quality

## Best Practices

### Email Content
- **Clear subject lines** that identify the platform
- **Professional branding** consistent with company
- **Actionable instructions** for next steps
- **Contact information** for support

### Security
- **Use app passwords** for Gmail/Outlook
- **Regular password rotation** for SMTP accounts
- **Monitor email logs** for unusual activity
- **Test with small batches** before large uploads

### User Experience
- **Send emails immediately** after account creation
- **Include clear next steps** in welcome email
- **Provide support contact** for questions
- **Follow up** if users don't login within 24 hours

## Support

### Getting Help
1. **Check email configuration** in admin settings
2. **Test email functionality** with single user
3. **Review error messages** for specific issues
4. **Contact platform admin** for technical support

### Documentation
- **Email configuration** in admin settings
- **Bulk upload process** documentation
- **Troubleshooting guide** for common issues
- **Security best practices** for email setup
