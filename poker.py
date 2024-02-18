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
        self.folded = False  # 表示玩家是否已弃牌
        

    def __repr__(self):
        return f"Player({self.name}, Chips: {self.chips}, Hand: {self.hand})"



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

        # 实施下注轮次
        self.betting_round()

        # 发公共牌
        self.flop()  # 前三张公共牌
        self.betting_round()
        self.turn()  # 转牌（第四张公共牌）
        self.betting_round()
        self.river()  # 河牌（第五张公共牌）
        self.betting_round()

        # 胜负判定和奖池分配（待实现）

    def betting_round(self):
        # 假设最小下注是10筹码
        min_bet = 10
        current_bet = 0
        for player in self.players:
            # 如果玩家筹码为0或已弃牌，则跳过
            if player.chips == 0 or player.folded:
                continue

            # 简化示例：让每个玩家选择跟注或弃牌
            player_decision = input(f"{player.name}, do you want to 'call' or 'fold'? ")
            if player_decision == 'call':
                bet_amount = min(min_bet, player.chips)
                player.chips -= bet_amount
                self.pot += bet_amount
                current_bet = max(current_bet, bet_amount)
                print(f"{player.name} called with {bet_amount}, current pot is {self.pot}")
            elif player_decision == 'fold':
                player.folded = True
                print(f"{player.name} has folded.")

    def flop(self):
        # 发前三张公共牌
        self.community_cards.extend(self.deck.deal_hand(3))

    def turn(self):
        # 发第四张公共牌
        self.community_cards.append(self.deck.deal())

    def river(self):
        # 发第五张公共牌
        self.community_cards.append(self.deck.deal())


# 创建玩家
players = [Player("Alice", 1000), Player("Bob", 800), Player("Charlie", 0)]

# 创建并开始游戏
game = PokerGame(players)
game.start_game()

