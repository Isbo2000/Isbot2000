import os
import re
import sentiment
import subprocess

def data(text):
    try:
        label = sentiment.bucket(text)
        if (("negative" not in label) and ("unwholesome" not in label) and ("mean" not in label) and ("offensive" not in label) and ("horny" not in label)):
            blacklist = ["cum","fart","sex","serbia","ploopy","greece",
                "politics","political","capitalist","capitalism","communist",
                "communism","socialist","socialism","democrat","democracy",
                "facist","facism","republic","republican"]
            for word in blacklist:
                if (word in text):
                    text = re.sub('(?i)'+re.escape(word), lambda m: '[**CENSORED**]', text)
            if ("u/" in text):
                text = re.sub('(?i)'+re.escape('u/'), lambda m: 'u~', text)

            text = text.encode('ascii', 'ignore')
            with open('./bucket/tempbucket.txt', 'a')as f:
                f.write(text.decode() + '\n')
    except BaseException as error:
        print("\n----ERROR----\nfailed 'BUCKET DATA'\n"+str(error))
        return

def reply():
    try:
        subprocess.getoutput("./bucket/mrkfeed.awk < ./bucket/tempbucket.txt >> ./bucket/model.mrkdb")
        if os.path.exists("./bucket/tempbucket.txt"):
            os.remove("./bucket/tempbucket.txt")
        message = subprocess.getoutput("./bucket/mrkwords.sh ./bucket/model.mrkdb 555|head -c1000|tr '\n' ' ' && echo")
        return message
    except BaseException as error:
        print("\n----ERROR----\nfailed 'BUCKET REPLY'\n"+str(error))
        return
