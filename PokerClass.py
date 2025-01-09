'''
Ibrahim Ijaduola 12/18/24
This class creates a deck of 52 Cards and deals out 5 hands of 5 cards to 5 players.
The program then ranks each hand that the player recieved and orders them from greatest to least.
'''

### Class for Creating a card (AS = Ace of Spades)
import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    # def for returning rank of card
    def printRank(self):
        return f"{self.rank}"
    
    # def for returning suit of card
    def printSuit(self):
        return self.suit
    
    
    # def for printing a card
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
class Deck:
    def __init__(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["H", "D", "C", "S"]

        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
    
    # def for shuffling cards in decks
    def shuffle(self):
        random.shuffle(self.cards)

    # def for drawing a card
    def drawCard(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            return None
    
    # def for dealing cards
    def dealCards(self, numCards):
        return [self.drawCard() for _ in range(numCards) if len(self.cards) > 0]

        
    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        # Creating a list of strings for each card and join them
        cardList = [str(card) for card in self.cards]

        # Grouping the cards in rows of 13
        groupCardList = [", ".join(cardList[i:i+13]) for i in range(0, len(cardList), 13)]
        return f" Deck with {len(self.cards)} cards remaining:\n" + "\n".join(groupCardList)
    

### Class for creating a player 
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    # adds list of cards to the end of the players hand (which is a list)
    def getCards(self, cards):
        self.hand.extend(cards)
    
    # def for showing a players hand (string representation)
    def showHand(self):
        return f"{self.name}'s hand: " + ", ".join(str(card) for card in self.hand)
    

## Class for ranking each hand
class RankHand:
     # defining rank values for the hands
    def __init__(self):
        self.rankValues = {str(i): i for i in range(2, 11)}
        self.rankValues.update({"J": 11, "Q": 12, "K": 13, "A": 14})

    # def for defining a straight
    def isStraight(self, values):
        values = sorted(values)
        if all(values[i] + 1 == values[i + 1] for i in range(len(values) - 1)):
            return True
        
        # checking for a low ace straight (1, 2, 3, 4, 5)
        if values == [2, 3, 4, 5, 14]:
            return True
        return False


    ## def for ranking a hand
    def evaluateHand(self, hand):
        values = sorted([self.rankValues[card.rank] for card in hand], reverse=True)
        suits = [card.suit for card in hand]


        # rank = Flush if all the suits in the hand are the same
        isFlush = len(set(suits)) == 1

        # rank = Straight if all values are consecutive
        isStraight = self.isStraight(values)

        ## Counting occurances of each rank
        valueCounts = {v:values.count(v) for v in set(values)}

        ## Determining hand type
        if isFlush and isStraight and set([10, 11, 12, 13, 14]).issubset(values):
            return (10, "Royal Straight Flush", values)

        if isFlush and isStraight:
            return (9, "Straight Flush", values)
        elif 4 in valueCounts.values():
            return (8, "Four of A Kind", values)
        elif sorted(valueCounts.values()) == [2,3]:
            return (7, "Full House", values)
        elif isFlush:
            return (6, "Flush", values)
        elif isStraight:
            return (5, "Straight", values)
        elif 3 in valueCounts.values():
            return (4, "Three of A Kind", values)
        elif list(valueCounts.values()).count(2) == 2:
            return (3, "Two Pair", values)
        elif 2 in valueCounts.values():
            return(2, "Pair", values)
        else:
            return(1, f"High Card: {max(values)}", values) # Returns the highest valued card
        
    ### Ranks the hands of the players and returns a sorted list
    def rankHands(self, players):
        rankedPlayers = [(player, self.evaluateHand(player.hand)) for player in players]
        rankedPlayers.sort(key=lambda x: (x[1][0], x[1][2]), reverse=True)
        return rankedPlayers
        

    
        

####################################
print(f"P O K E R  H A N D  A N A L Y Z E R")
print(f"*************************************")
deck = Deck()
print(deck)
deck.shuffle()
print("\nShuffled Deck\n")
print(deck)
print("\n")

#hand = [Card("2", "S"), Card("3", "H"), Card("A", "D"), Card("4", "H"), Card("5", "D")]
#testRanker = RankHand()
#newhandRank, newdescription = testRanker.evaluateHand(hand)
#print(f"{newdescription}")

numOfPlayers = 5
players = [Player(f"Player{i+1}") for i in range(numOfPlayers)]
for player in players:
    player.getCards(deck.dealCards(5))

for player in players:
    print(player.showHand())
    print("\n")


# Ranking the hands of each player
print(f"H A N D  R A N K S")

suitRank = {"S": 4, "H": 3, "C": 2, "D": 1}

ranker = RankHand()

rankedPlayers = [(player, ranker.evaluateHand(player.hand)) for player in players]
rankedPlayers.sort(key=lambda x: 
                   (x[1][0], x[1][2], [ranker.rankValues[card.rank] for card in sorted(x[0].hand, key=lambda card: suitRank[card.suit], reverse= True)]), reverse = True)

for player, handRank in rankedPlayers:
    print(player.showHand())
    print(f"{handRank[1]}")
    print()

'''for player in players:
    print(player.showHand())
    handRank = ranker.evaluateHand(player.hand)
    print(f"{handRank[1]}")
    print()
'''
#ranker = RankHand()
#rankedPlayers = ranker.rankHands(players)
#for player, (rank, description) in rankedPlayers:
    #handStr = ", ".join(str(card) for card in player.hand)
    #print(f"{player.name}: {player.hand}\n {description}")
