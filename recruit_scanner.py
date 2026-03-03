import os
from datetime import datetime
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText

# === SET THESE IN RAILWAY ===
API_KEY = os.getenv("XAI_API_KEY")
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.x.ai/v1"
)

def run_daily_scan():
    prompt = f"""You are my autonomous Navy Recruiting Lead Scanner for ZIP codes 43235 and 43064 in Columbus, Ohio (Worthington, Plain City, Jonathan Alder HS, Worthington Kilbourne HS).
Use web_search and x_search aggressively on public sources only.
Target: 17–39 year olds talking about Navy, ASVAB, enlisting, military careers, fitness, travel, leadership or career changes.
Also scan for school events and career fairs.
Qualify every lead and prepare outreach in a direct, no-BS recruiter voice.
Always output in this exact format:

# Daily Navy Recruit Leads - {datetime.now().strftime('%B %d, %Y')}
## Top Leads (3-5 hottest)
## Hot Events This Week
## Ready Outreach Templates
## Summary & Next Actions

Stay 100% DoD compliant — public data only."""

    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Run full daily scan for Columbus ZIPs now."}
        ],
        max_tokens=2800
    )

    report = response.choices[0].message.content
    print(report)

    if YOUR_EMAIL:
        msg = MIMEText(report)
        msg["Subject"] = f"🚀 Daily Navy Lead Scanner - {datetime.now().strftime('%b %d')}"
        msg["From"] = "NavyScanner@recruiting.com"
        msg["To"] = YOUR_EMAIL
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(YOUR_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            print("✅ Report emailed!")
        except:
            print("Email skipped - add SMTP_PASSWORD later")

    return report

if __name__ == "__main__":
    run_daily_scan()
