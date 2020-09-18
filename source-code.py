# Import necessary modules
import random
import time
import os
import sys

def getOpponent():
    '''
    Function to print opponent selection menu and ask the user for input.
    Choosing 1 will return True, which means the game will run player vs AI.
    Choosing 2 will return False, the game will run player vs player.
    :return: Boolean value
    '''
    print('=' * 30)
    print('''SELECT OPPONENT
    1. Play against CPU
    2. Play against human opponent''')
    print('=' * 30)

    while True:
        option = askIntegerRange('Select an option: ', 1, 2)
        if option == 1:
            return True
        elif option == 2:
            return False
        else:
            print('ERROR: Invalid option')

def getGameMode():
    '''
    Function to get the game mode. There are two game modes available.
    Normal, where the winner is the player that removes remaining items, and
    Misere, the opposite of normal mode. The last player to move is the loser.
    Will return False if the user chooses to play in normal mode, True otherwise.
    Choosing 3 from the menu will stop the program
    :return: Boolean value for game mode
    '''
    print('=' * 30)
    print('''WELCOME TO THE GAME OF NIM!
    SELECT GAME MODE
    1. Normal - The last player to remove wins
    2. Misere - The last player to remove loses
    3. Quit''')
    print('=' * 30)

    while True:
        option = askIntegerRange('Select an option: ', 1, 3)
        if option == 1:
            return False
        elif option == 2:
            return True
        elif option == 3:
            sys.exit(0)
        else:
            print('ERROR: Invalid option')

def askPlayAgain():
    '''
    Function to print and ask to the user whether the user want to play again or not.
    Will return True or False based on the user input. If the input is 1, return True.
    Otherwise, return False.
    :return: Boolean value. True if input is 1, False if input is 2
    '''
    print('''Do you wish to play again?
    1. Yes
    2. No''')
    option = askIntegerRange('Enter an option: ', 1, 2)
    if option == 1:
        return True
    else:
        return False

def askIntegerRange(prompt, min, max):
    '''
    Function to ask the user for an integer input within range min and max.
    Will keep asking the user until the input is valid.
    Invalid input is when the input is not an integer or out of range.
    :param prompt: The prompt messsage to ask the user
    :param min: The minimum integer value this function accepts
    :param max: The maximum integer value this function accepts
    :return: The validated user input
    '''
    while True:
        try:
            result = int(input(prompt))
            if result < min or result > max:
                raise ValueError
            return result
        except ValueError:
            print('ERROR: Invalid input.')
            print('Your number must be between ' + str(min) + ' and ' + str(max) + ' inclusive.')

def generateHeaps(min, max):
    '''
    Procedure to generate random amount of heaps and items for each heap.
    The number of heap is random from min to max piles, and
    the number of items in each heap is random from 2N+1 to 2N+5
    :param min: The minimum number for the random generated number
    :param max: The maximum number for the random generated number, exclusive
    :return: The generated heap including all items inside each heaps
    '''
    heapAmount = random.randrange(2, 6)    # Randomly generate 2-5 piles
    itemsEachHeap = []                     # Empty list to store the number of items each heap

    # Randomly generate the number of items each heap
    for i in range(heapAmount):
        if i == 0:
            itemsEachHeap.append(1)
        else:
            itemsEachHeap.append(2 * (i) + 1)

    return itemsEachHeap

def printHeaps(heaps):
    '''
    Procedure to print all heaps and items inside each heaps.
    :param heaps: The heaps to print
    :return: nothing
    '''
    print('-' * 30)
    print('Number of piles: ' + str(len(heaps)) + ' || Total items: ' + str(sum(heaps)))
    for i in range(len(heaps)):
        print('Heap #' + str(i + 1) + ': ' + str(heaps[i]) + ' items')
    print('-' * 30)

def removeItems(heaps, heapIndex, itemAmount):
    '''
    Procedure to remove items from a selected heap heapIndex.
    The amount of items to be removed is determined by itemAmount.
    :param heaps: The heaps for the items to be removed
    :param heapIndex: The specific heap for the items to be removed
    :param itemAmount: The amount of items to be removed
    :return: nothing
    '''
    heaps[heapIndex] -= itemAmount

def printWinner(playerMoveState, misereMode):
    '''
    Procedure to announce the winner of the game.
    If playerMoveState is True, that means the last move was made by CPU. Hence, the CPU won the game.
    Otherwise, this procedure will announce that the player won the game.
    :param playerMoveState: Current player move state, from player1ToMove
    :param misereMode: The game mode
    :return:nothing
    '''
    player1 = 'PLAYER 1'
    player2 = 'PLAYER 2'
    if vsBot:
        player2 = 'The CPU'

    print('=' * 15 + 'GAME RESULT' + '=' * 15)
    if playerMoveState:
        print(player2 + ' took all remaining items!')
        if misereMode:
            print(player1 + ' has won the game.')
        else:
            print(player2 + ' has won the game.')
    else:
        print(player1 + ' took all remaining items!')
        if misereMode:
            print(player2 + ' has won the game.')
        else:
            print(player1 + ' has won the game.')
    print('=' * 41)

