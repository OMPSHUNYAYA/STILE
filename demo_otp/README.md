# ⭐ OTP Without Sending — STILE Demo

A minimal deterministic demonstration that OTP verification does not require sending an OTP over SMS, email, or network transport.

---

## 🧱 Core Idea

OTP verification is not created by transmission.  
It is determined by structure.

`structure_aligned = complete AND consistent`  
`otp_verified iff structure_aligned`

---

## 🔍 What This Demo Shows

`valid structure -> VERIFIED`  
`wrong OTP -> CONFLICT`  
`expired window -> CONFLICT`  
`missing identity -> ABSTAIN`  
`same structure -> same certificate`

**Note:**  
`expected_hash` is derived deterministically from shared structure (no transmission involved).  
No OTP is transmitted.

No SMS.  
No email.  
No callbacks.  
No network dependency.  
No OTP transmission.

---

## ⚡ Run the Demo

```
python otp_without_sending.py
```
