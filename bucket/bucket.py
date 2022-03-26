import os
import re
import subprocess
import modules.gptj as gptj
from monkeylearn import MonkeyLearn

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
            try:
                keys = [
                    "807f0c685907e6bf77d2c362895f721e1eed5651",
                    "bbc5280e076bfc101c68a3567d6376a2399f43f9",
                    "de00d2efdc2d57a7ce6e4020913f25671cb36bbf",
                    "c01d8ad78c5d07c0597cf612131a1f385a2e4cdb",
                    "54ca0e7c4dfd764d9a7710d3a2cda04ff5cff974"
                ]
                k = 0
                for key in keys:
                    try: 
                        ml = MonkeyLearn(key[k])
                        data = [text]
                        model_id = 'cl_pi3C7JiL'
                        result = ml.classifiers.classify(model_id,data,retry_if_throttled=True)
                        continue
                    except:
                        k =+ 1
                k = 0
                tag = result.body[-1]['classifications'][0]['tag_name']
                confidence = result.body[-1]['classifications'][0]['confidence']
                if ((tag == "Negative") and (round(confidence*100, 2) > 0.80)):
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
