import unittest
from prosedecomposer import *
import inflect
import spacy

spacy_nlp = spacy.load('en_core_web_sm', disable=['ner'])
spacy_nlp.remove_pipe("parser")


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


class TextProcessingTestCase(unittest.TestCase):

    def test_reconcile_replacement_word(self):
        # No changes expected to the replacement word in these two cases
        self.assertEqual(reconcile_replacement_word('cat', 'NN', 'dog', 'NN'), 'dog')
        self.assertEqual(reconcile_replacement_word('cats', 'NNS', 'dogs', 'NNS'), 'dogs')
        # Just whitespace changes when both the original word and the replacement are singular or both are plural
        self.assertEqual(reconcile_replacement_word(' shark', 'NN', 'crow', 'NN'), ' crow')
        self.assertEqual(reconcile_replacement_word('street ', 'NN', 'shark', 'NN'), 'shark ')
        self.assertEqual(reconcile_replacement_word(' bicycle ', 'NN', 'lemur', 'NN'), ' lemur ')
        self.assertEqual(reconcile_replacement_word(' sharks', 'NNS', 'crows', 'NNS'), ' crows')
        self.assertEqual(reconcile_replacement_word('streets ', 'NNS', 'sharks', 'NNS'), 'sharks ')
        self.assertEqual(reconcile_replacement_word(' bicycles ', 'NNS', 'lemurs', 'NNS'), ' lemurs ')
        # Pluralize the replacement noun in these cases
        self.assertEqual(reconcile_replacement_word('cats', 'NNS', 'dog', 'NN'), 'dogs')
        self.assertEqual(reconcile_replacement_word(' sharks', 'NNS', 'crow', 'NN'), ' crows')
        self.assertEqual(reconcile_replacement_word('streets ', 'NNS', 'shark', 'NN'), 'sharks ')
        self.assertEqual(reconcile_replacement_word(' bicycles ', 'NNS', 'lemur', 'NN'), ' lemurs ')
        # Singularize the replacement word in these cases
        self.assertEqual(reconcile_replacement_word('cat', 'NN', 'dogs', 'NNS'), 'dog')
        self.assertEqual(reconcile_replacement_word(' shark', 'NN', 'crows', 'NNS'), ' crow')
        self.assertEqual(reconcile_replacement_word('street ', 'NN', 'sharks', 'NNS'), 'shark ')
        self.assertEqual(reconcile_replacement_word(' bicycle ', 'NN', 'lemurs', 'NNS'), ' lemur ')

    def test_swap_parts_of_speech(self):
        great_expectations_sample = ''.join([
            "It was then I began to understand that everything in the room had stopped, like the watch and the ",
            "clock, a long time ago. I noticed that Miss Havisham put down the jewel exactly on the spot from which ",
            "she had taken it up. As Estella dealt the cards, I glanced at the dressing-table again, and saw that the",
            " shoe upon it, once white, now yellow, had never been worn. I glanced down at the foot from which the ",
            "shoe was absent, and saw that the silk stocking on it, once white, now yellow, had been trodden ragged. ",
            "Without this arrest of everything, this standing still of all the pale decayed objects, not even the ",
            "withered bridal dress on the collapsed form could have looked so like grave-clothes, or the long veil ",
            "so like a shroud."
        ])  # a novel by Charles Dickens
        great_expectations_nouns = ['everything', 'room', 'watch', 'clock', 'time', 'jewel', 'spot', 'cards',
                                    'dressing', 'table', 'shoe', 'foot', 'silk', 'arrest', 'objects', 'dress', 'form',
                                    'grave', 'clothes', 'veil', 'shroud']
        great_expectations_adjectives = ['long', 'white', 'yellow', 'absent', 'pale', 'decayed', 'bridal']
        spacy_nlp = spacy.load('en_core_web_sm', disable=['ner'])
        spacy_nlp.remove_pipe("parser")
        tokenized_ge_sample = spacy_nlp(great_expectations_sample)
        great_expectations_pos_by_word_number = {}
        for i,token in enumerate(tokenized_ge_sample):
            if token.pos_ in ['ADJ', 'NOUN']:
                great_expectations_pos_by_word_number[i] = token.pos_
        shunned_house_sample = ''.join([
            "Yet after all, the sight was worse than I had dreaded. There are horrors beyond horrors, and this was one",
            " of those nuclei of all dreamable hideousness which the cosmos saves to blast an accursed and unhappy ",
            "few. Out of the fungus-ridden earth steamed up a vaporous corpse-light, yellow and diseased, which ",
            "bubbled and lapped to a gigantic height in vague outlines half human and half monstrous, through which I ",
            "could see the chimney and fireplace beyond. It was all eyes—wolfish and mocking—and the rugose insectoid ",
            "head dissolved at the top to a thin stream of mist which curled putridly about and finally vanished up ",
            "the chimney. I say that I saw this thing, but it is only in conscious retrospection that I ever ",
            "definitely traced its damnable approach to form. At the time, it was to me only a seething, dimly ",
            "phosphorescent cloud of fungous loathsomeness, enveloping and dissolving to an abhorrent plasticity the ",
            "one object on which all my attention was focused."
        ])  # a story by H.P. Lovecraft
        tokenized_shunned_house_sample = spacy_nlp(great_expectations_sample)
        shunned_house_pos_by_word_number = {}
        for i, token in enumerate(tokenized_shunned_house_sample):
            if token.pos_ in ['ADJ', 'NOUN']:
                shunned_house_pos_by_word_number[i] = token.pos_
        shunned_house_nouns = ['sight', 'horrors', 'nuclei', 'hideousness', 'cosmos', 'fungus', 'earth', 'corpse',
                               'height', 'outlines', 'half', 'chimney', 'fireplace', 'eyes', 'wolfish', 'mocking',
                               'head', 'top', 'stream', 'mist', 'thing', 'retrospection', 'approach', 'time',
                               'cloud', 'loathsomeness', 'enveloping', 'dissolving', 'abhorrent', 'plasticity',
                               'object', 'attention']
        shunned_house_adjectives = ['worse', 'dreamable', 'accursed', 'unhappy', 'few', 'vaporous', 'light', 'yellow',
                                    'diseased', 'gigantic', 'vague', 'human', 'monstrous', 'rugose', 'insectoid',
                                    'thin', 'conscious', 'damnable', 'seething', 'phosphorescent', 'fungous']
        shunned_house_pos_by_word_number = {}
        # Just test swapping nouns and adjectives for now
        new_ge_sample, new_sh_sample = swap_parts_of_speech(great_expectations_sample, shunned_house_sample)
        print("\n\n".join([new_ge_sample, new_sh_sample]))
        new_ge_doc, new_sh_doc = spacy_nlp(new_ge_sample), spacy_nlp(new_ge_sample)
        # Since the Dickens sample has fewer nouns and adjectives, all the Dickens nounsa and adjectives
        # should be replaced by Lovecraft's words
        inflector = inflect.engine()
        for i, token in enumerate(new_ge_doc):
            expected_pos = great_expectations_pos_by_word_number.get(i, None)
            if expected_pos is 'NOUN':
                self.assertTrue(token.text in shunned_house_nouns or inflector.plural(token.text) in
                                shunned_house_nouns or inflector.singular_noun(token.text) in shunned_house_nouns)
            elif token.pos is 'ADJ':
                self.assertTrue(token.text in shunned_house_adjectives)
        for i, token in enumerate(new_sh_doc):
            expected_pos = shunned_house_pos_by_word_number.get(i, None)
            if expected_pos is 'ADJ':
                # Since there are only 7 adjectives in the Dickens passage only that many substitutions can occur.
                self.assertTrue(token.text in great_expectations_adjectives or i > 6)
            elif token.pos is 'NOUN':
                # Since there are only 21 nouns in the Dickens passage only that many substitutions can occur.
                # Note: inflector.plural returns the singularized noun if the noun is already plural
                self.assertTrue((token.text in great_expectations_nouns or inflector.plural(token.text)
                                 in great_expectations_nouns or inflector.singular_noun(token.text)
                                 in great_expectations_nouns) or i > 20)

    def test_markov(self):
        # This does NOT test the markovify library itself, as that's out of scope and we can assume it does what it says
        self.assertRaises(Exception, lambda: markov(2))
        self.assertRaises(Exception, lambda: markov(2.5))
        self.assertRaises(Exception, lambda: markov(None))
        self.assertRaises(Exception, lambda: markov(False))
        file = open('tests/Cosmicomics.txt', 'r')
        cosmicomics = file.read()
        file.close()
        output = markov(cosmicomics)
        # Sentence tokenization for Markov chains is kinda screwed up because they're nonsense
        # self.assertEqual(len(sent_detector.tokenize(output)), 5)
        output = markov(cosmicomics, num_output_sentences=3)
        # self.assertEqual(len(sent_detector.tokenize(output)), 3)
        file = open('tests/AliceinWonderland.txt', 'r')
        alice_in_wonderland = file.read()
        output = markov([alice_in_wonderland, cosmicomics])
        # self.assertEqual(len(sent_detector.tokenize(output)), 5)
        output = markov([alice_in_wonderland, cosmicomics], num_output_sentences=3)
        # self.assertEqual(len(sent_detector.tokenize(output)), 3)


if __name__ == '__main__':
    unittest.main()
