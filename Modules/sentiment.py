from monkeylearn import MonkeyLearn
import random
import Modules.gptj as gptj

def reply(text,author,hug,sig):
    try:
        #defines labels and makes api call
        analyze = gptj.Sentiment()
        labels = (
            ["positive","neutral","negative"],
            ["happy","neutral","sad"],
            ["sarcastic","neutral","serious"],
            ["needs hug","does not need hug"],
            ["wants hug","does not want hug"]
        )
        results = analyze.multi(text, labels)

        #goes through the information returned and organizes it
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

        #looks for what the labels are and responds accordingly
        message = ""
        if (confidence > 80):
            if (("sarcastic" in classify) and ("needs hug" in classify) and ("wants hug" in classify)):
                message = ("Yeah right\n\nHave a huggie "+random.choice(hug)+"\n\nIly "+author+" <3")#message 1
                reason = "were being sarcastic and needed a hug"
            elif ("serious" in classify):
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
        
        #returns the message
        if (not message == ""):
            message = (message+"\n\n^(This message was sent because an AI is "+str(confidence)+"%"+" sure you "+reason+
                ".)\n\n^(If you have any problems please contact Isbo2000!)\n\n&#x200B;"+sig)
            return message
        else:
            return
    except BaseException as error:
        print("\n----ERROR----\nfailed 'SENTIMENT REPLY'\n"+str(error))
        #if above ai fails, this one is the backup
        try:
            keys = [
                "807f0c685907e6bf77d2c362895f721e1eed5651",
                "bbc5280e076bfc101c68a3567d6376a2399f43f9",
                "de00d2efdc2d57a7ce6e4020913f25671cb36bbf",
                "c01d8ad78c5d07c0597cf612131a1f385a2e4cdb",
                "54ca0e7c4dfd764d9a7710d3a2cda04ff5cff974"
            ]
            #try key and if it doesnt work due to api limits, move on to next one
            for key in keys:
                try: 
                    #classifies text and responds accordingly
                    ml = MonkeyLearn(key)
                    data = [text]
                    model_id = 'cl_pi3C7JiL'
                    result = ml.classifiers.classify(model_id,data,retry_if_throttled=True)
                    tag = result.body[-1]['classifications'][0]['tag_name']
                    confidence = result.body[-1]['classifications'][0]['confidence']
                    if ((tag == "Negative") and (confidence > 0.80)):
                        message = ("It sounds like you might need a hug :/\n\n"
                            "ily "+author+" <3\n\n"
                            "here is a hug if you want it "+random.choice(hug)+"\n\n"
                            "^(UH OH, the sentiment ai has broke so this is the backup B'\( \(sorry ;-;\))"
                            "\n\n^(This message was sent because the `backup ai` was "+str(round(confidence*100, 2))+"%"+" sure your message was negative)"
                            "\n\n^(If you have any problems please contact Isbo2000!)\n\n&#x200B;"+sig)
                        return message
                    else:
                        return
                except:
                    keys.remove(key)
        except BaseException as error:
            print("\n----ERROR----\nfailed 'SENTIMENT REPLY BACKUP'\n"+str(error))
            return
