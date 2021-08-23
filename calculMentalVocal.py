#--------Modules importation--------#
import random
from time import sleep
from gtts import gTTS
import os
import pygame


#--------Calcul generation--------#
# Lists of intervals
interval1 = [1, 10]
interval2 = [1, 100] 

# Liste of operators
operators = ["+", "-", "x", "/"]

# Other
thinkingTime = 5

def randomCalcul(interval):
    '''
    Generate a random calcul on a defined interval using the 4 operators
    Arg : 
        interval : list of two ints (begin, end) 
    Return : 
        question : string containing the calcul
        answer : string containing the answer of the calcul
    '''
    # Random operation
    n1 = random.randint(interval[0], interval[1])
    n2 = random.randint(interval[0], interval[1])
    operator = operators[random.randint(0, 3)]

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
    question = str(n1) + operator + str(n2) + "?"
    answer = str(result)
    return question, answer


#--------Voice generation--------#
def TTS(textToSay, language = 'en'):
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
    os.system("start calcul.mp3")


#--------G.U.I--------#
backgroundColour = (255,255,255)
(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mental calcul')

pygame.font.init()
font = pygame.font.Font('Verdana.ttf', 30)


#--------Main loop--------#
run = True
while run:
    print("----------------------")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #----QUESTION----#
    # Generate a calcul
    question, answer = randomCalcul(interval1)
    # Read the question
    TTS(question)
    
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
    TTS(answer)
    # Graphic user interface
    print(answer)

    screen.fill(backgroundColour)
    text = font.render(answer, False, (0, 0, 0))
    screen.blit(text, (width//2 - 20, height//2 - 10))
    pygame.display.flip()
    
    sleep(3)