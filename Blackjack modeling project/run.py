
from nnf import Var, NNF
from lib204 import Encoding


#Empty Arrays that hold the variables
player_first_card = []
player_second_card = []
player_final_score = []

dealer_first_card = []
dealer_second_card = []
dealer_final_score = []
dealer_hit_value = []
dealer_final_score_hit = []

#Proposition if the dealer stay's
dealer_stay = Var('dealer_stays')

#Card class used in the model
class Card(object):
    def __init__(self, name):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)

#Sets up Variables for card values
for i in range(10):

    pfc = Card(f'player_first_card_{i + 1}')
    psc = Card(f'player_second_card_{i + 1}')

    dfc = Card(f'dealer_first_card_{i + 1}')
    dsc = Card(f'dealer_second_card_{i + 1}')
    dhv = Card(f'dealer_hit_value_{i + 1}')

    player_first_card.append(Var(pfc))
    player_second_card.append(Var(psc))

    dealer_first_card.append(Var(dfc))
    dealer_second_card.append(Var(dsc))
    dealer_hit_value.append(Var(dhv))

#Sets up Variables for final scores
for i in range(30):
    #Initializes variables
    pfs = Card(f'player_final_score_{i + 1}')
    dfs = Card(f'dealer_final_score_{i + 1}')
    dfsh = Card(f'dealer_final_score_{i + 1}')

    #Appends to arrays
    player_final_score.append(Var(pfs))
    dealer_final_score.append(Var(dfs))
    dealer_final_score_hit.append(Var(dfsh))



def my_Theory(player_card_1, player_card_2, dealer_hidden_card, dealer_hit):

    E = Encoding()

    #Values for the card values prior to being converted into boolean values
    player_first_card_int = player_card_1 - 1
    player_second_card_int = player_card_2 - 1
    player_final_score_int = player_first_card_int + player_second_card_int

    dealer_first_card_int = 2
    dealer_second_card_int = dealer_hidden_card
    dealer_hit_value_int = dealer_hit
    dealer_final_score_int = dealer_first_card_int + dealer_second_card_int
    dealer_final_score_hit_int = dealer_final_score_int + dealer_hit_value_int


    #Constraints for cards, only the cards that match the values inputed by the user evaluate to True, the rest must be false
    for i in range(10):
        if i == player_first_card_int:
            E.add_constraint(player_first_card[i])
        else:
            E.add_constraint((player_first_card[i]).negate())

        if i == player_second_card_int:
            E.add_constraint(player_second_card[i])
        else:
            E.add_constraint((player_second_card[i]).negate())

        if i == dealer_first_card_int:
            E.add_constraint(dealer_first_card[i])
        else:
            E.add_constraint((dealer_first_card[i]).negate())

        if i == dealer_second_card_int:
            E.add_constraint(dealer_second_card[i])
        else:
            E.add_constraint((dealer_second_card[i]).negate())

        if i == dealer_hit_value_int:
            E.add_constraint(dealer_hit_value[i])
        else:
            E.add_constraint((dealer_hit_value[i]).negate())

    #Constraints for final card totals, simmilar premise as above
    for i in range(30):
        if i == player_final_score_int:
            E.add_constraint(player_final_score[i])
        else:
            E.add_constraint((player_final_score[i]).negate())

        if i == dealer_final_score_int:
            E.add_constraint(dealer_final_score[i])
        else:
            E.add_constraint((dealer_final_score[i].negate()))

        if i == dealer_final_score_hit_int:
            E.add_constraint(dealer_final_score_hit[i])
        else:
            E.add_constraint((dealer_final_score_hit[i]).negate())

    #Constraints for card totals
    E.add_constraint((player_first_card[player_first_card_int] & player_second_card[player_second_card_int]).negate() | player_final_score[player_final_score_int])
    E.add_constraint((dealer_first_card[dealer_first_card_int] & dealer_second_card[dealer_second_card_int]).negate() | dealer_final_score[dealer_final_score_int])

    #Loop starting from the player final score up till 21
    #Constraint goes from the player's final score up till 21 to ensure that the dealer's
    #score is not between the player's score and 21
    #Includes two scenarios to account if the dealer hit or stayed
    for i in range(player_final_score_int,21):

        E.add_constraint((player_final_score[player_final_score_int] & (dealer_final_score[i]).negate() & dealer_stay) | (player_final_score[player_final_score_int] & (dealer_final_score_hit[i]).negate() & (dealer_stay).negate()))

    #Loop starting from 21 to 30 to make sure the player did not bust
    for i in range(21, 30):
        E.add_constraint((player_final_score[i]).negate())


    #Loop to see if the dealer stay's
    dealer_stay_flag = False
    for i in range(17,21):
        if i == dealer_final_score_int:
            E.add_constraint(dealer_stay)
            dealer_stay_flag = True
            break

    if dealer_stay_flag == False:
        E.add_constraint((dealer_stay).negate())

    return E


if __name__ == "__main__":

    print("Welcome to the blackjack modeling solver, if you input your cards and the visible dealer card\nThis program will tell you the likely hood of you winning")

    player_first_card_value = int(input("Enter the value of your first card: "))
    player_second_card_value = int(input("Enter the value of your second card: "))

    num_win_solutions = 0
    num_loss_solutions = 0

    #We used a differnt method to find the number of solutions that best fit our goal
    for dealer_hidden_card in range(10):
        for dealer_hit_card in range(10):
            theory = my_Theory(player_first_card_value, player_second_card_value, dealer_hidden_card, dealer_hit_card)
            is_satisfiable = theory.is_satisfiable()
            if is_satisfiable == True:
                num_win_solutions += 1
            else:
                num_loss_solutions += 1

    print("Scenarios where you would win: %d" % num_win_solutions)
    print("Scenarios where you would lose: %d" % num_loss_solutions)
    print("You have a %d percent chance of winning this round if you choose to stay" % num_win_solutions)

