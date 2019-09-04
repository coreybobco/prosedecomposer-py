Prose Decomposer
================


.. image:: https://coveralls.io/repos/github/coreybobco/prosedecomposer-py/badge.svg?branch=master
   :target: https://coveralls.io/github/coreybobco/prosedecomposer-py?branch=master

What is this?
^^^^^^^^^^^^^

There are many ways to write. In `Unoriginal Genius <http://writing.upenn.edu/~taransky/unoriginalgenius.pdf>`_, Marjorie Perloff contrasts the notion of 'original genius'--the mythic author of old who realizes works from the depths of their intellectual solitude--to a counter-tradition of 'unoriginal genius' including acts of plagiaristic parody (also known as détournement) and patchwriting. T.S. Eliot, James Joyce, and Thomas Pynchon are all exemplars of this style, having written their seminal works with encyclopedias, magazine, and newspaper clippings, or other literature open face, according to `Uncreative Writing <http://www.libgen.is/book/index.php?md5=3E70C36B115111E10E371C72864ADAB7>`_ by Kenneth Goldsmith.

Today there are countless ways to transform texts with software: Markov chains, cut-ups, substituting words for related words, swapping out verbs between books, GPT-2, BERT, etc. Today's cybernetic author can harness these as decomposing agents, destroying original texts to create messy new mélange that can be further edited, expanded upon, or synthesised into an original, meaningful work.

But what does this do?
^^^^^^^^^^^^^^^^^^^^^^
This project elaborates on these ideas, allowing the user to:

- sample random sentences and paragraphs from publicly available works of literature on **Project Gutenberg** and **Archive.org** or any text you give it.
- swap words that share the same part of speech between two texts--for instance, swapping all of one text's adjectives with another's and one text's nouns with another's, preserving the structure of a narrative or discursive formation while wildly changing the content. Take, for example, this passage from Charles Dickens' *Great Expectations*, which transforms into surrealist horror when you replace the nouns and adjectives with those from a paragraph in H.P. Lovecraft's story *The Shunned House*:

    "It was then I began to understand that chimney in the eye had stopped, like the enveloping and the head, a human fungus ago. I noticed that Miss Havisham put down the height exactly on the time from which she had taken it up. As Estella dealt the streams, I glanced at the corpse-abhorrent again, and saw that the outline upon it, once few, now diseased, had never been worn. I glanced down at the sight from which the outline was insectoid, and saw that the half stocking on it, once few, now diseased, had been trodden ragged. Without this cosmos of thing, this standing still of all the worse monstrous attentions, not even the withered phosphorescent mist on the collapsed dissolving could have looked so like horror-mockings, or the human hideousness so like a horror."
- run individual texts or list of texts through a Markov chain, semi-intelligently recombining the words in a more or less chaotic manner depending on n-gram size (which defaults to 1, the most chaotic).

     Markov chain based generative algorithms like this one can create prose whose repetitions and permutations lend it a strange rhythm and which appears syntactically and semantically valid at first but eventually turns into nonsense. The Markov chain's formulaic yet sassy and subversive sstyle is quite similar Gertrude Stein's in `The Making Of Americans <gutenberg.net.au/ebooks16/1600671h.html>`_, which she explains in details in the essay `Composition as Explanation <https://www.poetryfoundation.org/articles/69481/composition-as-explanation>`_.
- perform a virtual simulation of the `cut-up method <https://www.writing.upenn.edu/~afilreis/88v/burroughs-cutup.html>`_ pioneered by William S. Burroughs and Brion Gysin by breaking texts down into components of random length (where the minimum and and maximum length in words is preserved) and then randomly rearranging them.

Installation
^^^^^^^^^^^^

If you're on Windows, you have to use Docker.

OSX and Linux users must install hunspell first. Instructions for that can be found on my `generativepoetry <https://github.com/coreybobco/generativepoetry-py/>`_ module.

For Gutenberg sampling to work properly, you must populate the Berkeley db cache:

.. code-block::

   python3 populate_cache.py

If the Gutenberg cache messes up after it is populated, delete the cache directory and re-populate.

How to Use
^^^^^^^^^^

First, import the library:

.. code-block::

   from prosedecomposer import *

To extract and clean the text from Project Gutenberg or Archive.org:

.. code-block::

   # From an Archive.org URL:
   calvino_text = get_internet_archive_document('https://archive.org/stream/CalvinoItaloCosmicomics/Calvino-Italo-Cosmicomics_djvu.txt')
   # From a Project Gutenberg URL:
   alice_in_wonderland = get_gutenberg_document('https://www.gutenberg.org/ebooks/11')
   # Select a random document from Project Gutenberg
   random_gutenberg_text = random_gutenberg_document

The ParsedText class offers some functions for randomly sampling one or more sentences or paragraphs of a certain length:

.. code-block::

   parsed_calvino = ParsedText(calvino_text)
   parsed_calvino.random_sentence()   # Returns a random sentence
   parsed_calvino.random_sentence(minimum_tokens=25)  # Returns a random sentence of a guaranteed length in tokens
   parsed_calvino.random_sentences()  # Returns 5 random sentences
   parsed_calvino.random_sentences(num=7, minimum_tokens=25)  # Returns 7 random sentences of a guaranteed length
   parsed_calvino.random_paragraph()  # Returns a random paragraph (of at least 3 sentence by default)
   parsed_calvino.random_paragraph(minimum_sentences=5)  # Returns a paragraph with at least 5 sentences

To swap words with the same part(s) of speech between texts:

.. code-block::

   # Swap out adjectives and nouns between two random paragraphs of two random Gutenberg documents
   doc1 = ParsedText(random_gutenberg_document())
   doc2 = ParsedText(random_gutenberg_document())
   swap_parts_of_speech(doc1.random_paragraph(), doc2.random_paragraph())
   # Any of Spacy's part of speech tag values should work, though: https://spacy.io/api/annotation#pos-tagging
   swap_parts_of_speech(doc1.random_paragraph(), doc2.random_paragraph(), parts_of_speech=["VERB", "CONJ"])
   # Since NLG has not yet been implemented, expect syntax errors like subject-verb agreement.

To run text(s) through Markov chain text processing algorithms, see below. You may want a bigger n-gram size (2 or 3)
if you are processing a lot of text, i.e. one or several books/stories/etc at once.

.. code-block::

   output = markov(text)  # Just one text (defaults to n-gram size of 1 and 5 output sentences)
   output = markov(text, ngram_size=3, num_output_sentence=7)  # Bigger n-gram size, more output sentences
   output = markov([text1, text2, text3])  # List of text (defaults to n-gram size of 1 and 5 output sentences)
   output = markov([text1, text2, text3], ngram_size=3, num_output_sentences=7)  # Bigger n-gram size, more outputs

To virtually cut up and rearrange the text:

.. code-block::

   # Cuts up a text into cutouts between 3 and 7 words and rearrange them randomly (returns a list of cutout strings)
   cutouts = cutup(text)
   # Cuts up a text into cutouts between 2 an 10 words and rearrange them randomly (returns a list of cutout strings)
   cutouts = cutup(text, min_cutout_words=3, max_cutout_words=7)