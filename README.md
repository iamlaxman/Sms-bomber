# SMS Bomber Nepal

A web-based SMS bombing tool specifically designed for Nepal numbers (98XXXXXXXX or 97XXXXXXXX). This tool allows users to send prank SMS messages to friends and family with their consent.

## Features

- Works exclusively with Nepal mobile numbers
- No signup required - completely anonymous
- Customizable message count (1-200 messages)
- Adjustable sending speed (Slow, Medium, Fast)
- Responsive design that works on all devices
- Secure and private - no data is stored

## Deployment to Render

This application can be deployed to Render for free using the following steps:

### Method 1: Connect GitHub Repository (Recommended)

1. Fork this repository to your GitHub account
2. Sign up or log in to [Render](https://render.com)
3. Click "New+" and select "Web Service"
4. Connect your GitHub account and select your forked repository
5. Configure the service:
   - Name: `sms-bomber-nepal`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. Click "Create Web Service"
7. Wait for the deployment to complete (usually takes 5-10 minutes)

### Method 2: Manual Deployment

1. Sign up or log in to [Render](https://render.com)
2. Click "New+" and select "Web Service"
3. Choose "Public Git repository"
4. Enter the repository URL: `https://github.com/your-username/sms-bomber-nepal.git`
5. Configure the service:
   - Name: `sms-bomber-nepal`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. Click "Create Web Service"
7. Wait for the deployment to complete

## Local Development

To run this application locally:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/sms-bomber-nepal.git
   cd sms-bomber-nepal
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a valid Nepal mobile number (98XXXXXXXX or 97XXXXXXXX)
2. Set the number of SMS messages to send (1-200)
3. Select the sending speed (Slow, Medium, or Fast)
4. Click "START SENDING"
5. Wait for the process to complete

## Important Notes

- This tool is for entertainment purposes only
- Always obtain consent before sending prank messages
- Do not use this tool for harassment or malicious purposes
- The service is only available for Nepal numbers
- Use responsibly and ethically

## Developer

**Laxman Poudel**
- Portfolio: [iamlaxman.github.io/laxmanpoudel](https://iamlaxman.github.io/laxmanpoudel)

## License

This project is for educational and entertainment purposes only. Use at your own risk and responsibility.