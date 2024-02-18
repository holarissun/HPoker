import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, value) for suit in suits for value in values]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def deal_hand(self, num_cards):
        return [self.deal() for _ in range(num_cards)]

# 测试代码
# deck = Deck()
# deck.shuffle()
# print(deck.deal())
# print(deck.deal())

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.folded = False
        self.current_bet = 0  # 当前轮次玩家的下注额
        self.all_in = False

    def bet(self, amount):
        """玩家下注或加注"""
        self.all_in = amount >= self.chips
        bet_amount = min(amount, self.chips)
        self.chips -= bet_amount
        self.current_bet += bet_amount
        return bet_amount

    def fold(self):
        """玩家弃牌"""
        self.folded = True
    def __repr__(self):
        return f"Player({self.name}, Chips: {self.chips}, Hand: {self.hand})"

class HandRanking:
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

class PokerHand:
    def __init__(self, cards):
        self.cards = cards
        self.rank = self.evaluate_hand()

    def evaluate_hand(self):
        ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                 '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        sorted_cards = sorted(self.cards, key=lambda card: ranks[card.value])

        # 检查同花顺或同花
        if self.is_flush(sorted_cards):
            if self.is_straight(sorted_cards):
                return HandRanking.STRAIGHT_FLUSH
            return HandRanking.FLUSH
        
        # 检查葫芦
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            return HandRanking.FULL_HOUSE

        # 检查顺子
        if self.is_straight(sorted_cards):
            return HandRanking.STRAIGHT

        # 检查其他牌型
        rank_counts = self.get_rank_counts(sorted_cards)
        if 4 in rank_counts.values():
            return HandRanking.FOUR_OF_A_KIND
        if 3 in rank_counts.values():
            if 2 in rank_counts.values():
                return HandRanking.FULL_HOUSE
            return HandRanking.THREE_OF_A_KIND
        if len(rank_counts) == 2:
            return HandRanking.TWO_PAIR
        if 2 in rank_counts.values():
            return HandRanking.PAIR

        return HandRanking.HIGH_CARD

    def is_flush(self, cards):
        first_suit = cards[0].suit
        return all(card.suit == first_suit for card in cards)

    def is_straight(self, cards):
        return all(cards[i].value == cards[i - 1].value + 1 for i in range(1, len(cards)))

    def get_rank_counts(self, cards):
        rank_counts = {}
        for card in cards:
            rank_counts[card.value] = rank_counts.get(card.value, 0) + 1
        return rank_counts

    def compare_with(self, other_hand):
        if self.rank > other_hand.rank:
            return 1
        elif self.rank < other_hand.rank:
            return -1
        else:
            # 如果等级相同，需要进一步比较
            return 0

def determine_winner(players):
    best_hand = None
    winning_player = None
    for player in players:
        if player.folded:
            continue
        player_hand = PokerHand(player.hand + game.community_cards)
        if best_hand is None or player_hand.compare_with(best_hand) == 1:
            best_hand = player_hand
            winning_player = player
    return winning_player


class PokerGame:
    def __init__(self, players):
        self.players = [player for player in players if player.chips > 0]
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0

    def start_game(self):
        if len(self.players) < 2:
            print("Not enough players to start the game.")
            return

        self.deck.shuffle()

        # 发两张手牌给每位玩家
        for player in self.players:
            player.hand = self.deck.deal_hand(2)

        # Pre-flop
        self.betting_round()

        # 发公共牌
        self.flop()  # flop
        self.display_game_state()
        self.betting_round()
        self.turn()  # turn 
        self.display_game_state()
        self.betting_round()
        self.river()  # river
        self.display_game_state()
        self.betting_round()

        # 胜负判定和奖池分配（待实现）
        winning_player = determine_winner(self.players)
        winning_player.chips += self.pot
        print(f"{winning_player.name} wins {self.pot} chips with {PokerHand(winning_player.hand + self.community_cards)}")
        
        

    def betting_round(self):
        current_bet = 0
        is_new_bet = True
        while is_new_bet:
            is_new_bet = False
            for player in self.players:
                if player.chips == 0 or player.folded:
                    continue

                print(f"Current highest bet: {current_bet}. {player.name}'s turn.")
                player_decision = input(f"{player.name}, do you want to 'call', 'raise', or 'fold'? ")

                if player_decision == 'fold':
                    player.fold()
                    print(f"{player.name} has folded.")
                elif player_decision == 'call':
                    bet_amount = player.bet(current_bet - player.current_bet)
                    self.pot += bet_amount
                    print(f"{player.name} called with {bet_amount}, current pot is {self.pot}.")
                elif player_decision == 'raise':
                    try:
                        raise_amount = int(input("Enter your raise amount: "))
                        if raise_amount <= 0 or raise_amount + current_bet > player.chips:
                            print("Invalid raise amount, try again.")
                            continue
                        total_bet = current_bet - player.current_bet + raise_amount
                        bet_amount = player.bet(total_bet)
                        current_bet += raise_amount
                        self.pot += bet_amount
                        is_new_bet = True
                        print(f"{player.name} raised to {current_bet}, current pot is {self.pot}.")
                    except ValueError:
                        print("Invalid input, please enter a number.")
                        continue
                else:
                    print("Invalid action, please choose 'call', 'raise', or 'fold'.")
                    continue

    def flop(self):
        # 发前三张公共牌
        self.community_cards.extend(self.deck.deal_hand(3))

    def turn(self):
        # 发第四张公共牌
        self.community_cards.append(self.deck.deal())

    def river(self):
        # 发第五张公共牌
        self.community_cards.append(self.deck.deal())

    def display_game_state(self):
        print("\n--- Game State ---")
        print(f"Community Cards: {self.community_cards}")
        print(f"Pot: {self.pot}")
        for player in self.players:
            print(f"{player.name}: Chips: {player.chips}, Hand: {player.hand if not player.folded else 'Folded'}")
        print("------------------\n")

# 创建玩家
players = [Player("Alice", 1000), Player("Bob", 800), Player("Charlie", 0)]

# 创建并开始游戏
game = PokerGame(players)
game.start_game()

