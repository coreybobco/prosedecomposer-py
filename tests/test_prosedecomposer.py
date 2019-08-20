import unittest
from prosedecomposer import *
import spacy

spacy_nlp = spacy.load('en_core_web_sm')

class TextExtractionTestCase(unittest.TestCase):

    def test_validate_url(self):
        self.assertRaises(Exception, lambda: validate_url(2))
        self.assertRaises(Exception, lambda: validate_url(2.5))
        self.assertRaises(Exception, lambda: validate_url(None))
        self.assertRaises(Exception, lambda: validate_url(False))
        self.assertRaises(Exception, lambda: validate_url('test'))
        validate_url('http://test')
        validate_url('http://test.com')
        self.assertRaises(Exception, lambda: validate_url(
            'http://test.com', expected_netloc='gutenberg.org'))
        self.assertRaises(Exception, lambda: validate_url(
            'https://archive.org/stream/leschantsdemaldo00laut/leschantsdemaldo00laut_djvu.txt',
            expected_netloc='gutenberg.org'))
        validate_url('https://www.gutenberg.org/ebooks/11', expected_netloc='gutenberg.org')
        validate_url('https://www.gutenberg.org/files/11/11-h/11-h.htm', expected_netloc='gutenberg.org')
        validate_url(
            'https://www.gutenberg.org/files/11/11-pdf.pdf?session_id=07199a8410f9c36952586dd2a3e108a082fc54e7',
            expected_netloc='gutenberg.org'
        )
        self.assertRaises(Exception, lambda: validate_url('https://www.gutenberg.org/ebooks/11',
                                                          expected_netloc='archive.org'))
        validate_url('https://archive.org/stream/CalvinoItaloCosmicomics/Calvino-Italo-Cosmicomics_djvu.txt',
                     expected_netloc='archive.org')

    def test_get_internet_archive_document(self):
        self.assertRaises(Exception, lambda: get_internet_archive_document(2))
        self.assertRaises(Exception, lambda: get_internet_archive_document(2.5))
        self.assertRaises(Exception, lambda: get_internet_archive_document(None))
        self.assertRaises(Exception, lambda: get_internet_archive_document(False))
        self.assertRaises(Exception, lambda: get_internet_archive_document('test'))
        self.assertRaises(Exception, lambda: get_internet_archive_document('http://test'))
        self.assertRaises(Exception, lambda: get_internet_archive_document('http://test.com'))
        self.assertRaises(Exception, lambda: get_internet_archive_document(
            'https://www.gutenberg.org/ebooks/11'))
        cosmicomics = get_internet_archive_document(
            'https://archive.org/stream/CalvinoItaloCosmicomics/Calvino-Italo-Cosmicomics_djvu.txt')
        file = open('tests/Cosmicomics.txt', 'r')
        mock_cosmicomics = file.read()
        file.close()
        self.assertEqual(cosmicomics, mock_cosmicomics)

    def test_get_gutenberg_document(self):
        self.assertRaises(Exception, lambda: get_gutenberg_document(2))
        self.assertRaises(Exception, lambda: get_gutenberg_document(2.5))
        self.assertRaises(Exception, lambda: get_gutenberg_document(None))
        self.assertRaises(Exception, lambda: get_gutenberg_document(False))
        self.assertRaises(Exception, lambda: get_gutenberg_document('test'))
        self.assertRaises(Exception, lambda: get_gutenberg_document('http://test'))
        self.assertRaises(Exception, lambda: get_gutenberg_document('http://test.com'))
        self.assertRaises(Exception, lambda: get_gutenberg_document(
            'https://archive.org/stream/CalvinoItaloCosmicomics/Calvino-Italo-Cosmicomics_djvu.txt'))
        alice_in_wonderland = get_gutenberg_document('https://www.gutenberg.org/ebooks/11')
        file = open('tests/AliceinWonderland.txt', 'r')
        mock_aiw = file.read()
        file.close()
        self.assertEqual(alice_in_wonderland, mock_aiw)

    def test_random_gutenberg_document(self):
        for i in range(3):
            doc = random_gutenberg_document()
            self.assertEqual(type(doc), str)
            self.assertGreater(len(doc), 0)


class ParsedTextTestCase(unittest.TestCase):

    def test_create(self):
        file = open('tests/AliceinWonderland.txt', 'r')
        doc = ParsedText(file.read())
        file.close()
        self.assertEqual(len(doc.sentences), 970)
        self.assertEqual(len(doc.paragraphs), 801)
        file = open('tests/Cosmicomics.txt', 'r')
        doc = ParsedText(file.read())
        self.assertEqual(len(doc.sentences), 2146)
        self.assertEqual(len(doc.paragraphs), 776)

    def test_random_sentence(self):
        file = open('tests/Cosmicomics.txt', 'r')
        doc = ParsedText(file.read())
        file.close()
        random_sentence = doc.random_sentence()
        self.assertIn(random_sentence, doc.sentences)
        num_tokens = len([token.text for token in spacy_nlp(random_sentence)])
        self.assertGreaterEqual(num_tokens, 1)
        random_sentence = doc.random_sentence(minimum_tokens=40)
        self.assertIn(random_sentence, doc.sentences)
        num_tokens = len([token.text for token in spacy_nlp(random_sentence)])
        self.assertGreaterEqual(num_tokens, 1)

    def test_random_sentences(self):
        file = open('tests/Cosmicomics.txt', 'r')
        doc = ParsedText(file.read())
        file.close()
        random_sentences = doc.random_sentences()
        self.assertEqual(len(random_sentences), 5)
        for random_sentence in random_sentences:
            self.assertIn(random_sentence, doc.sentences)
            num_tokens = len([token.text for token in spacy_nlp(random_sentence)])
            self.assertGreaterEqual(num_tokens, 1)
        random_sentences = doc.random_sentences(num=3, minimum_tokens=35)
        self.assertEqual(len(random_sentences), 3)
        for random_sentence in random_sentences:
            self.assertIn(random_sentence, doc.sentences)
            num_tokens = len([token.text for token in spacy_nlp(random_sentence)])
            self.assertGreaterEqual(num_tokens, 35)

    def test_random_paragraph(self):
        file = open('tests/Cosmicomics.txt', 'r')
        doc = ParsedText(file.read())
        file.close()
        random_paragraph = doc.random_paragraph()
        num_sentences = len(sent_detector.tokenize(random_paragraph))
        self.assertGreaterEqual(num_sentences, 3)
        random_paragraph = doc.random_paragraph(minimum_sentences=6)
        num_sentences = len(sent_detector.tokenize(random_paragraph))
        self.assertGreaterEqual(num_sentences, 6)

if __name__ == '__main__':
    unittest.main()