from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)
# player.travel('s')
# player.travel('w')
# print('DIRECTIONS AVAILABLE TO MOVE', player.current_room.get_exits())
# print('ID OF ROOM =', player.current_room.id)


#What am I trying to do?
    #Fill traversal path that when walked in order will visit every room on the map at least once
    #Fill list with valid traversal directions
    #Pick a random direction -> travel -> log direction -> loop
    #If you hit a deadend -> backtrack(need way to reverse direction) to nearest room with unexplored paths

#You may find the commands `player.current_room.id`, `player.current_room.get_exits()` and `player.travel(direction)` useful.
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

#get_exits
#
traversal_path = []
graph = {}

#bfs needs to be modified
#bfs can be part
# player will reach a dead end
#no avilable directions
#or already visited room
#backtrack
#shortest path from dead end to nearest rooom with available directions to explore
#current rooom updates
#is the potential room already in the graph set

def bfs(starting_node): #1
    # Build the graph
    # Do a BFS (storing the path)
    qq = Queue()
    qq.enqueue([starting_node]) #1
    visted = set()

    while qq.size() > 0:
        path = qq.dequeue()
        vertex = path[-1]
        # If the path is longer or equal and the value is smaller, or if the path is longer)
        if vertex not in visted:
            visted.add(vertex)

# {
#   0: {'n': '?', 's': 5, 'w': '?', 'e': '?'},
#   5: {'n': 0, 's': '?', 'e': '?'}
# }
            #DO THE THING
            for i in graph[vertex]:
                if graph[vertex][i] == '?':
                    return path

                    #loop thru all values in graph[path[-1]]
            for neighbor in graph[vertex]:
                adjacent_room = graph[vertex][neighbor]
                path_copy = path.copy()
                path_copy.append(adjacent_room)
                qq.enqueue(path_copy)
    return None

def opposite(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'
        #init direction to look like this 
        #{ 0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}
#Does the length of graph equal 500 yet?
    #init room_exit
while len(graph) != len(world.rooms):
    #init current to current room ID
    current = player.current_room.id
    #init room exit to None
    room_exit = None

    #Is the current room ID in graph={}?
    if player.current_room.id not in graph:
        #No? insert the room ID as the key and init all the exits that are returned from the get_exits with a value of '?' becuase we don't yet know what rooms are attached to those exits until we navigate through them
        graph[player.current_room.id] = {i: '?' for i in player.current_room.get_exits()}

    #For all directions available to travel e.g. 0:{'n':'?','s': '?'}
    for direction in graph[current]:
        #If value of any of the directions out of the current room is '?'
        if graph[current][direction] == '?':
            #set room_exit to that direction
            room_exit = direction
            
            #is room_exit valid?
            if room_exit is not None:
                #add that exit to the traversal path
                traversal_path.append(room_exit)
                #move the player to that exit
                player.travel(room_exit)
                #Is the current room ID in graph={}?
                if player.current_room.id not in graph:
                #No? insert the room ID as the key and init all the exits that are returned from the get_exits with a value of '?' becuase we don't yet know what rooms are attached to those exits until we navigate through them
                    graph[player.current_room.id] = {
                        i: '?' for i in player.current_room.get_exits()
                    }

            graph[current][room_exit] = player.current_room.id
            graph[player.current_room.id][opposite(room_exit)] = current
            current = player.current_room.id
            break

    traveral_of_map = bfs(player.current_room.id)

    if traveral_of_map is not None:
        for room in traveral_of_map:
            for direction in graph[current]:
                if graph[current][direction] == room:
                    traversal_path.append(direction)
                    player.travel(direction)
            
            current = player.current_room.id

        
    
























# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
