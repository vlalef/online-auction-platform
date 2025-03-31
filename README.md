# Commerce - Online Auction Platform

This is an eBay-like e-commerce auction site built with Django and MySQL. The project enables users to post auction listings, place bids, comment on listings, and add listings to a watchlist.

## Features

- **User Authentication**: Register, login, and logout functionality
- **Listing Creation**: Users can create auction listings with title, description, starting bid, and optional image URL
- **Bidding**: Users can place bids on active listings
- **Comments**: Users can leave comments on listings
- **Watchlist**: Users can add/remove listings to/from their personal watchlist
- **Categories**: Browse listings by category
- **Active/Closed Auctions**: Creators can open or close their auctions

## Technology Stack

- **Backend**: Django
- **Database**: MySQL
- **Frontend**: HTML, Bootstrap

## Prerequisites

- Python 3.x
- Django
- MySQL

## Installation & Setup

### Setting up MySQL

1. **Install MySQL**: Follow the instructions on the [MySQL installation page](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/).
2. **Create a database** via terminal:
    ```bash
    mysql -u root -p
    CREATE DATABASE commerce;
    CREATE USER 'commerceuser'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON commerce.* TO 'commerceuser'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;
    ```

### Setting up the Django Project

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd commerce
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database settings** in `commerce/settings.py`:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'commerce',
            'USER': 'commerceuser',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

5. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser** (optional, for admin access):
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

8. **Open your browser** and navigate to `http://127.0.0.1:8000`

## Usage

1. **Register** a new account or login with existing credentials
2. **Create listings** by filling out the listing form
3. **Browse active listings** on the homepage
4. **Place bids** on active listings
5. **Add listings to watchlist** for later viewing
6. **Comment on listings** to ask questions or provide feedback
7. **Create and browse categories** to organize listings

## Administration

Access the Django admin panel at `/admin` with superuser credentials to:
- Manage users
- Edit/delete listings
- Manage categories
- View and moderate bids and comments
