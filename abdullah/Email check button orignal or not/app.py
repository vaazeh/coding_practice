import os
import re
import random
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
import smtplib

# ------------------ Config ------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-production")

SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
EMAIL_ADDRESS = os.environ.get("EMAIL_USER")            # Your Gmail
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")           # Your Gmail App Password
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", EMAIL_ADDRESS)  # Admin notification email

# OTP settings
OTP_EXPIRY_MIN = 10          # OTP valid for 10 minutes
RESEND_COOLDOWN_SEC = 60     # Wait 60s before resending

# In-memory store (use DB in production)
# { email: {"otp":..., "expires_at":..., "last_sent":..., "name":..., "cnic":...} }
otp_store = {}

# ------------------ Helpers ------------------
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CNIC_REGEX  = re.compile(r"^\d{5}-\d{7}-\d$")

def send_email(to_addr: str, subject: str, body: str):
    """Send email using Gmail SMTP"""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise RuntimeError("EMAIL_USER/EMAIL_PASS environment variables are not set.")
    message = f"Subject: {subject}\nFrom: {EMAIL_ADDRESS}\nTo: {to_addr}\n\n{body}"
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_addr, message)

def validate_inputs(name: str, cnic: str, email: str):
    errors = []
    if not name or len(name.strip()) < 2:
        errors.append("Name is required (min 2 characters).")
    if not cnic or not CNIC_REGEX.match(cnic.strip()):
        errors.append("CNIC must match 12345-1234567-1 format.")
    if not email or not EMAIL_REGEX.match(email.strip()):
        errors.append("Enter a valid email address.")
    return errors

def generate_and_store_otp(name: str, cnic: str, email: str):
    now = time.time()
    previous = otp_store.get(email)
    if previous and now - previous.get("last_sent", 0) < RESEND_COOLDOWN_SEC:
        remaining = int(RESEND_COOLDOWN_SEC - (now - previous["last_sent"]))
        raise RuntimeError(f"Please wait {remaining}s before requesting another OTP.")

    otp = str(random.randint(100000, 999999))
    otp_store[email] = {
        "otp": otp,
        "expires_at": now + OTP_EXPIRY_MIN * 60,
        "last_sent": now,
        "name": name.strip(),
        "cnic": cnic.strip()
    }
    return otp

# ------------------ Routes ------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        cnic = request.form.get("cnic", "").strip()
        email = request.form.get("email", "").strip()

        errors = validate_inputs(name, cnic, email)
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("login.html", name=name, cnic=cnic, email=email)

        try:
            otp = generate_and_store_otp(name, cnic, email)
            send_email(email, "Your OTP Code",
                       f"Hello {name},\n\nYour verification code is: {otp}\n"
                       f"This code will expire in {OTP_EXPIRY_MIN} minutes.")
            session["pending_email"] = email
            flash("OTP sent to your email. Please check your inbox.", "success")
            return redirect(url_for("verify"))
        except Exception as ex:
            flash(str(ex), "error")
            return render_template("login.html", name=name, cnic=cnic, email=email)

    return render_template("login.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    email = session.get("pending_email")
    if not email or email not in otp_store:
        flash("Session expired or invalid request. Please fill the form again.", "error")
        return redirect(url_for("login"))

    record = otp_store[email]

    if request.method == "POST":
        entered_otp = request.form.get("otp", "").strip()
        now = time.time()

        if now > record["expires_at"]:
            flash("OTP expired. Please request a new one.", "error")
            return redirect(url_for("resend"))

        if entered_otp != record["otp"]:
            flash("Invalid code. Please try again.", "error")
            return render_template("verify.html", email=email)

        # OTP verified — notify admin and optionally the user
        name, cnic = record["name"], record["cnic"]
        try:
            admin_body = (f"A user has completed verification.\n\n"
                          f"Name: {name}\nCNIC: {cnic}\nEmail: {email}\n"
                          f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            send_email(ADMIN_EMAIL, "User Verified (Login/Signup)", admin_body)

            user_body = f"Hi {name},\n\nYour email has been verified successfully. Welcome!"
            send_email(email, "Welcome! Email Verified", user_body)
        except Exception as ex:
            # Even if emails fail, show success page (but inform)
            flash(f"Verified, but failed to send notification emails: {ex}", "error")

        # Cleanup
        otp_store.pop(email, None)
        session.pop("pending_email", None)

        return render_template("success.html", name=name, email=email)

    return render_template("verify.html", email=email)

@app.route("/resend")
def resend():
    email = session.get("pending_email")
    if not email or email not in otp_store:
        flash("Session expired. Please fill the form again.", "error")
        return redirect(url_for("login"))

    rec = otp_store[email]
    try:
        otp = generate_and_store_otp(rec["name"], rec["cnic"], email)
        send_email(email, "Your OTP Code",
                   f"Hello {rec['name']},\n\nYour new verification code is: {otp}\n"
                   f"This code will expire in {OTP_EXPIRY_MIN} minutes.")
        flash("New OTP sent. Please check your inbox.", "success")
    except Exception as ex:
        flash(str(ex), "error")

    return redirect(url_for("verify"))

if __name__ == "__main__":
    # Use the LAN IP/port you want
    app.run(host="192.168.1.20", port=5001, debug=True)
