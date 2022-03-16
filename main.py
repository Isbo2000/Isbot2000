import os
import praw
import json
import post
import inbox
import random
from timeloop import Timeloop
from datetime import timedelta

reddit = praw.Reddit(
    client_id = "", 
    client_secret = "", 
    username = "", 
    password = "", 
    user_agent = "")
hug = ["(づ｡◕‿‿◕｡)づ"," つ ◕‿◕ つ","(っ.❛ ᴗ ❛.)っ","(つ≧▽≦)つ",
    "(づ￣ ³￣)づ","(> \^_\^ )>","ʕ ⊃･ ◡ ･ ʔ⊃"," つ ◕o◕ つ",
    " つ ◕_◕ つ","(.づ◡﹏◡)づ.","(.づσ▿σ)づ.","（っ・∀・）っ",
    "(っ\^_\^)っ","(.づσ▿σ)づ.","(つ✧ω✧)つ","(づ ◕‿◕ )づ"]
sig = ("\n\n[**beep boop im a bot**]"
    "(https://www.reddit.com/user/Isbot2000/comments/t84xrl/isbot2000_wholesomeness_bot_for_rteenagersbutpog/)")

subreddit = reddit.subreddit('teenagersbutpog')
subreddits = reddit.subreddit('teenagersbutpog+IsboCult+TESTYTOSTY+ThePogNation')
reddit._validate_on_submit = True
tl = Timeloop()
with open('./Assets/Data/pstdone.json') as pst:
    pstdone = json.load(pst)
with open('./Assets/Data/cmtdone.json') as cmt:
    cmtdone = json.load(cmt)
with open('./Assets/Data/optout.json') as optout:
    users = json.load(optout)

@tl.job(interval=timedelta(minutes=5))
def OPT_OUT():
    post = reddit.submission(id='t84xrl')
    try:
        for comment in post.comments:
            with open('./Assets/Data/optout.json') as optout:
                users = json.load(optout)
            author = str(comment.author)
            text = comment.body.lower()
            id = comment.id
            with open('./Assets/Data/cmtdone.json') as cmt:
                cmtdone = json.load(cmt)
            
            if ((("opt" in text) and ("out" in text)) and (
                    ("opt" in text) and ("in" in text))) and id not in cmtdone:
                if (author not in users):
                    comment.mod.remove(spam=False)
                    cmtdone.append(id)
                    with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                        json.dump(cmtdone, cmt)
                    comment.collapse()

            elif (("opt" in text) and ("out" in text)) and id not in cmtdone:
                if (author not in users):
                    users.append(author)
                    comment.reply("opted you out"+sig).distinguish(how='yes', sticky=False)
                    with open('./Assets/Data/optout.json', 'w') as optout:
                        json.dump(users, optout)
                    cmtdone.append(id)
                    with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                        json.dump(cmtdone, cmt)
                    comment.collapse()
                    print("\nOPT OUT\nopted "+author+" out")

            elif (("opt" in text) and ("in" in text)) and id not in cmtdone:
                if (author not in users):
                    comment.mod.remove(spam=False)
                    cmtdone.append(id)
                    with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                        json.dump(cmtdone, cmt)
                    comment.collapse()
                if (author in users):
                    users.remove(author)
                    comment.reply("opted you back in").distinguish(how='yes', sticky=False)
                    cmtdone.append(id)
                    with open('./Assets/Data/optout.json', 'w') as optout:
                        json.dump(users, optout)
                    with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                        json.dump(cmtdone, cmt)
                    comment.collapse()
                    print("\nOPT OUT\nopted "+author+" back in")
            
            elif (id not in cmtdone):
                comment.mod.remove(spam=False)
                cmtdone.append(id)
                with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                    json.dump(cmtdone, cmt)
                comment.collapse()
    except BaseException as error:
        print("\n----ERROR----\nfailed 'OPT OUT'\n"+str(error))
        return

@tl.job(interval=timedelta(seconds=30))
def INBOX_REPLY():
    try:
        inbox.reply(reddit,sig,hug)
    except BaseException as error:
        print("\n----ERROR----\nfailed 'INBOX REPLY'\n"+str(error))
        return

@tl.job(interval=timedelta(seconds=30))
def POST_REPLY():
    try:
        post.reply(subreddits,sig,hug)
    except BaseException as error:
        print("\n----ERROR----\nfailed 'POST REPLY'\n"+str(error))
        return

@tl.job(interval=timedelta(hours=1))
def WHOLESOME():
    choice = random.randrange(15)
    title = "Hourly Wholesomeness"
    flair = "5e7f6884-9a44-11eb-8dd2-0ee36a4197b1"
    sub = ["Aww","Awww","cute","Eyebleach","illegallysmolanimals",
        "IllegallySmolCats","IllegallySmolDogs","MadeMeSmile",
        "wholesome","wholesomegifs","wholesomememes"]

    if (choice < 4):
        try:
            path = r"./Assets/Images/"
            filename = random.choice([
                x for x in os.listdir(path)
                if os.path.isfile(os.path.join(path, x))])
            image = "./Assets/Images/"+filename
            submit = subreddit.submit_image(title=title,image_path=image,flair_id=flair)
            print('\nPosted:\n' + "https://www.reddit.com/"+submit.permalink + "\nimage post")
        except BaseException as error:
            print("\n----ERROR----\nfailed 'WHOLESOME'\nimage post\n"+str(error))
            return
        
    if (choice > 3) and (choice < 6):
        try:
            path = r"./Assets/Texts/"
            filename = random.choice([
                x for x in os.listdir(path)
                if os.path.isfile(os.path.join(path, x))])
            with open(path+filename) as f:
                text = f.read()
            submit = subreddit.submit(title=title,selftext=text,flair_id=flair)
            print('\nPosted:\n' + "https://www.reddit.com/"+submit.permalink + "\ntext post")
        except BaseException as error:
            print("\n----ERROR----\nfailed 'WHOLESOME'\ntext post\n"+str(error))
            return
    
    if (choice > 5):
        try:
            post = random.choice([x for x in reddit.subreddit(random.choice(sub)).top("day",limit=10)])
            submit = post.crosspost(subreddit=subreddit,title=title,flair_id=flair)
            print('\nPosted:\n' + "https://www.reddit.com/"+submit.permalink + "\ncrosspost")
        except BaseException as error:
            print("\n----ERROR----\nfailed 'WHOLESOME'\ncrosspost\n"+str(error))
            return

if __name__ == "__main__":
    tl.start(block=True)
