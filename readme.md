# Online Tic-Tac-Toe

* This game is built in Python using Sockets, Pygame and Tkinter, Playsound libraries
* There are two files in this repository, one is the master file while the other is slave file. The master acts as the server and the slave acts as the client here.
* One user must have the maste file and the other must have the slave file. One who has the master file, his IP address must be on both files
* The IP Address on both of these files MUST be the same

### Details on Server
* If both users are on the same network, then any user can use their local IP address on both scripts and it will work locally
* For internet communication, either a Static Public ID is needed or service like Zero-Tier can be used. Using Zero-Tier a virtual local network can be created and both clients can join the virtual network. Then the IP assigned by Zero-Tier can be used in the scripts. No other modifications ar necessary
