# SQL Injection (SQLi) Vulnerability Writeup

---

## 🔍 Overview

SQL Injection (SQLi) is a critical vulnerability that allows attackers to manipulate SQL queries by injecting malicious input. This can lead to unauthorized data access, authentication bypass, or even full database compromise.

---

## 💥 Location in VulnVault

- **Route:** `/login`
- **Vulnerable Code Snippet:**

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
````

This code directly interpolates user input into a SQL query string without sanitization or parameterization.

---

## 🧪 Proof of Concept

Login using the following credentials:

```
Username: ' OR 1=1 --
Password: anything
```

**Constructed SQL Query:**

```sql
SELECT * FROM users WHERE username = '' OR 1=1--' AND password = 'anything'
```

Since `1=1` is always true, the query returns the first user in the database, effectively bypassing authentication.

---

## 🔓 Impact

* Authentication bypass
* Data leakage or exfiltration
* Data manipulation or deletion
* Remote code execution (in advanced cases)
* Full database takeover

---

## 🛡️ Mitigation Strategies

* **Use parameterized queries** (also called prepared statements):

```python
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
```

* **Never concatenate raw input** into SQL strings.
* **Sanitize and validate input**, even if using ORMs.
* **Apply least privilege** to the database user account (e.g., no `DROP`, `ALTER`, or `GRANT` privileges).
* **Log suspicious input patterns** to detect exploitation attempts.

---

## 🧰 Tools for Testing

* [sqlmap](https://sqlmap.org/)
* Burp Suite Intruder
* SQLite CLI or browser

---

## 📚 References

* [OWASP SQL Injection Guide](https://owasp.org/www-community/attacks/SQL_Injection)
* [PortSwigger SQLi Labs](https://portswigger.net/web-security/sql-injection)
* [SQLite Injection Basics](https://www.sqlite.org/security.html)

---

**Always assume input is hostile. Escape it, validate it, and parameterize it.** 🛡️
