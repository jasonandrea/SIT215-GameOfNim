# Import necessary modules
import random
import time
import os

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
    itemsEachHeap = []              # Empty list to store the number of items each heap

    # Randomly generate the number of items each heap
    for i in range(heapAmount):
        itemsEachHeap.append(random.randrange(2 * heapAmount + 1, 2 * heapAmount + 5))

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

def printWinner(playerMoveState):
    '''
    Procedure to announce the winner of the game.
    If playerMoveState is True, that means the last move was made by CPU. Hence, the CPU won the game.
    Otherwise, this procedure will announce that the player won the game.
    :param playerMoveState: Current player move state, from playerToMove
    :return:nothing
    '''
    print('=' * 15 + 'GAME RESULT' + '=' * 15)
    if playerMoveState:
        print('The CPU took all remaining items!')
        print('CPU has won the game.')
    else:
        print('You took all remaining items!')
        print('You have won the game.')
    print('=' * 41)

HEAP_MIN = 2   # The minimum amount of heaps
HEAP_MAX = 5   # The maximum amount of heaps

heaps = generateHeaps(HEAP_MIN, HEAP_MAX + 1)   # Generate random amount of heaps and random amount of items
playerToMove = random.choice([True, False])     # Random boolean value. If True, the player move first

while sum(heaps) > 0:
    heapToRemove = -1       # -1 is just placeholder. Will be removed by input
    itemAmountRemove = -1   # Same as the above
    printHeaps(heaps)       # Print current heaps

    if playerToMove:    # If playerToMove is True, it's player's turn to move
        print('*YOUR TURN!*')
        while True:
            heapToRemove = askIntegerRange('Select heap (1-' + str(len(heaps)) + '): ', 1, len(heaps)) - 1
            if heaps[heapToRemove] <= 0:
                print('ERROR: You can\'t select an empty pile!')
            else:
                break
        itemAmountRemove = askIntegerRange('Select the amount of item to be removed (1-' + str(heaps[heapToRemove]) + '): ', 1, int(heaps[heapToRemove]))
        playerToMove = False    # Change playerToMove to False, so the next turn will be the CPU's turn
    else:               # If playerToMove is False, it's CPU's turn to move
        print('*CPU\'s TURN!*')
        time.sleep(1)           # A little delay so the game does not run too fast
        while True:
            heapToRemove = random.randrange(0, len(heaps))
            if heaps[heapToRemove] <= 0:
                print('ERROR: You can\'t select an empty pile!')
            else:
                break
        itemAmountRemove = random.randrange(1, heaps[heapToRemove] + 1)
        playerToMove = True     # Change playerToMove to True, so the next turn will be the player's turn

    removeItems(heaps, heapToRemove, itemAmountRemove)                                           # Remove items from heap
    print('// REMOVED ' + str(itemAmountRemove) + ' ITEMS FROM HEAP #' + str(heapToRemove + 1))  # Confirm removed items

printWinner(playerToMove)   # At this point, there are no items left. The game ends
