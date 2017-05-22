from math import ceil

#TODO TEST EVERYTHING

class Meld:
    def __init__(self):
        self.tiles = ''
        self.suit = ''
        self.meld_type = ''
        self.closed = True
        self.simple = True
        self.wind = False
        self.dragon = False
        self.green = False

    def valid_meld(self):
        # standard error checking for meld inputs, given a non-chiitoitsu hand
        # function is applied to all inputted melds
        # a False result causes the program to pause until the user inputs a valid meld
        if len(self.tiles) not in range(3,6):
            return False
            # range(3,6) encompasses 3, 4, and 5
            # string length 3 denotes honors pon
            # string length 4 denotes chi, non-honors pon, or honors kan
            # string length 5 denots non-honors kan
            # any other string length is an invalid meld
        self.tiles = self.tiles.upper()
        if self.tiles[0] in "ESWNRHG":
            if len(self.tiles) > 4:
                return False
            for j in range(len(self.tiles)):
                if self.tiles[j] != self.tiles[0]:
                    return False
            # if the string begins with an honor tile, then string length must not exceed 4
            # honor melds must be pons or kans, so the meld is only valid if all tiles are the same
        elif self.tiles[0] in "MPB":
            if len(self.tiles) < 4:
                return False
                # a non-honors meld is denoted using 1 char for suit and at least 3 for tiles
                # if string length is less than 4, the meld is invalid
            for k in range(len(self.tiles)-1):
                if self.tiles[k+1] not in "123456789":
                    return False
                # chars after the suit indicator must be numbers
            if len(self.tiles) == 5:
                for m in range(2,5):
                    if self.tiles[m] != self.tiles[1]:
                        return False
                # length 5 indicates a kan, so all numbers following the tile indicator must be the same
            elif len(self.tiles) == 4:
                # length 4 is ambiguous, so we check the tile numbers
                if self.tiles[1] == self.tiles[2]:
                    if self.tiles[3] != self.tiles[2]:
                        return False
                    # if the first two numbers are the same, meld should be a pon
                    # meld is valid only if the third number matches the first two
                elif self.tiles[1] != self.tiles[2]:
                    if int(self.tiles[2]) != (int(self.tiles[1]) + 1) or int(self.tiles[3]) != (int(self.tiles[2]) + 1):
                        return False
                    # if the first two numbers are not the same, meld should be a chi
                    # meld is valid only if the numbers form an ascending sequence with d = 1
        else:
            return False
            # a meld starting with anything other than a suit indicator or an honor tile is invalid

        return True
        # if the program gets through all checks without returning False, the tile must be valid

    def suit_meld(self):
        # this function is called only if a meld is valid as defined by valid_meld()
        # we can assume that the meld begins with any of 'MPBESWNRHG'
        # we use the first char in the tile string to set the meld suit and other variables
        if self.tiles[0] == 'M':
            self.suit = 'manzu'
        elif self.tiles[0] == 'P':
            self.suit = 'pinzu'
        elif self.tiles[0] == 'B':
            self.suit = 'souzu'
        elif self.tiles[0] in 'ESWNRHG':
            self.suit = 'honor'
            if self.tiles[0] in 'ESWN':
                self.wind = True
            else:
                self.dragon = True
        return self.suit

    def type_meld(self):
        # this function is called only if a meld is valid as defined by valid_meld()
        # we can assume that the meld is of length 3, 4, or 5
        # we use the first char in the tile string as well as the string length to set the meld type
        # meld types are chi, pon, and kan as defined in comments of valid_meld()
        if len(self.tiles) == 5:
            self.meld_type = 'kan'
            hand_has_kan = True
        elif len(self.tiles) == 4 and self.tiles[0] in 'ESWNRHG':
            self.meld_type = 'kan'
            hand_has_kan = True
        elif len(self.tiles) == 4 and self.tiles[0] in 'MPB':
            if self.tiles[1] == self.tiles[2]:
                self.meld_type = 'pon'
            else:
                self.meld_type = 'chi'
        elif len(self.tiles) == 3:
            self.meld_type = 'pon'
        return self.meld_type

    def is_chi(self):
        return self.meld_type == 'chi'

    def is_pon(self):
        return self.meld_type == 'pon'

    def is_kan(self):
        return self.meld_type == 'kan'
        # preceding three functions for future cleanup and optimization work: delete if unneeded

    def closed_meld(self):
        # closed melds are formed entirely by tiles the player drew themselves
        # this cannot be determined by the tiles alone, so the program asks the user if the meld was closed
        # a chiitoitsu hand is necessarily closed, so this function is not called in that case
        self.closed = evaluate_yn('closed_meld')
        return self.closed

    def green_meld(self):
        # green tiles are so called because their tiles use only green ink
        # a meld is green if and only if it is comprised of souzu 23468 or hatsu
        if self.suit == 'manzu' or self.suit == 'pinzu':
            self.green = False
        if self.suit == 'souzu':
            for i in range(len(self.tiles)-1):
                if self.tiles[i+1] not in '23468':
                    self.green = False
        if self.suit == 'honor':
            if self.tiles[0] != 'G':
                self.green = False

    def simple_meld(self):
        # a simple meld is comprised of only number tiles with value 2-8
        # important for scoring
        if self.suit == 'honor':
            self.simple = False
        else:
            for i in range(3):
                if self.tiles[i+1] in '19':
                    self.simple = False

