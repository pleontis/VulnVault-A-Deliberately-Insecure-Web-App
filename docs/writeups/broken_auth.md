# Broken Authentication Vulnerability Writeup

---

## 🔍 Overview

Broken Authentication occurs when an application incorrectly implements login, session management, or password handling, allowing attackers to compromise accounts and impersonate users. Common flaws include weak session secrets, predictable credentials, and lack of brute-force protections.

---

## 💥 Location in VulnVault

- **Route:** `/login`
- **Issues Identified:**
  - **Hardcoded session secret key** in `app.py`:
    ```python
    app.secret_key = "dev"
    ```
  - **No brute-force protection**: unlimited login attempts are allowed.
  - **No MFA**, CAPTCHA, or account lockout.

---

## 🧪 Proof of Concept

1. Run a simple brute-force script with a list of usernames and passwords.
2. Successfully log in with weak or guessed credentials (e.g., `admin:admin`).
3. Inspect cookies:
    ```bash
    curl -I http://localhost:5000 --cookie "session=..."
    ```
4. Modify the session cookie or reuse it across browsers — it works due to the weak session key.

---

## 🔓 Impact

- Credential stuffing attacks
- Account takeover (especially admin)
- Session hijacking
- Unauthorized access to sensitive data

---

## 🛡️ Mitigation Strategies

- **Use a strong, random secret key**:
    ```python
    import secrets
    app.secret_key = secrets.token_hex(32)
    ```

- **Implement rate limiting and account lockout**:
  - Use Flask extensions like `Flask-Limiter`
  - Introduce exponential backoff for failed logins

- **Enforce strong password policies**

- **Enable multi-factor authentication (MFA)** for critical accounts

- **Invalidate sessions after logout or on password change**

- **Use `HttpOnly` and `Secure` cookie flags** to protect session cookies:
    ```python
    session.permanent = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    ```

---

## ✅ Example Secure Login Logic

```python
if check_password_hash(user.password_hash, entered_password):
    session['user_id'] = user.id
````

And for session protection:

```python
app.secret_key = secrets.token_hex(32)
```

---

## 📚 References

* [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
* [OWASP Session Management](https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication)
* [Flask Security Tips](https://flask.palletsprojects.com/en/latest/security/)

---

**Strong auth isn't optional. Protect users and sessions like your app depends on it — because it does.** 🔐🚨
