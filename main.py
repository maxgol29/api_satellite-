import time

import requests
from datetime import datetime
import smtplib

FROM_EMAIL = "my@gmail.com"
TO_EMAIL = "my@gmail.com"
PORT = 587
PASSWORD = "my"

MY_LAT = 00.00
MY_LONG = 00.00


def is_satellite():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT + MY_LONG - iss_longitude - iss_longitude == 10:
        return True


# Your position is within +5 or -5 degrees of the ISS position.

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if time_now.hour > sunset or time_now.hour < sunrise:
        return True


while True:
    time.sleep(60)
    if is_night() and is_satellite():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(FROM_EMAIL, PASSWORD)
            connection.sendmail(FROM_EMAIL, TO_EMAIL, msg="Subject:Satellite in the sky\n\n Look up, buddy")

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