class Pair:
    def __init__(self):
        self.tiles = ''
        self.suit = ''
        self.simple = True
        self.wind = False
        self.dragon = False
        self.green = True
        self.significant = False

    def valid_pair(self):
        if len(self.tiles) not in range(2,4):
            return False
        # a pair can be 2 or 3 chars long
        # length 2 denotes an honors pair
        # length 3 denotes a non-honors pair
        # tiles in a pair are necessarily the same
        self.tiles = self.tiles.upper()
        if self.tiles[0] in "ESWNRHG":
            if len(self.tiles) != 2:
                return False
            if self.tiles[0] != self.tiles[1]:
                return False
        elif self.tiles[0] in "MPB":
            if len(self.tiles) != 3:
                return False
            for num in range(2):
                if self.tiles[num+1] not in "123456789":
                    return False
            if self.tiles[1] != self.tiles[2]:
                return False
        else:
            return False

        return True

    def suit_pair(self):
        # performs the same function as suit_meld(), but for pairs
        if self.tiles[0] == 'M':
            self.suit = 'manzu'
        elif self.tiles[0] == 'P':
            self.suit = 'pinzu'
        elif self.tiles[0] == 'B':
            self.suit = 'souzu'
        elif self.tiles[0] in 'ESWNRHG':
            self.suit = 'honor'
            if self.tiles[0] in 'ESWN':
                self.wind = True
            else:
                self.dragon = True

    def significant_pair(self):
        # used for determining pinfu and fu calculation
        if self.tiles[0] in "RHG" or self.tiles[0] == round_wind or self.tiles[0] == personal_wind:
            self.significant = True

    def green_pair(self):
        # performs the same function as green_meld(), but for pairs
        if self.suit == 'manzu' or self.suit == 'pinzu':
            self.green = False
        if self.suit == 'souzu':
            for i in range(len(self.tiles)-1):
                if self.tiles[i+1] not in '23468':
                    self.green = False
        if self.suit == 'honor':
            if self.tiles[0] != 'G':
                self.green = False

    def simple_pair(self):
        # performs the same function as simple_meld(), but for pairs
        if self.suit == 'honor':
            self.simple = False
        for i in range(2):
            if self.tiles[i+1] in '19':
                self.simple = False

# user input functions
def yes_or_no_valid(yn):
    # for use in evaluate_yn()
    # returns True if input string is an acceptable yes/no answer and False otherwise
    yn = yn.upper()
    return yn in ['Y','N','YES','NO']

def return_yn(yn):
    # for use in evaluate_yn()
    # returns True if input string indicates 'yes' and False otherwise
    yn = yn.upper()
    return (yn == 'Y' or yn == 'YES')

def evaluate_yn(ask):
    # evaluates yes/no user input for a given prompt and returns True/False
    # if the input is invalid, the program pauses until a valid input is given
    prompts = {
    'hand_closed':'Was the hand fully closed?',
    'closed_meld':'Was it fully closed?',
    'tsumo':'Did the player tsumo?',
    'chiitoitsu':'Was the winning hand chiitoitsu/seven pairs?',
    'kokushi':'Was the winning hand Kokushi Musou/Thirteen Orphans?',
    'riichi':'Did the winner declare riichi?',
    'double_riichi':'Was it declared on the first turn without interruption?',
    'ippatsu':'Did the winner win in one turn of riichi without interruption?',
    'rinshan':'Did the winner declare kan, then win on the extra draw?',
    'chankan':'Did the winner ron off of a late kan?',
    'haitei':'Did the winner tsumo on the last tile?',
    'houtei':'Did the winner ron on the last discard?',
    'paarenchan':'Is this the eighth consecutive victory for the winner?',
    'chiihou':'Did the winner tsumo on the first draw?',
    'renhou':'Did the winner ron off the first discard without interruption?',
    'tenhou':'Did the winner tsumo on the first draw as dealer?'
    }
    string_input = str(input(prompts[str(ask)] + ' (y/n) '))
    while not yes_or_no_valid(string_input):
        invalid()
        string_input = str(input(prompts[str(ask)] + ' (y/n) '))
    return return_yn(string_input)

def valid_wind(wind):
    # for use in evaluate_wind
    # performs same function as yes_or_no_valid() but for winds
    wind = wind.upper()
    return wind in ['E','S','W','N','EAST','SOUTH','WEST','NORTH']

def evaluate_wind(ask):
    # evaluates wind input for scoring purposes
    # if the input is invalid, the program pauses until a valid input is given
    prompts = {
    'round_wind':'Round wind (E/S/W/N): ',
    'personal_wind':'Personal wind (E/S/W/N): '
    }
    string_input = str(input(prompts[str(ask)]))
    while not valid_wind(string_input):
        invalid()
        string_input = str(input(prompts[str(ask)]))
    return string_input.upper()

def valid_number(num):
    # for use in evaluate_number
    # prevents program from crashing by attempting to convert non-numerical string to int
    for i in num:
        if i not in "1234567890":
            return False

    return True

def evaluate_number(ask):
    # evaluates various numerical questions for scoring purposes
    # if the input is invalid, the program pauses until a valid input is given
    prompts = {
    'bonus_round':'Number of bonus sticks on table: ',
    'riichibon':'Number of riichi sticks on table, including any placed by the winner: ',
    'dora':'Total dora value of hand: '
    }
    string_input = str(input(prompts[str(ask)]))
    while not valid_number(string_input):
        invalid()
        string_input = str(input(prompts[str(ask)]))
    return int(string_input)

def invalid():
    # prints an error message that asks the user to try again
    print(invalid_input)

# yaku checking functions

# yakuman functions
def chuuren_check():
    # chuuren is a hand comprised of 1112345678999 in one suit, plus an extra tile in the same suit
    # this configuration always forms a valid hand and is worth yakuman
    # if the player has a 9-sided wait, the hand is optionally worth double yakuman
    if melds[0].suit == melds[1].suit == melds[2].suit == melds[3].suit == std_pair.suit and hand_closed:
        if melds[0].suit != 'honor':
            numbers = [hand[i][1:len(hand[i])] for i in range(len(hand))]
            numbers = ''.join(sorted(numbers))
            return numbers in chuuren_strings
        else:
            return False
    else:
        return False

# functions called only if chuuren is False
def shousuushi_check():
    # shousuushi ("small four winds") is a hand containing pons/kans of three winds and a pair of the fourth
    # the hand may be open, and requires at least one non-wind meld
    # would it be easier to use sets here...?
    if std_pair.wind != True:
        return False
    winds = [melds[i].tiles for i in range(4) if melds[i].wind == True]
    if len(winds) != 3:
        return False
    for i in range(len(winds)):
        winds[i] = winds[i][:3]
    # truncates any kans for ease of checking
    winds.append(std_pair.tiles)
    winds = ''.join(sorted(winds))
    return winds in shousuushi_strings      # can probably be reduced to first if statement once duplicate tile checking is integrated

