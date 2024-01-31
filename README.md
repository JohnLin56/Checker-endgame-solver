# Checker-endgame-solver
## Heuristic Description
The heuristic that I tried to implement is to let the king always move first. The rationale behind this heuristic is that the kings have a big advantage over the normal piece because they are able to move backward. This makes them powerful because they can capture the opponent’s pieces from behind. Moreover, the normal pieces that are staying near the base can act as road barricades, capturing the opponent’s pieces that are trying to reach to the home row. Therefore, the purpose of this heuristic is to prevent the opponent’s pieces to become kings and capturing them with the kings.
When implementing this heuristic, I first searched for a list of successors containing moves that are capturing the opponent, and another list of successors that are moving one step to the nearby empty space. The combination of these two lists would be all the possible moves I can make with all the red pieces on the board. I would then sort the two lists based on a specific set of rules:
1. Compare the utility of each successor. The utility is calculated in the same manner as the one suggested in Minimax. The value for a red king is 2, for a red normal piece is 1, for a black king is -2, for a black normal piece is -1. The utility of a board is the sum of all the pieces on the board. So whichever successor can bring the max utility for red or minimum utility for black will be explored by alpha-beta search first.
2. If the two successors have the same utility, then I would compare what piece is being move in each of the successor. If one successor is generated by moving a king, and the other one is generated by moving a normal piece, the former successor would have a higher priority than the latter successor.
3. If both successors have the same utility and they are both generated by moving the same type of chess, then whichever is found first would be explore first, i.e., there is an entry count for them, first come first out.
With this set of rule, moves with capturing will always be executed and explored first, and my heuristic of using the kings to eliminate the enemies will be enforced as well.
