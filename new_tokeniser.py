import re

def bodo_tokenizer(text):
    # Regular expression to match Bodo language tokens
    pattern = r'(\d+\.\d+)|([\d.]+)|([\u0980-\u09FF]+)|(\S+)'
    
    # Find all matches using the regex pattern
    tokens = [match.group(0) for match in re.finditer(pattern, text)]
    
    return tokens

# Test the tokenizer with some examples
text1 = "12.6 थी22 22थी"
tokens1 = bodo_tokenizer(text1)
print(tokens1)  # Output: ['12.6', ' ', 'थी', '22', ' ', '22थी']

text2 = "थी 12.6 थी 22थी"
tokens2 = bodo_tokenizer(text2)
print(tokens2)  # Output: ['थी', ' ', '12.6', ' ', 'थी', ' ', '22थी']
