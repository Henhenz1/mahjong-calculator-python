class Meld:
    def __init__(self):
        self.tiles = ''
        self.suit = ''
        self.meld_type = ''
        self.closed = True
        self.wind = False
        self.dragon = False

    def valid_meld(self):
        if len(self.tiles) not in range(3,6):                           # Minimum length 3 for honor pon
            return False                                            # Maximum length 5 for simple kan
        self.tiles = self.tiles.upper()                                         # Standardizing input for easier checking
        if self.tiles[0] in "ESWNRHG":                                    # Check melds of honor tiles
            if len(self.tiles) > 4:                                       # Max length of honor meld is 4
                return False
            for j in range(len(self.tiles)):                              # All tiles in honor meld are the same
                if self.tiles[j] != self.tiles[0]:
                    return False
        elif self.tiles[0] in "MPB":
            if len(self.tiles) < 4:                                       # Simple meld needs 1 for suit and 3 for numbers
                return False
            for k in range(len(self.tiles)-1):                            # Chars after suit indicator must be numbers
                if self.tiles[k+1] not in "123456789":
                    return False
            if len(self.tiles) == 5:                                      # Length 5 indicates kan - numbers must be the same
                for m in range(2,5):
                    if self.tiles[m] != self.tiles[1]:
                        return False
            elif len(self.tiles) == 4:
                if self.tiles[1] == self.tiles[2]:                              # If first two numbers are the same, meld should be a pon
                    if self.tiles[3] != self.tiles[2]:                          # Third number should also be the same
                        return False
                elif self.tiles[1] != self.tiles[2]:                            # If not the same, should be a chi: numbers sequential
                    if int(self.tiles[2]) != (int(self.tiles[1]) + 1) or int(self.tiles[3]) != (int(self.tiles[2]) + 1):
                        return False
        else:                                                       # Only acceptable first chars are "MPBESWNRHG"
            return False

        return True                                                 # Made it all the way through? Meld is valid

    def suit_meld(self):                        # To be run only if meld is valid
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

    def closed_meld(self):
        self.closed = evaluate_yn('closed_meld')
        return self.closed

class Pair:
    def __init__(self):
        self.tiles = ''
        self.suit = ''
        self.wind = False
        self.dragon = False

    def valid_pair(self):
        if len(self.tiles) not in range(2,4):
            return False
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
        return suit

    def significant_pair(self):
        if self.tiles[0] in "RHG" or self.tiles[0] == round_wind or self.tiles[0] == personal_wind:
            return True
        else:
            return False

def yes_or_no_valid(yn):                #takes a string and checks to see if it fits accepted yes/no strings
    yn = yn.upper()                     # MAKE SURE TO CONVERT INPUT TO STR OR upper() WILL BREAK
    if yn in ['Y','N','YES','NO']:
        return True
    else:
        return False

def return_yn(yn):
    yn = yn.upper()
    return (yn == 'Y' or yn == 'YES')

def evaluate_yn(ask):
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
    wind = wind.upper()
    return wind in ['E','S','W','N','EAST','SOUTH','WEST','NORTH']

def evaluate_wind(ask):
    prompts = {
    'round_wind':'Round wind (E/S/W/N): ',
    'personal_wind':'Personal wind (E/S/W/N): '
    }
    string_input = str(input(prompts[str(ask)]))
    while not valid_wind(string_input):
        invalid()
        string_input = str(input(prompts[str(ask)]))
    return string_input

def valid_number(num):
    for i in num:
        if i not in "1234567890":
            return False

    return True

def evaluate_number(ask):
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
    print(invalid_input)

def chuuren_check():                    # called only when suits are the same and not honors
    numbers = [hand[i][1:len(hand[i])] for i in range(len(hand))]
    numbers = ''.join(sorted(numbers))
    return numbers in chuuren_strings

def shousuushi_check():                 # called only if pair is a wind
    if std_pair.wind != True:
        return False
    winds = [melds[i].tiles for i in range(4) if melds[i].wind == True]
    if len(winds) != 3:
        return False
    for i in range(len(winds)):
        winds[i] = winds[i][:3]             # truncates any kans for ease of checking
    winds.append(std_pair.tiles)
    winds = ''.join(sorted(winds))
    return winds in shousuushi_strings      # can probably be reduced to first if statement once duplicate tile checking is integrated

def daisuushi_check():
    if std_pair.wind != False:
        return False
    for i in range(4):
        if melds[i].wind != True:
            return False
    winds = [melds[i].tiles for i in range(4)]
    for i in range(len(winds)):
        winds[i] = winds[i][:3]
    winds = ''.join(sorted(winds))
    return winds in daisuushi_string

