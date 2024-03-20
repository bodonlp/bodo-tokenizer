from . import normalizer
import re

DARI_MARKER = u'\u0964'

def tokenize(sentence):
    ns = normalizer.normalize(sentence)

    # Define punctuation excluding the period
    string_punctuation = '!"#$%&\()*+,-/:;<=>?@[\\]^_`{|}~'
    # Define period separately for decimal handling
    decimal_separator = '.'

    # Combine punctuation and DARI_MARKER for regex
    punctuation_pattern = re.escape(string_punctuation + DARI_MARKER)

    punc_regex = re.compile(f'([{punctuation_pattern}])')

    sent = punc_regex.sub(r' \1 ', ns)
    # remove extra space after sentence end
    sent = sent.strip()
    # remove more than one space to single space
    # this problem occurs when two punctuation tokens are one after another
    extra_space_pattern = r"(\s{2,})"
    extra_space_regex = re.compile(extra_space_pattern)
    sent = extra_space_regex.sub(" ", sent)

    # single comma pattern
    # https://unicode.org/charts/PDF/U0900.pdf
    single_quote_pattern = r"('\s?)([\u0900-\u097F]+)(\s?')"
    single_quote_regex = re.compile(single_quote_pattern)
    sent = single_quote_regex.sub(r'\1 \2 \3', sent)

    # double comma pattern
    double_quote_pattern = r'("\s?)([\u0900-\u097F]+)(\s?")'
    double_quote_regex = re.compile(double_quote_pattern)
    sent = double_quote_regex.sub(r'\1 \2 \3', sent)
    
    # numbers
    # e.g. 123आरो
    number_pattern_f = r"(\d+)([\u0900-\u097F]+)"
    number_regex = re.compile(number_pattern_f)
    sent = number_regex.sub(r'\1 \2', sent)
    # e.g. आरो123
    number_pattern_b = r"([\u0900-\u097F]+)(\d+)"
    number_regex = re.compile(number_pattern_b)
    sent = number_regex.sub(r'\1 \2', sent)
    
    
    # for separating bodo word and fullstop symbol
    word_period_pattern = r"([\u0900-\u097F]+)(\.)([\u0900-\u097F]+)"
    word_period_regex = re.compile(word_period_pattern)
    sent = word_period_regex.sub(r'\1 \2 \3', sent)
    
    word_period_pattern = r"([\u0900-\u097F]+)(\.)"
    word_period_regex = re.compile(word_period_pattern)
    sent = word_period_regex.sub(r'\1 \2', sent)
    
    word_period_pattern = r"(\.)([\u0900-\u097F]+)"
    word_period_regex = re.compile(word_period_pattern)
    sent = word_period_regex.sub(r'\1 \2', sent)


    # numbers with decimal part
    # Modified to handle numbers with optional decimal part
    # e.g. 33.3
    number_pattern = r"(\d+(\.\d*)?|\.\d+)"
    number_regex = re.compile(number_pattern)

    def handle_decimal(match):
        # Replace the period in the decimal part with . character
        return match.group(0).replace(decimal_separator, '.')

    sent = number_regex.sub(handle_decimal, sent)

    return sent

def tokenize_file(input, output):
    with open(input, 'r', encoding='utf-8') as rf:
        with open(output, 'w', encoding='utf-8') as wf:
            sentences = rf.readlines()
            output_sentences = []
            for sentence in sentences:
                tokenized_sentence = tokenize(sentence)
                output_sentences.append(tokenized_sentence+'\n')
            wf.writelines(output_sentences)
    return None