def getNimSum(heaps):
    '''
    Function to calculate the Nim sum of current item configuration
    for all heaps. This method is used for the AI opponent to calculate
    a good move.
    :param heaps: The heaps for this method to get the Nim sum
    :return: The Nim sum of the passed heaps
    '''
    heapAmount = len(heaps)         # Get the amount of heaps
    nimSum = heaps[0] ^ heaps[1]    # Get the Nim sum for the first two heaps

    # If there are more than three heaps, calculate Nim sum for heap #3 and more
    if heapAmount > 2:
        i = 2
        while i < heapAmount:
            nimSum = nimSum ^ heaps[i]
            i += 1

    # Return the calculated Nim sum
    return nimSum

def selectRandomHeap(heaps, exclude):
    '''
    Function to select a heap randomly. At the end of this function, the index
    of the selected heap is returned. This function will only return
    a heap that is not empty or a heap that is not in excluded list
    :param heaps: The heaps to be selected
    :param exclude: List that prevent this function from returning index included in this list
    :return: The selected heap index
    '''
    # The bot will choose a random heap and random amount of items to be removed
    # This validOption list stores the available heap for the bot to choose
    validOption = [i for i in range(len(heaps))]
    heapIndex = -1

    # Keep looping until the chosen heap is a valid heap (not an empty heap)
    while True:
        # Pick a random number between 0 and the amount of elements in validOption
        index = random.randrange(0, len(validOption))
        heapIndex = validOption[index]
        if heaps[heapIndex] == 0 or heapIndex in exclude:
            validOption.remove(heapIndex)  # If the chosen heap is empty, remove the option from validOption
        else:
            break  # If the chosen heap is not empty, break the loop

    # Return the index of chosen heap that is not empty
    return heapIndex

def decideBotMove(heaps, misereMode):
    '''
    This function is the brain of the AI opponent. This function will return the index of heap selected
    and the amount of items to be removed from the selected heap. The decisions are based on the Nim sum.
    This method will try to find a move that makes the Nim sum of the current configuration to 0.
    If it is impossible to get Nim sum of 0 after the AI opponent's move, then the AI will move randomly.
    :param heaps: The heaps for the AI opponent to decide
    :param misereMode: If the game is running in Misere mode, decision will be adjusted
    :return: The index of selected heap, the amount of item to be removed from the selected heap
    '''
    selectHeap = selectRandomHeap(heaps, [])    # Select a random heap. No exclusion
    selectItemAmount = -1                       # -1 is just a placeholder. Will be changed below


    if getNimSum(heaps) == 0:   # If the current Nim sum is 0, the bot is in disadvantage
        selectItemAmount = random.randrange(1, heaps[selectHeap] + 1)   # Select random amount of items to be removed
    else:   # If the current Nim sum does not equal to 0, this method will find a move that makes it 0
        attempted = []                                                  # List to store attempted bad heap choice
        emptyHeaps = [i for i in range(len(heaps)) if heaps[i] == 0]    # List to store indices of empty heaps
        heapIndices = [i for i in range(len(heaps)) if i != 0]          # List to store indices of heaps that are not empty
        nonEmptyHeaps = len(heaps) - len(emptyHeaps)                    # Variable to store the number of heaps that are not empty

        # If there are only 1 item in all heaps, remove the whole heap randomly
        if nonEmptyHeaps == sum(heaps):
            selectHeap = selectRandomHeap(heaps, emptyHeaps)
            selectItemAmount = 1    # Only 1 as there is only 1 item left in the heap

        while selectItemAmount == -1:
            if not misereMode:
                for i in range(heaps[selectHeap]):
                    tempHeaps = heaps.copy()        # Temporary heaps for checking Nim sum after moving
                    tempHeaps[selectHeap] -= i + 1  # Remove i + 1 items from tempHeaps at index selectHeap
                    if getNimSum(tempHeaps) == 0:   # Checks if after removing the items in tempHeaps makes the Nim sum 0
                        selectItemAmount = i + 1    # If yes, then assign i + 1 to selectItemAmount. It will be returned later
                        break                       # Break the while loop as a good move has been found (Nim sum == 0)
                if selectItemAmount == -1:                          # If this check is executed, that means no good move exist in selected heap
                    attempted.append(selectHeap)                    # Add the selected heap to attempted list
                    selectHeap = selectRandomHeap(heaps, attempted) # Choose a new heap. Excluding the previous selected heap
            else:
                # A list that stores indices of heaps that has only 1 item
                singleItemHeaps = [i for i in range(len(heaps)) if heaps[i] == 1]
                if nonEmptyHeaps == 1:
                    selectItemAmount = heaps[selectHeap] - 1
                elif nonEmptyHeaps == 2:
                    if len(singleItemHeaps) == 1:
                        if heaps[selectHeap] == 1:
                            attempted.append(selectHeap)
                            selectHeap = selectRandomHeap(heaps, attempted)
                        selectItemAmount = heaps[selectHeap]
                    else:
                        selectItemAmount = heaps[selectHeap] - (heaps[selectHeap] - 1)
                else:
                    if nonEmptyHeaps == 3 and len(singleItemHeaps) == 2:
                        selectHeap = selectRandomHeap(heaps, singleItemHeaps)
                        selectItemAmount = heaps[selectHeap] - 1
                    else:
                        for i in range(heaps[selectHeap]):
                            tempHeaps = heaps.copy()        # Temporary heaps for checking Nim sum after moving
                            tempHeaps[selectHeap] -= i + 1  # Remove i + 1 items from tempHeaps at index selectHeap
                            if getNimSum(tempHeaps) == 0:   # Checks if after removing the items in tempHeaps makes the Nim sum 0
                                selectItemAmount = i + 1    # If yes, then assign i + 1 to selectItemAmount. It will be returned later
                                break                       # Break the while loop as a good move has been found (Nim sum == 0)
                        if selectItemAmount == -1:                          # If this check is executed, that means no good move exist in selected heap
                            attempted.append(selectHeap)                    # Add the selected heap to attempted list
                            selectHeap = selectRandomHeap(heaps, attempted) # Choose a new heap. Excluding the previous selected heap

    # Return the index of selected heap and the amount of items to be removed from the selected heap
    return selectHeap, selectItemAmount

