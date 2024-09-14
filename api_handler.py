from groq import Groq

api_key = "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"
prompt = "You are going to be looking at data from a machine learning model from a web application. You are going to be looking at a list of recorded emotions on a users face throughout their speech. This list will be words seperated by commas. These emotions are predicted every single frame, so work with the data to remove discrepancies and redundancies. Then give the user a score from 1-10 based on their tone throughout the speech. You will also be getting a transcript of the users speech as input. Give them a score out of 10 for the speech. Then create an overall score which is an average of the two Your output must only be two ratings out of ten, one for the emotions and one for the speech. Then a final rating which is an average. Then give the user feedback on how to improve the speech. Work with the emotion data as best you can, keeping in mind it must be referenced with the script to determine effectiveness. I.E. a sad expression for a sad story, and nothing else. " + "\n" + "Emotions: "
client = Groq(
    api_key=api_key,
)
def get_feedback(emotions_list, transcript):
    for i in emotions_list:
        prompt = prompt + ", " + i

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt + "\n" + "Transcript: " + transcript,
            }
        ],
        model="llama3-8b-8192",
    )

    feedback = chat_completion.choices[0].message.content
    return feedback