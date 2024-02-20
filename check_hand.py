def is_flush(cards):
    is_flush = False
    is_straight_flush = False
    all_suits = [card.suit for card in cards]
    suit_dict = {'Hearts':0, 'Diamonds':0, 'Clubs':0, 'Spades':0}

    for card in cards:
        suit_dict[card.suit] += 1
    for key in suit_dict:
        if suit_dict[key] >=5:
            is_flush = True
            flush_key = key


    # filter all flush cards
    if is_flush:
        effect_cards = []
        for card in cards:
            if card.suit == flush_key:
                effect_cards.append(card)
    print('effective cards are', effect_cards)
    # if straigiht_flush?
    is_straight_flush, max_effect_cards = is_straight(effect_cards)

    # return effective cards

    if is_straight_flush:
        print('Straight Flush!')
        effect_cards = max_effect_cards
    else:
        effect_cards = [card.value for card in effect_cards]
    return is_flush, is_straight_flush, effect_cards


def is_straight(cards):
    is_straight = False
    effect_cards = None
    cards_value_set = []
    for card in cards:
        cards_value_set.append(card.value)
    for straight_set in [['A', '2', '3', '4', '5'],
                        ['2', '3', '4', '5', '6'],
                        ['3', '4','5', '6', '7'],
                        ['4', '5', '6', '7', '8'],
                        ['5', '6', '7', '8', '9'],
                        ['6', '7', '8', '9', '10'],
                        ['7', '8', '9', '10', 'J'],
                        ['8', '9', '10', 'J', 'Q'],
                        ['9', '10', 'J', 'Q', 'K'],
                        ['10', 'J', 'Q', 'K', 'A'],
                        ]:
        if set(straight_set) <= set(cards_value_set):
            is_straight = True
            max_straight = straight_set
    if is_straight:
        print('is strainght, max straight is', max_straight)
        effect_cards = max_straight
    return is_straight, effect_cards


def is_quads(cards):
    pass


def is_full_house(cards):
    pass

def is_three_of_a_kind(cards):
    pass

def is_two_pairs(cards):
    pass

def is_pairs(cards):
    pass

def compare_high_card(cards_1, cards_2):
    pass 





