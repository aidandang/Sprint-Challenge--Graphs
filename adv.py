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
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
    # while the queue is not empty
    while stack.size() > 0:
        current_room = stack.pop()

        if current_room.id not in visited:
            visited[current_room.id] = {}
            for e in current_room.get_exits():
                visited[current_room.id][e] = '?'
                stack.push(current_room.get_room_in_direction(e))
           
    return visited

def main(starting_room):
    graph = dft(starting_room)
    stack = Stack()
    stack.push(starting_room)
    current_path = Stack()
    back_path = Queue()
    moves = []
    
    # while the stack is not empty
    while stack.size() > 0:
        current_room = stack.pop()
        is_next_room = False
        for direction in current_room.get_exits():
            if graph[current_room.id][direction] == '?':
                current_path.push([current_room, direction])
                moves.append(direction)
                stack.push(current_room.get_room_in_direction(direction))
                graph[current_room.id][direction] = current_room.get_room_in_direction(direction).id
                if direction == 'n':
                    graph[current_room.get_room_in_direction(direction).id]['s'] = current_room.id
                if direction == 's':
                    graph[current_room.get_room_in_direction(direction).id]['n'] = current_room.id
                if direction == 'w':
                    graph[current_room.get_room_in_direction(direction).id]['e'] = current_room.id
                if direction == 'e':
                    graph[current_room.get_room_in_direction(direction).id]['w'] = current_room.id
                is_next_room = True
                break
        if is_next_room is False:
            is_closest = False
            # print(current_path.size())
            while current_path.size() > 0 and is_closest is False:
                closest_room_to_explore = current_path.pop()
                # print(closest_room_to_explore[0].id)
                back_path.enqueue(add_room_to_back_path(closest_room_to_explore))
                
                for d in closest_room_to_explore[0].get_exits():
                    if graph[closest_room_to_explore[0].id][d] == '?':
                        stack.push(closest_room_to_explore[0])
                        while back_path.size() > 0:
                            b = back_path.dequeue()
                            moves.append(b[1])
                        is_closest = True
            

    return moves

def get_direction_from_room(graph, room, next_room_id):
    for d in room.get_exits():
        if graph[room.id][d] == next_room_id:
            return d
    return None

def add_room_to_back_path(current_room):
    d = current_room[1]
    if d == 'n':
        return [current_room, 's']
    if d == 's':
        return [current_room, 'n']
    if d == 'w':
        return [current_room, 'e']
    if d == 'e':
        return [current_room, 'w']
    return None

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = main(world.starting_room)

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
