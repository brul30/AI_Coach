import requests
import json
import os
from openai import OpenAI


def make_openAI_request(data_dict):
    OPENAI_SECRET_KEY = os.getenv("OPENAI_SECRET_KEY",default='none')
    #OPENAI_ENDPOINT = config("OPENAI_ENDPOINT",default='none')
    client = OpenAI(api_key=OPENAI_SECRET_KEY)

    assistant = client.beta.assistants.create(
        name = "Math tutor",
        description = "You are a personal fitnes trainer Trainer, give me a detailed weekly meal plan using the following parameters",
        tools=[{"type": "code_interpreter"}],
    #  model="gpt-4-1106-preview",
        model="gpt-3.5-turbo",
    )

    thread = client.beta.threads.create()


    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = data_dict
    )


    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant.id
    )

    run = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id = run.id
    )

    messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )

    for message in reversed(messages.data):
        print(message.role + ": " + message.content[0].text.value)


