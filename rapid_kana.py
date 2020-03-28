import sys
import wanakana
import time
import os
from random import randint
from google_speech import Speech

# CONFIGURATION FILE
DIRNAME, FILENAME = os.path.split(os.path.abspath(__file__))
SOURCE_FILE = "news.txt"
LANG = "ja"
class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class UserInterface:
    
    def __init__(self,):
        print('Start UI')

    def display(self, word):
        print(word)

    def display_answer(self, word):
        print(word)
        
    def get_response(self,):
        return input()

    def display_score(self, score, max_score):
        print("You get "+str(score)+" from "+ str(max_score))

    def display_speed(self, time, score):
        if time == 0:
            return
        print("SPEED: "+str(round(score*60/time))+" word/minute")

    def display_time(self, time):
        print("Total time: "+str(time)+' seconds')
    
class Timer:
    def __init__(self,):
        self._start_time = None

    def start(self):
        self._start_time = time.perf_counter()

    def stop(self):
        if (self._start_time == None):
            raise TimerError(f"Timer is running. Use .stop() to stop it")
    
        return time.perf_counter()-self._start_time

class RapidKana:
    EXIT= 'q'
    PARTICLE_LIST=['ga','ka','no','kara', 'ha','made','de','ni','wo','he','to','’','nado', 'desu']
    NONLETTER = '~!,.1234567890;:\'-"`"’‘'
    _script = None
    _ui = None
    _num_of_correct_ans = 0
    _total_word = 0
    _timer = None 
    
    def __init__(self, source):
        self._timer=Timer()
        self._ui=UserInterface()
        if (source == 'online'):
            self._script = self.get_script_from_web()
        elif (source == 'offline'):
            self._script = self.get_script_from_text(SOURCE_FILE)
            self._total_word = len(self._script)
            

    def get_script_from_web(self,):
        return None
    
    def get_script_from_text(self, text_file):
        with open(DIRNAME+'/'+text_file, 'r', encoding="utf8") as reader:
            full_text = reader.read()
        # read each word (split first)
        return full_text.split()

    def sequential_reading(self,):
        self._timer.start()
        for each_word in self._script:
            self._ui.display(each_word)
            response = self._ui.get_response()
            correct_answer=wanakana.to_romaji(each_word)
            if (response == correct_answer):
                self._num_of_correct_ans = self._num_of_correct_ans+1
            else :
                self._ui.display_answer(correct_answer)
                
        time_elapse = self._timer.stop()
        self._ui.display(time_elapse)

    def is_particle(self, word):
        kana = self.only_letters(wanakana.to_romaji(word))
        if kana in self.PARTICLE_LIST:
            return True
        else:
            return False

    def only_letters(self, word):
        for char in self.NONLETTER:
            word = word.replace(char, "");
        return word
    
    def random_reading(self,):
        self._timer.start()
        word_counter = 0
        for each_word in self._script:
            word_counter=word_counter+1
            rand_num=randint(0,len(self._script)-1)
            word = self._script[rand_num];
            if (self.is_particle(word)):
                continue
            self._ui.display(word)
            response = self._ui.get_response()

            if (response == self.EXIT):
                break;
            correct_answer=self.only_letters(wanakana.to_romaji(word))
            if (response == correct_answer):
                self._num_of_correct_ans = self._num_of_correct_ans+1
            else :
                self._ui.display_answer(correct_answer)
                
        time_elapse = int(self._timer.stop())
        self._ui.display_time(time_elapse)
        self._ui.display_score(self._num_of_correct_ans, word_counter)
        self._ui.display_speed(time_elapse, self._num_of_correct_ans)

def kana_reading():
    kana_reader=RapidKana('offline')
    kana_reader.random_reading()

def play_speech(text, speed):
    speech=Speech(text,LANG)
    sox_effects = ("speed", speed)
    speech.play(sox_effects)
    ##speech.play()

def rand_num_speech(max_num):
    user_input = input("'SPACE' to continue, 'q' to exit.")
    while (user_input!='q'):
        rand_num=str(randint(0,max_num))
        play_speech(rand_num, "1.0")
        user_input = input("'SPACE' to continue, 'q' to exit.")

def is_number(text):
    try:
        val=int(text)
        return True
    except ValueError:
        try:
            val=float(text)
            return True
        except ValueError:
            return False
    
def number_speech(options):
    
    if (len(options)==0):
        rand_num_speech(10000) # default range
    elif (options[0]=='-telp'):
        telp_speech()
    elif (options[0]=='-time'):
        time_speech()
    elif (options[0]=='-month'):
        month_speech()
    elif (is_number(options[0])):
        rand_num_speech(int(options[0]))
    else:
        print("unknown options")
    
def main():
    speech=Speech("10","ja")
    speech.play()
    arg = sys.argv[1:]          # ignore script name (arg[0])
    if (len(arg)==0):
        print('empty argument')
    elif (arg[0]=='kana' or arg[0]=='Kana'):
        kana_reading()
    elif (arg[0]=='num' or arg[0]=='Num'):
        number_speech(arg[1:])  # ignore the 'num' element
    else:
        print("unknown argument")
        
if __name__ == '__main__':
    main()
