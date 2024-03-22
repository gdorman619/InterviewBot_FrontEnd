from audio import record_user_audio
import vlc
import os
from dotenv import load_dotenv
import sys


from interview_functions import login_interview_bot, \
    reset_chat_context_with_detail, \
    receive_bot_message, \
    send_user_audio, \
    view_chat_history, \
    reset_chat_with_custom_context
    
    
voices_dict = {
    "Liam":"TX3LPaxmHKxFdv7VOQHJ",
    "Serena":"pMsXgVXv3BLzUgSXRplE",
    "Jeremy":"bVMeCyTHy58xNoL34h3p",
    "Michael":"flq6f7yk4E4fJM5XTYuZ",
    "Freya":"jsCqWAovK2LkecY7zXl4",
    "Grace":"oWAxZDx7w5VEj9dCyTzz",
    "Jessie":"t0jbNlBVZ17f02VDIeMI",
    "Domi":"AZnzlk1XvdvUeBnXmlld",
    "Drew":"29vD33N1CtxCmqQRPOHJ",
}

input_text = ''

while input_text != "8":
    
    print("")
    print("Please choose from the following options:")
    print("")
    print("1: Login To Interview Bot - This should be selected first when program is first executed.")
    print("2: Reset Chat Context - Template Using Variables")
    print("3: Reset Chat Context - Full Custom Context")
    print("4: Receive Bot Message")
    print("5: Replay Last Bot Message - Will only work if audio has already played once during program execution.")
    print("6: Record/Send User Audio")
    print("7: View Chat History")
    print("8: Exit Program")
    print("")
    input_text = input("Enter Selection: ")
    print("")
    
    load_dotenv(override=True)
    
    

    if input_text == '1':

        # Logging in

        response_code, response_json = login_interview_bot(
            os.environ.get("input_email"), os.environ.get("input_pw"))

        if response_code == 200:

            user_username = response_json['Username']

            user_token = response_json['Token']

            print(f'Logged In as: {os.environ.get("input_email")}')

        else:
            # Need to make backend say bad credentials
            print(response_json["message"])

    elif input_text == '2':

        # Resetting Chat Context - Template Using Variables
        response_code, response_json = reset_chat_context_with_detail(
            token=user_token,
            industry=os.environ.get("industry"),
            subject=os.environ.get("subject"),
            job_level=os.environ.get("job_level"),
            num_interview_questions=os.environ.get("num_interview_questions"),
            dest_translate_lang=os.environ.get("dest_translate_language"))

        if response_code == 200:

            user_username = response_json['user_id']

            user_email = response_json['user_email']

            context_message = response_json['message']

            print(context_message)

            print("")

        else:
            print("Error during setting chat context template with variables.")
            print(response_json)
            
    elif input_text == '3':
        
        with open('custom_context.txt','r') as f:
            custom_context = f.read()

        # Resetting Chat Context - Full Custom Context
        response_code, response_json = reset_chat_with_custom_context(
            token=user_token,
            context=custom_context)

        if response_code == 200:

            user_username = response_json['user_id']

            user_email = response_json['user_email']

            context_message = response_json['message']

            print(context_message)

            print("")

        else:
            print("Error during setting custom chat context.")
            print(response_json)


    elif input_text == '4':
        
        # Defaults to Jessie voice if incorrect name put in .env file.
        chosen_voice_id = voices_dict.get(os.environ.get("voice_name"),"t0jbNlBVZ17f02VDIeMI")

        # Receiving Bot Message
        response_code, response_json = receive_bot_message(
            token=user_token, elevenlabs_voice_id=chosen_voice_id)

        if response_code == 200:

            user_username = response_json['user_id']

            user_email = response_json['user_email']

            bot_message = response_json['message']

            bot_audio_url = response_json['audio_url']

            p = vlc.MediaPlayer(bot_audio_url)

            p.play()

        elif response_code == 503:
            print("")
            print(response_json)
            print("")

        else:
            print("")
            print("Error during receiving bot message")
            print(response_json)

    elif input_text == '5':

        try:
            # Replay Bot Audio
            p = vlc.MediaPlayer(bot_audio_url)

            p.play()
        except NameError:
            print("Last bot audio not able to be played.")
            print("")

    elif input_text == '6':

        record_again = True

        while record_again == True:
            record_user_audio()

            user_replay_choice = input(
                "Would you like to re-record your message? If so enter 'Y'. ")

            if user_replay_choice.upper() == 'Y':
                record_again = True
            else:
                record_again = False

        # Send User Response
        response_code, response_json = send_user_audio(
            token=user_token,
            audio_file_path=r"User Recording.wav")

        if response_code == 200:

            user_username = response_json['user_id']

            user_email = response_json['user_email']

            user_transcribed_text = response_json['user_transcribed_text']

            print(user_transcribed_text)

        else:
            print("Error during transcribing user text")
            print(response_json)

    elif input_text == '7':

        # Receiving Bot Message
        response_code, response_json = view_chat_history(
            token=user_token)

        if response_code == 200:

            user_username = response_json['user_id']

            user_email = response_json['user_email']

            chat_history = response_json['chat_history']

            print("")

            for item in chat_history:
                print("")
                print("Content: ", item['content'])
                print("")
                print("Role: ", item['role'])

            print("")

        else:
            print("")
            print("Error during receiving bot message")
            print(response_json)
            
    elif input_text == '8':
        print("Program exited!")
        sys.exit(0)
            
    else:
        print("Not a valid response. Please try again.")
