# The Holy Bible NABRE JSON Dataset

This repository contains New American Bible Revised Edition ([NABRE](https://www.biblegateway.com/versions/New-American-Bible-Revised-Edition-NABRE-Bible/)) of The Holy Bible in JSON dataset along with the Bash script (`get_nabre_books`) used to generate it.
The Bash script scrapes [biblegateway.com](https://www.biblegateway.com/versions/New-American-Bible-Revised-Edition-NABRE-Bible/#booklist) to get the verses for each chapter in each book (credits to [bible_verse-cli](https://github.com/RaynardGerraldo/bible_verse-cli) for the idea).

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