def daisuushi_check():
    # daisuushi ("big four winds") is a hand containing pons/kans of all four winds
    # therefore, the pair cannot be a wind
    if std_pair.wind != False:
        return False
    for i in range(4):
        if melds[i].wind != True:
            return False
    winds = [melds[i].tiles for i in range(4)]
    for i in range(len(winds)):
        winds[i] = winds[i][:3]
    # truncates any kans for ease of checking
    winds = ''.join(sorted(winds))
    return winds == daisuushi_string

def daisangen_check():
    # daisangen ("big three dragons") is a hand containing pons/kans of all three dragons
    # therefore, the pair cannot be a dragon, or the hand can only be shousangen at best
    if std_pair.dragon == True:
        return False
    dragons = [melds[i].tiles for i in range(4) if melds[i].dragon == True]
    if len(dragons) != 3:
        return False
    for i in range(len(dragons)):
        dragons[i] = dragons[i][:3]
    # truncates any kans for ease of checking
    dragons = ''.join(sorted(dragons))
    return dragons == daisangen_string

def daichisei_check():
    # daichisei ("big seven stars") is chiitoitsu combined with tsuuiisou
    # there are seven different honor tiles and chiitoitsu requires seven distinct pairs
    # therefore, there is only one acceptable combination of tiles for daichisei
    for i in range(7):
        if ct_pairs[i].suit != 'honor':
            return False
    pairs = [ct_pairs[i].tiles for i in range(7)]
    pairs = ''.join(sorted(pairs))
    return pairs == daichisei_string

def tsuuiisou_check():
    # tsuuiisou is a hand composed of only honors
    # all four melds and the pair must be made of honors
    if std_pair.suit != 'honor':
        return False
    for i in range(4):
        if melds[i].suit != 'honor':
            return False
    return True

def chinroutou_check():
    # chinroutou is a hand composed of only terminals
    # thus, no honor melds or chi melds are allowed
    for i in range(4):
        if melds[i].suit == 'honor' or melds[i].meld_type == 'chi':
            return False
        for j in range(len(melds[i].tiles)-1):
            if melds[i].tiles[j+1] not in '19':
                return False
    return True

def ryuuiisou_check():
    # ryuuiisou is a hand composed of only "green" tiles as defined by green_meld() and green_pair()
    for i in range(4):
        if not melds[i].green_meld():
            return False
    if not std_pair.green_pair():
        return False
    return True

def daisharin_check():
    # daisharin is an optional yakuman for a closed hand containing 22334455667788 in one suit
    # with other yaku only, a daisharin hand is worth pinfu + tanyao + ryanpeikou + chinitsu
    # without this yakuman condition, the hand is still worth at least 11 han for sanbaiman
    # an additional 2 han from riichi/ippatsu/dora easily bring the hand to a kazoe-yakuman
    # there are three different names, one for each suit
    if melds[0].suit == melds[1].suit == melds[2].suit == melds[3].suit == std_pair.suit != 'honor':
        numbers = [melds[i].tiles[1:] for i in range(4)]
        numbers.append(std_pair.tiles[1:])
        numbers = ''.join(sorted(''.join(numbers)))
        return numbers == daisharin_string

def iipeikou_ryanpeikou_check():
    # called only if hand is closed
    # iipeikou is true if a hand contains two identical sequences in the same suit
    # ryanpeikou is true if a hand contains two pairs of identical sequences
    # ryanpeikou resembles chiitoitsu but is composed of melds and is therefore not scored as chiitoitsu
    # it is worth 3 han if closed and 2 han if open
    sets = [melds[i].tiles for i in range(4) if melds[i].meld_type == 'chi']
    if melds[0].tiles == melds[1].tiles == melds[2].tiles == melds[3].tiles:
        return 2
    duplicate_sets = set([meld for meld in sets if sets.count(meld) > 1])
    return len(duplicate_sets)

def itsuu_check():
    # itsuu is true if a hand contains three sequences in the same suit forming a straight from 1-9
    # it is worth 2 han if closed and 1 if open
    sets = sorted([melds[i].tiles for i in range(4) if melds[i].meld_type == 'chi'])
    if len(sets) < 3:
        return False
    # an itsuu hand must have at least three chi melds
    if len(sets) == 3:
        # if there are exactly three chi melds, then their numbers must form 123456789 and their suits must be the same
        if not (sets[0][0] == sets[1][0] == sets[2][0]):
            return False
        itsuu_tiles = ''.join(sorted(([sets[i][1:] for i in range(3)])))
        return itsuu_tiles == itsuu_string
    if len(sets) == 4:
        itsuu_suits = sorted([melds[i].tiles[0] for i in range(4)])
        for suit in ['B','M','P']:
            if itsuu_suits.count(suit) == 3:
                # if there are three chi melds of the same suit, their numbers must form 123456789
                itsuu_tiles = ''.join(sorted(([sets[i][1:] for i in range(4) if sets[i][0] == suit])))
                return itsuu_tiles == itsuu_string
            elif itsuu_suits.count(suit) == 4:
                # if there are four chi melds, there is at least one meld that does not contribute to itsuu
                # if all four chi melds are of the same suit, then the set of their numbers must contain '123', '456', and '789'
                itsuu_tiles = set()
                for i in range(4):
                    itsuu_tiles.add(sets[i][1:])
                return '123' in itsuu_tiles and '456' in itsuu_tiles and '789' in itsuu_tiles
        return False

def sanshoku_doujun_check():
    # sanshoku doujun is true if a hand contains a given chi meld in all three non-honor suits
    # it is worth 2 han if closed and 1 if open
    sets = sorted([melds[i].tiles for i in range(4) if melds[i].meld_type == 'chi'])
    if len(sets) < 3:
        return False
    if len(sets) == 3:
        if sets[0][1:] == sets[1][1:] == sets[2][1:] and sets[0][0] != sets[1][0] != sets[2][0] != sets[0][0]:
            return True
    if len(sets) == 4:
        suit_check = ''.join(sorted([sets[i][0] for i in range(4)]))
        if suit_check not in sanshoku_four_suits:               # if this doesn't trigger when it's supposed to, it might be a problem with not putting upper()
            return False
        for i in range(3):
            for j in range(3-i):
                sanshoku_four_compare_tiles[i][j] = sets[i][1:] == sets[j+i+1][1:]
        if suit_check == 'BBMP':
            return sanshoku_four_compare_tiles == sanshoku_four_compare_same or sanshoku_four_compare_tiles in sanshoku_four_compare_bbmp
        elif suit_check == 'BMMP':
            return sanshoku_four_compare_tiles == sanshoku_four_compare_same or sanshoku_four_compare_tiles in sanshoku_four_compare_bmmp
        elif suit_check == 'BMPP':
            return sanshoku_four_compare_tiles == sanshoku_four_compare_same or sanshoku_four_compare_tiles in sanshoku_four_compare_bmpp
        # this honestly seems like such a horrifyingly bad way to do it but it's the best I got for now
        # TODO explain how this works in comments

