import speech_recognition as sr
import random
from textblob import TextBlob
from gtts import gTTS
import playsound

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    return playsound.playsound('E:/Hacktopia-GNI/code/bot/output.mp3')

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""
sum=0
if __name__ == "__main__":
    # Name and nickname conversation
    t1='Hello please tell me your name or nickname?'
    t=speak_text(t1)
    name = speech_to_text()  # Input name directly
    print('')
    e1='Do you have a nickname Yes/No?'
    e=speak_text(e1)
    ans = speech_to_text()  # Input answer directly
    print('')

    if ans.lower() == 'yes' or ans.lower() == 'y':
        m='what is your nickname?'
        m1=speak_text(m)
        nickname = speech_to_text() # Input nickname directly
        z='Nice to meet you' + nickname
        z1=speak_text(z)
    else:
        nickname = name + ' ' 
        m='I will call you ' +nickname
        m1=speak_text(m)
    print('')

    # Greeting random selection and polarity-based response
    questions = [
        'So ' + nickname + ' how are you today?',
        'Howdy ' + nickname + ' how are you feeling?',
        "So " + nickname + " what's up with you?",
        'Greetings human, are you well?',
        'So ' + nickname + ' how are things going?'
    ]

    o=random.choice(questions)
    o1=speak_text(o)
    ans = speech_to_text()
    print('')
    blob = TextBlob(ans)
    if blob.polarity > 0:
        m='I am glad that you are well'
        m1=speak_text(m)
    else:
        m= nickname+ "that doesn't sound so good"
        m1=speak_text(m)

    # Random question on a random topic
    topics = [
        'football',
        'this weather',
        'Melbourne',
        'The Joker',
        'Endgame',
        'Python',
        'computer games',
        'chatbots'
    ]

    questions = [
        'What is your take on ',
        'What do you think about ',
        'How do you feel about ',
        nickname + ' do you like ',
        'I would like your opinion on ',
        'I would love to know what you think about ' 
    ]

    for i in range(0, random.randint(2, 4)):
        topic = random.choice(topics)
        topics.remove(topic)
        question = random.choice(questions)
        questions.remove(question)
        x=(question + topic + '?')
        x1=speak_text(x)

        # Response to random question using sentiment analysis
        ans = speech_to_text()
        print('')
        blob = TextBlob(ans)

        # Respond appropriately to positive and negative sentiment
        if blob.polarity > 0.5:
            a = 'Wow you really love ' + topic
        elif blob.polarity > 0.1:
            a = 'Cool you like ' + topic
        elif blob.polarity < -0.1:
            a = 'Hmm, not a fan of ' + topic
        elif blob.polarity < -0.5:
            a = 'So you hate ' + topic
        else:
            a = 'That is a very neutral view on ' + topic
            
        sum=sum+blob.polarity

        if blob.subjectivity > 0.6:
            m= (a + ' and you are totally biased')
            m1=speak_text(m)
        elif blob.subjectivity > 0.3:
            m=(a + ' and you are a bit biased')
            m1=speak_text(m)
        else:
            m=(a + ' and quite objective')
            m1=speak_text(m)
        

    print("sum is" ,sum)

    # Random goodbye
    goodbyes = [
        'Catch ya later ' + nickname,
        'Nice chatting yo you ' + name + ' I am off now',
        'Yaawn, I am tired of chatting with you, bye bye',
        'Good talk my friend, see you next time',
        'That was a pleasant chat ' + name + ' goodbye for now'
    ]

    b=(random.choice(goodbyes))
    b1=speak_text(b)
