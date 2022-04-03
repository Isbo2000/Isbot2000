#need
import json
import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module

def out(reddit,sig,config):
    post = reddit.submission(id=config["post_id"])
    for comment in post.comments:
        with open('../Assets/Data/optout.json') as optout:
            users = json.load(optout)
        author = str(comment.author)
        text = comment.body.lower()
        id = comment.id
        with open('../Assets/Data/cmtdone.json') as cmt:
            cmtdone = json.load(cmt)
        
        if ((("opt" in text) and ("out" in text)) and (
                ("opt" in text) and ("in" in text))) and id not in cmtdone:
            comment.mod.remove(spam=False)
            cmtdone.append(id)
            with open('../Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            comment.collapse()

        elif (("opt" in text) and ("out" in text)) and id not in cmtdone:
            if (author in users):
                comment.mod.remove(spam=False)
                cmtdone.append(id)
                with open('../Assets/Data/cmtdone.json', 'w') as cmt:
                    json.dump(cmtdone, cmt)
                comment.collapse()
            elif (author not in users):
                users.append(author)
                com = comment.reply("opted you out"+sig)
                com.mod.distinguish(how='yes', sticky=False)
                com.mod.lock()
                comment.mod.lock()
                with open('../Assets/Data/optout.json', 'w') as optout:
                    json.dump(users, optout)
                cmtdone.append(id)
                with open('../Assets/Data/cmtdone.json', 'w') as cmt:
                    json.dump(cmtdone, cmt)
                comment.collapse()
                print("\nOPT OUT\nopted "+author+" out")

        elif (("opt" in text) and ("in" in text)) and id not in cmtdone:
            if (author not in users):
                comment.mod.remove(spam=False)
                cmtdone.append(id)
                with open('../Assets/Data/cmtdone.json', 'w') as cmt:
                    json.dump(cmtdone, cmt)
                comment.collapse()
            elif (author in users):
                users.remove(author)
                com = comment.reply("opted you back in")
                com.mod.distinguish(how='yes', sticky=False)
                com.mod.lock()
                comment.mod.lock()
                cmtdone.append(id)
                with open('../Assets/Data/optout.json', 'w') as optout:
                    json.dump(users, optout)
                with open('../Assets/Data/cmtdone.json', 'w') as cmt:
                    json.dump(cmtdone, cmt)
                comment.collapse()
                print("\nOPT OUT\nopted "+author+" back in")
        
        elif (id not in cmtdone):
            comment.mod.remove(spam=False)
            cmtdone.append(id)
            with open('../Assets/Data/cmtdone.json', 'w') as cmt:
                json.dump(cmtdone, cmt)
            comment.collapse()
