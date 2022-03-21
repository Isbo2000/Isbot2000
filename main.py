import praw
import getpass
import post,inbox
import os,sys,random,json
from timeloop import Timeloop
from datetime import timedelta

with open('./Assets/Config/config.json') as cfg:
    config = json.load(cfg)
files = ["optout.json","pstdone.json","cmtdone.json"]
for file in files:
    if not(os.path.exists('./Assets/Data/'+file)):
        with open('./Assets/Data/'+file, 'w') as f:
            json.dump('["Isbot2000"]', f)

def redlog(login):
    return praw.Reddit(
        client_id = login["id"], 
        client_secret = login["secret"], 
        username = login["username"], 
        password = login["password"], 
        user_agent = config["user_agent"])
def asklogin():
    print("PLease enter your bot login info (dw, it is only stored locally)\n")
    i = getpass.getpass('Id: ')
    s = getpass.getpass('Secret: ')
    u = input('Username: ')
    p = getpass.getpass('Password: ')
    login = {"id":i,"secret":s,"username":u,"password":p}
    with open('./Assets/Config/login.json', 'w') as lgn:
        json.dump(login, lgn)
    try:
        print("\nChecking details...\n")
        redlog(login).user.me()
    except:
        print("ERROR: Invalid login")
        os.remove('./Assets/Config/login.json')
        sys.exit()
    print("Logging in...\n")
    return redlog(login)
def checklogin():
    if os.path.exists('./Assets/Config/login.json'):
        with open('./Assets/Config/login.json') as lgn:
            login = json.load(lgn)
        try:
            print("\nChecking details...\n")
            redlog(login).user.me()
        except:
            return asklogin()
    else:
        return asklogin()
    print("Logging in...\n")
    return redlog(login)
reddit = checklogin()
print("Logged in as: "+str(reddit.user.me())+"\n")

hug = ["(づ｡◕‿‿◕｡)づ"," つ ◕‿◕ つ","(っ.❛ ᴗ ❛.)っ","(つ≧▽≦)つ",
    "(づ￣ ³￣)づ","(> \^_\^ )>","ʕ ⊃･ ◡ ･ ʔ⊃"," つ ◕o◕ つ",
    " つ ◕_◕ つ","(.づ◡﹏◡)づ.","(.づσ▿σ)づ.","（っ・∀・）っ",
    "(っ\^_\^)っ","(.づσ▿σ)づ.","(つ✧ω✧)つ","(づ ◕‿◕ )づ"]
sig = "\n\n[**beep boop im a bot**]("+config["link"]+")"
subreddit = reddit.subreddit(config["subreddit"])
subreddits = reddit.subreddit(config["subreddits"])
reddit._validate_on_submit = True
tl = Timeloop()

@tl.job(interval=timedelta(minutes=5))
def OPT_OUT():
    post = reddit.submission(id=config["post_id"])
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
                comment.mod.remove(spam=False)
                cmtdone.append(id)
                with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                    json.dump(cmtdone, cmt)
                comment.collapse()

            elif (("opt" in text) and ("out" in text)) and id not in cmtdone:
                if (author in users):
                    comment.mod.remove(spam=False)
                    cmtdone.append(id)
                    with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                        json.dump(cmtdone, cmt)
                    comment.collapse()
                elif (author not in users):
                    users.append(author)
                    com = comment.reply("opted you out"+sig)
                    com.mod.distinguish(how='yes', sticky=False)
                    com.mod.lock()
                    comment.mod.lock()
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
                elif (author in users):
                    users.remove(author)
                    com = comment.reply("opted you back in")
                    com.mod.distinguish(how='yes', sticky=False)
                    com.mod.lock()
                    comment.mod.lock()
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
            submit = subreddit.submit_image(title=title,image_path=image,flair_id=config["post_flair"])
            print('\nPosted:\n' + "https://www.reddit.com"+submit.permalink + "\nimage post")
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
            submit = subreddit.submit(title=title,selftext=text,flair_id=config["post_flair"])
            print('\nPosted:\n' + "https://www.reddit.com"+submit.permalink + "\ntext post")
        except BaseException as error:
            print("\n----ERROR----\nfailed 'WHOLESOME'\ntext post\n"+str(error))
            return
    
    if (choice > 5):
        try:
            post = random.choice([x for x in reddit.subreddit(random.choice(sub)).top("day",limit=10)])
            submit = post.crosspost(subreddit=subreddit,title=title,flair_id=config["post_flair"])
            print('\nPosted:\n' + "https://www.reddit.com"+submit.permalink + "\ncrosspost")
        except BaseException as error:
            print("\n----ERROR----\nfailed 'WHOLESOME'\ncrosspost\n"+str(error))
            return

if __name__ == "__main__":
    tl.start(block=True)
