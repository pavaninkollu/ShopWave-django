# ShopWave - E-commerce Platform

ShopWave is a fully functional e-commerce platform built using Django. It offers a seamless shopping experience with secure payment integration via Razorpay.

## Features
- User authentication (Login/Register)
- Product catalog with categories
- Shopping cart and checkout
- Razorpay payment integration
- Order management
- Admin panel for product and order management

## Technologies Used
- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL / SQLite
- **Payment Gateway:** Razorpay
- **Other Tools:** Docker, Kubernetes (optional)

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-username/shopwave.git
   cd shopwave
   ```
2. **Create a Virtual Environment & Install Dependencies:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. **Set Up the Database:**
   ```sh
   python manage.py migrate
   python manage.py createsuperuser  # Create an admin user
   ```
4. **Configure Razorpay:**
   - Sign up at [Razorpay](https://razorpay.com/)
   - Get API keys and add them to `.env` file:
     ```
     RAZORPAY_KEY_ID=your_key_id
     RAZORPAY_KEY_SECRET=your_key_secret
     ```
5. **Run the Development Server:**
   ```sh
   python manage.py runserver
   ```

## Usage
- Visit `http://127.0.0.1:8000/` in your browser.
- Browse products, add them to the cart, and proceed to checkout.
- Make payments securely using Razorpay.
- Admin panel available at `/admin/` for managing orders and products.

## Screenshots
![Homepage](# ShopWave - E-commerce Platform

ShopWave is a fully functional e-commerce platform built using Django. It offers a seamless shopping experience with secure payment integration via Razorpay.

## Features
- User authentication (Login/Register)
- Product catalog with categories
- Shopping cart and checkout
- Razorpay payment integration
- Order management
- Admin panel for product and order management

## Technologies Used
- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL / SQLite
- **Payment Gateway:** Razorpay
- **Other Tools:** Docker, Kubernetes (optional)

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-username/shopwave.git
   cd shopwave
   ```
2. **Create a Virtual Environment & Install Dependencies:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. **Set Up the Database:**
   ```sh
   python manage.py migrate
   python manage.py createsuperuser  # Create an admin user
   ```
4. **Configure Razorpay:**
   - Sign up at [Razorpay](https://razorpay.com/)
   - Get API keys and add them to `.env` file:
     ```
     RAZORPAY_KEY_ID=your_key_id
     RAZORPAY_KEY_SECRET=your_key_secret
     ```
5. **Run the Development Server:**
   ```sh
   python manage.py runserver
   ```

## Usage
- Visit `http://127.0.0.1:8000/` in your browser.
- Browse products, add them to the cart, and proceed to checkout.
- Make payments securely using Razorpay.
- Admin panel available at `/admin/` for managing orders and products.

## Screenshots
![Homepage](                  )
![Cart Page](https://via.placeholder.com/800x400)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss.

## License
This project is licensed under the MIT License.

## Contact
For any queries, reach out to `your-email@example.com`.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss.


## Contact
For any queries, reach out to `your-email@example.com`.
