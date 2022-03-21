import os
import re
import subprocess
import modules.gptj as gptj

def data(text):
    try:
        blacklist = ["cum","fart","sex","serbia","ploopy","greece",
            "politics","political","capitalist","capitalism","communist",
            "communism","socialist","socialism","democrat","democracy",
            "facist","facism","republic","republican"]
        try:
            analyze = gptj.Sentiment()
            labels = (
                ["positive","neutral","negative"],
                ["wholesome","neutral","unwholesome"],
                ["nice","neutral","mean"],
                ["harmless","neutral","offensive"]
            )
            results = analyze.multi(text, labels)
            classify = []
            for result in results:
                tags = []
                scores = []
                for labels in result.keys():
                    tags.append(labels)
                for probability in result.values():
                    scores.append(round(probability*100, 2))
                score = scores[0]
                tag = tags[0]
                for n in range(len(tags)):
                    if scores[n] > score:
                        score = scores[n]
                        tag = tags[n]
                if (score > 60):
                    classify.append(tag)
                if (("negative" not in classify) and ("unwholesome" not in classify) and ("mean" not in classify) and ("offensive" not in classify)):
                    text_ok = True
                else:
                    text_ok = False
        except:
            text_ok = False

        if (text_ok):
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
        if os.name == "posix":
            subprocess.getoutput("chmod +x ./bucket/mrkfeed.awk")
            subprocess.getoutput("chmod +x ./bucket/mrkwords.sh")
            subprocess.getoutput("./bucket/mrkfeed.awk < ./bucket/tempbucket.txt >> ./bucket/model.mrkdb")
            if os.path.exists("./bucket/tempbucket.txt"):
                os.remove("./bucket/tempbucket.txt")
            message = subprocess.getoutput("./bucket/mrkwords.sh ./bucket/model.mrkdb 555|head -c1000|tr '\n' ' ' && echo")
            return message
        else:
            return
    except BaseException as error:
        print("\n----ERROR----\nfailed 'BUCKET REPLY'\n"+str(error))
        return
