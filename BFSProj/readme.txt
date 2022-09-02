breadth first search
maze shortest path finder


how to use:
there must exist a .txt file named maze to read in from the same folder.
maze must consist of...
- for open spaces
x for walls
s for start
f for finish

to use program, maze file must fit these criteria
1. width and height are uniform, no missing pieces
2. no extrenuous characters
3. there must be atleast one path between the s and f.

how it works
the program uses a user defined linked list and a queue to keep track of current paths.
the program will explore a given maze in all open directions (open meaning no wall, edge, or already traveled to path)
once the program hits the final destination, the shortest path is marked by the symbol "0".