def sanshoku_doukou_check():
    # sanshoku doukou is true if a hand contains a given pon/kan meld in all three non-honor suits
    # it is incompatible with any yaku requiring two or more chi melds
    # it is worth 2 han if closed and 1 if open
    sets = sorted([melds[i].tiles[0:4] for i in range(4) if melds[i].meld_type == 'pon' or melds[i].meld_type == 'kan'])
    if len(sets) < 3:
        return False
    if len(sets) == 3:
        if sets[0][1:4] == sets[1][1:4] == sets[2][1:4] and sets[0][0] != sets[1][0] != sets[2][0] != sets[0][0]:
            return True
    if len(sets) == 4:
        suit_check = ''.join(sorted([sets[i][0] for i in range(4)]))
        if suit_check not in sanshoku_four_suits:               # if this doesn't trigger when it's supposed to, it might be a problem with not putting upper()
            return False
        for i in range(3):
            for j in range(3-i):
                sanshoku_four_compare_tiles[i][j] = sets[i][1:4] == sets[j+i+1][1:4]
        if suit_check == 'BBMP':
            return sanshoku_four_compare_tiles == sanshoku_four_compare_same or sanshoku_four_compare_tiles in sanshoku_four_compare_bbmp
        elif suit_check == 'BMMP':
            return sanshoku_four_compare_tiles == sanshoku_four_compare_same or sanshoku_four_compare_tiles in sanshoku_four_compare_bmmp
        elif suit_check == 'BMPP':
            return sanshoku_four_compare_tiles == sanshoku_four_compare_same or sanshoku_four_compare_tiles in sanshoku_four_compare_bmpp
        # this is literally just sanshoku_doujun but slightly modified...maybe find a way to merge? not high on priorities list as long as it works

def honroutou_check():
    # this function is only called if the yakuman counter is 0
    # therefore, we can assume the hand is neither chinroutou not tsuuiisou
    # if this check finds honroutou is true, then junchanta must be false and there is no need to check
    if chiitoitsu:
        return all([not ct_pairs[i].simple_pair() for i in range(7)])
    else:
        return all([(not melds[i].is_chi() and not melds[i].simple_meld()) for i in range(4)]) and not std_pair.simple_pair()

def junchanta_check():
    # this function is only called if the yakuman counter is 0 and chiitoitsu is false
    # therefore, we can assume the hand is not chinroutou and we need only check for a terminal in each set and no honors
    # this check is skipped if honroutou_check returns True
    # junchanta is incompatible with chiitoitsu because there are only six distinct terminals
    return all([not melds[i].simple_meld() and not melds[i].suit == 'honor' for i in range(4)])

def shousangen_check():
    # this function is only called if the yakuman counter is 0 and chiitoitsu is false
    # shousangen requires pons of two dragons and a pair of the third
    # we can assume the user doesn't input an impossible hand (e.g. two pons of the same dragon)
    # therefore, dragon melds and the dragon pair (if they exist) are necessarily all of different dragons
    dragon_melds = [melds[i].tiles for i in range(4) if melds[i].dragon]
    return all([std_pair.dragon, len(dragon_melds) == 2])

def flush_check():
    # this function is called only if the yakuman counter is zero, so we can assume the hand is not tsuuiisou
    # because sets have no duplicate elements, they can be used to test the presence of suits in the hand
    # if there is only one element in the suit set, chinitsu is true
    # if there are two elements and one is 'honor', then honitsu is true
    # if there are three or four, neither is true
    # this function does not return anything
    # kinda breaks the conventions we've had so far but it shouldn't be too big a deal
    global honitsu_pinzu
    global honitsu_souzu
    global honitsu_manzu
    global chinitsu_pinzu
    global chinitsu_souzu
    global chinitsu_manzu
    global yaku_han
    flush_suits = set()
    if chiitoitsu:
        for i in range(7):
            flush_suits.add(ct_pairs[i].suit)
    else:
        for i in range(4):
            flush_suits.add(melds[i].suit)
        flush_suits.add(std_pair.suit)
    if len(flush_suits) == 1:
        if 'pinzu' in flush_suits:
            chinitsu_pinzu = True
        elif 'souzu' in flush_suits:
            chinitsu_souzu = True
        elif 'manzu' in flush_suits:
            chinitsu_manzu = True
        yaku_han += 5
        if hand_closed:
            yaku_han += 1
    elif len(flush_suits) == 2 and 'honor' in flush_suits:
        if 'pinzu' in flush_suits:
            honitsu_pinzu = True
        elif 'souzu' in flush_suits:
            honitsu_souzu = True
        elif 'manzu' in flush_suits:
            honitsu_manzu = True
        yaku_han += 2
        if hand_closed:
            yaku_han += 1

def tanyao_check():
    if chiitoitsu:
        return all([ct_pairs[i].simple for i in range(7)])
    if not chiitoitsu:
        return all([all([melds[i].simple for i in range(4)]), std_pair.simple])

# suit = []                           # come back to this after the rest of the calculator is done
# for i in range(1,10):               # creates list of numbers for checking if user has specified more tiles than exist
#     for j in range (4):             # e.g. tries to specify two melds reading 'P333' when there are only 4 P3 in a set
#         suit.append(i)
#         j+=1
# print(suit)

