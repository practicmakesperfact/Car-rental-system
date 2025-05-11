
# 🏎️ Car Rental System – Django

A secure and fully functional web application for booking and managing car rentals. Includes user registration with ID verification, login/logout, and an admin panel.

---

## 📌 Features

- 🚗 Car listing and booking
- 🔐 Secure user registration with ID upload and OCR verification
- 📬 Email-based authentication 
- 📂 Image handling for ID/passport uploads
- 📊 Admin dashboard for managing cars and users

---

## 🛠️ Tech Stack

- **Backend**: Django, SQLite3
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **OCR**: Tesseract (for ID text extraction)

---

## ⚙️ Installation

### 1. Clone the repository:

```bash
git clone https://github.com/practicmakesperfect/car-rental-system.git
cd car-rental-system
```

### 2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser:

```bash
python manage.py createsuperuser
```

### 6. Run the server:

```bash
python manage.py runserver
```

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
| Account Cleanup on Failure       | ✅ Enabled |

### 👥 Registration Flow

1. User enters name, email, and password,phoneNumber
2. Uploads front and back of ID or passport
3. OCR extracts name and compares with input
4. If matched → account is created and logged in
5. If not → error shown and data discarded

### 🧪 Testing Tips

- Try registering with the same email twice
- Try uploading duplicate ID filenames
- Try entering mismatched names on form vs. ID

---

## 📁 Project Folder Structure

```
car-rental-system/
├── car_rental/
│   └── settings.py, wsgi.py ...
├── media/
├── rental/
│   ├── __pycache__/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── middleware.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── static/
│   ├── css/
│   └── images/
├── venv/
├── db.sqlite3
├── manage.py
├── README.md
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

Pull requests are welcome! If you find a bug or have a suggestion, open an issue or PR.

---

## 📧 Contact

For any inquiries or support, feel free to open an issue or email the maintainer.
