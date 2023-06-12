import openai
import os
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from pydub import AudioSegment
from pydub.playback import play

openai.api_key = os.getenv("OPENAI_API_KEY")

def makemp3(text: str):
    azure_key = os.getenv("AZURE_KEY")
    print("Start creating Voice mp3")
    speech_config = SpeechConfig(
        subscription=azure_key, region="eastus")

    speech_config.speech_synthesis_language = "zh-tw"
    audio_config = AudioOutputConfig(filename="gpt-out.mp3")
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    speech_config.set_speech_synthesis_output_format(
        SpeechSynthesisOutputFormat["Audio16Khz128KBitRateMonoMp3"])
    synthesizer.speak_text_async(text).get()
    print("End of create")



def gpt(content: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個友善的人，請在回答時優先使用中文"},
            {"role": "user", "content": content}
        ]
    )
    data = completion['choices'][0]['message']['content']
    out = ("GPT說: ", data)
    reply = ("".join('%s' % id for id in out))
    makemp3(reply)

while (True):
    say = input("你的問題？:")
    gpt(say)
    voice = AudioSegment.from_file("gpt-out.mp3")
    play(voice)
    os.remove("gpt-out.mp3")