# winning hand variables
tiles = ''
wait = ''
hand = []
hand_closed = True
valid_closed = False                  # to stop user from inputting invalid hand_closed/open information combinations
hand_has_kan = False
tsumo = True
dealer = False
# 1 han yaku
menzen_tsumo = False
pinfu = False
riichi = False
ippatsu = False
iipeikou = False
rinshan = False
chankan = False
haitei = False
houtei = False
tanyao = False
yakuhai_east = False
yakuhai_south = False
yakuhai_west = False
yakuhai_north = False
yakuhai_red = False
yakuhai_white = False
yakuhai_green = False
# 2/1 han yaku
chanta = False
itsuu = False
sanshoku_doujun = False
sanshoku_doukou = False
# 2 han yaku
double_riichi = False
toitoi = False
sanankou = False
sankantsu = False
honroutou = False
shousangen = False
chiitoitsu = False
# 3/2 han yaku
honitsu_pinzu = False
honitsu_souzu = False
honitsu_manzu = False
junchanta = False
# 3 han yaku
ryanpeikou = False
# 6/5 han yaku
chinitsu_pinzu = False
chinitsu_souzu = False
chinitsu_manzu = False
# yakuman
kokushi = False
paarenchan = False
renhou = False
chiihou = False
tenhou = False
chuuren = False
suuankou = False
shousuushi = False
daisangen = False
suukantsu = False
daichisei = False
tsuuiisou = False
chinroutou = False
ryuuiisou = False
daisharin = False
daichikurin = False
daisuurin = False
# double yakuman
kokushi_thirteen = False
chuuren_nine = False
suuankou_tanki = False
daisuushi = False

# scoring variables
yakuman_counter = 0
yaku_han = 0
total_han = 0
fu = 20
meld_fu = [0,0,0,0]
basic_points = 0
tsumo_nondealer_points = 0
tsumo_dealer_points = 0
ron_points = 0
total_points = 0
chombo = False


# board variables
round_wind = ''
personal_wind = ''

invalid_input = "Invalid input. Please re-enter."

chuuren_strings = ['11112345678999','11122345678999','11123345678999','11123445678999','11123455678999','11123456678999','11123456778999','11123456788999','11123456789999']
shousuushi_strings = ['EEENNNSSSWW','EEENNNSSWWW','EEENNSSSWWW','EENNNSSSWWW']
daisuushi_string = 'EEENNNSSSWWW'
daisangen_string = 'GGGHHHRRR'
daichisei_string = 'EEGGHHNNRRSSWW'
daisharin_string = '22334455667788'

itsuu_string = '123456789'

sanshoku_four_suits = ['BBMP','BMMP','BMPP']
sanshoku_four_compare_tiles = [[False,False,False],[False,False],[False]]
sanshoku_four_compare_same = [[True,True,True],[True,True],[True]]
sanshoku_four_compare_bbmp = [[[False,True,True],[False,False],[True]],[[False,False,False],[True,True],[True]]]
sanshoku_four_compare_bmmp = [[[True,False,True],[False,True],[False]],[[False,True,True],[False,False],[True]]]
sanshoku_four_compare_bmpp = [[[True,True,False],[True,False],[False]],[[True,False,True],[False,True],[False]]]
# there HAS to be a better way to do this

print('Japanese Mahjong Point Calculator\nPython Edition\n')

print('1. Ryanmen/Open (two consecutive non-terminal number tiles waiting for a tile on either side)')
print('2. Penchan/Edge (1-2 or 8-9 of a suit waiting for 3 or 7)')
print('3. Shanpon/Double Pair (two pairs waiting for a third tile of either)')
print('4. Kanchan/Closed (two non-consecutive number tiles waiting for the middle number)')
print('5. Tanki/Pair (one tile waiting for pair)')
print('6. 9+ Sided (nine or more possible winning tiles)\n')
wait = str(input('What was the winning wait? '))
while wait not in "123456" or len(wait) != 1:
    invalid()
    wait = str(input('What was the winning wait? '))

hand_closed = evaluate_yn('hand_closed')

tsumo = evaluate_yn('tsumo')
if tsumo and hand_closed:
    menzen_tsumo = True

if wait == '5' and hand_closed:
    chiitoitsu = evaluate_yn('chiitoitsu')
    print(chiitoitsu)
else:
    chiitoitsu = False

if chiitoitsu:
    ct_pairs = [Pair() for i in range(7)]
    print('Input pairs:')
    for i in range(7):
        ct_pairs[i].tiles = str(input('Pair ' + str(i+1) + ': '))
        while not ct_pairs[i].valid_pair():
            invalid()
            ct_pairs[i].tiles = str(input('Pair ' + str(i+1) + ': '))
            ct_pairs[i].suit = ct_pairs[i].suit_pair()
    hand = [ct_pairs[i].tiles for i in range(7)]
    print(hand)             # merge with previous conditional?

elif not chiitoitsu:
    if wait in "56" and hand_closed:
        kokushi = evaluate_yn('kokushi')
        if kokushi:
            yakuman_counter += 1
            if wait == "6":
                kokushi_thirteen = True
                yakuman_counter += 1
    if not kokushi:
        melds = [Meld() for i in range(4)]
        std_pair = Pair()
        print('Enter melds. For non-honor melds, use a suit indicator followed by 3 or 4 numbers.')
        print('Suits are (P)inzu/coins, souzu/(B)amboo, and (M)anzu/characters.')
        print('Honors are (E)ast, (S)outh, (W)est, (N)orth, (R)ed/Chun, White/(H)aku, and (G)reen/Hatsu.')
        print('Examples: P123, M555, B9999, HHH, EEEE')
        while valid_closed == False:
            for i in range(len(melds)):
                melds[i].tiles = str(input('Meld ' + str(i+1) + ': '))
                while not melds[i].valid_meld():
                    invalid()
                    melds[i].tiles = str(input('Meld ' + str(i+1) + ': '))
                melds_set = set(melds[i].tiles for i in range(4))
                melds[i].suit_meld()
                melds[i].type_meld()
                melds_types = [melds[i].meld_type for i in range(4)]
                melds[i].green_meld()
                melds[i].simple_meld()
                if not hand_closed:
                    melds[i].closed_meld()
                print(melds[i].tiles, melds[i].suit, melds[i].meld_type, melds[i].closed, melds[i].simple, melds[i].wind, melds[i].dragon, melds[i].green)
            if not hand_closed and melds[0].closed == melds[1].closed == melds[2].closed == melds[3].closed == True and tsumo:
                print('Invalid input. You cannot win an open hand with four closed melds with tsumo. Please re-input melds.')
                continue
            valid_closed = True

        std_pair.tiles = str(input("Enter pair: "))
        while not std_pair.valid_pair():
            invalid()
            std_pair.tiles = str(input("Enter pair: "))
        std_pair.suit_pair()
        std_pair.simple_pair()
        std_pair.significant_pair()
        std_pair.green_pair()
        print(std_pair.tiles, std_pair.suit, std_pair.simple, std_pair.wind, std_pair.dragon, std_pair.green, std_pair.significant)

        hand = [melds[i].tiles for i in range(4)]
        hand.append(std_pair.tiles)
        print(hand)

