Prose Decomposer
================


.. image:: https://coveralls.io/repos/github/coreybobco/prosedecomposer-py/badge.svg?branch=master
   :target: https://coveralls.io/github/coreybobco/prosedecomposer-py?branch=master

What is this?
^^^^^^^^^^^^^

There are many ways to write. In `Unoriginal Genius <http://writing.upenn.edu/~taransky/unoriginalgenius.pdf>`_, Marjorie Perloff contrasts the notion of 'original genius'--the mythic author of old who realizes works from the depths of their intellectual solitude--to a counter-tradition of 'unoriginal genius' including acts of plagiaristic parody (also known as détournement) and patchwriting. T.S. Eliot, James Joyce, Thomas Pynchon are all exemplars of this style, having written their seminal works with encyclopedias, magazine, and newspaper clippings, or other literature open face, according to `Uncreative Writing <http://www.libgen.is/book/index.php?md5=3E70C36B115111E10E371C72864ADAB7>`_ by Kenneth Goldsmith.

Today there are countless ways to transform texts with software: Markov chains, cut-ups, substituting words for related words, swapping out verbs between books, GPT-2, BERT, etc. Today's cybernetic/satirical author can harness these as decomposing agents, destroying original texts to create messy new mélange that can be further edited, expanded upon, or synthesised into an original, meaningful work.

This project elaborates on these ideas, allowing the user to sample random sentences and paragraphs from publicly available works of literature on Project Gutenberg and Archive.org or any text you give it.

I've only implemented that basic sampling right now. Expect more very soon.

Installation
^^^^^^^^^^^^

If you're on Windows, you have to use Docker. OSX and Linux users must install hunspell first. Instructions for that can be found on my `generativepoetry <https://github.com/coreybobco/generativepoetry-py/>`_ module.

For Gutenberg sampling to work properly, you must populate the Berkeley db cache:

.. code-block::
   python3 populate_cache.py

If the Gutenberg cache messes up after it is populated, delete the cache directory and re-populate.

Usage
~~~~~~~~

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

   #  Swap out adjectives and nouns between two random paragraphs of two random Gutenberg documents
   doc1 = ParsedText(random_gutenberg_document())
   doc2 = ParsedText(random_gutenberg_document())
   swap_parts_of_speech(doc1.random_paragraph(), doc2.random_paragraph())

