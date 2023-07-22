class Helper:

    #limit to one couple of cards

    @staticmethod
    def findSumBetweenCards(cards, pile_card = None):
        #privilege kings
        sorted_cards = sorted(cards, key=lambda card: card.getCardValue(), reverse=True)

        res = list()

        if pile_card != None:
            if pile_card.isKing():
                return [(pile_card, None)]
        
        for i in range(len(sorted_cards)):

            if len(res) > 0:
                break

            if sorted_cards[i].isKing():
                res.append((sorted_cards[i], None))
                continue

            if pile_card != None and pile_card.checkSum(sorted_cards[i]):
                res.append((pile_card, sorted_cards[i]))
                continue

            for j in range(i+1, len(sorted_cards)):
                if sorted_cards[i].checkSum(sorted_cards[j]):
                    res.append((sorted_cards[i], sorted_cards[j]))

                    #limit to one couple of cards
                    break
            
        return res