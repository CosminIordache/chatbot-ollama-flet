from flet import *
import requests
import json
from controllers.speech import audio_user
from controllers.audio import speak

#Model use for chat messages
model = 'mistral:latest'

#Generate text with a lengague model and do a request to the API that have the model
def generate(prompt, context, temp= 0):
    r = requests.post('http://localhost:11434/api/generate', json={'model': model, 'prompt': prompt, 'context': context, 'temp': temp}, stream=True)
    for line in r.iter_lines():
        if line:
            body = json.loads(line.decode('utf-8'))
            response = body.get('response', '')
            if response:
                yield response

def main(page: Page):

    context = []

    def send_message(e):

        if txt_input.value.strip():
            # Get text input
            user_input = txt_input.value.strip()
        elif audio_bnt.on_click:
            user_input = audio_user(audio_bnt)

        if user_input:

            #Add the user message to the message list
            chat_view.controls.append(
                Container(
                    content= Column(
                        spacing=5,
                        controls=[
                                Row(
                                    spacing=5,
                                    controls=[
                                    CircleAvatar(
                                        content=Icon(icons.PERSON),
                                        scale=0.8,
                                        bgcolor= colors.BLUE
                                    ),
                                    Text(value="User")
                                ]),
                                Container(
                                    padding= padding.only(left=47),
                                    content= Text(value=f"{user_input}")
                                )
                            ]),
                    margin=margin.only(top= 10)
                )
                
            )
            #Set the TextField to empty when the user sends a message
            txt_input.value = ""
            #Update the page to show instant the message
            page.update()
            
            #Generate a pre response and add it to the message list to get all the message with "\n"
            pre_response = Text(value="")
            chat_view.controls.append(
                Container(
                    content= Column(
                            spacing=5,
                            controls=[
                                Row(
                                    spacing=5,
                                    controls=[
                                    CircleAvatar(
                                        content=Text(value="B"),
                                        scale=0.8,
                                        bgcolor= colors.GREEN
                                    ),
                                    Text(value="Bot")
                                ]),
                                Container(
                                    padding= padding.only(left=47),
                                    content= pre_response
                                )
                            ]),
                    margin=margin.only(top= 10)
                )
            )
            page.update()
            
            #Create a empty string and concat the response that the ia generate and we can see the response in real time becouse we got the pre response
            response_text = ""
            for response_generate in generate(user_input, context):
                response_text += response_generate
                pre_response.value = response_text
                #Update the page to show all message 
                page.update()

            speak(response_text)

    #App structure
    chat_view = ListView(expand= True, auto_scroll= True)
    audio_bnt = IconButton(icon= icons.MIC, on_click=send_message)
    txt_input = TextField(hint_text="Type your message here", expand= True, autofocus= True, on_submit= send_message)
    send_btn = IconButton(icon= icons.SEND, on_click= send_message)
    input_row = Container(
            content= Row(
            [audio_bnt,txt_input, send_btn], 
            alignment= alignment.bottom_center
            )
        )

    #Title
    page.title = 'Chat IA Local'
    #Add all componenst to the page
    page.add(Column([chat_view, input_row], expand= True))

if __name__ == "__main__":
    app(target=main)
