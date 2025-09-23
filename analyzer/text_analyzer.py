import statistics as stats
import collections
import utils as ut
import exporters.export_analyze as exa

class TextAnalyzer():
    def __init__(self):
        
        self.text = ""           #النص المراد تحليله
        self.cleaned_text = ""   #حفظ النص النظيف
        self.results = {}        #حفظ النتائج
        self.num_of_top_words = 2
        self.word_characters = 1
        self.support_statistics = True
        self.support_clean = True
        self.file_number = 1

    # characters count
    def _chars_count(self):
        number_of_chars = len(self.cleaned_text)
        self.results.update({"chars_count": number_of_chars})
        return number_of_chars
        
    # the average of words length
    def _words_length_avg(self):
        total_length = 0
        length_avg = 0
        lengths = ut.words_length(self.cleaned_text)
        length_avg = sum(lengths) / len(lengths) if lengths else 0
        self.results["words_length_avg"] = length_avg
        return length_avg
        
    # top mode words
    def _top_popular_words(self):
        top_mode = []
        i = 1

        if len(ut.convert_to_list(self.cleaned_text)) <= 1:
            return None
            
        if self.word_characters < 1:
            return "Word Characters can not be less than 1"
        elif self.word_characters > 1:
            all_words = ut.filtered_words_by_char_num(self.cleaned_text, self.word_characters)
        else:
            all_words = ut.convert_to_list(self.cleaned_text)

        for top in collections.Counter(all_words).most_common(self.num_of_top_words):
            top_mode = top_mode + [top[0]]

        self.results.update({"top_popular_words": top_mode})
        return top_mode
        
    # Popular word
    def _popular_word(self):
        if len(ut.convert_to_list(self.cleaned_text)) <= 1:
            return None

        if self.word_characters < 1 or self.word_characters not in ut.words_length(self.cleaned_text):
            self.results.update({"popular_word": "Word Characters is invalid"})
            return "Word Characters is invalid"
        elif self.word_characters > 1:
            populars = collections.Counter(ut.filtered_words_by_char_num(self.cleaned_text, self.word_characters)).most_common(1)[0][0]
            self.results.update({"popular_word": populars})
            return populars
        else:
            populars = stats.mode(ut.convert_to_list(self.cleaned_text))
            self.results.update({"popular_word": populars})
            return populars
            

    # words count
    def _words_count(self):
        if len(ut.convert_to_list(self.cleaned_text)) <= 1:
            return 0
        counts = len(ut.convert_to_list(self.cleaned_text))
        self.results.update({"words_count": counts})
        return counts
    
    def analyze(self, text, file_number = 1, num_of_top_words = 2, word_characters = 1, support_statistics = True, support_clean = True):
        self.text = text
        self.cleaned_text = ut.clean_text(self.text)
        if not self.cleaned_text.strip():
            self.results.update({
            "words_count": 0,
            "chars_count": 0,
            "words_length_avg": 0,
            "popular_word": None,
            "top_popular_words": []})
            return

        self.results.update({"file_number": file_number})
        self.num_of_top_words = num_of_top_words
        self.word_characters = word_characters
        self.support_statistics = support_statistics
        self.support_clean = support_clean
        self.file_number = file_number
    
        self._chars_count()
        self._words_length_avg()
        self._top_popular_words()
        self._popular_word()
        self._words_count()

        exa.Export.print_console(self.text, self.cleaned_text, self.results, support_clean, support_statistics)
        exa.Export.export_csv(self.results, self.file_number)
        exa.Export.export_json(self.results, self.file_number)