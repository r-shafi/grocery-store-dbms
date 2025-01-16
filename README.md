# Grocery Store Application

[![YouTube](https://img.youtube.com/vi/HwSxZm_Uqr4/0.jpg)](https://www.youtube.com/watch?v=HwSxZm_Uqr4)

## Objective

The Grocery Store Application is a user-friendly platform for managing grocery store operations efficiently. It enables product management, user roles, order processing, and public-facing features to provide a seamless experience for administrators, and customers.

## Features

This application offers role-based access control with tailored features for admins, and customers. Admins can manage products, categories, users, orders, customers and contacts, while customers can browse products, manage their carts, and place orders. Public-facing pages like the homepage, product details, and contact us enhance usability and engagement.

## Technologies and Choices

- **Python**: Backend development for robust logic and integration.
- **Flask**: Lightweight web framework for API and server handling.
- **SQL**: Database management for structured data storage.
- **HTML**: Structuring web content.
- **Tailwind CSS**: Responsive and modern web design.

## Setup Guide

Follow these steps to set up the application locally:

1. **Clone the Repository**

   ```bash
   git clone github.com/r-shafi/grocery-store-dbms
   cd grocery-store-dbms
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database**

   - Ensure your database server is running.
   - Update the database connection string in `configs/config.py`.

5. **Run the Application**

   ```bash
   flask run
   ```

6. **Access the Application**  
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Developed By

- Rayhan Aziz Chowdhury Shafi
- Fatematuj Johura Mim
