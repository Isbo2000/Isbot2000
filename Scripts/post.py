import random,json,re
import Modules

def reply(subreddits,sig,hug):
    for submission in subreddits.new(limit=10):
        text = submission.title+" "+submission.selftext
        author = str(submission.author)
        title = submission.title.lower()
        body = submission.selftext.lower()
        post = title+" "+body
        id = submission.id
        with open('./Assets/Data/pstdone.json') as pst:
            pstdone = json.load(pst)
        with open('./Assets/Data/optout.json') as optout:
            users = json.load(optout)
        if (id in pstdone): return

        #dimibot reply
        if (author == "DimittrikovBot") and id not in pstdone:
            message = Modules.bucket.reply()
            if message:
                submission.reply(message+sig)
                submission.hide()
                pstdone.append(id)
                with open('./Assets/Data/pstdone.json', 'w') as pst:
                    json.dump(pstdone, pst)
                print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
        
        #automod reply
        if (author == "AutoModerator") and id not in pstdone:
            message = Modules.bucket.reply()
            if message:
                submission.reply(message+sig)
                submission.hide()
                pstdone.append(id)
                with open('./Assets/Data/pstdone.json', 'w') as pst:
                    json.dump(pstdone, pst)
                print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
        
        if (author in users): return

        #if bot is being talked about
        if ("isbot" in post) and id not in pstdone:
            Modules.bucket.data(text)
            submission.reply("what What WHAT, what do you want from me???"+sig)
            submission.hide()
            pstdone.append(id)
            with open('./Assets/Data/pstdone.json', 'w') as pst:
                json.dump(pstdone, pst)
            print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
        
        #random useless replies
        if ("cult" in post) and id not in pstdone:
            Modules.bucket.data(text)
            submission.reply("CULT CULT CULT"+sig)
            submission.hide()
            pstdone.append(id)
            with open('./Assets/Data/pstdone.json', 'w') as pst:
                json.dump(pstdone, pst)
            print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
        if ("sandwich" in post) and id not in pstdone:
            Modules.bucket.data(text)
            submission.reply("SANDWICHES ARE VERY YUMMY :D"+sig)
            submission.hide()
            pstdone.append(id)
            with open('./Assets/Data/pstdone.json', 'w') as pst:
                json.dump(pstdone, pst)
            print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
        
        #ily bot
        if ((re.search(r'\b%s\b' % (re.escape("love")), post) is not None) or (
                re.search(r'\b%s\b' % (re.escape("ily")), post) is not None) or (
                "<3" in post)) and id not in pstdone:
            Modules.bucket.data(text)
            submission.reply("ily "+author+" <3"+sig)
            submission.hide()
            pstdone.append(id)
            with open('./Assets/Data/pstdone.json', 'w') as pst:
                json.dump(pstdone, pst)
            print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
        
        #good morning and good night
        if ((("good" in post) and ("night" in post)) or (
                re.search(r'\b%s\b' % (re.escape("gn")), post) is not None)) and id not in pstdone:
            Modules.bucket.data(text)
            submission.reply("Goodnight :D"+sig)
            submission.hide()
            pstdone.append(id)
            with open('./Assets/Data/pstdone.json', 'w') as pst:
                json.dump(pstdone, pst)
            print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
        if ((("good" in post) and ("morning" in post)) or (
                re.search(r'\b%s\b' % (re.escape("gm")), post) is not None)) and id not in pstdone:
            Modules.bucket.data(text)
            submission.reply("Good morning :D"+sig)
            submission.hide()
            pstdone.append(id)
            with open('./Assets/Data/pstdone.json', 'w') as pst:
                json.dump(pstdone, pst)
            print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
        
        #ew politics
        if (("politic" in post) or ("capitalis" in post) or ("communis" in post) or (
                "socialis" in post) or ("democra" in post) or (
                "facis" in post) or ("republic" in post)) and id not in pstdone:
            Modules.bucket.data(text)
            submission.reply("ew, politics :P"+sig)
            submission.hide()
            pstdone.append(id)
            with open('./Assets/Data/pstdone.json', 'w') as pst:
                json.dump(pstdone, pst)
            print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
        
        #needs hug
        if ((( re.search(r'\b%s\b' % (re.escape("i")), post) is not None) and (
                ("need" in post) or ("want" in post)) and ("hug" in post)) and not (
                ("don't" in post) or ("dont" in post) or (re.search(r'\b%s\b' % (
                re.escape("no")), post) is not None) or ("not" in post))) and id not in pstdone:
            Modules.bucket.data(text)
            submission.reply("It seems like you might want a hug\n\nHere is a hug if you want it "
                +random.choice(hug)+"Ily "+author+" <3"+sig)
            submission.hide()
            pstdone.append(id)
            with open('./Assets/Data/pstdone.json', 'w') as pst:
                json.dump(pstdone, pst)
            print('\nPOST REPLY\nreplied to:\n' + "https://www.reddit.com"+submission.permalink)
