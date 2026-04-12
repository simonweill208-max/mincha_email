import requests
import datetime as dt
import smtplib
import pandas as pd
from email.mime.text import MIMEText
import os

my_email = os.environ["MY_EMAIL"]
email_password = os.environ["EMAIL_PASSWORD"]

MY_LAT = 40.708911
MY_LONG = -73.967388

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()["results"]

sunrise = data["sunrise"]
sunset = data["sunset"]

formated_time_for_edit = dt.datetime.fromisoformat(sunset)

nyc_sunset_long_format = formated_time_for_edit - dt.timedelta(hours=4)
zman_mariv_72_long_format = nyc_sunset_long_format + dt.timedelta(hours=1, minutes=12)
zman_mariv_60_long_format = nyc_sunset_long_format + dt.timedelta(hours=1)

nyc_sunset = nyc_sunset_long_format.strftime("%-I:%M")
zman_mariv_72 = zman_mariv_72_long_format.strftime("%-I:%M")
zman_mariv_60 = zman_mariv_60_long_format.strftime("%-I:%M")



message = f"זמן מעריב – 72 דקות | {zman_mariv_72}\nזמן מעריב – 60 דקות | {zman_mariv_60}"
msg = MIMEText(message, "plain", "utf-8")

emails_file_path = "people.csv"

df = pd.read_csv(emails_file_path)
all_emails = df["email"].tolist()

for email in all_emails:
    with smtplib.SMTP("smtp.gmail.com" , port=587) as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=email_password)

        msg["Subject"] = "Zmanim"

        connection.sendmail(
            from_addr=my_gmail,
            to_addrs=email,
            msg=msg.as_string()
        )
