#
# This program creates a Deck of Cards
#

from collections import namedtuple
from random import choice

# What is the card composed of? A card is made up of a rank and suit
Card = namedtuple('Card',['rank', 'suit'])

class FrenchDeck: 
	# create an array of cards regardless of the suit
	ranks = [str(n) for n in range(2,11)] + ['Jack','Queen','King','Ace']
	#ranks = [str(n) for n in range(2,11)] + list('JQKA')

	# create an array of suits regardless of the cards
	suits = 'spades hearts diamonds clubs'.split()

	suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
	
	def spades_high(card):
		rank_index = FrenchDeck.ranks.index(card.rank)
		return rank_index * len(suit_values) + suit_values[card.suit]

	# initialize cards in the constructor
	def __init__(self):
		self._cards = [Card(r, s) 	for r in self.ranks
									for s in self.suits]

	# return length of the deck
	def __len__(self):
		return len(self._cards)

	# returns an item from the deck
	def __getitem__(self, index):
		return self._cards[index]

	def __str__(self):
		return "Deck contains: %s" % '\n'.join([str(card) for card in self._cards])

if __name__ == '__main__':
	new_deck = FrenchDeck()

	# deck responds to the len() function
	print ('I bought a new deck of cards. It has %i cards in it'  % len(new_deck))

	random_card = choice(new_deck)
	print ('A random card is: %s of %s' % (random_card.rank, random_card.suit))
	
	# reading specific cards is possible because of the __getitem__ api
	last_card = new_deck[-1].rank + ' of ' + new_deck[-1].suit
	first_card = new_deck[0].rank + ' of ' + new_deck[0].suit
	print ('Last card in the deck is "%s" and first card is "%s"' % (last_card , first_card))

	# slicing is possible with deck thanks to __getitem__
	top_3_cards = new_deck[:3]
	print ('Top 3 cards in the deck are %s' % [str(card) for card in top_3_cards])

	picking_aces = new_deck[12::13]
	print ('Picking the aces in the deck: %s' % [str(ace) for ace in picking_aces])

	# deck is iterable thanks to __getitem__
	print ('Here is the entire deck:')
	for card in new_deck:
		print card

	# If a collection has no __contains__ method, the in operator does a sequential scan
	queen_of_hearts = Card('Queen', 'Hearts')
	print ('Does the deck contain %s: %s' % (queen_of_hearts, queen_of_hearts in new_deck))

	joker = Card('Joker', '')
	print ('Does the deck contain %s: %s' % (joker, joker in new_deck))

	for card in sorted(new_deck, key=new_deck.spades_high):
		print card