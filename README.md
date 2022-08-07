# Spellcheck
A simple spell checking program.

**How to use:**

- Opening `spellcheck.py` launches the spelling correction program
- Once you see `->` enter some words and it will suggest corrections
- Enter nothing to exit the program

Run with `python spellcheck.py` to add some of the following options

- Add `-eval` or `-evaluate`
    To evaluate the accuracy and performance with 100 random words
- Add `-eval 50`
    Same as above, but with 50 random words (100 is default, but you can input any number)
-  Add `edit` or `jaccard` at the end of any command to use Edit Distance or Jaccard Distance algorithms respectively
-  Add `all` to use all the algorithms in the program

*Note: "Edit Distance" is particularly slow, so don't use too many words or evalutaions with that algorithm*

*The default algorithm uses Peter Norvig's technique*
