import json

def out(reddit,sig,config):
    post = reddit.submission(id=config["post_id"])
    for comment in post.comments:
        with open('./Assets/Data/optout.json') as optout:
            users = json.load(optout)
        author = str(comment.author)
        text = comment.body.lower()
        id = comment.id
        with open('./Assets/Data/cmtdone.json') as cmt:
            cmtdone = json.load(cmt)
        
        #looks for and removes comments that say both 'opt in' and 'opt out'
        if ((("opt" in text) and ("out" in text)) and (
                ("opt" in text) and ("in" in text))) and id not in cmtdone:
            comment.mod.remove(spam=False)
            cmtdone.append(id)
            with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            comment.collapse()
        
        #looks for comments with 'opt out' and opts out author of coment
        #if user is already opted out remove
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
        
        #looks for comments with 'opt in' and if user is opted out, opt them back in, otherwise remove
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
        
        #removes all other comments
        elif (id not in cmtdone):
            comment.mod.remove(spam=False)
            cmtdone.append(id)
            with open('./Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            comment.collapse()
