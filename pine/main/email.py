import requests
from django.conf import settings

MAILGUN_API_KEY = '2b778fc3-08c40cdb' 

def Send(to,subject,content,sender="pinetown@sandbox010e8efdb6104b3fab9cec20eb3973b0.mailgun.org",replyto="pinetown@gmail.com",name="Cushyrooms",cc=[],bcc=[]):

    return requests.post(
        "https://api.mailgun.net/v3/techniche.org/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": name+" <"+sender+">",
            "to": to,
            "cc": cc,
            "bcc": bcc,
            "subject": subject,
            "h:Reply-To": replyto,
            "html": content})