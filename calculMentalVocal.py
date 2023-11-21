#--------Modules importation--------#
import random
from time import sleep
from gtts import gTTS
import os
import pygame
from pydub import AudioSegment
import ffmpeg

AudioSegment.converter = "C:/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffmpeg = "C:/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffprobe = "C:/ffmpeg/bin/ffprobe.exe"

#--------Calcul generation--------#
# Lists of intervals
Intervals = [
    [1, 10],
    [1, 20],
    [1, 30],
    [1, 50],
    [1, 100], 
    [1, 1000]
]

# Liste of operators
Operators = [
    ["+", "-", "x", "/"],
    ["+", "-"],
    ["x", "/"]
]

def randomCalcul(interval: list, operators:list) -> str:
    '''
    Generate a random calcul on a defined interval using the choosen operators
    Arg : 
        interval : list of two ints (begin, end) 
        operators : list of the possible operations 
    Return : 
        question : string containing the calcul
        answer : string containing the answer of the calcul
    '''
    # Random numbers
    n1 = random.randint(interval[0], interval[1])
    n2 = random.randint(interval[0], interval[1])
    # Random calcul operators
    operator = operators[random.randint(0, len(operators) -1)]

    # Calcul of the answer
    if operator == "+":
        result = n1 + n2
    elif operator == "-":
        result = n1 - n2
    elif operator == "x":
        result = n1 * n2
    else:
        result = n1 / n2
    
    # Composition of question & answer, and return
    question = str(n1) + operator + str(n2) + " = ?"
    answer = str(result)

    return question, answer

#--------Voice generation--------#
def TTS(textToSay: str, language: str, play_sound: str):
    '''
    Convert a string text into speech
    Arg : 
        textToSay : string containing the text to convert into speech
        language : string containing the required language speech
    return : 
        void
    '''
    # create vocal calcul
    vocalCalcul = gTTS(text=textToSay, lang=language, slow=False)
    # save vocal calcul
    vocalCalcul.save("calcul.mp3")
    # play vocal calcul
    if play_sound:
        os.system("start calcul.mp3")

def save_TTS_playlist(textToSay:str, language: str, file_name:str):
    # create vocal calcul
    vocalCalcul = gTTS(text=textToSay, lang=language, slow=False)
    # save vocal calcul
    vocalCalcul.save(file_name)


#--------Choice of game parameters--------#
def chooseParameters():
    '''
    Let the player choose its interval of calcul, operators and time to think of the result
    Arg : 
        void
    Return : 
        choosenInterval : int representing the interval reading index
        choosenOperators : int representing the operators reading index
        thinkingTime : int representing the time to think of the result
    '''
    # ask the player for its game parameters

    # interval choice
    for i in range(len(Intervals)):
        print(f'{i+1} : {Intervals[i]}')
    choosenInterval = int(input("Intervalle choisi > "))

    # operators choice
    for i in range(len(Operators)):
        print(f'{i+1} : {Operators[i]}')   
    choosenOperators = int(input('Opérateurs choisi > '))

    # thinking time choice 
    thinkingTime = int(input('Combien de temps de réflexion ? > '))

    # Game mode
    GUImode = bool(int(input('0: Generate a playlist\n 1: Play now > ')))

    return choosenInterval, choosenOperators, thinkingTime, GUImode


#--------G.U.I--------#
backgroundColour = (255,255,255)
(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mental calcul')

pygame.font.init()
font = pygame.font.Font('Verdana.ttf', 30)
pygame.display.flip()

# Asking for parameters
choosenInterval, choosenOperators, thinkingTime, GUImode = chooseParameters()

#--------Main loop--------#
if GUImode:
    run = True
    while run:
        pygame.display.flip()
        print("----------------------")

        #----QUESTION----#
        # Generate a calcul
        question, answer = randomCalcul(Intervals[choosenInterval - 1], Operators[choosenOperators - 1])

        # Pygame events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Read the question
        TTS(question, 'en', True)
        
        # Graphic interface update
        print(question)

        screen.fill(backgroundColour)
        text = font.render(question, False, (0, 0, 0))
        screen.blit(text, (width//2 - 40, height//2 - 10))
        pygame.display.flip()


        #----THINKING TIME----#
        sleep(thinkingTime)

        #----ANSWER----#
        # Read the answer
        TTS(answer, 'en', True)
        # Graphic user interface
        print(answer)
        pygame.display.flip()

        screen.fill(backgroundColour)
        text = font.render(answer, False, (0, 0, 0))
        screen.blit(text, (width//2 - 20, height//2 - 10))
        pygame.display.flip()
        
        sleep(1)
else:
    joined_sound = AudioSegment.silent(duration=1000)
    for i in range(3):
        # Generate a calcul
        question, answer = randomCalcul(Intervals[choosenInterval - 1], Operators[choosenOperators - 1])
       
        print(question)
        print(answer)

        # Generate mp3 files
        question_title, answer_title = 'question' + str(i+1) + '.mp3', 'answer' + str(i+1) + '.mp3'
        save_TTS_playlist(question, 'en', question_title)
        save_TTS_playlist(answer, 'en', answer_title)

        print(question_title)
        print(answer_title)

        print(os.getcwd())

        joined_sound += AudioSegment.from_mp3(question_title)
        joined_sound += AudioSegment.silent(duration = thinkingTime * 1000)
        joined_sound += AudioSegment.from_mp3(answer_title)
    
    joined_sound.export("joinedCalculus.mp3", format="mp3")