import requests
from datetime import date
from datetime import timedelta
import os
import smtplib


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
class Data:
    def __init__(self) -> None:
        self.STOCK = "TSLA"
        self.api_key = os.environ.get("api_key")
        self.daily_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": self.STOCK,
            "apikey": self.api_key,
        }
        self.weekly_params = {
            "function": "TIME_SERIES_WEEKLY",
            "symbol": self.STOCK,
            "apikey": self.api_key,
        }
        self.monthly_params = {
            "function": "TIME_SERIES_MONTHLY",
            "symbol": self.STOCK,
            "apikey": self.api_key,
        }
        self.url = "https://www.alphavantage.co/query"

    def get_data(self, type):
        match type.lower():
            case "daily":
                r = requests.get(self.url, params=self.daily_params)
                r
            case "weekly":
                r = requests.get(self.url, params=self.weekly_params)
            case "monthly":
                r = requests.get(self.url, params=self.monthly_params)

        return r.json()["Time Series (Daily)"]

    def calculate_pct(self, data):
        data_list = [value for (key, value) in data.items()]
        yesterday_closing = data_list[0]
        yesterday_closing = yesterday_closing["4. close"]
        day_before_yesterday_closing = data_list[0]
        day_before_yesterday_closing = day_before_yesterday_closing["4. close"]

        difference = abs(float(yesterday_closing) - float(day_before_yesterday_closing))

        diff_pct = (difference / float(yesterday_closing)) * 100

        if diff_pct >= 5:
            return True
        return False


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
class News:
    def __init__(self) -> None:
        self.COMPANY_NAME = "Tesla Inc"
        self.news_api_key = os.environ.get("newsapi")
        self.url = "https://newsapi.org/v2/everything"
        self.news_params = {
            "apiKey": self.news_api_key,
            "q": self.COMPANY_NAME,
            "sortBy": "publishedAt",
            "from": str(date.today() - timedelta(days=1)),
        }

    def get_news(self):
        r = requests.get(self.url, self.news_params)
        return [
            r.json()["articles"][0]["description"],
            r.json()["articles"][0]["title"],
        ]


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
class Alert:
    def __init__(self) -> None:
        self.account_sid = os.environ.get("twilio_sid")
        self.auth_token = os.environ.get("twilio_auth_token")
        self.client = Client(self.account_sid, self.auth_token)
        self.my_email = "kai2flie@gmail.com"
        self.password = os.environ.get("app_password2")

    def sendMessage(self, subject, message):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.password)
            connection.sendmail(
                from_addr=self.my_email,
                to_addrs=self.my_email,
                msg=f"Subject:{subject}\n\n{message}",
            )
        # message = self.client.messages.create(
        #     from_="+18447524823", body="It's gonna rain today ☔️", to="+18777804236"
        # )
        return message.status


# Optional: Format the SMS message like this:


"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


d = Data()
news = News()
alert = Alert()
# data = d.get_data("daily")

# if d.calculate_pct(data) == True:
#     print(news.get_news())

l = news.get_news()
alert.sendMessage(message=l[0], subject=l[1])
