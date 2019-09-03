import random, re
from collections import defaultdict
from gutenberg.acquire import load_etext
from gutenberg.query import get_metadata
from gutenberg.cleanup import strip_headers
from gutenberg_cleaner import super_cleaner
from internetarchive import download
import nltk
import spacy
from urllib.parse import urlsplit


sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
spacy_nlp = spacy.load('en_core_web_sm')
spacy_nlp.remove_pipe("parser")


class ParsedText:

    def __init__(self, text):
        self.raw_text = text
        self.sentences = sent_detector.tokenize(text)
        self.paragraphs = self.raw_text.split("\n\n")

    def random_sentence(self, minimum_tokens=1) -> str:
        num_tokens = 0
        while num_tokens < minimum_tokens:
            sentence = random.choice(self.sentences)
            num_tokens = len([token.text for token in spacy_nlp(sentence)])
        return sentence

    def random_sentences(self, num=5, minimum_tokens=1) -> list:
        random_sentences = []
        while len(random_sentences) < num:
            random_sentence = self.random_sentence(minimum_tokens=minimum_tokens)
            if random_sentence not in random_sentences:
                random_sentences.append(random_sentence)
        return random_sentences

    def random_paragraph(self, minimum_sentences=3) -> str:
        num_sentences = 0
        while num_sentences < minimum_sentences:
            paragraph = random.choice(self.paragraphs)
            num_sentences = len(sent_detector.tokenize(paragraph))
        return paragraph


def validate_url(url, expected_netloc=''):
    url_parts = urlsplit(url)
    if not url_parts.netloc or (expected_netloc and expected_netloc not in url_parts.netloc):
        raise Exception(f'Not a valid f{expected_netloc} document url')


def get_internet_archive_document(url) -> str:
    """Downloads a document (book, etc.) from Internet Archive and returns it as a string. The linked document must
       have a text version. PDF text extraction is not supported at this time"""

    validate_url(url, expected_netloc='archive.org')
    url_parts = urlsplit(url).path.split("/")
    if len(url_parts) > 2:
        document_id = url_parts[2]
    else:
        raise Exception(f'Not a valid url')
    try:
        response = download(document_id, glob_pattern="*txt", return_responses=True)[0]
        # Remove single newlines, preserve double  newlines (because they demarcate paragraphs
        text = re.sub('(?<![\r\n])(\r?\n|\n?\r)(?![\r\n])', ' ', response.text.strip())
        # This usually creates double spaces between lines because most lines end with single spaces, but to account
        # for cases in which lines end without spaces, we will handle this in two lines
        return re.sub('(?<=[\S])(\s\s)(?=[\S])', ' ', text)

    except Exception:
        raise Exception(f'Archive.org download failed for url: {url}')


def get_gutenberg_document(url) -> str:
    """Downloads a document (book, etc.) from Project Gutenberg and returns it as a string."""
    # Get Project Gutenberg document ID from url string
    validate_url(url, expected_netloc='gutenberg.org')
    match = re.search("(?:files|ebooks|epub)\/(\d+)", urlsplit(url).path)
    if not match:
        raise Exception('Not a valid url')
    document_id = int(match.group(1))
    return super_cleaner(strip_headers(load_etext(document_id).strip()), mark_deletions=False)


def random_gutenberg_document(language_filter='en') -> str:
    doc_language = None
    document = ''
    while (not doc_language or language_filter) and doc_language != language_filter and len(document) == 0:
        # Keep grabbing random documents until 1 meets the language filter, if specified, and verify it really has text
        document_id = random.randint(1, 60134)  # Pick book at random (max id is currently 60134)
        lang_metadata = get_metadata('language', document_id)
        doc_language = next(iter(lang_metadata)) if len(lang_metadata) else False
        document = super_cleaner(strip_headers(load_etext(document_id).strip()), mark_deletions=False)
    return document


def swap_parts_of_speech(text1, text2, parts_of_speech=['ADJ', 'NOUN']) -> (str, str):
    doc1 = spacy_nlp(text1)
    doc2 = spacy_nlp(text2)
    # First build two dictionaries (one for each text) whose keys are parts of speech and values are lists of words
    doc1_words_keyed_by_pos, doc2_words_keyed_by_pos = defaultdict(lambda: []), defaultdict(lambda: [])
    for token in doc1:
        if token.pos_ in parts_of_speech and not token.text in doc1_words_keyed_by_pos[token.pos_]:
            doc1_words_keyed_by_pos[token.pos_].append(token.text)
    random.shuffle(doc1_words_keyed_by_pos[token.pos_])  # For variety's sake
    # Also build two dictionaries to store the word swaps we will do at the end. (Token text is immutable in spaCy.)
    # We can simultaneously build the second text's word-by-part-of-speech dict and its word swap dict
    text1_word_swaps, text2_word_swaps = {}, {}
    for token in doc2:
        if token.pos_ in parts_of_speech:
            if token.text not in doc2_words_keyed_by_pos[token.pos_]:
                doc2_words_keyed_by_pos[token.pos_].append(token.text)
            try:
                #  Use regex to preserve the whitespace of the word-to-be-replaced
                text2_word_swaps[token.text_with_ws] = \
                    re.sub('(?<!\S)\S+(?!\S)', doc1_words_keyed_by_pos[token.pos_].pop(), token.text_with_ws)
            except IndexError:  # There are no more words to substitute; the other text had more words of this p.o.s.
                pass
    random.shuffle(doc2_words_keyed_by_pos[token.pos_])
    for token in doc1:
        if token.pos_ in parts_of_speech:
            try:
                text1_word_swaps[token.text_with_ws] = \
                    re.sub('(?<!\S)\S+(?!\S)', doc2_words_keyed_by_pos[token.pos_].pop(), token.text_with_ws)
            except IndexError:  # There are no more words to substitute; the other text had more words of this p.o.s.
                pass
    # Recompose the text from its whitespace-aware tokens, substituting words if needed.
    text1 = ''.join([text1_word_swaps.get(token.text_with_ws, token.text_with_ws) for token in doc1])
    text2 = ''.join([text2_word_swaps.get(token.text_with_ws, token.text_with_ws) for token in doc2])
    return text1, text2
