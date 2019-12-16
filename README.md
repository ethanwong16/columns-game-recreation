# columns-game-recreation

This was a project which focused on utilizing Python and the third party library Pygame to recreate a simplified version of the game known as "Columns". 
The game is quite similar to Tetris, as sets of falling Jewels of varying colors need to be rearranged to create matches of 
three or more same-colored Jewels and keep the game board as empty as possible. Once the board becomes overfilled, the game 
ends.

To run the game, please download the user interface and game mechanics modules into the same directory, and run the user interface script.

Game Instructions / Controls:

Overview: The goal of the game is to keep the game board from over-filling with falling Jewel objects by creating matches of three or more same-colored Jewels either vertically, horizontally, or diagonally. Players will operate on a 13x6 grid board, and Jewels will always fall in vertical sets of three randomly selected colors. There are a total of 7 different possible Jewel colors, and the game will end once a set of three Jewels cannot fit completely in any column on the board. Jewels will never fall into columns that cannot fit three or more Jewels unless all columns have been filled, in which case the player has lost.

Controls: Players have three controls they can use.
1) Spacebar Key: This allows players to rotate the orientation of the sets of three jewels while they are still falling or when they have landed but have not yet been "frozen" into a locked position.
2) Right/Left Arrow Key: This allows players to move the sets of three jewels to the right or left.
3) (optional) Down Arrow Key: This allows players to accelerate the falling of the sets of jewels in the downwards direction.

Visual Indicators: 
1) Falling Jewels: While jewels are falling, a light orange-yellow background can be seen behind the falling jewels. 
2) Landed Jewels: When jewels land on top of other jewels or on the bottom of the game board, a green background can be seen behind the jewels. Jewels can still be moved and rotated in this state.
3) Frozen Jewels: When jewels become frozen, they will be enlarged to fit the entire cell and will have no visible background color them. Once jewels are frozen, a new set of falling jewels will be created.
4) Matches: When matches are created, jewels will shrink into small circles before disappearing as an indicator of a match.

The full project was split into two assignments from a course at the University of California, Irvine called ICS32A or Python Programming with Libraries. These two assignments received full scores of 30/30, and the full project specifications can be found at the following two links:

Project Part 1: https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project4/

Project Part 2: https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project5/
