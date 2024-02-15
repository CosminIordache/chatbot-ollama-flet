from flet import *
import requests
import json

#Model use for chat messages
model = 'llama2:latest'

#Generate text with a lengague model and do a request to the API that have the model
def generate(prompt, context, top_k=0, top_p=0.9, temp=0.7):
    r = requests.post('http://localhost:11434/api/generate', json={'model': model, 'prompt': prompt, 'context': context, 'top_k': top_k, 'top_p': top_p, 'temp': temp}, stream=True)
    for line in r.iter_lines():
        if line:
            body = json.loads(line.decode('utf-8'))
            response = body.get('response', '')
            if response:
                yield response

def main(page: Page):
    context = []

    def send_message(e):
        user_input = txt_input.value.strip()
        if user_input:

            #Add the user message to the message list
            chat_view.controls.append(Text(value=f"You: {user_input}"))
            #Set the TextField to empty when the user sends a message
            txt_input.value = ""
            #Update the page to show instant the message
            page.update()
            
            #Generate a pre response and add it to the message list to get all the message with "\n"
            pre_response = Text(value="", color= "green")
            chat_view.controls.append(pre_response)
            page.update()
            
            #Create a empty string and concat the response that the ia generate and we can see the response in real time becouse we got the pre response
            response_text = "Bot: "
            for response_generate in generate(user_input, context):
                response_text += response_generate + " "
                pre_response.value = response_text
                #Update the page to show all message 
                page.update()

    #App structure
    chat_view = ListView(expand= True, auto_scroll= True)
    txt_input = TextField(hint_text="Type your message here", expand= True, autofocus= True, on_submit= send_message, multiline= True)
    send_btn = IconButton(icon= icons.SEND, on_click= send_message)
    input_row = Row([txt_input, send_btn], alignment= alignment.bottom_center)

    #Title
    page.title = 'Chat IA Local'
    #Add all componenst to the page
    page.add(Column([chat_view, input_row], expand= True))

if __name__ == "__main__":
    app(target=main)
