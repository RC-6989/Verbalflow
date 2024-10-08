# Currently an incomplete project.
VerbalFlow was created for HTN2024, but currently has a few (corruption) bugs.

#### What it does
Verbalflow gives its users tailored feedback on their communication skills using various APIs. It collects data about the user's face using vgg-face and facenet APIs, and it also records the user's word choice and tone. It then feeds all of the data it collected into groq's API to create it's feedback.


#### Requirements
ffmpeg


#### How to start
Run `python app.py`

Links:
https://devpost.com/software/verbalflow

How to install ffmpeg on Windows: 
https://phoenixnap.com/kb/ffmpeg-windows

How to fix mac os pyaudio install error:
https://stackoverflow.com/questions/73268630/error-could-not-build-wheels-for-pyaudio-which-is-required-to-install-pyprojec
