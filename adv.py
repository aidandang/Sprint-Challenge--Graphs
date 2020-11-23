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
map_file = "maps/test_loop_fork.txt"
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
    current_path = []
    path = []
    
    # while the stack is not empty
    while stack.size() > 0:
        current_room = stack.pop()
        is_next_room = False
        for direction in current_room.get_exits():
            if graph[current_room.id][direction] == '?':
                current_path.append([current_room, direction])
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
            if len(current_path) > 0:
                for c in current_path:
                    path.append(c[1])

                d = current_path[len(current_path)-1][1]
                if d == 'n':
                    path.append('s')
                if d == 's':
                    path.append('n')
                if d == 'w':
                    path.append('e')
                if d == 'e':
                    path.append('w')
                
                i = len(current_path)
                is_closest = False

                while (i > 0) and (is_closest is False):
                    i = i - 1
                    closest_room_to_explore = current_path[i][0]
                    for d in closest_room_to_explore.get_exits():
                        if graph[closest_room_to_explore.id][d] == '?':
                            stack.push(closest_room_to_explore)
                            current_path = []
                            is_closest = True
                    if is_closest is False:
                        if i > 0:
                            if get_direction_from_room(graph, closest_room_to_explore, current_path[i-1][0].id):
                                path.append(get_direction_from_room(graph, closest_room_to_explore, current_path[i-1][0].id))
                            stack.push(current_path[i-1][0])
                        if i == 0:
                            if get_direction_from_room(graph, closest_room_to_explore, current_room.id):
                                path.append(get_direction_from_room(graph, closest_room_to_explore, current_room.id))
                            stack.push(current_room)
                            current_path = []

    return print(path)

def get_direction_from_room(graph, room, next_room_id):
    for d in room.get_exits():
        if graph[room.id][d] == next_room_id:
            return d
    return None

main(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# def get_path(starting_room):
#     queue = Queue()
#     queue.enqueue({
#         'current_room': starting_room,
#         'path': [starting_room.id]
#     })
#     visited = set()

#     while queue.size() > 0:
#         current_obj = queue.dequeue()
#         current_path = current_obj['path']
#         current_room = current_obj['current_room']

#         if current_room.id not in visited:
#             if len(current_room.get_exits()) == 1:
#                 return current_path

#             visited.add(current_room.id)

#             for e in current_room.get_exits():
#                 new_path = list(current_path)
#                 new_path.append(current_room.get_room_in_direction(e).id)
#                 queue.enqueue({
#                     'current_room': current_room.get_room_in_direction(e),
#                     'path': new_path
#                 })

#     return None   

# def get_connections(current_path, graph):
#     for i in range(len(current_path) - 1):
#         for d in world.rooms[current_path[i]].get_exits():
#             if world.rooms[current_path[i]].get_room_in_direction(d).id == current_path[i+1]:
#                 graph[current_path[i]][d] = current_path[i+1]
#                 if d == 'n':
#                     graph[current_path[i+1]]['s'] = current_path[i]
#                 if d == 's':
#                     graph[current_path[i+1]]['n'] = current_path[i]
#                 if d == 'w':
#                     graph[current_path[i+1]]['e'] = current_path[i]
#                 if d == 'e':
#                     graph[current_path[i+1]]['w'] = current_path[i]

#     return graph

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
