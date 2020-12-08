import sys
import wanakana
import time
import os
import pandas as pd
from random import randint
from google_speech import Speech
import re

# CONFIGURATION FILE
filename_txt="vocab.txt"
DIRNAME, FILENAME = os.path.split(os.path.abspath(__file__))
DEFAULT_VOCAB_FILE = 0
DRIVER_DELAY = 0.5 # second(s)
N_TIMES = 3 #repetition

class Vocab:
    def __init__(self, filename, format_file):
        if(format_file=='txt'):
            with open(DIRNAME+"/"+filename, 'r', encoding="utf8") as reader:
                raw_data = reader.read().splitlines()
            self.__df=self.__parse_txt(raw_data)
        elif (format_file=='csv'):
            # not completed yet
            self.__df=pd.read_csv(filename, error_bad_lines=False)
        else:
            print('error')

    def __parse_txt(self, raw_data):
        en=[]
        jp=[]
        for idx in range (len(raw_data)):
            line = raw_data[idx]
            en.append(re.search('/(.+?)/', line).group(1))
            end=line.find(' ')
            jp.append(line[:end])
        list_of_tuples=list(zip(jp,en))
        return pd.DataFrame(list_of_tuples, columns=('jp', 'en'))
        
    def get_rand_vocab(self,):
        row_num = randint(0,self.__df.shape[0]-1)
        en=self.__df.iloc[row_num]['en']
        jp=self.__df.iloc[row_num]['jp']
        print(row_num)
        print(en)
        print(jp)
        return en,jp
    
class Speaker:
    def __init__(self, lesson_num):
        filename='vocab/Minna_no_nihongo_2.'+str(lesson_num)+".txt"
        self.__vocab = Vocab(filename, 'txt')

    def __driver(self, text, lang):
        speech=Speech(text, lang)
        sox_effects = ("speed", "1.0")
        speech.play(sox_effects)
        time.sleep(DRIVER_DELAY)

    def __driver_jp(self, text):
        self.__driver(text, "ja")

    def __driver_en(self, text):
        self.__driver(text, "en")
        
    def speak_jp_to_en(self, interval):
        en,jp=self.__vocab.get_rand_vocab()
        for idx in range(N_TIMES):
            self.__driver_jp(jp)
            self.__driver_en(en)
        time.sleep(interval)
                
    def speak_en_to_jp(self, interval):
        en,jp=self.__vocab.get_rand_vocab()
        for idx in range(N_TIMES):
            self.__driver_en(jp)
            self.__driver_jp(en)
        time.sleep(interval)
        
def main():
    arg=sys.argv[1:]
    try:
        if (len(arg)==0):
            speaker=Speaker(DEFAULT_VOCAB_FILE)
        else:
            speaker=Speaker(arg[0])
        while True:
            speaker.speak_jp_to_en(DRIVER_DELAY)
    except KeyboardInterrupt:
        print("Interrupt")
        pass

if __name__ == '__main__':
    main()