round_wind = evaluate_wind('round_wind')

personal_wind = evaluate_wind('personal_wind')
if personal_wind == 'E' or personal_wind == 'EAST':
    dealer = True

bonus_round = evaluate_number('bonus_round')
print(bonus_round)
riichibon = evaluate_number('riichibon')
print(riichibon)
dora = evaluate_number('dora')
print(dora)

if riichibon != 0:
    riichi = evaluate_yn('riichi')

if riichi:
    double_riichi = evaluate_yn('double_riichi')
    ippatsu = evaluate_yn('ippatsu')

if not chiitoitsu and not kokushi and tsumo and hand_has_kan:
    rinshan = evaluate_yn('rinshan')

if not rinshan and not tsumo:
    chankan = evaluate_yn('chankan')

if not rinshan and not chankan and tsumo and (not ippatsu and not double_riichi):
    haitei = evaluate_yn('haitei')
    # if haitei:
    #     yakuman_counter += 1
    # TODO this is clearly wrong. I'm not sure why this is a thing, but I'll look into it later.

if not rinshan and not chankan and not haitei and not tsumo and (not ippatsu and not double_riichi):
    houtei = evaluate_yn('houtei')

if not dealer and not riichi and not rinshan and not chankan and not haitei and not houtei and hand_closed and not hand_has_kan:
    if tsumo:
        chiihou = evaluate_yn('chiihou')
        if chiihou:
            yakuman_counter += 1
    if not tsumo:
        renhou = evaluate_yn('renhou')
        if renhou:
            yakuman_counter += 1

if dealer and not riichi and not rinshan and not chankan and not haitei and not houtei and tsumo and hand_closed and not hand_has_kan:
    tenhou = evaluate_yn('tenhou')
    if tenhou:
        yakuman_counter += 1

paarenchan = evaluate_yn('paarenchan')
if paarenchan:
    yakuman_counter += 1

# check for yakuman
if not kokushi:

    if chiitoitsu:
        if daichisei_check():
            tsuuiisou = True
            daichisei = True
            yakuman_counter += 2

    elif not chiitoitsu:
        if tsuuiisou_check():
            tsuuiisou = True
            yakuman_counter += 1

        if chuuren_check():
            chuuren = True
            yakuman_counter += 1
            if wait == '6':
                chuuren_nine = True
                yakuman_counter += 1

        if not chuuren:
            if hand_closed and melds[0].closed == melds[1].closed == melds[2].closed == melds[3].closed == True:
                if melds_types.count('chi') == 0:
                    suuankou = True
                    yakuman_counter += 1
                    if wait == '5':
                        suuankou_tanki = True
                        yakuman_counter += 1

            if shousuushi_check():
                shousuushi = True
                yakuman_counter += 1
            elif daisuushi_check():
                daisuushi = True
                yakuman_counter += 2

            if daisangen_check():
                daisangen = True
                yakuman_counter += 1

            if melds_types.count('kan') == 4:
                suukantsu = True
                yakuman_counter += 1

            if not tsuuiisou and not shousuushi and not daisuushi and not daisangen:
                if chinroutou_check():
                    chinroutou = True
                    yakuman_counter += 1

                if ryuuiisou_check():
                    ryuuiisou = True
                    yakuman_counter += 1

                if daisharin_check():
                    if melds[0].suit == 'pinzu':
                        daisharin = True
                    elif melds[0].suit == 'souzu':
                        daichikurin = True
                    elif melds[0].suit == 'manzu':
                        daisuurin = True
                    yakuman_counter += 1

