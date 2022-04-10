from datetime import timedelta
from timeloop import Timeloop
import os,sys,json,getpass
import Scripts
import praw

#check data and config files
with open('./Assets/Config/config.json') as cfg:
    config = json.load(cfg)
files = ["optout.json","pstdone.json","cmtdone.json"]
if not(os.path.exists('./Assets/Data')):
    os.makedirs('./Assets/Data')
for file in files:
    if not(os.path.exists('./Assets/Data/'+file)):
        with open('./Assets/Data/'+file, 'w') as f:
            json.dump(["Isbot2000"], f)

#check for login info and login
def redlog(login):
    return praw.Reddit(
        client_id = login["id"], 
        client_secret = login["secret"], 
        username = login["username"], 
        password = login["password"], 
        user_agent = login["username"]+config["version"])
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
        print("ERROR: Invalid login\n")
        os.remove('./Assets/Config/login.json')
        checklogin()
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
try:
    reddit = checklogin()
    print("Logged in as: "+str(reddit.user.me())+"\n")
except KeyboardInterrupt:
    sys.exit()

hug = ["(づ｡◕‿‿◕｡)づ"," つ ◕‿◕ つ","(っ.❛ ᴗ ❛.)っ","(つ≧▽≦)つ",
    "(づ￣ ³￣)づ","(> \^_\^ )>","ʕ ⊃･ ◡ ･ ʔ⊃"," つ ◕o◕ つ",
    " つ ◕_◕ つ","(.づ◡﹏◡)づ.","(.づσ▿σ)づ.","（っ・∀・）っ",
    "(っ\^_\^)っ","(.づσ▿σ)づ.","(つ✧ω✧)つ","(づ ◕‿◕ )づ"]
sig = ("\n\n[**beep boop im a bot**]("+config["link"]+") | [**"+config["version"]+"**]("+config["github"]+")")
subreddit = reddit.subreddit(config["subreddit"])
subreddits = reddit.subreddit(config["subreddits"])
reddit._validate_on_submit = True
tl = Timeloop()

#calls opt out script (checks for and opts people out)
@tl.job(interval=timedelta(minutes=5))
def OPT_OUT():
    try:
        Scripts.opt_out(reddit,sig,config)
    except BaseException as error:
        print("\n----ERROR----\nfailed 'OPT OUT'\n"+str(error))
        return

#calls inbox reply script (replies to all messages)
@tl.job(interval=timedelta(seconds=30))
def INBOX_REPLY():
    try:
        Scripts.inbox_reply(reddit,sig,hug,config)
    except BaseException as error:
        print("\n----ERROR----\nfailed 'INBOX REPLY'\n"+str(error))
        return

#calls post reply script (only replies to some posts in specified subreddits)
@tl.job(interval=timedelta(seconds=30))
def POST_REPLY():
    try:
        Scripts.post_reply(subreddits,sig,hug)
    except BaseException as error:
        print("\n----ERROR----\nfailed 'POST REPLY'\n"+str(error))
        return

#calls wholesome post script (posts wholesome thing every hour)
@tl.job(interval=timedelta(hours=1))
def WHOLESOME_POST():
    try:
        Scripts.wholesome_post(subreddit,reddit,config,sig)
    except BaseException as error:
        print("\n----ERROR----\nfailed 'WHOLESOME'\n"+str(error))
        return

#calls questions post script (posts question thing every 6? hours)
@tl.job(interval=timedelta(hours=6))
def QUESTIONS_POST():
    try:
        Scripts.question_post(subreddit,config,sig)
    except BaseException as error:
        print("\n----ERROR----\nfailed 'QUESTIONS'\n"+str(error))
        return

if __name__ == "__main__":
    tl.start(block=True)
