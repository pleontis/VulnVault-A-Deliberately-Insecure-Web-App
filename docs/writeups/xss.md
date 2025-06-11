# Cross-Site Scripting (XSS) Vulnerability Writeup

---

## 🔍 Overview

Cross-Site Scripting (XSS) is a security vulnerability that allows attackers to inject malicious scripts into web pages viewed by other users. This can lead to session hijacking, defacement, or redirecting users to malicious sites.

---

## 💥 Location in VulnVault

- **Route:** `/comment`
- **Vulnerable Code Snippet:**

```html
<li>{{ c|safe }}</li>
````

The `|safe` filter in Jinja2 tells the template engine to render the comment without escaping HTML characters, making the app vulnerable to XSS attacks.

---

## 🧪 Proof of Concept

Submitting the following comment:

```html
<script>alert('XSS Attack!')</script>
```

will cause a JavaScript alert to pop up in any user’s browser when viewing the comments section.

---

## 🔓 Impact

* Stealing cookies and session tokens
* Performing actions on behalf of logged-in users
* Redirecting users to malicious websites
* Delivering malware or keyloggers

---

## 🛡️ Mitigation Strategies

* **Remove the `|safe` filter:** Change `{{ c|safe }}` to `{{ c }}` to automatically escape HTML special characters.
* **Sanitize user input:** Use libraries like [Bleach](https://github.com/mozilla/bleach) to whitelist allowed tags.
* **Content Security Policy (CSP):** Implement CSP headers to restrict JavaScript execution sources.
* **Use HTTPOnly cookies:** Prevent client-side scripts from accessing session cookies.

---

## 📚 References

* [OWASP Cross-Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/)
* [MDN Web Docs on XSS](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting)
* [Google Web Fundamentals - XSS Prevention](https://developers.google.com/web/fundamentals/security/csp)

---

## 🔧 Secure Code Example

```html
<!-- Escaped output to prevent XSS -->
<li>{{ c }}</li>
```

Or sanitize input before rendering:

```python
import bleach

clean_comment = bleach.clean(user_comment)
```

---

**Stay safe and sanitize everything!** 🚀🔐
