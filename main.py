import smtplib
import speech_recognition as sr
import email
import pyaudio
import pyttsx3
import imaplib
import os
import pyaudio
import wave
import email.mime.application
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


listener = sr.Recognizer()
tts = pyttsx3.Engine()

audio_format = pyaudio.paInt16
channels = 1
sample_rate = 44100
chunk_size = 1024
audio_filename =""

dict = {"arpit": "dakshrao0805@gmail.com", "mitali": "mitaleeverma763@gmail.com", "anand": "suthar.anand28@gmail.com", "ishan": "ishan.md1911@gmail.com"}
files = {"test": "test.txt", "sorry": "sorry.txt", "congrats": "congrats.txt"}
audio_files ={"bela": "bella.wav","bella": "bella.wav", "benz": "benz.wav"}

myMail = "testbyarpit007@gmail.com"
myPass = "auoezywsqcrtakwu"


def speak(text):
    tts.say(text)
    tts.runAndWait()


def mic():
    with sr.Microphone() as source2:
        print("program is listening....")
        speak("speak")
        # listener.adjust_for_ambient_noise(source2, duration=0.2)
        voice = listener.listen(source2)
        data = listener.recognize_google(voice)
        print(data)
        return data.lower()


def record():
    speak("Now you can record the message")
    speak("Enter duration for which you want to record")
    duration = int(mic())
    audio=pyaudio.PyAudio()

    stream = audio.open(format=audio_format, channels=channels,
                        rate=sample_rate, input=True,
                        frames_per_buffer=chunk_size)

    speak("Now you can start recording")
    frames = []
    for i in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    filename = "recording.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(audio_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    speak("Recording saved successfully")

def send_email():
    speak("Speak the recipient's name")
    name = mic()
    receiver = dict[name]
    speak("Speak the subject of the email")
    subject = mic()
    speak("Speak the body of the email")
    body = mic()
    speak("Do you want to attach any text file")
    text_file_choice = mic()
    if(text_file_choice =="yes"):
        speak("Speak the name of text file")
        choice1 = mic()
        text_filename = files[choice1]
        with open(text_filename, 'r') as f:
            # Create an instance of MIMEText and attach the text file to it
            text = MIMEText(f.read())
            text.add_header('Content-Disposition', 'attachment', filename=text_filename)

    speak("Do you want to attach any audio file")
    audio_file_choice = mic()
    if (audio_file_choice == "yes"):     #what if the user don't want to send a text file
        speak("Do you want to record audio or attach the file")
        subchoice=mic()
        if subchoice=="record":
            record()
            audio_filename = "recording.wav"
        else:
            speak("Speak the name of audio file")
            choice2 = mic()
            audio_filename = audio_files[choice2]

        with open(audio_filename, 'rb') as a:
            # Create an instance of MIMEText and attach the text file to it
            audio = MIMEAudio(a.read())
            audio.add_header('Content-Disposition', 'attachment', filename=audio_filename)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(myMail, myPass)

    msg = MIMEMultipart()
    msg["From"] = myMail
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body))
    if(text_file_choice=="yes" and audio_file_choice=="yes"):
        msg.attach(text)
        msg.attach(audio)
        server.sendmail(myMail, receiver, msg.as_string())
    elif(text_file_choice=="yes"):
        msg.attach(text)
        server.sendmail(myMail, receiver, msg.as_string())
    elif(audio_file_choice=="yes"):
        msg.attach(audio)
        server.sendmail(myMail, receiver, msg.as_string())
    else:
        server.send_message(msg)
    # email.set_content(body)
    # server.send_message(email)


    speak("Congratulations, your email has been sent")


def read_email():
    # Connect to the IMAP server
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
    imap_server.login(myMail, myPass)
    imap_server.select("inbox")

    # Search for emails
    status, messages = imap_server.search(None, "UNSEEN")  # Only search for unread emails

    if status == "OK":
        for num in messages[0].split():
            # Fetch the email and parse its contents
            status, message = imap_server.fetch(num, "(RFC822)")
            email_data = message[0][1]
            mail = email.message_from_bytes(email_data)

            # Extract the relevant information from the email
            subject = mail["Subject"]
            sender = mail["From"]
            body = ""

            if mail.is_multipart():
                for part in mail.walk():
                    part_type = part.get_content_type()
                    if part_type == "text/plain":
                        body += part.get_payload(decode=True).decode("utf-8")
                    elif part_type == "audio/wav":
                        audio_data = part.get_payload(decode=True)
                        audio_file = wave.open("received_audio.wav", "wb")
                        audio_file.setnchannels(1)
                        audio_file.setsampwidth(2)
                        audio_file.setframerate(44100)
                        audio_file.writeframes(audio_data)
                        audio_file.close()

                    elif "attachment" in part_type:
                        filename = part.get_filename()
                        attachment = email.mime.application.MIMEApplication(part.get_payload(decode=True),
                                                                            _subtype=os.path.splitext(filename)[1][1:])
                        attachment.add_header("Content-Disposition", "attachment", filename=filename)
                        with open(filename, "wb") as f:
                            f.write(attachment.as_bytes())
            else:
                body = mail.get_payload(decode=True).decode("utf-8")

            # Speak the contents of the email
            print(f"New email from {sender}. Subject: {subject}. Body: {body}")
            speak(f"New email from {sender}. Subject: {subject}. Body: {body}")

    # Disconnect from the IMAP server
    imap_server.close()
    imap_server.logout()




def main():
    speak("Whether you want to send the email or read the unread emails")
    choice = mic()
    # try:
    #     if choice=="read":
    #         read_email()
    #     else:
    #         send_email(dict)
    #
    # except Exception as e:
    #     speak(f"Sorry, an error occurred: {e}")

    if choice == "read":
        read_email()
    else:
        send_email()

main()
