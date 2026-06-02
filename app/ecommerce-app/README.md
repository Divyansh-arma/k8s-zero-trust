# EcomStore - Python E-commerce Application

A full-featured e-commerce application built with Flask, ready for deployment on AWS Elastic Beanstalk.

## Features

- **User Management**: Registration, login, profile management
- **Product Catalog**: Browse products by category, search functionality
- **Shopping Cart**: Add, remove, update quantities
- **Order Processing**: Complete checkout flow with order tracking
- **Admin Dashboard**: Manage products, categories, and orders
- **Responsive Design**: Works on all devices
- **Payment Ready**: Structured for Stripe integration

## Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python application.py
   ```

3. **Create Admin User**:
   ```bash
   python create_admin.py
   ```
   Default admin credentials:
   - Username: admin
   - Password: admin123

## AWS Elastic Beanstalk Deployment

### Prerequisites
- AWS CLI installed and configured
- Elastic Beanstalk CLI (eb cli) installed

### Deployment Steps

1. **Initialize EB Application**:
   ```bash
   eb init -p python-3.11 ecomstore-app
   ```

2. **Create Environment**:
   ```bash
   eb create ecomstore-prod
   ```

3. **Set Environment Variables**:
   ```bash
   eb setenv SECRET_KEY=your-secret-key-here
   eb setenv STRIPE_PUBLISHABLE_KEY=pk_test_...
   eb setenv STRIPE_SECRET_KEY=sk_test_...
   ```

4. **Deploy**:
   ```bash
   eb deploy
   ```

5. **Create Admin User** (after first deployment):
   ```bash
   eb ssh
   cd /var/app/current
   python create_admin.py
   ```

### Alternative Deployment (Manual)

1. **Create Application Archive**:
   ```bash
   zip -r ecomstore-app.zip . -x "*.git*" "__pycache__/*" "*.pyc"
   ```

2. **Upload to Elastic Beanstalk**:
   - Go to AWS Elastic Beanstalk console
   - Create new application
   - Upload the zip file
   - Configure environment variables in the console

## Environment Variables

Set these environment variables in your deployment:

- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)
- `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
- `STRIPE_SECRET_KEY`: Stripe secret key

## Project Structure

```
├── application.py          # Entry point for Elastic Beanstalk
├── app/                    # Main application package
│   ├── __init__.py        # App factory
│   ├── models.py          # Database models
│   ├── main/              # Main blueprint
│   ├── auth/              # Authentication blueprint
│   ├── admin/             # Admin blueprint
│   ├── cart/              # Shopping cart blueprint
│   └── templates/         # Jinja2 templates
├── requirements.txt       # Python dependencies
├── config.py             # Configuration settings
├── create_admin.py       # Admin user creation script
└── .ebextensions/        # Elastic Beanstalk configuration
```

## Database Schema

The application includes the following models:
- **User**: User accounts and authentication
- **Category**: Product categories
- **Product**: Product catalog
- **CartItem**: Shopping cart items
- **Order**: Customer orders
- **OrderItem**: Individual items within orders

## Admin Access

After deployment, create an admin user using the `create_admin.py` script. The admin interface provides:
- Product management (add, edit, remove)
- Category management
- Order tracking and status updates
- User management
- Sales analytics dashboard

## Payment Integration

The application is structured for Stripe payment processing. To complete payment integration:
1. Set up Stripe account
2. Add Stripe keys to environment variables
3. Implement payment processing in checkout flow
4. Add webhook handling for payment confirmations

## Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session management with Flask-Login
- SQL injection prevention with SQLAlchemy ORM
- Input validation and sanitization

## Customization

The application uses Tailwind CSS for styling, making it easy to customize:
- Modify color schemes in `base.html`
- Update layouts in individual templates
- Add new features by creating additional blueprints

## Support

For deployment assistance or customization needs, refer to the AWS Elastic Beanstalk documentation or Flask deployment guides.