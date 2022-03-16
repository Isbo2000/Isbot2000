import re
import praw
import json
import sentiment
import praw.models
import bucket.bucket as bucket

def reply(reddit,sig,hug):
    for reply in reddit.inbox.unread(limit=10):
        author = str(reply.author)
        text = reply.body.lower()
        id = reply.id
        with open('./Assets/Data/cmtdone.json') as cmt:
            cmtdone = json.load(cmt)
        with open('./Assets/Data/optout.json') as optout:
            users = json.load(optout)
        if (author in users): return
        if (id in cmtdone): return
        if not(isinstance(reply, praw.models.Comment)): return
        
        if (id not in cmtdone):
            bucket.data(reply.body)

        if (("good" in text) and ("bot" in text)) and id not in cmtdone:
            reply.reply("yay, thanks :D"+sig)
            cmtdone.append(id)
            with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            reply.collapse()
            reply.mark_read()
            print("\nINBOX REPLY\nreplied to:\nhttps://www.reddit.com" + reply.context)

        if ((("bad" in text) and ("bot" in text)) or (("hate" in text) and (
                (re.search(r'\b%s\b' % (re.escape("u")), text) is not None) or ("you" in text))) or (
                (re.search(r'\b%s\b' % (re.escape("no")), text) is not None)) and (
                "love" in text) or (("don" in text) and ("love" in text))) and id not in cmtdone:
            reply.reply("aw :'( ok..."+sig)
            cmtdone.append(id)
            with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            reply.collapse()
            reply.mark_read()
            print("\nINBOX REPLY\nreplied to:\nhttps://www.reddit.com" + reply.context)
        
        if ((("thank" in text) and (re.search(r'\b%s\b' % (re.escape("no")), text) is not None)) or (
                (re.search(r'\b%s\b' % (re.escape("no")), text) is not None) and (
                re.search(r'\b%s\b' % (re.escape("ty")), text) is not None)) or (
                (re.search(r'\b%s\b' % (re.escape("no")), text) is not None) and (
                "thx" in text)) or (("thank" in text) and (re.search(r'\b%s\b' % (
                re.escape("not")), text) is not None))) and id not in cmtdone:
            reply.reply("oh, alright.."+sig)
            cmtdone.append(id)
            with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            reply.collapse()
            reply.mark_read()
            print("\nINBOX REPLY\nreplied to:\nhttps://www.reddit.com" + reply.context)
        
        if (("thank" in text) or (re.search(r'\b%s\b' % (re.escape("ty")), text) is not None) or (
                "thx" in text)) and id not in cmtdone:
            reply.reply("You're welcome :D"+sig)
            cmtdone.append(id)
            with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            reply.collapse()
            reply.mark_read()
            print("\nINBOX REPLY\nreplied to:\nhttps://www.reddit.com" + reply.context)
        
        if ("slake" in text) and id not in cmtdone:
            reply.reply("Slakey is amazing, I love her <3"+sig)
            cmtdone.append(id)
            with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            reply.collapse()
            reply.mark_read()
            print("\nINBOX REPLY\nreplied to:\nhttps://www.reddit.com" + reply.context)
        
        if ("cum" in text) and id not in cmtdone:
            reply.reply("WEE WOO WEE WOO\n\nALERT! COMEDY GOD HAS ENTERED THE BUILDING! GET TO COVER!\n\n"+
                "steps on stage\n\nBystander: 'Oh god! Don`t do it! I have a family!'\n\nComedy God: 'Heh...'\n\n"+
                "adjusts fedora\n\nthe building is filled with fear and anticipation\n\n"+
                "God and Jesus himself looks on in suspense\n\ncomedy god clears throat\n\n"+
                "everything is completely quiet not a single sound is heard\n\n"+
                "world leaders look and wait with dread\n\neverything in the world stops\n\n"+
                "nothing is happening\n\ncomedy god smirks\n\nno one is prepared for what is going to happen\n\n"+
                "comedy god musters all of this power\n\nhe bellows out to the world\n\n'CUM'\n\n"+
                "all at once, absolute pandemonium commences\n\nall nuclear powers launch their nukes at once\n\n"+
                "giant brawls start\n\n43 wars are declared simultaneously\n\na shockwave travels around the earth\n\n"+
                "earth is driven into chaos\n\nhumanity is regressed back to the stone age\n\n"+
                "the pure funny of that joke destroyed civilization itself\n\n"+
                "all the while people are laughing harder than they ever did\n\n"+
                "people who aren`t killed die from laughter\n\nliterally the funniest joke in the world\n\n"+
                "then the comedy god himself posts his creation to reddit and gets karma\n\n&#x200B;"+sig)
            cmtdone.append(id)
            with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            reply.collapse()
            reply.mark_read()
            print("\nINBOX REPLY\nreplied to:\nhttps://www.reddit.com" + reply.context)
        
        if (id not in cmtdone):
            message = sentiment.reply(text,author,hug,sig)
            if (message):
                reply.reply(message)
                cmtdone.append(id)
                with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                    json.dump(cmtdone, cmt)
                reply.collapse()
                reply.mark_read()
                print("\nSENTIMENT AI\nreplied to:\nhttps://www.reddit.com" + reply.context)
        
        if (id not in cmtdone):
            message = bucket.reply()
            if (message):
                reply.reply(message+sig)
                cmtdone.append(id)
                with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                    json.dump(cmtdone, cmt)
                reply.collapse()
                reply.mark_read()
                print("\nBUCKET\nreplied to:\nhttps://www.reddit.com" + reply.context)
