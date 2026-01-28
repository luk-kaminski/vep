# About
Vector Embedding Playground is a tool that helps you play with Vector Embeddings (provided in a file).

# Installation
Install the package and all its dependencies:
```bash
pip install .
```

Or in editable mode for development:
```bash
pip install -e .
```

# Supported file formats
 - .vec format of GloVe : https://nlp.stanford.edu/projects/glove
 - .txt format of FastText : https://fasttext.cc/
 - Every other textual file format that by accident is the same as one of the two mentioned ones.

# Usage
1. Get a file with vector embeddings.
2. Start the program: `vep [vector_embeddings_file]`
3. Type help to get the list of supported functions.
4. Play with it!

You can also run it as a Python module:
```bash
python -m vep [vector_embeddings_file]
```

# Examples of what you can achieve

![similarity_distribution](https://github.com/luk-kaminski/vep/assets/100699120/abd93365-91d8-413a-b881-a34d95f17f58)

![embeddings_clustering_visualisation](https://github.com/luk-kaminski/vep/assets/100699120/c4ae28b2-ce0d-4945-b370-b1983bbc611e)


# Cutting Large Files
The files with Vector Embeddings tend to be huge. Significant portion of words are rare or even strange.
You can cut only the words from the top (the most popular ones) and work on a smaller file, faster.
The command for that is:

```bash
vep-cut [file] [word_limit]
```

Example:
```bash
vep-cut glove.6B.300d.txt 30000
```

# Warning
The project is still work in progress and has some problems here and there...

