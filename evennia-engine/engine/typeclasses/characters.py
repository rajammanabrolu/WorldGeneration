"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter

MAX_EXPLORE = {'ABCD': 3, 'N766': 5, '5F6Z': 5, 'R28B': 5, '8F66': 5, 'X43K': 6, 'SB88': 11, 'B78H': 6, '9Q4F': 6}
# not using answer key anymore
# ANSWER_KEY = {'ABCD': 'Y4Q8KM19ZTP7', 'N766': 'VD47G3T899AH', '5F6Z': 'CDBRC43WUC74', 'R28B': '7DZ6A98SH33S', '8F66': 'ZX478N822WYS', 'X43K': 'Y7CMHE46JKN6', 'SB88': 'EZ89R8K4AS38', 'B78H': '7SV6K84RJ3UG', '9Q4F': 'V9WNGN7WQ78B'}
EXPLANATION = {'ABCD': 'the demo game', 'N766': 'random mystery world', '5F6Z': 'rule-based mystery world',
               'R28B': 'neural-generated mystery world', '8F66': 'human-authored mystery world',
               'X43K': 'random fairy tale world', 'SB88': 'rule-based mystery world',
               'B78H': 'neural-generated fairy tale world', '9Q4F': 'human-authored fairy tale world'}

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    def at_object_creation(self):
        self.db.explored = str(self.location.dbref)

    def at_after_move(self, _):
        if self.location.access(self, "view"):
            self.msg(self.at_look(self.location))
            self.track_view(self.location)

        # rooms = self.db.rooms_explored.split(',')
        # if self.location.key not in rooms:
        #     self.db.rooms_explored += ',' + self.location.key
        #
        #     self.check_win_condition()

    def check_win_condition(self):
        explored = self.db.explored.split('\t')

        if self.location.db.zone:
            if self.location.db.zone in EXPLANATION and self.location.db.zone in MAX_EXPLORE:
                if len(explored) == MAX_EXPLORE[self.location.db.zone]:
                    self.msg(
                        '|gCongrats! You have explored ' + EXPLANATION[self.location.db.zone]
                        + '. Feel free to keep exploring, or '
                        + 'close this window and try out a new game.|n')
                else:
                    self.msg(
                        '|gYou have explored {0} entities. Explore {1} total.|n'.format(
                            len(explored), MAX_EXPLORE[self.location.db.zone]))

    def track_view(self, target):
        if target.__class__.__name__ == "Room" or target.__class__.__name__ == "Object":
            explored = self.db.explored.split('\t')
            if target.dbref not in explored:
                self.db.explored += '\t' + target.dbref
                self.check_win_condition()
