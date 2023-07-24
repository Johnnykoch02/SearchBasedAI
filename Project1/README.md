### HOW TO USE ###

1. Download and Unzip Source Code,
2. cd into the project directory (this is where Assignment1.py is located),
3. Edit the test file such that each row of numbers entered follow this format: Starting Node, Ending Node, Vertex Weight
ex. a row entered: 3, 4, 2 corresponds to creating a link from node ID 3 to node ID 4 and has a weight of 2.

# For developers:

4. Once the desired graph has been entered into the text file, locate line 156 which should be the first line of the main function
5. Modify the Argument being passed in as a reference to the file as a string where that file is located either locally to the repository or a global reference on the Computing Device

### NOTE: This only applies to users who are using a separate file than that provided in the project. ###

6. run program command: python Assignment1.py
7. The program will ask for a starting node and ending node. Based on the file data provided, the program will output the corresponding paths between the starting node and ending node, including 0 if the starting node is the same as the ending node, and 
infinity if the path does not exist.
8. Since the main loop will continue indefinetly, to quit the program enter CTRL+C

### Jonathan Koch U25318998
