class Helper:

    #limit to one couple of cards

    @staticmethod
    def findSumBetweenCards(cards, pile_card = None):
        #sorted_cards = sorted(cards, key=lambda card: card.getCardValue())
        res = list()
        
        for i in range(len(cards)):

            if len(res) > 0:
                break

            if cards[i].isKing():
                res.append((cards[i], None))
                continue

            if pile_card != None and pile_card.checkSum(cards[i]):
                res.append((pile_card, cards[i]))
                continue

            for j in range(i+1, len(cards)):
                if cards[i].checkSum(cards[j]):
                    res.append((cards[i], cards[j]))

                    #limit to one couple of cards
                    break
            
        return res