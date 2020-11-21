from room import Room
from player import Player
from world import World
from util import Stack, Queue 

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def dft(starting_room):
    stack = Stack()
    visited = {}
    stack.push(starting_room)
    # while the stack is not empty
    while stack.size() > 0:
        current_room = stack.pop()

        if current_room.id not in visited:
            stack.push(current_room)
            visited[current_room.id] = {}
            for e in current_room.get_exits():
                visited[current_room.id][e] = current_room.get_room_in_direction(e).id
                stack.push(current_room.get_room_in_direction(e))

                
    return print(visited)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
dft(world.rooms[0])

traversal_path = []



# TRAVERSAL TEST - DO NOT MODIFY
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
