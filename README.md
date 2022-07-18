# Spellcheck
A simple spell checking program.

`spellcheck.py` 
  Launches the spelling correction program. Enter some words and it will suggest corrections. Enter nothing to exit the program
  
Add `-eval` or `-evaluate`
  To evaluate the accuracy and performance with 100 random words
 
Add `-eval 50`
  Same as above, but with 50 random words (100 is default)
 
Add `edit` or `jaccard` at the end of any command to use Edit Distance and Jaccard Distance algorithms as well
 
Add `all` to use all the algorithms in the program

*Note: Edit Distance is particularly slow, so don't use too many words or evalutaions with it*
