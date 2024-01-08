import requests
import os
import sys
from bs4 import BeautifulSoup

# Set list of allowed languages
lang_list = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese',
             'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']

def scratch(req, target_lang):
    soup = BeautifulSoup(req.content, 'html.parser')

    # Get translated words
    words = soup.find_all('span', {'class': 'display-term'})
    word_list = []
    for tag in words:
        word_list.append(tag.text)

    # Get source example sentences
    div_src_ltr = soup.find_all('div', {'class': 'src'})
    src_sentence_list = []
    for div in div_src_ltr:
        span = div.find('span')
        if span is not None:
            src_sentence_list.append(span.text.strip())

    # Get target example sentences
    div_trg_ltr = soup.find_all('div', {'class': 'trg'})
    trg_sentence_list = []
    for div in div_trg_ltr:
        span = div.find('span', {'class': 'text'})
        if span is not None:
            trg_sentence_list.append(span.text.strip())

    # Add leading empty line unless it's empty
    if os.stat(output_file_name).st_size != 0:
        output_file.write('\n')

    # Print section title and only the first word
    print(f'{target_lang.capitalize()} Translations:')
    print(word_list[0])
    print()
    # Save the same info to file
    output_file.write(f'{target_lang.capitalize()} Translations:' + '\n')
    output_file.write(word_list[0] + '\n')
    output_file.write('\n')

    # Print section title and only the first pair of sentences
    print(f'{target_lang.capitalize()} Example:')
    print(src_sentence_list[0])
    print(trg_sentence_list[0])
    print()
    # Save the same info to file
    output_file.write(f'{target_lang.capitalize()} Example:' + '\n')
    output_file.write(src_sentence_list[0] + '\n')
    output_file.write(trg_sentence_list[0] + '\n')
    output_file.write('\n')


def translate_once(source_language, target_language, word):
    lang_combination = source_language + "-" + target_language
    url = f'https://context.reverso.net/translation/{lang_combination}/{word}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)

    while True:
        if r.status_code == 200:
            scratch(r, target_language)
            break
        elif r.status_code // 100 == 4:
            print(f'Sorry, unable to find {word}')
            sys.exit()
        elif r.status_code // 100 == 5:
            print('Something wrong with your internet connection')
            sys.exit()
        else:
            r = requests.get(url)


def translate_all(source_language, word):
    for target_lang in lang_list:
        if target_lang != source_language and target_lang != 'all':
            lang_combination = source_language + "-" + target_lang
            url = f'https://context.reverso.net/translation/{lang_combination}/{word}'
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)

            while True:
                if r.status_code == 200:
                    scratch(r, target_lang)
                    break
                elif r.status_code // 100 == 4:
                    print(f'Sorry, unable to find {word}')
                    sys.exit()
                elif r.status_code // 100 == 5:
                    print('Something wrong with your internet connection')
                    sys.exit()
                else:
                    r = requests.get(url)


# Implement command line inputI
args = sys.argv
source_language = args[1]
target_language = args[2]
word = args[3]

lang_list_all = lang_list
lang_list_all.append('all')

# Check for valid languages
invalid_source = source_language not in lang_list_all

if invalid_source:
    print(f"Sorry, the program doesn't support {source_language}")
    sys.exit()

if target_language not in lang_list_all:
    print(f"Sorry, the program doesn't support {target_language}")
    sys.exit()

# Create file
output_file_name = word + '.txt'
output_file = open(output_file_name, 'a', encoding='utf-8')

# Check and execute
if target_language != "all":
    translate_once(source_language, target_language, word)
else:
    translate_all(source_language, word)

# Close output file
output_file.close()
