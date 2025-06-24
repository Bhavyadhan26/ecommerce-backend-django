# E-commerce Backend (Django)
This is a basic RESTful e-commerce backend built with Django and Django REST Framework.


✅ **Note:** This project contains only the backend logic (APIs and database models).  
🚫 No frontend (HTML/CSS/JS or React/Angular) is included.

## 💡 Features

- 🔐 User Signup/Login (with password hashing)
- 🛍️ Product Listing API
- 🛒 Add to Cart with Quantity Update
- 💳 Checkout and Order Placement
- 📦 Order Tracking (visible in admin panel)
- 🧾 Admin Interface to manage Products, Orders & Users

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
