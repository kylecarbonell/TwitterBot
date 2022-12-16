from Twitter import Tweet
import smtplib
from email.message import EmailMessage
import configparser

class Message:
    def __init__(self) -> None:
        self.tweet = Tweet()
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.user = config['message']['user']
        self.pw = config['message']['pw']

    def alert(self, body, to):
        msg = EmailMessage()
        msg.set_content(body)
        msg['to'] = to

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.user, self.pw)
        server.send_message(msg)

        server.quit()

    def tweetMsg(self, to):
        text = self.tweet.get_tweet('valkyrae')
        self.alert(text, to)

if __name__ == "__main__":
    msg = Message()
    msg.alert('Hiiii!!! Little update! Filming rn but after Im done Im heading over to hasan’s around 3ish pm PT to play poppy playtime then Ill be live on my channel at 6ish pm PT for games with fuslie, rated and taco','4088588974@txt.att.net')
    #msg.tweetMsg("kylecarbonell13@gmail.com")
    #msg.tweetMsg('4088588974@txt.att.net')
