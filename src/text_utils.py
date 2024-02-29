import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

class TextWizard:
    '''
    Several text manipulation tools.
    '''
    def __init__(self, bot):
        self.bot = bot
        self.messages_dic = {}
        self.client = OpenAI()
        with open("text/summarize_prompt.txt", "r", encoding="utf-8") as f:
            self.summarize_prompt = f.read()


    def get_answer(self, message):
        '''
        Take a Telebot message oject, passes its text to chatGPT
        and returns the answer.
        '''
        if (message.from_user.id not in self.messages_dic):
            self.messages_dic[message.from_user.id] =  [{'role': 'system', 'content': 'You are a intelligent assistant.'}]
        
        text = message.text

        self.messages_dic[message.from_user.id].append({"role": "user", "content": text})
        chat = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=self.messages_dic[message.from_user.id])
        reply = chat.choices[0].message.content
        return(reply)
    
    def get_summary(self, message):
        '''
        Summarize message.text using chatGPT.
        '''
        message.text = self.summarize_prompt + "\n" + message.text
        reply = self.get_answer(message)
        return(reply)
    
    def clear(self, message):
        '''
        Clear chatGPT message queue.
        '''
        try:
            del self.messages_dic[message.from_user.id]
            answer = "Historial de chatGPT borrado."
        except KeyError:
            answer = "El historial ya está vacío."
        except Exception:
            answer = "Ha ocurrido un error"
        return(answer)


