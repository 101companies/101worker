# simpleSentiment

Sentiment of comments per File

# Description

This module uses TextBlob to analyse the sentiment of comments per File. Textblob is python library for language processing. A Textblob can be created by using any String. The sentiment property returns a tuple of the form (polarity, subjectivity), where polarity is a float within the range [-1.0, 1.0] and subjectivity within the range [0, 1.0] (0 means very objective and 1.0 very subjective).
A resource file named sentiment.json is saved containing the polarity and subjectivity of the comments (output-example: [0.3, 0.5] ).

# Requirements

This module requires a working installation of TextBlob and extractComments to be run first.

# How to install TextBlob

$ pip install -U textblob
$ python -m textblob.download_corpora