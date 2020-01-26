"""
Shame(less/ful)ly stolen from:
https://gist.github.com/kylebgorman/c61cb02f511cd0cb0168d1dc9bdd8f5a

English function words.

Sets of English function words, based on

    E.O. Selkirk. 1984. Phonology and syntax: The relationship between
    sound and structure. Cambridge: MIT Press. (p. 352f.)

The categories are of my own creation.
"""

AUXILIARIES = frozenset([
    'AM', 'ARE', "AREN\'T", 'BEEN', 'DID', 'DO', 'DOES', "DON\'T", 'HAD',
    "HADN\'T", 'HAS', "HASN\'T", 'HAVE', "HAVEN\'T", 'IS', "ISN\'T", 'WAS',
    "WASN\'T", 'WERE', "WEREN\'T"
])
CONJUNCTIONS = frozenset([
    'AND', 'AS', 'BECAUSE', 'BEFORE', 'BOTH', 'BUT', 'CUZ', 'EXCEPT', 'IF',
    'OR', 'NOR', 'SINCE', 'SO', 'THAT'
])
DETERMINERS = frozenset([
    'A', 'AN', 'ANY', 'EACH', 'EITHER', 'EVERY', 'NEITHER', 'SOME', 'SUCH',
    'THAT', 'THIS', 'THE', 'ALL', 'BOTH', 'ONE', 'ANOTHER'
])
Q_ADJECTIVES = frozenset([
    'HALF', 'TWICE', 'FIRST', 'OTHER', 'NEXT', 'SECOND', 'LAST', 'MANY', 'MUCH',
    'MORE', 'MOST', 'SEVERAL', 'FEW', 'LITTLE', 'LESS', 'LEAST', 'OWN'
])
INTENSIFIERS = frozenset(['SO', 'TOO'])
MODALS = frozenset([
    'CAN', "CAN\'T", 'COULD', "COULDN\'T", 'MAY', 'MIGHT', 'MUST', "MUSTN\'T",
    'OUGHT', 'SHALL', "SHAN\'T", 'SHOULD', "SHOULDN\'T", 'WILL', 'WOULD',
    "WOULDN\'T"
])
NEGATION = frozenset(['NO', 'NOT'])
SPACE_DEIXIS = frozenset([
    'ABOVE', 'ACROSS', 'AGAINST', 'AMONG', 'AMONGST', 'AT', 'BEHIND', 'BENEATH',
    'BETWEEN', 'BEYOND', 'BY', 'FROM', 'IN', 'HERE', 'ON', 'OUT', 'THERE',
    'THROUGH', 'TO', 'TOWARD', 'TOWARDS', 'WITH', 'UNDER', 'UP'
])
TIME_DEIXIS = frozenset(['AFTER', 'AT', 'DURING', 'IN', 'ON', "'TIL", 'UNTIL'])
PREPOSITIONS = (frozenset(['ABOUT', 'FOR', 'LIKE', 'OF']) | SPACE_DEIXIS
                | TIME_DEIXIS)
TIME = frozenset([
    'TODAY', 'TOMORROW', 'NOW', 'THEN', 'ALWAYS', 'NEVER', 'SOMETIMES',
    'USUALLY', 'OFTEN'
])
ADVERBS = frozenset([
    'THEREFORE', 'HOWEVER', 'BESIDES', 'MOREOVER', 'THOUGH', 'OTHERWISE',
    'ELSE', 'INSTEAD', 'ANYWAY', 'INCIDENTALLY', 'MEANWHILE'
])
PRONOUNS = frozenset([
    'HE', 'HER', 'HIM', 'HIS', 'I', 'IT', 'ITS', 'ME', 'MY', 'OUR', 'SHE',
    'THEIR', 'THEM', 'THESE', 'THOSE', 'THEY', 'US', 'YOU', 'WE', 'MINE',
    'OURS', 'THEIRS', 'MYSELF', 'HIMSELF', 'HERSELF', 'ITSELF', 'OURSELVES',
    'THEMSELVES', 'ANYTHING', 'EVERYTHING', 'SOMETHING', 'NOTHING', 'ANYONE',
    'EVERYONE', 'SOMEONE', 'ONE', 'SUCH'
])
WH = frozenset(
    ['HOW', 'WHAT', 'WHEN', 'WHERE', 'WHICH', 'WHO', 'WHOM', 'WHOSE', 'WHY'])

FUNCTION_WORDS = (AUXILIARIES | CONJUNCTIONS | DETERMINERS | Q_ADJECTIVES
                  | INTENSIFIERS | MODALS | NEGATION | PREPOSITIONS | PRONOUNS
                  | WH)
