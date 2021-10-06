import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#Authenticate to Twitter
auth = tweepy.OAuthHandler(" ", " ")
auth.set_access_token(" ", " ")

#API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Kept this around to use in future, maybe
'''try:
	api.verify_credentials()
	print("Authentication OK!")
except:
	print("error during authentication...")'''	

def check_mentions(api, keywords, since_id):
	logger.info("Retrieving mentions")
	new_since_id = since_id
	for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
		new_since_id = max(tweet.id, new_since_id)
		if tweet.in_reply_to_status_id is not None:
			continue
		if any(keyword in tweet.text.lower() for keyword in keywords):
			logger.info(f"Answering to {tweet.user.name}")

			if not tweet.user.following:
				tweet.user.follow()

			api.update_status(status=" https://tenor.com/view/pat-head-pat-gif-12018845 ", in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
	return new_since_id			


def main():
	since_id = 1
	while True:
		since_id = check_mentions(api, ["praise me"], since_id)
		logger.info("Waiting...")
		time.sleep(60)

if __name__ == "__main__":
	main()