# check non-yakuman yaku if no yakuman
if yakuman_counter == 0:
    if riichi:
        yaku_han += 1
        if double_riichi:
            yaku_han += 1
        if ippatsu:
            yaku_han += 1
    if chiitoitsu:
        yaku_han += 2
    if menzen_tsumo:
        yaku_han += 1
    if haitei:
        yaku_han += 1
    if houtei:
        yaku_han += 1
    if rinshan:
        yaku_han += 1
    if chankan:
        yaku_han += 1
    flush_check()

    if tanyao_check():
        tanyao = True
        yaku_han += 1
    if chiitoitsu:
        if honroutou_check():
            yaku_han += 2
    elif not chiitoitsu:
        if wait == '1' and hand_closed and melds_types.count('chi') == 4 and not std_pair.significant_pair():
            pinfu = True                    # should i write a function for pinfu_check()?
            yaku_han += 1
        if itsuu_check():
            itsuu = True
            yaku_han += 1
            if hand_closed:
                yaku_han += 1
        if hand_closed:
            if iipeikou_ryanpeikou_check() == 2:
                ryanpeikou = True
                yaku_han += 3
            elif iipeikou_ryanpeikou_check() == 1:
                iipeikou = True
                yaku_han += 1
        if sanshoku_doujun_check():
            sanshoku_doujun = True
            yaku_han += 1
            if hand_closed:
                yaku_han += 1
        if melds_types.count('chi') == 0:
            toitoi = True
            yaku_han += 2
        if sum(1 for meld in melds if meld.meld_type == 'pon' and meld.closed) == 3:
            sanankou = True
            yaku_han += 2
        if sanshoku_doukou_check():
            sanshoku_doukou = True
            yaku_han += 2
        if melds_types.count('kan') == 3:
            sankantsu = True
            yaku_han += 2
        if 'EEE' in melds_set or 'EEEE' in melds_set:
            if round_wind == 'E' or personal_wind == 'E':
                yakuhai_east = True
                if round_wind == 'E':
                    yaku_han += 1
                if personal_wind == 'E':
                    yaku_han += 1
        if 'SSS' in melds_set or 'SSSS' in melds_set:
            if round_wind == 'S' or personal_wind == 'S':
                yakuhai_south = True
                if round_wind == 'S':
                    yaku_han += 1
                if personal_wind == 'S':
                    yaku_han += 1
        if 'WWW' in melds_set or 'WWWW' in melds_set:
            if round_wind == 'W' or personal_wind == 'W':
                yakuhai_west = True
                if round_wind == 'W':
                    yaku_han += 1
                if personal_wind == 'W':
                    yaku_han += 1
        if 'NNN' in melds_set or 'NNNN' in melds_set:
            if round_wind == 'N' or personal_wind == 'N':
                yakuhai_north = True
                if round_wind == 'N':
                    yaku_han += 1
                if personal_wind == 'N':
                    yaku_han += 1
        if 'RRR' in melds_set or 'RRRR' in melds_set:
            yakuhai_red = True
            yaku_han += 1
        if 'HHH' in melds_set or 'HHHH' in melds_set:
            yakuhai_white = True
            yaku_han += 1
        if 'GGG' in melds_set or 'GGGG' in melds_set:
            yakuhai_green = True
            yaku_han += 1
        if sum(1 for meld in melds if meld.simple_meld()) == 0 and not std_pair.simple_pair() and melds_types.count('chi') >= 1:
            chanta = True           # chanta_check()?
            yaku_han += 1           # careful, chanta can be overwritten by junchanta or honroutou
            if hand_closed:
                yaku_han += 1
        if chanta:
            if honroutou_check():   # TODO include another chanta check for chiitoitsu since chanta and chiitoi are incompatible
                honroutou = True
                chanta = False
                if not hand_closed:
                    yaku_han += 1
            elif junchanta_check(): # if program reaches this point, hand is definitely not chinroutou
                junchanta = True
                chanta = False
                yaku_han += 1
        if shousangen_check():
            shousangen = True
            yaku_han += 2

if yakuman_counter == 0:
    total_han = yaku_han + dora
    if total_han < 5:
        if chiitoitsu:
            fu += 5
        else:
            if pinfu:
                if not tsumo:
                    fu += 10
            else:
                if wait == 2 or wait == 4 or wait == 5:
                    fu += 2
                if hand_closed and not tsumo:
                    fu += 10
                if tsumo:
                    fu += 2
                if not hand_closed and not tsumo:
                    fu += 0
                if std_pair.significant_pair():
                    fu += 2
                if std_pair.tiles[0] == round_wind == personal_wind:
                    fu += 2
                for i in range(4):
                    if melds[i].meld_type != 'chi':
                        meld_fu[i] = 2
                        if not melds[i].simple_meld():
                            meld_fu[i] *= 2
                        if melds[i].closed:
                            meld_fu[i] *= 2
                        if melds[i].meld_type == 'kan':
                            meld_fu[i] *= 4
                fu += sum(meld_fu)
                fu = 10 * ceil(fu/10)
        basic_points = fu * pow(2, (2 + han))
        if basic_points > 2000:
            basic_points = 2000
    elif total_han == 5:
        basic_points = 2000
    elif total_han in range(6,8):
        basic_points = 3000
    elif total_han in range(8,11):
        basic_points = 4000;
    elif total_han in range(11,13):
        basic_points = 6000
    elif total_han >= 13:
        basic_points = 8000

if yakuman_counter > 0:
    if dealer:
        total_points = yakuman_counter * 4 * 8000 * 1.5
        if tsumo:
            tsumo_nondealer_points = total_points / 3
        else:
            ron_points = total_points
    else:
        total_points = yakuman_counter * 4 * 8000
        if tsumo:
            tsumo_nondealer_points = total_points / 4
            tsumo_dealer_points = total_points / 2
        else:
            ron_points = total_points
else:
    if dealer:
        if tsumo:
            tsumo_nondealer_points = 100 * ceil((basic_points * 2) / 100)
            total_points = 3 * tsumo_nondealer_points
        else:
            ron_points = 100 * ceil((basic_points * 6) / 100)
            total_points = ron_points
    else:
        if tsumo:
            tsumo_nondealer_points = 100 * ceil(basic_points / 100)
            tsumo_dealer_points = 100 * ceil((basic_points * 2) / 100)
            total_points = tsumo_dealer_points + (2 * tsumo_nondealer_points)
        else:
            ron_points = 100 * ceil((basicPointsFloat * 4) / 100)
            total_points = ron_points

print('\n')
if yakuman_counter > 0:
    if suuankou:
        if suuankou_tanki:
            print('Suuankou Tanki Machi:             Double Yakuman')
        else:
            print('Suuankou:                         Yakuman')
    if kokushi:
        if kokushi_thirteen:
            print('Kokushi Musou Juusanmen Machi:    Double Yakuman')
        else:
            print('Kokushi Musou:                    Yakuman')
    if daisangen:
        print('Daisangen:                        Yakuman')
    if shousuushi:
        print('Shousuushi:                       Yakuman')
    if daisuushi:
        print('Daisuushi:                        Double Yakuman')
    if tsuuiisou and not daichisei:
        print('Tsuuiisou:                        Yakuman')
    if daichisei:
        print('Daichisei:                        Double Yakuman')
    if chinroutou:
        print('Chinroutou:                       Yakuman')
    if ryuuiisou:
        print('Ryuuiisou:                        Yakuman')
    if daisharin:
        print('Daisharin:                        Yakuman')
    if daichikurin:
        print('Daichikurin:                      Yakuman')
    if daisuurin:
        print('Daisuurin:                        Yakuman')
    if chuuren:
        if chuuren_nine:
            print('Junsei Chuuren Poutou:            Double Yakuman')
        else:
            print('Chuuren Poutou:                   Yakuman')
    if suukantsu:
        print('Suukantsu:                        Yakuman')
    if paarenchan:
        print('Paarenchan:                       Yakuman')
    if renhou:
        print('Renhou:                           Yakuman')
    if chiihou:
        print('Chiihou:                          Yakuman')
    if tenhou:
        print('Tenhou:                           Yakuman')
    print('\n')
    if yakuman_counter == 1:
        print('Yakuman')
    elif yakuman_counter == 2:
        print('Double Yakuman')
    elif yakuman_counter == 3:
        print('Triple Yakuman')
    elif yakuman_counter >= 4:
        print('%dx Yakuman' %yakuman_counter)

