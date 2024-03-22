import requests
import json


def login_interview_bot(email, pw):

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'email': email,
        'password': pw,
    }

    response = requests.post(
        'https://interview-bot-py-run-uuzwn5a7ca-uc.a.run.app/login', params=params, headers=headers)

    output_json = json.loads(response.text)

    response_code = response.status_code

    return response_code, output_json


def reset_chat_context_with_detail(token,
                                   dest_translate_lang='',
                                   industry='Programming',
                                   job_level='Senior',
                                   num_interview_questions=3,
                                   subject='Python'):

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'dest_translate_lang': dest_translate_lang,
        'industry': industry,
        'job_level': job_level,
        'num_interview_questions': num_interview_questions,
        'subject': subject,
        'token': token
    }

    response = requests.post(
        'https://interview-bot-py-run-uuzwn5a7ca-uc.a.run.app/reset-chat-and-set-chat-context',
        headers=headers,
        json=json_data,
    )

    output_json = json.loads(response.text)

    response_code = response.status_code

    return response_code, output_json


def receive_bot_message(token, elevenlabs_voice_id="t0jbNlBVZ17f02VDIeMI"):

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'token': token,
        'voice_id': elevenlabs_voice_id
    }

    response = requests.post(
        'https://interview-bot-py-run-uuzwn5a7ca-uc.a.run.app/receive-bot-message',
        headers=headers,
        json=json_data,
    )
    
    if response.status_code == 503:
            return(response.status_code, "Text too big for Eleven Labs.\nYou can try looking up the chat history to see what the bot stated in text.")

    output_json = json.loads(response.text)

    response_code = response.status_code
    
    return response_code, output_json


def send_user_audio(token, audio_file_path):

    headers = {'accept': 'application/json'}

    files = {
        'user_token': (None, token),
        'file': (audio_file_path, open(audio_file_path, 'rb'), 'audio/mpeg'),
    }

    response = requests.post(
        'https://interview-bot-py-run-uuzwn5a7ca-uc.a.run.app/transcribe-user-audio/',
        headers=headers,
        files=files,
    )

    output_json = json.loads(response.text)

    response_code = response.status_code

    return response_code, output_json


def view_chat_history(token):

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'token': token,
    }

    response = requests.post(
        'https://interview-bot-py-run-uuzwn5a7ca-uc.a.run.app/return-chat-history',
        headers=headers,
        json=json_data,
    )

    output_json = json.loads(response.text)

    response_code = response.status_code
    
    return response_code, output_json


def reset_chat_with_custom_context(token,
                                   context='Hello, I want you to interview me for a job.'):

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'context': context,
        'token': token
    }

    response = requests.post(
        'https://interview-bot-py-run-uuzwn5a7ca-uc.a.run.app/reset-chat-and-set-custom-chat-context',
        headers=headers,
        json=json_data,
    )

    output_json = json.loads(response.text)

    response_code = response.status_code

    return response_code, output_json
