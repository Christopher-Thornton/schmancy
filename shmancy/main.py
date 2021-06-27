import re

def tokenize(text):
    tokenize_re = re.compile(r'(?:\-{2,}|\.{2,}|(?:\.\s){2,}\.)|'
                             r'(?=[^\(\"\`{\[:;&\#\*@\)}\]\-,])\S+?'
                             r'(?=\s|$|(?:[)";}\]\*:@\({\[\?!])|'
                             r'(?:\-{2,}|\.{2,}|(?:\.\s){2,}\.)|,|\.'
                             r'(?=$|\s|(?:[)";}\]\*:@\'\({\[\?!])|'
                             r'(?:\-{2,}|\.{2,}|(?:\.\s){2,}\.)))|\S')

    return tokenize_re.findall(text)


punctuation = {':', '^', '=', '-', '&', '#', '.', '@',
               '/', "'", '$', ']', ')', '<', '*', '`',
               '[', '!', '>', ',', '"', '{', '|', '~',
               '_', ';', '+', '}', '%', '?', '\\', '('}

stop = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
    'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
    'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
    'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
    'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
    'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't",
    'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
    "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}


def syllables(word):
    # single syllable word
    if len(re.findall('[aeiouy]', word)) <= 1:
        return [word]

    # sonority hierarchy: vowels, nasals, fricatives, stops
    hierarchy = {
        'a': 4, 'e': 4, 'i': 4, 'o': 4, 'u': 4, 'y': 4,
        'l': 3, 'm': 3, 'n': 3, 'r': 3, 'w': 3,
        'f': 2, 's': 2, 'v': 2, 'z': 2,
        'b': 1, 'c': 1, 'd': 1, 'g': 1, 'h': 1, 'j': 1, 'k': 1, 'p': 1, 'q': 1, 't': 1, 'x': 1,
    }
    syllables_values = [(c, hierarchy[c]) for c in word]

    syllables = []
    syll = syllables_values[0][0]
    for trigram in zip(*[syllables_values[i:] for i in range(3)]):
        (phonemes, values) = zip(*trigram)
        (previous, val, following) = values
        phoneme = phonemes[1]

        if previous > val < following:
            syllables.append(syll)
            syll = phoneme
        elif previous >= val == following:
            syll += phoneme
            syllables.append(syll)
            syll = ''
        else:
            syll += phoneme
    syll += syllables_values[-1][0]
    syllables.append(syll)

    final_syllables = []
    front = ''
    for (i, syllable) in enumerate(syllables):
        if not re.search('[aeiouy]', syllable):
            if len(final_syllables) == 0:
                front += syllable
            else:
                final_syllables = final_syllables[:-1] \
                                  + [final_syllables[-1] + syllable]
        else:
            if len(final_syllables) == 0:
                final_syllables.append(front + syllable)
            else:
                final_syllables.append(syllable)
    return final_syllables


def get_reduplicant(word, start):
    if (len(word) < 4 and word.lower() in stop) or not word.isalnum() or word.lower().startswith(start):
        return word
    if 'y' in word:
        y = word.find('y')
        # Y is considered to be a vowel if The word has no other vowel
        if len(re.findall("[aeiou]", word, re.IGNORECASE)) == 0 and word.count('y') == 1:
            word = word[:y] + '#' + word[y + 1:]
        # or if the letter is at the end of a word
        if word[-1] == 'y':
            word = word[:-1] + '#'
        # or middle/end of syllable
        if word.find('y') != -1:
            syll = syllables(word)
            for i, s in enumerate(syll):
                snew = s[:-1] + '#' if s[-1] == 'y' else s
                y = snew.find('y')
                if len(snew) // 2 == y:
                    snew = snew[:y] + '#' + snew[y + 1:]
                syll[i] = snew
            word = ''.join(syll)

    if word.isupper():
        prefix = start.upper()
    elif word.istitle():
        word = word.lower()
        prefix = start.title()
    else:
        prefix = start.lower()
    vowels = re.search("[aeiou#]", word, re.IGNORECASE)
    if not vowels:
        return word
    position = vowels.start()
    new = prefix + word[position:].replace('#', 'y')
    return new


def reduplicate(text, start='shm', repeat=False):
    text = tokenize(text)
    dup = ([get_reduplicant(word, start) for word in text])
    # join strings
    if repeat:
        text = "".join([i if i in punctuation
                        else " " + i if i == j
        else " " + i + "-" + j
                        for i, j in zip(text, dup)]).strip()
    else:
        text = "".join([" " + i if i not in punctuation else i for i in dup]).strip()
    return text


if __name__ == '__main__':
    # reduplication on a word
    print(reduplicate('fancy', repeat=True))
    # reduplication on an entire sentence
    text = "The quick brown fox jumps over the lazy dog."
    print(reduplicate(text))
    print(reduplicate(text, repeat=True))
    print(reduplicate(text, start='w'))
