# Ren-Py-Dialogue-Parser
A small utility I made to parse my Ren'Py files and add proper tagging (mainly wait tags) to dialogue. Might be edited to be more customizable in future.

## CRUCIAL NOTE: 
This WILL save over your files. Anything in the selected Output or Backup folders with the same names as a given input will be re-written. I already keep version-control backups of my files Input into this program so this isn't an issue for me, but it may be for you.

## Usage:
Run file 'gui.py' with Python 3.8 or higher. You will be asked to select input, output, and backup folders. All '.rpy' files in these folders will be input.

## Parsing Specifications:
Right now, this parser is specifically meant to add consistent wait tags in dialogue to give dialogue a more "natural" feel. It currently parses character-by-character but will be switched to a more robust RegEx system in the future if I need more flexibility. It's still pretty smart, and follows these rules:
- Characters within brackets '( )' '[ ]' '{ }' will be copied with no changes, to not mess with Python or Ren'Py functions
- Existing wait tags will not be copied
- All other dialogue tags remain unchanged
- At the end of each set of punctuation, place either a 0.8s or a 0.4s wait tag depending on the punctuation
- Punctuation such as hyphenated words or periods used on acronyms are exempt
- Wait tags will not be placed at the end of dialogue
- Both single-quote and triple-quote paragraphs are recognized as dialogue

Right now, it differentiates soft/single punctuation such as commas and hyphens with 0.4s waits from hard/double punctuation such as periods and exclamation points with 0.8s waits.

## Future Updates
I want to make the tagging system more flexible and add more options of where/what to tag. Allowing a customized wait period for each given type of punctuation is a priority, too.
In the future depending on the scale of the project I made this for I might revamp it.