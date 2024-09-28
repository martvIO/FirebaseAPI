# 🚀 Firebase Authentication API with FastAPI

Welcome to the **Firebase Authentication API** powered by **FastAPI**! This project allows user registration, login, and account management with the power of Firebase Realtime Database and FastAPI. Get started with a simple `.env` setup and an OAuth2 authentication mechanism. 🎉

## 📁 Project Structure

```bash
.
├── main.py               # The entry point of the FastAPI app 🚀
├── auth.py               # Authentication routes and user management 🔐
├── .env                  # Environment variables 🔑
└── database-key.json     # Firebase service account credentials 🔥
```

## 🛠 How to Get Started

To run this project, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a `.env` file** in the root of your project and add the following:

   ```bash
   SECRET_KEY=your_secret_key
   ```

   - `SECRET_KEY`: This is a cryptographic key used to sign the JWT tokens. You can generate a random key using Python:

     ```python
     import secrets
     print(secrets.token_hex(32))
     ```

3. **Install the required dependencies:**

   Run the following command to install all dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Firebase credentials:**

   Download your Firebase Admin SDK private key file (JSON) from your Firebase project settings and replace the placeholder `database-key.json` with your file.

   Make sure the Firebase database URL is correctly set in the `auth.py` file under this section:

   ```python
   cred = credentials.Certificate("path_to_your_firebase_key.json")
   firebase_admin.initialize_app(cred, {
       'databaseURL': 'https://your-database.firebaseio.com/'
   })
   ```

5. **Run the FastAPI server:**

   Finally, run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

   Your API should be up and running on `http://127.0.0.1:8000`. 🎉

---

## 🔑 Environment Variables

Make sure to set up the following environment variables in your `.env` file:

- `SECRET_KEY`: Your JWT signing secret key.

---

## 📂 File Explanations

### `main.py`

This is the **entry point** of the FastAPI app. It initializes the app and includes the routes defined in the `auth.py` file.

- **Imports** the authentication routes.
- **Includes** the router to handle `/auth`-related requests.

### `auth.py`

The **heart of the authentication system**! This file handles:

- **User Signup**: `/auth/signup`
- **User Login**: `/auth/login`
- **Protected Routes**: Access user details and change account information.
- **JWT Token Creation**: Manages token-based authentication using OAuth2.
- **Password Hashing**: Securely hashes user passwords using `bcrypt`.
- **User Management**: Signup, login, delete accounts, update usernames, and emails.

### `database-key.json`

This file contains your **Firebase service account credentials**. It’s used to authenticate your FastAPI app with Firebase Realtime Database.

⚠️ **Do not share this file**! Make sure it is added to your `.gitignore` file to prevent exposure.

---

## 📋 API Endpoints

### 🚪 **Authentication**

- **POST** `/auth/signup`: Registers a new user.
- **POST** `/auth/login`: Logs in a user and returns a JWT token.

### 🧑‍💼 **User Management**

- **GET** `/auth/users/me`: Returns the current user info (requires token).
- **DELETE** `/auth/delete_account`: Deletes the authenticated user's account.

---

## 🚀 Run the Application

Run the FastAPI server with:

```bash
uvicorn main:app --reload
```

---

## 🛡 Security

- **JWT Tokens** are used to authorize API requests. Make sure you always use your `SECRET_KEY` to sign and validate these tokens.
- Passwords are hashed using `bcrypt` to provide strong protection against attackers. 🔐

---

## 🏗 Future Improvements

- 🔄 Add features like password reset via email.
- 📧 Integrate email verification for new users.
- 🔑 Enhance security by implementing more comprehensive token management (e.g., refresh tokens).

---

## 🤝 Contributions

Feel free to contribute by opening issues or submitting pull requests! Let's make this project even better together! 💪

---

Happy coding! 🎉