# Constants
HEAP_MIN = 2   # The minimum amount of heaps
HEAP_MAX = 5   # The maximum amount of heaps

play = True    # If this is True, then the game will run. Otherwise, the game will not run

while play:
    misereMode = getGameMode()                      # If this is False, the game will run in normal mode
    vsBot = getOpponent()                           # If this is False, the game will run for player 1 and player 2
    heaps = generateHeaps(HEAP_MIN, HEAP_MAX + 1)   # Generate random amount of heaps and random amount of items
    player1ToMove = random.choice([True, False])    # Random boolean value. If True, it's player 1's turn to move

    # The game will keep running until there is no item left in all heaps
    while sum(heaps) > 0:
        heapToRemove = -1       # -1 is just placeholder. Will be removed by input
        itemAmountRemove = -1   # Same as the above
        printHeaps(heaps)       # Print current heaps
        currentTurn = ''

        if player1ToMove:    # If player1ToMove is True, it's player 1's turn to move
            currentTurn = 'PLAYER 1'
            print('*' + currentTurn + '\'s TURN!*')
            while True:
                heapToRemove = askIntegerRange('Select heap (1-' + str(len(heaps)) + '): ', 1, len(heaps)) - 1
                if heaps[heapToRemove] <= 0:
                    print('ERROR: You can\'t select an empty pile!')
                else:
                    break
            itemAmountRemove = askIntegerRange(
                'Select the amount of item to be removed (1-' + str(heaps[heapToRemove]) + '): ', 1,
                int(heaps[heapToRemove]))
        else:               # If player1ToMove is False, it's CPU or Player 2 to move, depends on vsBot
            if vsBot:
                currentTurn = 'CPU'
                print('*' + currentTurn + '\'s TURN!*')
                heapToRemove, itemAmountRemove = decideBotMove(heaps, misereMode)
            else:
                currentTurn = 'PLAYER 2'
                print('*' + currentTurn + '\'s TURN!*')
                while True:
                    heapToRemove = askIntegerRange('Select heap (1-' + str(len(heaps)) + '): ', 1, len(heaps)) - 1
                    if heaps[heapToRemove] <= 0:
                        print('ERROR: You can\'t select an empty pile!')
                    else:
                        break
                itemAmountRemove = askIntegerRange(
                    'Select the amount of item to be removed (1-' + str(heaps[heapToRemove]) + '): ', 1,
                    int(heaps[heapToRemove]))

        clear = lambda: os.system('cls')
        clear()
        removeItems(heaps, heapToRemove, itemAmountRemove)                                           # Remove items from heap
        print('// ' + currentTurn + ' REMOVED ' + str(itemAmountRemove) + ' ITEMS FROM HEAP #' + str(heapToRemove + 1))  # Confirm removed items
        if player1ToMove:
            player1ToMove = False   # If player1ToMove is currently True, change it to false
        else:
            player1ToMove = True    # The opposite of above

    printWinner(player1ToMove, misereMode)   # At this point, there are no items left. The game ends
    play = askPlayAgain()                    # Ask whether the user want to have another game