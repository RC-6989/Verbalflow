from groq import Groq

api_key = "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"
prompt = "Give feedback for the following speech as if you were a professional speaker. Compliment what you think is effective and give guidance on what you think could be improved upon. Keep the feedback/compliments brief and in point form notes under 2 categories: “Strengths” and “Areas for Improvement. You will also be given an array of emotions detected from the users face, approximately 2 a second. Remove redundant and useless emotion data that might be unrealiable and give the user a general rating based on their emotion. Then evaluate their word choice and describe the tone it conveys. Your ouput must include the following in the correct format. Jot note feedback for strengths, jot note feedback for weaknesses, a overall emotion rating /10, a word that describes the tone of the speech based on the words used, a tone rating /10 and an overall rating for the speech /100."

client = Groq(
    api_key=api_key,
)
def get_feedback(emotions_list, transcript):
    global prompt
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