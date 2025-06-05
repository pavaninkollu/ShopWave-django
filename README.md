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



![E-commerce-Site (7)](https://github.com/user-attachments/assets/9dc50d50-b520-45a4-86f1-25bcc2b280cc)
![E-commerce-Site (8)](https://github.com/user-attachments/assets/708704b8-149c-4f92-871a-572e5ba5092d)
![E-commerce-Site (11)](https://github.com/user-attachments/assets/381ad547-d0a5-4f85-89d2-3d8bcc514545)
![E-commerce-Site (12)](https://github.com/user-attachments/assets/0fed6b6a-42a0-4542-a3c1-b1d9e223e27a)
![E-commerce-Site (13)](https://github.com/user-attachments/assets/833a3755-df4c-463f-a1d7-8b74eb449ade)
![E-commerce-Site (9)](https://github.com/user-attachments/assets/ca23a3a8-4caa-4ebd-aa69-2042a928225e)



![E-commerce-Site (14)](https://github.com/user-attachments/assets/582cf6fb-eee1-4cb6-9817-5d42a41ca7f7)

## 📽️ Demo Video

<video width="700" controls>
  <source src="assets/E-commerce Site (1).mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss.



## Contact
For any queries, reach out to `pavankumarinkollu@gmail.com`.

