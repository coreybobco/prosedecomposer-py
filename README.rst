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

If you're on Windows, you have to use Docker. OSX and Linux users must install hunspell first. Instructions for that can be found on my generativepoetry module.

Sorry for the lackluster instructions. I'm waiting to update this section until after I add Markov chains and some other stuff and publish to PyPi.

Features
~~~~~~~~

Swap words with the same part of speech between texts: nouns and adjectives, for example

.. code-block::
doc1 = ParsedText(random_gutenberg_document())
doc2 = ParsedText(random_gutenberg_document())
swap_parts_of_speech(doc1.random_paragraph(), doc2.random_paragraph())