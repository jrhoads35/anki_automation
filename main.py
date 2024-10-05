import pystardict
from bs4 import BeautifulSoup

def load_stardict(dictionary_name):
    try:
        stardict = pystardict.Dictionary(dictionary_name)
        return stardict
    except Exception as e:
        print(f"Error loading dictionary: {e}")
        return None

def extract_translations_and_examples(html):
    soup = BeautifulSoup(html, 'html.parser')
    translations = []
    examples = []

    # Find all <li> tags which contain translations
    for li in soup.find_all('li'):
        # Extract text from each <div> within the <li> tags
        translation_divs = li.find_all('div')
        for div in translation_divs:
            translation_text = div.get_text(strip=True)
            if translation_text and translation_text not in translations:
                translations.append(translation_text)
        
        # Also extract example sentences if available
        example_sentence = li.find_next('div', class_='example')
        if example_sentence:
            examples.append(example_sentence.get_text(strip=True))

    return translations, examples

def get_translations_and_examples(word, stardict):
    html_output = stardict.get(word)
    if html_output:
        return extract_translations_and_examples(html_output)
    else:
        return f"No translations found for '{word}'."

# Adjust the dictionary name based on your StarDict installation
dictionary_name = 'wikdict-de-en/stardict'  # Should be the name without file extensions

# Load the StarDict dictionary
stardict = load_stardict(dictionary_name)

# Example usage
word = "laufen"  # German word
if stardict:
    translations, examples = get_translations_and_examples(word, stardict)
    if isinstance(translations, list):
        print(f"Possible translations for '{word}': {translations}")
        if examples:
            print(f"Example sentences for '{word}':")
            for example in examples:
                print(f"- {example}")
    else:
        print(translations)
