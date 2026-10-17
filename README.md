# The Holy Bible NABRE JSON Dataset

The [New American Bible, Revised Edition (NABRE)](https://www.biblegateway.com/versions/New-American-Bible-Revised-Edition-NABRE-Bible/) as JSON: 73 books, organized by chapter and verse, plus the Python script used to generate it.
 
The script scrapes [biblegateway.com](https://www.biblegateway.com/versions/New-American-Bible-Revised-Edition-NABRE-Bible/#booklist) one chapter at a time.

The dataset can be found in the `generated_data` directory - 
* The `nabre.json` which is the entire dataset containing all the verses in the New American Bible Revised Edition of The Holy Bible. The dataset format is as follows -
```
[
  {
    "book": "Genesis",
    "chapters": [
      {
        "chapter": 1,
        "verses": [
          {
            "verse": 1,
            "text": "Preamble. The Creation of the World Chapter 1 - The Story of Creation. In the beginning, when God created the heavens and the earth—"
          },
          {
            "verse": 2,
            "text": "and the earth was without form or shape, with darkness over the abyss and a mighty wind sweeping over the waters—"
          },
        ...
        ]
      }
      ...
    ]
  }
  ...
]
```
* Each JSON file under `books/` contains all the verses for each book in the New American Bible Revised Edition of The Holy Bible. Each JSON file format is as follows -
```
{
  "book": "Genesis",
  "chapters": [
    {
      "chapter": 1,
      "verses": [
        {
          "verse": 1,
          "text": "Preamble. The Creation of the World Chapter 1 - The Story of Creation. In the beginning, when God created the heavens and the earth—"
        },
        {
          "verse": 2,
          "text": "and the earth was without form or shape, with darkness over the abyss and a mighty wind sweeping over the waters—"
        },
        ...
      ]
    }
    ...
  ]
}
```

The directory `data/` contains -
* `bible-all-books.json` - contains a JSON array of Books in the New American Bible Revised Edition of The Holy Bible.
* `bible-nabre-book-chapters.json` - contains the number of chapters for each book in the New American Bible Revised Edition of The Holy Bible. The format is as follows -
```
[
  {
    "Book": "Genesis",
    "Chapters": 50
  },
  {
    "Book": "Exodus",
    "Chapters": 40
  },
  ...
]
```

## Generating the data yourself
 
Requires Python 3.9+.
 
```bash
pip install -r requirements.txt
 
# run from the repository root
python generate_nabre.py
```
