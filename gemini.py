import requests
import json
import os

userName = "USER"
aiName = "GEMINI"
memoryDeep =10
memory = []
prompts = []
models = ["gemini-1.0-pro","gemini-1.5-pro","gemini-1.5-flash"]
model = models[2]
#ENTER YOUR API KEY HERE!
API_KEY = ""
color_codes = [
        "\033[91m",
        "\033[92m",
        "\033[93m",
        "\033[94m",
        "\033[95m",
        "\033[96m",
        "\033[97m",
        "\033[0m"
        ]


def LoadPrompt(name):
    global memory, aiName, userName
    memory = []
    try:
        ftmp =os.path.abspath(__file__).split("/")
        d = ""
        for i in range(len(ftmp)-1):
            d+=ftmp[i]+"/"
        
        with open(d +"PROMPTS/"+name, "r", encoding='utf-8') as file:
            text = file.read()
        memory.append(text)
        print("PROMPT:\n    > "+text)
    except:
        print(color_codes[5]+"SYSTEM:"+color_codes[7] + ":\n    >"+color_codes[0]+" Err! (Maybe you dont have PROMPT file and/or access to it)"+color_codes[7])
    
    try:
        with open(d +"PROMPTS/"+name+".settings", "r", encoding='utf-8') as file:
            text = file.read()
        settings = text.split("_/_")
        aiName = settings[0].replace("\n","")
        userName = settings[1].replace("\n","")
    except:
        print(color_codes[5]+"SYSTEM:"+color_codes[7] + ":\n    >"+color_codes[0]+" Err! (Maybe you dont have prompt .settings file and/or access to it)"+color_codes[7])

def MakeQuestion(q):
    mem = ""
    for m in memory:
        mem+=m
    api_key = API_KEY

    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        }
]

    parameter = "MEMORY: "+mem + f" CURRENT MESSAGE TO YOU(RESPOND ON IT): "+q

    payload = {
        "contents": [{"parts": [{"text": parameter}]}],
        "safetySettings": safety_settings,
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        obj = response.json()
    
        if obj.get("candidates") and len(obj["candidates"]) > 0 and len(obj["candidates"][0]["content"]["parts"]) > 0:
            response_message = obj["candidates"][0]["content"]["parts"][0]["text"]
        else:
            response_message = "ERROR IN RESPONSE"
    else:
        response_message = f"{color_codes[0]} Request failed with status code {response.status_code} {color_codes[7]}"
        if response.status_code == 400:
            response_message+="(maybe wrong location or api) "
        #response = requests.post(url, headers=headers, params=params, data=json.dumps(data))

    #text = response.json()['candidates'][0]['content']['parts'][0]['text']
    text = response_message[:-1]
    text_new = ""
    for t in text:
        if t == "\n":
            text_new+="\n    "
        else:
            text_new+=t
    # Печать извлеченного текста
    print(color_codes[1] + aiName+color_codes[7] +':\n    > ', text_new)
    memory.append(userName+": " + q+" ")
    memory.append(aiName+": " + text+" ")
    if(len(memory) > memoryDeep): memory.pop(0)

runProgram = True
while runProgram:
    question = input(color_codes[2]+userName+color_codes[7]+":\n    > ")
    if question[0] == "/":
        if "help" in question:
            print(color_codes[5]+"SYSTEM"+color_codes[7] +":\n    > Command | Do:")
            print("      /help | this window")
            print("      /stop | stop the program")
            print("      /memory | show current ai memory as text")
            print("      /clear | clears all memory")
            print("      /username [name] | set new name to user")
            print("      /ainame [name] | set new name to ai")
            print("      /load [promptFileName.promptFileExtension] | loads prompt from file from PROMPTS directory")
            print("      /switch:\n           >\n            /switch [index] | switch to model by index\n            /switch list | show avaliable models and indexes")
            print("      /info | shows info about ai")
            print("      /save [fileName]| saves current dialogue to file with name [fileName]")
            print("      /memorydeep [int] | set memorydeep to [int]")
        if "pwd" in question:
            print(color_codes[5]+"SYSTEM: "+color_codes[7]+":\n    > Working directory:", end = "  ")
            os.system("pwd")
        if "api" in question:
            qParts = question.split(" ")
            API_KEY = qParts[1]
            print(color_codes[5]+"SYSTEM"+color_codes[7]+":\n    > Switched to ["+qParts[1]+"]")
        if "memory" in question:
            mem = ""
            print(color_codes[5]+"SYSTEM"+color_codes[7] +":\n    > Memory:")
            for m in memory:
                mem+="MESSAGE> "+m+" <MESSAGE\n"
            print(mem)
        if "stop" in question:
            runProgram = False
        if "clear" in question:
            memory = []
        if "username" in question:
            userName = question.split(" ")[1]
        if "ainame" in question:
            aiName = question.split(" ")[1]
        if "load" in question:
            LoadPrompt(question.split(" ")[1])
        if "switch" in question:
            if "list" in question:
                print(color_codes[5]+"SYSTEM"+color_codes[7]+":\n    > Models:", end = "")
                for m in models:
                    print(f"\n        [{models.index(m)}] : {m}")
            else:
                model = models[int(question.split(" ")[1])]
                print(color_codes[5]+"SYSTEM"+color_codes[7]+":\n    > Switched to ["+models[int(question.split(" ")[1])]+"]")
        if "info" in question:
            print(f"{color_codes[5]}SYSTEM{color_codes[7]}:\n    > Info\n        Current model: {model}\n        Memory: {len(memory)}/{memoryDeep}")
        if "save" in question:
            try:
                mem = ""
                for m in memory:
                    mem+=m+"\n"
                qParts = question.split(" ")
                print(color_codes[5]+"SYSTEM"+color_codes[7]+":\n    > Saved to: ["+ qParts[1]+"]")
                open(qParts[1], 'w').close()
                file = open(qParts[1], 'a')
                file.write(mem)
            except:
                print(color_codes[5]+"SYSTEM:"+color_codes[7]+"\n    > Error!")
        if "memorydeep" in question:
            memoryDeep = int(question.split(" ")[1])
            print(f"{color_codes[5]}SYSTEM{color_codes[7]}:\n    > Set memoryDeep to: [{memoryDeep}]")
    else: MakeQuestion(question)