def daisangen_check():

def daichisei_check():
    for i in range(7):
        if ct_pairs[i].suit != 'honor':
            return False
    pairs = [ct_pairs[i].tiles for i in range(7)]
    pairs = ''.join(sorted(pairs))
    return pairs in daichisei_string

def tsuuiisou_check():
    for i in range(4):
        if melds[i].suit != 'honor':
            return False
    if std_pair.suit != 'honor':
        return False

    return True


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


# board variables
round_wind = ''
personal_wind = ''

invalid_input = "Invalid input. Please re-enter."

chuuren_strings = ['11112345678999','11122345678999','11123345678999','11123445678999','11123455678999','11123456678999','11123456778999','11123456788999','11123456789999']
shousuushi_strings = ['EEENNNSSSWW','EEENNNSSWWW','EEENNSSSWWW','EENNNSSSWWW']
daisuushi_string = ['EEENNNSSSWWW']
daichisei_string = ['EEGGHHNNRRSSWW']


print('Japanese Mahjong Point Calculator\nPython Edition\n')

print('1. Ryanmen/Open (two consecutive non-terminal number tiles waiting for a tile on either side)')
print('2. Penchan/Edge (1-2 or 8-9 of a suit waiting for 3 or 7)')
print('3. Shanpon/Double Pair (two pairs waiting for a third tile of either)')
print('4. Kanchan/Closed (two non-consecutive number tiles waiting for the middle number)')
print('5. Tanki/Pair (one tile waiting for pair)')
print('6. 9+ Sided (nine or more possible winning tiles)\n')
wait = str(input('What was the winning wait? '))
while wait not in "123456" or len(wait) > 1:
    invalid()
    wait = str(input('What was the winning wait? '))

hand_closed = evaluate_yn('hand_closed')
print(hand_closed)

tsumo = evaluate_yn('tsumo')
print(tsumo)

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
    print(hand)

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
        for i in range(len(melds)):
            melds[i].tiles = str(input('Meld ' + str(i+1) + ': '))
            while not melds[i].valid_meld():
                invalid()
                melds[i].tiles = str(input('Meld ' + str(i+1) + ': '))
            melds[i].suit_meld()
            melds[i].type_meld()
            if not closed:
                melds[i].closed_meld()

        std_pair.tiles = str(input("Enter pair: "))
        while not std_pair.valid_pair():
            invalid()
            std_pair.tiles = str(input("Enter pair: "))

        hand = [melds[i].tiles for i in range(4)]
        hand.append(std_pair.tiles)
        print(hand)

        round_wind = evaluate_wind('round_wind')
        print(round_wind)

        personal_wind = evaluate_wind('personal_wind')
        if personal_wind == 'E' or personal_wind == 'EAST':
            dealer = True
        print(personal_wind)
        print(dealer)

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
            if haitei:
                yakuman_counter += 1

        if not rinshan and not chankan and not haitei and not tsumo and (not ippatsu and not double_riichi):
            houtei = evaluate_yn('houtei')

        if not dealer and not riichi and not rinshan and not chankan and not haitei and not houtei and closed and not hand_has_kan:
            if tsumo:
                chiihou = evaluate_yn('chiihou')
                if chiihou:
                    yakuman_counter += 1
            if not tsumo:
                renhou = evaluate_yn('renhou')
                if renhou:
                    yakuman_counter += 1

        if dealer and not riichi and not rinshan and not chankan and not haitei and not houtei and tsumo and closed and not hand_has_kan:
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

                if melds[0].suit == melds[1].suit == melds[2].suit == melds[3].suit == std_pair.suit and closed:
                    if melds[0].suit != 'honor':
                        if chuuren_check():
                            chuuren = True
                            yakuman_counter += 1
                            if wait == '6':
                                chuuren_nine = True
                                yakuman_counter += 1

                if not chuuren:
                    if closed and melds[0].closed == melds[1].closed == melds[2].closed == melds[3].closed == True:
                        if melds[0].meld_type != 'chi' and melds[1].meld_type != 'chi' and melds[2].meld_type != 'chi' and melds[3].meld_type != 'chi':
                            suuankou = True
                            yakuman_counter += 1
                            if wait = '5':
                                suuankou_tanki = True
                                yakuman_counter += 1

                    if shousuushi_check():
                        shousuushi = True
                        yakuman_counter += 1
                    elif daisuushi_check():
                        daisuushi = True
                        yakuman_counter += 2

                if not chuuren:
