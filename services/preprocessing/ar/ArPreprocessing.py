import pandas as pd
import re
from nltk.corpus import stopwords;
from nltk.tokenize import word_tokenize
from nltk.stem.isri import ISRIStemmer
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer
from camel_tools.tokenizers.word import simple_word_tokenize as tokenizer
from camel_tools.utils.normalize import normalize_unicode, normalize_alef_maksura_ar, normalize_teh_marbuta_ar, normalize_alef_ar
from camel_tools.utils.dediac import dediac_ar

class ArPreprocessing:

    # Remove non-Arabic characters
    def remove_non_arabic(self, text):
        arabic_text = re.sub(r'[^\u0600-\u06FF\s]', '', str(text))
        return arabic_text
        
    # Remove Arabic numbers
    def remove_arabic_numbers(self, text):
        return re.sub(r'[٠-٩]', '', text)

    # Punctuation removal
    arabic_punctuation = """/ːː،؛؟.٪؛،:«»::–()[]{}<>+=-%*/&:|~\\''``"""
    translator = str.maketrans('', '', arabic_punctuation)

    def remove_punctuation(self, text):
        if isinstance(text, str):
            return text.translate(self.translator)
        return text

    # Initialize disambiguators
    mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
    msa_atb_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='atbtok')

    # Regex pattern to split by _ and +
    pattern = re.compile(r'[^_+]+')

    # Remove stopwords
    def remove_stopwords_arabic(self, text):
        if pd.isna(text):
            return text 
        custom_stopwords = ['لل', 'أليس', '', 'ك', 'س', 'ف', 'ب', 'أو', 'و', 'ما', 'لو', 'ال', 'لا', 'ّ', 'ٌ', ' ', 'ء', 'ئ', '‘', '؛', 'أ', 'إ', ',', '’', 'آ', '~', 'ًٍَُِْ', ' ', '  ', 'ؤ', ' ', ' ', ' ', ' ', 'وهي', 'او', 'و', 'بهذا', 'هذا',  'وايضا', 'ايضا', 'ومع', 'مع', 'ما', 'وما', 'والتي', 'اليها', 'الي','علي','على', 'كان', 'ان', 'في', 'التي', 'اذا','معظم','هي',  'متي','متى','الى','م','سم','لهذا','ال','حوالي', 'لأ', 'NOAN']
        stop_words = set(stopwords.words('arabic')) | set(custom_stopwords)
        tokens = word_tokenize(text)
        filtered_text = [word for word in tokens if word.lower() not in stop_words]
        return ' '.join(filtered_text)
        
    # Normalization
    def normalize_arabic_text(self, text):
        if pd.isna(text):
            return text 
        text = normalize_unicode(text)
        text = normalize_alef_maksura_ar(text)
        text = normalize_teh_marbuta_ar(text)
        text = normalize_alef_ar(text)
        text = dediac_ar(text)
        return text

    # Stemming
    st = ISRIStemmer()
    def stem_arabic_text(self, text):
        if pd.isna(text):
            return text
        words = word_tokenize(text)
        stemmed_words = [self.st.stem(word) for word in words]
        return ' '.join(stemmed_words)
    # Explicitly remove NOAN
    def remove_specific_word(self,text, word):
        return ' '.join([t for t in text.split() if t != word])

    # All text processors
    def text_proccessers(self, text):
        text = self.remove_non_arabic(text)
        text = self.tokenizer(text)
        text = self.msa_atb_tokenizer.tokenize(text)
        text = self.pattern.findall(' '.join(text))
        text = ' '.join(text)
        text = self.remove_stopwords_arabic(text)
        text = self.remove_arabic_numbers(text)
        text = self.remove_punctuation(text)
        text = self.normalize_arabic_text(text)
        text = self.stem_arabic_text(text)
        text = self.remove_specific_word(text, "NOAN")
        return text