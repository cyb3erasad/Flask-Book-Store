# 📚 Online Bookstore - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Database Models](#database-models)
6. [Installation Guide](#installation-guide)
7. [Configuration](#configuration)
8. [Blueprints & Routes](#blueprints--routes)
9. [User Guide](#user-guide)
10. [Admin Guide](#admin-guide)
11. [Troubleshooting](#troubleshooting)

---

## Project Overview

**Online Bookstore** is a full-featured e-commerce web application for selling books online. It provides a complete shopping experience with user authentication, cart management, order processing, customer reviews, and a comprehensive admin panel for managing inventory and orders.

### Key Highlights
- 🛍️ Complete shopping cart functionality
- 👤 User authentication & authorization
- 📦 Order management system
- ⭐ Customer review & rating system
- 🎨 Modern, responsive UI with Tailwind CSS
- 🔐 Secure payment processing (Cash on Delivery)
- 📊 Admin dashboard with analytics
- 🔍 Search functionality

---

## Features

### Customer Features
- **Browse Books**: View all available books with images, prices, and stock status
- **Search**: Search books by title or author
- **Book Details**: View detailed information including description, binding type, and customer reviews
- **Shopping Cart**: Add/remove books, adjust quantities
- **Checkout**: Complete order with shipping details
- **Order Tracking**: View order history and status
- **Reviews**: Rate and review purchased books (1-5 stars)
- **User Authentication**: Secure login/signup system

### Admin Features
- **Dashboard**: Overview of sales, revenue, and inventory
- **Book Management**: Add, edit, delete books with image upload
- **Order Management**: View all orders, update order status
- **Inventory Tracking**: Monitor stock levels and low stock alerts
- **Analytics**: Top selling books, recent orders, revenue tracking
- **User Management**: View registered users

---

## Technology Stack

### Backend
- **Framework**: Flask (Python 3.x)
- **Database**: SQLAlchemy ORM with MYSQL
- **Authentication**: Flask-Login
- **Migrations**: Flask-Migrate
- **Security**: Werkzeug password hashing

### Frontend
- **CSS Framework**: Tailwind CSS 3.x
- **Icons**: Font Awesome 6.4
- **JavaScript**: Vanilla JS (ES6+)
- **Animations**: AOS (Animate On Scroll)
- **Responsive**: Mobile-first design

### File Upload
- **Image Storage**: Local filesystem
- **Allowed Formats**: PNG, JPG, JPEG
- **Max Size**: 5MB

---

## Project Structure

```
online-bookstore/
│
├── app/
│   ├── __init__.py              # App factory
│   ├── models.py                # Database models
│   ├── extension.py             # Flask extensions
│   │
│   ├── auth/                    # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── decorators.py
│   │
│   ├── books/                   # Books blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── cart/                    # Cart blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── orders/                  # Orders blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── reviews/                 # Reviews blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── admin/                   # Admin blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── book_routes.py
│   │   └── decorators.py
│   │
│   ├── static/                  # Static files
│   │   ├── uploads/
│   │   │   └── books/           # Book cover images
│   │   └── css/
│   │
│   └── templates/               # HTML templates
│       ├── home.html
│       ├── book_detail.html
│       ├── cart.html
│       ├── checkout.html
│       ├── my_orders.html
│       ├── order_details.html
│       ├── login.html
│       ├── register.html
│       └── admin/
│           ├── dashboard.html
│           ├── add_book.html
│           ├── manage_books.html
│           ├── admin_order.html
│           └── admin_order_details.html
│
├── migrations/                  # Database migrations
├── config.py                    # Configuration
├── run.py                       # Application entry point
└── requirements.txt             # Dependencies
```

---

## Database Models

### User Model
```python
class User(db.Model):
    id = Integer (Primary Key)
    full_name = String(100)
    email = String(120) - Unique
    password = String(200) - Hashed
    is_admin = Boolean - Default: False
    created_at = DateTime
```

### Books Model
```python
class Books(db.Model):
    id = Integer (Primary Key)
    title = String(200)
    author = String(100)
    price = Float
    stock = Integer
    binding = String(50) - (Paperback/Hardcover/eBook/Audiobook)
    description = Text
    image = String(200) - Image path
    created_at = DateTime
```

### Order Model
```python
class Order(db.Model):
    id = Integer (Primary Key)
    user_id = Foreign Key -> User
    first_name = String(100)
    last_name = String(100)
    country = String(100)
    street_address = String(200)
    appartment = String(100)
    city = String(100)
    state = String(100)
    phone = String(20)
    email = String(120)
    sub_total = Float
    shipping_fee = Float
    total_amount = Float
    status = String(50) - (Pending/Processing/Shipped/Delivered/Cancelled)
    payment_method = String(50)
    payment_status = String(50)
    created_at = DateTime
```

### Order_Item Model
```python
class Order_Item(db.Model):
    id = Integer (Primary Key)
    order_id = Foreign Key -> Order
    book_id = Foreign Key -> Books
    quantity = Integer
    price = Float
    created_at = DateTime
```

### Reviews Model
```python
class Reviews(db.Model):
    id = Integer (Primary Key)
    user_id = Foreign Key -> User
    book_id = Foreign Key -> Books
    rating = Integer (1-5)
    review_text = Text
    created_at = DateTime
    updated_at = DateTime
```

---

## Configuration

### config.py
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///bookstore.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads/books'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
```

### Shipping Configuration
- **Fixed Shipping Fee**: Rs 250.00 (defined in `cart/routes.py`)

---

## Blueprints & Routes

### Books Blueprint (`/`)
- `GET /` - List all books and top selling books
- `GET /search` - Search books by title/author
- `GET /book/<int:book_id>` - Book detail page

### Auth Blueprint (`/auth`)
- `GET|POST /auth/register` - User registration
- `GET|POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Cart Blueprint (`/`)
- `GET /add-to-cart/<int:book_id>` - Add book to cart
- `GET /cart` - View shopping cart
- `GET /remove-from-cart/<int:book_id>` - Remove from cart
- `GET /checkout` - Checkout page (requires login)
- `POST /place-order` - Process order

### Orders Blueprint (`/`)
- `GET /my-orders` - User's order history (requires login)
- `GET /order/<int:order_id>` - Order details (requires login)

### Reviews Blueprint (`/reviews`)
- `POST /reviews/add/<int:book_id>` - Add review (requires login)
- `POST /reviews/edit/<int:review_id>` - Edit review (requires login)
- `GET /reviews/delete/<int:review_id>` - Delete review (requires login)

### Admin Blueprint (`/admin`)
- `GET /admin/dashboard` - Admin dashboard (requires admin)
- `GET|POST /admin/add-book` - Add new book
- `GET /admin/manage-book` - Manage all books
- `GET /admin/delete-book/<int:book_id>` - Delete book
- `GET /admin/orders` - View all orders
- `GET /admin/order/<int:order_id>` - Order details
- `GET /admin/order/<int:order_id>/status/<string:new_status>` - Update order status

---

## User Guide

### 1. Browsing Books
- Visit the homepage to see featured and all available books
- Use the search bar to find specific books by title or author
- Click on any book card to view detailed information

### 2. Adding to Cart
- On the book detail page, select quantity
- Click "Add to Cart" button
- Cart icon shows the number of items

### 3. Checkout Process
1. Click the cart icon to review your items
2. Adjust quantities using +/- buttons
3. Click "Proceed to Checkout" (requires login)
4. Fill in shipping information
5. Review order summary
6. Click "Place Order (COD)"
7. Order confirmation displayed

### 4. Tracking Orders
- Navigate to "My Orders" from the navbar
- View all past and current orders
- Click "View Full Details" to see order specifics
- Track order status (Pending → Processing → Shipped → Delivered)

### 5. Writing Reviews
1. Go to a book detail page
2. Click on "Customer Reviews" tab
3. Select star rating (1-5)
4. Write optional review text
5. Click "Submit Review"
6. Edit or delete your reviews anytime

---

## Admin Guide

### 1. Accessing Admin Panel
- Login with admin credentials
- You'll be redirected to the admin dashboard automatically

### 2. Dashboard Overview
The dashboard displays:
- **Total Books**: Number of books in inventory
- **Total Users**: Registered customers
- **Total Orders**: All orders placed
- **Total Revenue**: Sum of approved/paid orders
- **Recent Orders**: Last 10 orders
- **Top Selling Books**: Top 5 bestsellers
- **Low Stock Alerts**: Books with stock ≤ 5

### 3. Managing Books

#### Adding Books
1. Click "Add Book" in sidebar
2. Fill in required information:
   - Title *
   - Author *
   - Price (Rs) *
   - Stock Quantity *
   - Binding Type (Paperback/Hardcover/eBook/Audiobook)
   - Description (optional)
   - Book Cover Image * (PNG/JPG/JPEG, max 5MB)
3. Click "Add Book"

#### Managing Books
1. Click "Manage Books" in sidebar
2. View all books with images, prices, and stock
3. Use delete button (trash icon) to remove books
4. Confirm deletion (also deletes the image file)

### 4. Managing Orders

#### Viewing All Orders
1. Click "All Orders" in sidebar
2. Filter by status: All, Pending, Processing, Shipped, Delivered, Cancelled
3. View customer details, order items, and totals

#### Updating Order Status
1. Click "View Details" on any order OR use "Update Status" dropdown
2. Select new status:
   - **Pending**: Order received, awaiting processing
   - **Processing**: Order being prepared
   - **Shipped**: Order dispatched
   - **Delivered**: Order completed (auto-updates payment to "Approved")
   - **Cancelled**: Order cancelled (auto-updates payment to "Cancelled")
3. Status updates are immediate

#### Order Details
- Full customer information
- Shipping address
- All order items with quantities and prices
- Payment information
- Print invoice functionality

---

#### Cart Session Structure
```python
session['cart'] = {
    'book_id': quantity,
    '1': 2,      # Book ID 1, Quantity 2
    '5': 1,      # Book ID 5, Quantity 1
}
```

### Flash Message Categories
- `success` - Green background (successful actions)
- `danger` - Red background (errors)
- `warning` - Yellow background (warnings)
- `info` - Blue background (informational)

### Order Status Flow
```
Pending → Processing → Shipped → Delivered
    ↓
Cancelled (can be set from any status)
```

### Payment Status Auto-Update
- Status changed to **Delivered** → Payment Status = "Approved"
- Status changed to **Cancelled** → Payment Status = "Cancelled"

---

## Troubleshooting

### Common Issues

#### 1. Database Migration Errors
```bash
# Remove migrations folder
rm -rf migrations/

# Re-initialize
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 2. Image Upload Not Working
- Check `UPLOAD_FOLDER` path exists: `app/static/uploads/books`
- Verify file permissions
- Ensure file size < 5MB
- Check allowed extensions: PNG, JPG, JPEG

#### 3. Login Issues
- Clear browser cookies/cache
- Check if user exists in database
- Verify password hashing is working

#### 4. Admin Access Denied
```python
# Set is_admin = True for user
flask shell
>>> from app.models import User
>>> from app.extension import db
>>> user = User.query.filter_by(email='user@example.com').first()
>>> user.is_admin = True
>>> db.session.commit()
```

#### 5. Reviews Not Showing
- Verify `Reviews` model is imported (not `Review`)
- Check database has reviews table
- Ensure `reviews`, `avg_rating`, `user_review` passed to template

#### 6. Cart Not Persisting
- Sessions require `SECRET_KEY` to be set
- Check browser allows cookies
- Session data stored server-side

---

## Color Palette

The application uses a consistent color scheme:

```css
Main Background: #FCF8F8
Card Background: #FBEFEF
Highlight Background: #F9DFDF
Accent (Primary): #F5AFAF
Primary Text: #3A2E2E
Secondary Text: #4A3A3A
Muted Text: #7A6A6A
```

---

## Security Considerations

1. **Password Security**
   - Passwords hashed using Werkzeug's `generate_password_hash`
   - Never store plain text passwords

2. **Session Security**
   - Use strong `SECRET_KEY` in production
   - Sessions are server-side only

3. **File Upload Security**
   - Only allowed file types: PNG, JPG, JPEG
   - File size limit: 5MB
   - Filenames sanitized using `secure_filename()`

4. **Access Control**
   - `@login_required` decorator for authenticated routes
   - `@admin_required` decorator for admin-only routes
   - Authorization checks on sensitive operations

---

## Future Enhancements

Potential features to add:
- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Email notifications for orders
- [ ] Wishlist functionality
- [ ] Advanced search filters (genre, price range, publication date)
- [ ] Book recommendations based on purchase history
- [ ] Coupon/discount system
- [ ] Multi-image support for books
- [ ] Pagination for book listings
- [ ] Export orders to CSV/PDF
- [ ] SMS notifications for order updates
- [ ] Social media login (OAuth)
- [ ] Book categories/genres
- [ ] Featured/bestseller tags
- [ ] Related books suggestions

---

## Credits

**Developed by**: Asad Nadeem
**Date**: 3/10/2026
**Framework**: Flask
**Design**: Tailwind CSS

---
