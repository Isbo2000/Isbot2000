import datetime
import random,os

def question_post(subreddit,config,sig):
    title = "Question post!"
    #gets the most recent post and returns the time in seconds that has passed since it was made
    pstime = (datetime.datetime.strptime(datetime.datetime.utcnow()
        .strftime("%H:%M:%S"),"%H:%M:%S")-datetime.datetime.strptime(
        datetime.datetime.utcfromtimestamp([post for post in subreddit.new(
        limit=1)][0].created_utc).strftime("%H:%M:%S"),"%H:%M:%S")).seconds
    
    #limits the posting based on how active the subreddit is
    if pstime > 3600: True
    elif pstime > 1800:
        if not random.randint(1,5)==5:
            False; return
    elif pstime > 600:
        if not random.randint(1,10)==10:
            False; return
    else: False; return
    
    #gets a random question and posts it
    with open("./Assets/Data/Questions.txt") as f:
        text = random.choice(f.read().splitlines())
    text = ("###"+text+"\n\ncomment and discuss with others"
        +"\n\n^(this feature is currently being tested out, so any feedback would be awesome, thanks!)"
        +"\n\n^(thank you to u/what_iffff for the idea and some of the questions!)"+sig)
    submit = subreddit.submit(title=title,selftext=text,flair_id=config["post_flair"])
    print('\nPosted:\n' + "https://www.reddit.com"+submit.permalink + "\nquestion post")