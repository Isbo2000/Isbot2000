import modules.gptj as gptj
import random

def reply(text,author,hug,sig):
    try:
        analyze = gptj.Sentiment()
        labels = (
            ["positive","neutral","negative"],
            ["happy","neutral","sad"],
            ["sarcastic","neutral","serious"],
            #["suicidal","neutral"],
            ["needs hug","does not need hug"],
            ["wants hug","does not want hug"]
        )
        results = analyze.multi(text, labels)

        classify = []
        confidence = []
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
            if not(tag == "neutral" or score < 60):
                classify.append(tag)
                confidence.append(score)
        confidence = round(sum(confidence)/len(confidence), 2)

        message = ""
        if (confidence > 80):
            if (("sarcastic" in classify) and ("needs hug" in classify) and ("wants hug" in classify)):
                message = ("Yeah right\n\nHave a huggie "+random.choice(hug)+"\n\nIly "+author+" <3")#message 1
                reason = "were being sarcastic and needed a hug"
            elif ("serious" in classify):
                #if (("needs hug" in classify) and ("wants hug" in classify) and ("suicidal" in classify)):
                #    message = (" ")#message 2
                #    reason = "wanted to die and needed a hug"
                if (("needs hug" in classify) and ("wants hug" in classify) and ((("positive" not in classify) and (
                        "happy" not in classify)) and (("negative" not in classify) and ("sad" not in classify)))):
                    message = ("Ily "+author+" <3\n\nHere is a huggie for you " +random.choice(hug))#message 3
                    reason = "needed a hug"
                elif (("needs hug" in classify) and ("wants hug" in classify) and ((("positive" in classify) and (
                        "happy" in classify)) and (("negative" not in classify) and ("sad" not in classify)))):
                    message = ("Yay, you seem happy! :D\n\nHere is a huggie for you "+random.choice(hug)+"\n\nIly "+author+" <3")#message 4
                    reason = "were happy and needed a hug"
                elif (("needs hug" in classify) and ("wants hug" in classify) and ((("positive" not in classify) and (
                        "happy" not in classify)) and (("negative" in classify) and ("sad" in classify)))):
                    message = ("Awww, you seem sad :(\n\nWhat is wrong? :(\n\nHere is a huggie for you "+random.choice(hug)+"\n\nIly "+author+" <3")#message 5
                    reason = "were sad and needed a hug"
                #elif ("suicidal" in classify):
                #    message = (" ")#message 6
                #    reason = "wanted to die"
                elif (((("positive" not in classify) and ("happy" not in classify)) and (("negative" in classify) and ("sad" in classify)))):
                    message = ("Awww, you seem sad :(\n\nWhat is wrong? :(\n\nI would suggest doing something that makes you happy!\n\nIly "+author+" <3")#message 7
                    reason = "were sad"
            else:
                if (("needs hug" in classify) and ("wants hug" in classify) and ((("positive" not in classify) and (
                        "happy" not in classify)) and (("negative" not in classify) and ("sad" not in classify)))):
                    message = ("Ily "+author+" <3\n\nHere is a huggie for you " +random.choice(hug))#3
                    reason = "needed a hug"
                elif (("needs hug" in classify) and ("wants hug" in classify) and ((("positive" in classify) and (
                        "happy" in classify)) and (("negative" not in classify) and ("sad" not in classify)))):
                    message = ("Yay, you seem happy! :D\n\nHere is a huggie for you "+random.choice(hug)+"\n\nIly "+author+" <3")#4
                    reason = "were happy and needed a hug"
                elif (("needs hug" in classify) and ("wants hug" in classify) and ((("positive" not in classify) and (
                        "happy" not in classify)) and (("negative" in classify) and ("sad" in classify)))):
                    message = ("Awww, you seem sad :(\n\nWhat is wrong? :(\n\nHere is a huggie for you "+random.choice(hug)+"\n\nIly "+author+" <3")#5
                    reason = "were sad and needed a hug"

        if (not message == ""):
            message = (message+"\n\n^(This message was sent because an AI is "+str(confidence)+"% you "+reason+
                ".)\n\n^(If you have any problems please contact Isbo2000!)\n\n&#x200B;"+sig)
            return message
        else:
            return
    except BaseException as error:
        print("\n----ERROR----\nfailed 'SENTIMENT REPLY'\n"+str(error))
        return
