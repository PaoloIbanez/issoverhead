import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 19.432540 # Change to your latitude
MY_LONG = -99.132939 # Change to your longitude
MY_EMAIL = "mygmail@gmail.com"
MY_PASSWORD = "my_app_password"

def is_iss_overhead():
    # 1. Get ISS position
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])

    # 2. Check if within 5 degrees
    if (abs(iss_lat - MY_LAT) <= 5) and (abs(iss_long - MY_LONG) <= 5):
        return True
    return False


def is_dark():
    # Sunrise-Sunset logic
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

    current_hour = datetime.now().hour
    # If current time is < sunrise hour or > sunset hour, it's dark
    if current_hour < sunrise or current_hour > sunset:
        return True
    return False


while True:
    time.sleep(60)  # wait 60 seconds between checks so it keeps checking

    if is_iss_overhead() and is_dark():
        # 3. Send an email
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Look Up!\n\nThe ISS is near you and it's dark outside!"
            )