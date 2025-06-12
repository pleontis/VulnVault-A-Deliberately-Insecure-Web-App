# Insecure Direct Object Reference (IDOR) Vulnerability Writeup

---

## 🔍 Overview

Insecure Direct Object Reference (IDOR) occurs when an application exposes internal object references (like IDs or filenames) and fails to properly verify user access. This allows attackers to manipulate these references to access unauthorized data.

---

## 💥 Location in VulnVault

* **Route:** `/invoice/<int:invoice_id>`
* **Vulnerable Code Snippet:**

```python
@app.route('/invoice/<int:invoice_id>')
def invoice(invoice_id):
    if invoice_id == 1:
        return "Invoice #1 for Alice"
    elif invoice_id == 2:
        return "Invoice #2 for Bob"
    else:
        return "Access Denied"  # IDOR vulnerability (no auth check)
```

There’s no check to verify whether the logged-in user owns the requested invoice, allowing any authenticated user to enumerate invoices.

---

## 🧪 Proof of Concept

1. Login as a low-privilege user (e.g., Alice).
2. Navigate to:

```
http://localhost:5000/invoice/1
```

Result: See Alice’s invoice ✅

3. Then try:

```
http://localhost:5000/invoice/2
```

Result: See Bob’s invoice ❌ (This should not happen.)

This shows that there's no ownership validation.

---

## 🔓 Impact

* Exposure of sensitive business or personal data
* Bypass of access control mechanisms
* Data leakage (invoices, files, user records)
* Could lead to full account takeover in chained attacks

---

## 🛡️ Mitigation Strategies

* **Enforce access control checks** on all resource-access endpoints (check ownership).
* **Avoid exposing predictable IDs** — use UUIDs or random tokens instead.
* **Implement permission logic server-side**, never rely on hidden fields or client validation.
* **Log access attempts** to sensitive resources and monitor for anomalies.

---

## ✅ Example Secure Implementation

```python
@app.route('/invoice/<int:invoice_id>')
def invoice(invoice_id):
    if 'user' not in session:
        return redirect('/login')

    user = session['user']

    # Lookup invoice ownership in the database
    with sqlite3.connect(db_path) as conn:
        result = conn.execute(
            "SELECT * FROM invoices WHERE id=? AND owner=?", (invoice_id, user)
        ).fetchone()

    if result:
        return f"Invoice #{invoice_id} for {user}"
    else:
        return "Access Denied"
```

---

## 🔧 Tools for Testing

* [Burp Suite Intruder](https://portswigger.net/burp) (for ID fuzzing)
* Manual enumeration via browser or curl
* OWASP ZAP forced browsing plugin

---

## 📚 References

* [OWASP IDOR Explanation](https://owasp.org/www-community/attacks/Indirect_Object_Reference)
* [PortSwigger: IDOR](https://portswigger.net/web-security/access-control/idor)
* [OWASP Access Control Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html)

---

**Access control is not optional. Always verify ownership on server-side resources.** 🔐📄
