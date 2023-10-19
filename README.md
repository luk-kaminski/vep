# About
Vector Embedding Playground is a tool that helps you play with Vector Embeddings (provided in a file).

# Prerequisites
Needed Python libraries: numpy, matplotlib, scikit-learn.
```
pip3 install numpy
pip3 install matplotlib
pip3 install scikit-learn
```

# Supported file formats
 - .vec format of GloVe : https://nlp.stanford.edu/projects/glove
 - .txt format of FastText : https://fasttext.cc/
 - Every other textual file format that by accident is the same as one of the two mentioned ones.

# Usage
1. Get a file with vector embeddings.
2. Start the program: `python3 vep.py [vector_embeddings_file]`
3. Type help to get the list of supported functions.
4. Play with it!

# Clues
The files with Vector Embeddings tend to be huge. Significant portion of words are rare or even strange. 
You can cut only the words from the top (the most popular ones) and work on a smaller file, faster.
The command for that is:
`python3 vector_file_cutter.py [file] [word_limit]`
i.e.:
`python3 vector_file_cutter.py glove.6B.300d.txt 30000`

# Warning
The project is still work in progress and has some problems here and there...

