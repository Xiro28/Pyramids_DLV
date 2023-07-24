class Helper:

    #limit to one couple of cards

    @staticmethod
    def findSumBetweenCards(cards, pile_card = None):

        #privilege kings and high level cards
        sorted_cards = sorted(cards, key=lambda card: card.getCardValue() + card.getLevel(), reverse=True)

        res = list()

        if pile_card != None:
            if pile_card.isKing():
                return [(pile_card, None)]
        
        for i in range(len(sorted_cards)):

            if len(res) > 0:
                return res

            if sorted_cards[i].isKing():
                res.append((sorted_cards[i], None))
                return res

            #privilege cards on table
            for j in range(len(sorted_cards)-1, -1, -1):
                if sorted_cards[i].checkSum(sorted_cards[j]):
                    res.append((sorted_cards[i], sorted_cards[j]))

                    #limit to one couple of cards
                    return res

            if pile_card != None and pile_card.checkSum(sorted_cards[i]):
                res.append((pile_card, sorted_cards[i]))
                return res
            
        return res