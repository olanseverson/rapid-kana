import wanakana
import time

# CONFIGURATION FILE
SOURCE_FILE = "news.txt"
class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class UserInterface:
    
    def __init__(self,):

    def display(word):
        print(word)

    def display_answer(word):
        print(word);
    def get_response():
        return input()
    
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
    _script = None
    _ui = None
    _num_of_correct_ans = 0
    _total_word = 0
    _timer = None 
    
    def __init__(self, source):
        self._timer=Timer()
        self._ui=UserInterface()
        if (method == 'online'):
            self._script = self.get_script_from_web()
        elif (source == 'offline'):
            self._script = self.get_script_from_text(SOURCE_FILE)
            self._total_word = len(self._script)
            

    def get_script_from_web():
        return None
    
    def get_script_from_text(self, text_file):
        with open(DIRNAME + text_file, 'r', encoding="utf8") as reader:
            full_text = reader.read()

        # read each word (split first)
        return full_text.split()

    def start_reading():
        self._timer.start()
        for each_word in self._script:
            self._ui.display(each_word)
            response = self._ui.get_response()
            correct_answer=wanakana.to_romaji(each_word)
            if (response == correct_answer){
                self._num_of_correct_ans = self._num_of_correct_ans+1
            } else {
                self._ui.display_answer(correct_answer)
            }
        time_elapse = self._timer.stop()
        self._ui.display(time_elapse)

def main():
    kana_reader=RapidKana('offline')
    kana_reader.start_reading()
    
if __name == '__main__':
    main()

