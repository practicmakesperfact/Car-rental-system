
# 🏎️ Car Rental System – Django

A secure, feature-rich web application for booking and managing car rentals in Ethiopia. Built with Django, Tailwind CSS, and OCR + Payment integration.

---

## 📌 Key Features

- 🔐 Secure user registration with ID upload and OCR verification
- 📧 Email-based authentication with password reset
- 🚗 Real-time car listings and search functionality
- 📅 Online booking and payment via **Chapa**
- 🧾 Invoice generation and payment confirmation
- 🎁 Loyalty & reward point system for discounts
- 🧭 GPS tracking for car security and admin monitoring
- 💬 Customer reviews and ratings
- 📊 Admin dashboard for car, user, and booking management

---

## 🛠️ Tech Stack

- **Backend**: Django, Python 3.13
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Database**: SQLite3 (can migrate to PostgreSQL (coming soon))
- **OCR**: Tesseract (via `pytesseract`)
- **Payments**: Chapa Payment Gateway

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/practicmakesperfact/car-rental-system.git
cd car-rental-system
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```ini
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=Car Rental <your_email@gmail.com>
CHAPA_SECRET_KEY=your_chapa_secret_key
```

And add `.env` to `.gitignore`.

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

---

## 🔐 Security Highlights

| Feature                           | Status |
|----------------------------------|--------|
| CSRF Protection                  | ✅     |
| Email-based Authentication       | ✅     |
| Password Reset                   | ✅     |
| ID Verification via OCR          | ✅     |
| Chapa Payment Integration        | ✅     |
| Role-based Access Control        | ✅     |
| Input Validation & Sanitization  | ✅     |
| GPS Security Tracking            | ✅     |

---
## 🔐 Secure User Registration

| Feature                           | Status     |
|----------------------------------|------------|
| CSRF Protection                  | ✅ Enabled |
| Unique Email Check               | ✅ Enabled |
| Duplicate Profile Prevention     | ✅ Enabled |
| File Validation (ID images)      | ✅ Enabled |
| OCR Name Matching                | ✅ Enabled |
| Detailed Error Handling          | ✅ Enabled |
| GPS Security Tracking            | ✅ Enabled |
| Account Cleanup on Failure       | ✅ Enabled |
| Chapa Payment Integration        | ✅ Enabled |
| Password Reset                   | ✅ Enabled |


### 👥 Registration Flow

1. User enters name, email, and password,phoneNumber
2. Uploads front and back of ID or passport
3. OCR extracts name and compares with input
4. If matched → account is created and logged in
5. If not → error shown and data discarded

## 🧾 Payment Flow (Chapa)

1. User selects a car and enters booking details.
2. Redirected to **Chapa** payment gateway.
3. After payment, redirected back for server verification.
4. If success → booking confirmed, invoice sent.
5. If fail → user notified and prompted to retry.

---

## 🎁 Loyalty & Rewards

- Earn points for each completed booking
- Points shown in user dashboard
- Redeem for discounts (automatic if eligible)
- Admin can adjust rewards manually

---

## 📄 Password Reset System

- Reset view: `/password-reset/`
- Email sent via SMTP (Gmail or other)
- User confirms via secure link
- Can set a new password immediately

---
### 🧪 Testing Tips

- Try registering with the same email twice
- Try uploading duplicate ID filenames
- Try entering mismatched names on form vs. ID


## 📁 Project Folder Structure

```
car-rental-system/
├── car_rental/
│   └── settings.py, wsgi.py ...
├── media/
├── rental/
│   ├── migrations/
│   ├── templates/
│   │   └── rental/
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── password_reset.html
│   │       └── ...
│   ├── static/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── venv/
├── db.sqlite3
├── .env
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 📄 License – MIT

This project is licensed under the **MIT License**, which means:

- ✅ You can **use**, **copy**, **modify**, **merge**, **publish**, and **distribute** the software freely.
- ❗ You must include the original license text in any distribution.
- 🚫 The author is **not liable** for any damages from using this software.

It’s a permissive and open-source friendly license.


---

## 🙌 Contributions

Pull requests are welcome. If you find a bug or want a new feature, open an issue or submit a PR.

---

## 📧 Contact

For any inquiries or support, feel free to open an issue or email the maintainer.