if yakuman_counter == 0:
    if riichi:
        if double_riichi:
            print('Double Riichi:                    2 Han')
        if not double_riichi:
            print('Riichi:                           1 Han')
        if ippatsu:
            print('Ippatsu:                          1 Han')
    if chiitoitsu:
        print('Chiitoitsu:                       2 Han')
    if menzen_tsumo:
        print('Menzen Tsumo:                     1 Han')
    if haitei:
        print('Haitei Raoyue:                    1 Han')
    if houtei:
        print('Houtei Raoyui:                    1 Han')
    if rinshan:
        print('Rinshan Kaihou:                   1 Han')
    if chankan:
        print('Chankan:                          1 Han')
    if pinfu:
        print('Pinfu:                            1 Han')
    if itsuu:
        if hand_closed:
            print('Itsuu (Closed):                   2 Han')
        else:
            print('Itsuu (Open):                     1 Han')
    if iipeikou:
        if ryanpeikou:
            print('Ryanpeikou:                       3 Han')
        else:
            print('Iipeikou:                         1 Han')
    if sanshoku_doujun:
        if hand_closed:
            print('Sanshoku Doujun (Closed):         2 Han')
        else:
            print('Sanshoku Doujun (Open)            1 Han')
    if toitoi:
        print('Toitoi:                           2 Han')
    if sanankou:
        print('Sanankou:                         2 Han')
    if sanshoku_doukou:
        print('Sanshoku Doukou:                  2 Han')
    if sankantsu:
        print('Sankantsu:                        2 Han')
    if tanyao:
        print('Tanyao:                           1 Han')
    if yakuhai_east:
        if round_wind == personal_wind:
            print('Double Ton:                       2 Han')
        else:
            print('Ton:                              1 Han')
    if yakuhai_south:
        if round_wind == personal_wind:
            print('Double Nan:                       2 Han')
        else:
            print('Nan:                              1 Han')
    if yakuhai_west:
        if round_wind == personal_wind:
            print('Double Sha:                       2 Han')
        else:
            print('Sha:                              1 Han')
    if yakuhai_north:
        if round_wind == personal_wind:
            print('Double Pei:                       2 Han')
        else:
            print('Pei:                              1 Han')
    if yakuhai_green:
        print('Hatsu:                            1 Han')
    if yakuhai_red:
        print('Chun:                             1 Han')
    if yakuhai_white:
        print('Haku:                             1 Han')
    if chanta:
        if hand_closed:
            print('Chanta (Closed):                  2 Han')
        else:
            print('Chanta (Open):                    1 Han')
    if junchanta:
        if hand_closed:
            print('Junchan (Closed):                 3 Han')
        else:
            print('Junchan (Open):                   2 Han')
    if honroutou:
        print('Honroutou:                        2 Han')
    if shousangen:
        print('Shousangen:                       2 Han')
    if honitsu_pinzu:
        if hand_closed:
            print('Pinzu Honitsu (Closed):           3 Han')
        else:
            print('Pinzu Honitsu (Open):             2 Han')
    if honitsu_souzu:
        if hand_closed:
            print('Souzu Honitsu (Closed):           3 Han')
        else:
            print('Souzu Honitsu (Open):             2 Han')
    if honitsu_manzu:
        if hand_closed:
            print('Manzu Honitsu (Closed):           3 Han')
        else:
            print('Manzu Honitsu (Open):             2 Han')
    if chinitsu_pinzu:
        if hand_closed:
            print('Pinzu Chinitsu (Closed):          6 Han')
        else:
            print('Pinzu Chinitsu (Open):            5 Han')
    if chinitsu_souzu:
        if hand_closed:
            print('Souzu Chinitsu (Closed):          6 Han')
        else:
            print('Souzu Chinitsu (Open):            5 Han')
    if chinitsu_manzu:
        if hand_closed:
            print('Manzu Chinitsu (Closed):          6 Han')
        else:
            print('Manzu Chinitsu (Open):            5 Han')
    if dora > 0:
        if dora < 10:
            print('%d Dora:                           %d Han' %(dora, dora))
        else:
            print('%d Dora:                          %d Han' %(dora, dora))
print('\n')

if yakuman_counter == 0 and yaku_han == 0:
    chombo = True
    print('Invalid hand: no yaku!')
    if dealer:
        print('Chombo Penalty: -4000 All')
    else:
        print('Chombo Penalty: -2000/-4000')

if not chombo and yakuman_counter == 0:
    if total_han < 5:
        print('%d Han %d Fu' %(total_han, fu))
    elif total_han>= 5:
        print('%d Han' %total_han)
    if basic_points == 2000:
        print('Mangan')
    elif basic_points == 3000:
        print('Haneman')
    elif basic_points == 4000:
        print('Baiman')
    elif basic_points == 6000:
        print('Sanbaiman')
    elif basic_points == 8000:
        print('Yakuman')

if not chombo:
    if bonus_round > 0:
        print('Bonus %d                           +%d' %(bonus_round, (300 * bonus_round)))
    if riichibon > 0:
        print('Riichi Bet(s)                     +%d' %(riichibon*1000))
    if dealer:
        if tsumo:
            print('%d All\n' %(tsumo_nondealer_points + (100 * bonus_round)))
        else:
            print('%d\n' %(ron_points + (300 * bonus_round)))
    else:
        if tsumo:
            print('%d/%d\n' %((tsumo_nondealer_points + (100 * bonus_round)),(tsumo_dealer_points + (100 * bonus_round))))
        else:
            print('%d\n' %(ron_points + (300 * bonus_round)))

if not chombo:
    print('Total Points Earned: %d\n' %(total_points + (300 * bonus_round) + (1000 * riichibon)))
else:
    print('No Points Earned \n')
