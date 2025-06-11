# Security Misconfiguration Vulnerability Writeup

---

## 🔍 Overview

Security Misconfiguration occurs when systems, frameworks, or applications are configured insecurely or left with default settings. This opens the door for attackers to gain unauthorized access, enumerate sensitive data, or escalate privileges.

---

## 💥 Location in VulnVault

- **Exposed Debug Mode** in `app.py`:

```python
app.run(debug=True)
````

* **Hardcoded Secret Key**:

```python
app.secret_key = "dev"
```

* **Directory Listing Enabled**:

  * Files in the `/uploads/` directory are directly accessible and browsable via URL.

* **No HTTPS Enforcement**:

  * Application does not redirect HTTP to HTTPS or set `Secure` flags on cookies.

---

## 🧪 Proof of Concept

### 1. Debug Mode

Visiting a URL with an error (e.g., `/login?username=`) reveals an interactive Flask debugger with full traceback and the ability to execute server-side code in some configurations.

### 2. Exposed Files

Access:

```
http://localhost:5000/uploads/
```

Shows a list of all uploaded files (including potentially malicious ones).

### 3. Weak Session Protection

Inspecting cookies reveals:

```
Set-Cookie: session=...; HttpOnly; Path=/
```

But lacks:

* `Secure`
* `SameSite`
* Strong `secret_key`

---

## 🔓 Impact

* Remote code execution via debug console
* Exposure of sensitive files
* Session hijacking
* Unauthorized access to server internals or configuration
* Easier exploitation of other vulnerabilities (like file upload)

---

## 🛡️ Mitigation Strategies

* **Disable debug mode** in production:

  ```python
  app.run(debug=False)
  ```

* **Use a strong, unique secret key**:

  ```python
  import secrets
  app.secret_key = secrets.token_hex(32)
  ```

* **Restrict access to upload directories**:

  * Store files outside the web root.
  * Deny directory listing at the web server level (e.g., Nginx or Apache config).

* **Enforce HTTPS**:

  * Redirect all HTTP traffic to HTTPS.
  * Use `SESSION_COOKIE_SECURE = True` and `SESSION_COOKIE_SAMESITE = 'Lax'`.

* **Automated Security Scanning**:

  * Use tools like [Flask-Seasurf](https://flask-seasurf.readthedocs.io/en/latest/) or [Bandit](https://bandit.readthedocs.io/en/latest/) to identify insecure configurations.

---

## 📚 References

* [OWASP Security Misconfiguration](https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration)
* [Flask Deployment Checklist](https://flask.palletsprojects.com/en/latest/deploying/)
* [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)

---

**Misconfiguration is the easiest vulnerability to exploit — and the easiest to fix. Review settings, scan regularly, and never deploy with debug enabled.** 🧯🛠️
