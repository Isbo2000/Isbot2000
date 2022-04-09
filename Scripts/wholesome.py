import os,random

def post(subreddit,reddit,config,sig):
    choice = random.randrange(15)
    title = "Hourly Wholesomeness"
    sub = ["Aww","Awww","cute","Eyebleach","illegallysmolanimals",
        "IllegallySmolCats","IllegallySmolDogs","MadeMeSmile",
        "wholesome","wholesomegifs","wholesomememes"]
    
    #chooses and posts random wholesome image
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
    
    #chooses and posts random wholesome text
    if (choice > 3) and (choice < 6):
        try:
            path = r"./Assets/Texts/"
            filename = random.choice([
                x for x in os.listdir(path)
                if os.path.isfile(os.path.join(path, x))])
            with open(path+filename) as f:
                text = f.read()
            submit = subreddit.submit(title=title,selftext=text+sig,flair_id=config["post_flair"])
            print('\nPosted:\n' + "https://www.reddit.com"+submit.permalink + "\ntext post")
        except BaseException as error:
            print("\n----ERROR----\nfailed 'WHOLESOME'\ntext post\n"+str(error))
            return
    
    #chooses and crossposts random wholesome post
    if (choice > 5):
        try:
            post = random.choice([x for x in reddit.subreddit(random.choice(sub)).top("day",limit=10)])
            submit = post.crosspost(subreddit=subreddit,title=title,flair_id=config["post_flair"])
            print('\nPosted:\n' + "https://www.reddit.com"+submit.permalink + "\ncrosspost")
        except BaseException as error:
            print("\n----ERROR----\nfailed 'WHOLESOME'\ncrosspost\n"+str(error))
            return
