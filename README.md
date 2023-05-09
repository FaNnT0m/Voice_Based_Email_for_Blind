# Voice_Based_Email_for_Blind

README for Voice-Based Email for Blind

This project is a voice-based email system designed for blind individuals. It allows users to compose, send, and receive emails without having to rely on a visual interface. The system uses speech recognition and text-to-speech conversion to allow the user to interact with the email system through voice commands.

Prerequisites:
- Python 3.x installed on your system
- Access to an gmail account that supports IMAP and SMTP protocols
- PyAudio library installed on your system
- SpeechRecognition library installed on your system
- gTTS library installed on your system
- mpg321 or another audio player installed on your system

Installation:

1. Clone or download the project repository to your local machine.
2. Install the necessary Python libraries: PyAudio, SpeechRecognition, and gTTS.
3. Install an audio player such as mpg321 on your system.
4. Update the email account credentials and email server settings in the "config.py" file.
5. Run the "voice_based_email.py" file to start the voice-based email system.

Usage:

1. To compose a new email, say "compose email" or "new email".
2. The system will prompt you to speak the recipient's email address. Say the email address.
3. Next, the system will prompt you to speak the subject of the email. Say the subject.
4. Then, the system will prompt you to speak the body of the email. Say the body.
5. After you finish speaking the body of the email, the system will confirm if you want to send the email. Say "yes" or "no" to confirm or cancel the email.
6. To check your inbox, say "check email" or "inbox".
7. The system will read the subject and sender of each email in your inbox. To hear the body of a specific email, say "read email number X" where X is the number of the email you want to read.
8. To reply to an email, say "reply email number X" and follow the prompts to compose your reply.
9. To delete an email, say "delete email number X" where X is the number of the email you want to delete.
