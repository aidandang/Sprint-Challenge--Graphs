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

class Graph:
    def __init__(self, starting_room):
        self.starting_room = starting_room

    def get_moves(self):

        # get graph of all rooms needed to explore
        # all directions with '?' mean the neighbors of these direcions have not been explored
        graph = self.dft(self.starting_room)

        # set a stack of rooms needed to explore, begin with the given starting room
        stack = Stack()
        stack.push(self.starting_room)

        # set a visited path for going back to the closest room needed to explore
        current_path = Stack()

        # set back path to the closest room needed to explore then update to the moves
        back_path = Queue()

        # initiate the moves
        moves = []
        
        # while the stack is not empty, which mean there is still a room to be explored
        while stack.size() > 0:
            # explore rooms in order
            current_room = stack.pop()
            
            # check if any neighbor room has not been yet to explore then add to stack
            # update a visited path for going back to the closest room needed to explore
            # until there is no room to explore
            is_there_next_room_to_explore = False
            for direction in current_room.get_exits():
                if graph[current_room.id][direction] == '?':
                    current_path.push([current_room, direction])
                    moves.append(direction)
                    stack.push(current_room.get_room_in_direction(direction))

                    # update graph bi-directions beetwen current room and next explored room
                    graph[current_room.id][direction] = current_room.get_room_in_direction(direction).id
                    if direction == 'n':
                        graph[current_room.get_room_in_direction(direction).id]['s'] = current_room.id
                    if direction == 's':
                        graph[current_room.get_room_in_direction(direction).id]['n'] = current_room.id
                    if direction == 'w':
                        graph[current_room.get_room_in_direction(direction).id]['e'] = current_room.id
                    if direction == 'e':
                        graph[current_room.get_room_in_direction(direction).id]['w'] = current_room.id
                    
                    # if next explored room is true break the loop to go to that room
                    is_there_next_room_to_explore = True
                    break

            # if there are no rooms to explore then go back to closest room where can be explored. 
            if is_there_next_room_to_explore is False:
                is_closest = False
                while current_path.size() > 0 and is_closest is False:
                    closest_room_to_explore = current_path.pop()
                    back_path.enqueue(self.add_room_to_back_path(closest_room_to_explore))
                    for d in closest_room_to_explore[0].get_exits():
                        if graph[closest_room_to_explore[0].id][d] == '?':
                            stack.push(closest_room_to_explore[0])
                            while back_path.size() > 0:
                                b = back_path.dequeue()
                                moves.append(b[1])
                            is_closest = True              
        # if there is nothing in the stack which means there is no room lelf the return the result
        return moves

    def dft(self, starting_room):
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

    def add_room_to_back_path(self, current_room):
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

# def dft(starting_room):
#     stack = Stack()
#     visited = {}
#     stack.push(starting_room)
#     # while the queue is not empty
#     while stack.size() > 0:
#         current_room = stack.pop()

#         if current_room.id not in visited:
#             visited[current_room.id] = {}
#             for e in current_room.get_exits():
#                 visited[current_room.id][e] = '?'
#                 stack.push(current_room.get_room_in_direction(e))
           
#     return visited

# def main(starting_room):
#     graph = dft(starting_room)
#     stack = Stack()
#     stack.push(starting_room)
#     current_path = Stack()
#     back_path = Queue()
#     moves = []
    
#     # while the stack is not empty
#     while stack.size() > 0:
#         current_room = stack.pop()
#         is_next_room = False
#         for direction in current_room.get_exits():
#             if graph[current_room.id][direction] == '?':
#                 current_path.push([current_room, direction])
#                 moves.append(direction)
#                 stack.push(current_room.get_room_in_direction(direction))
#                 graph[current_room.id][direction] = current_room.get_room_in_direction(direction).id
#                 if direction == 'n':
#                     graph[current_room.get_room_in_direction(direction).id]['s'] = current_room.id
#                 if direction == 's':
#                     graph[current_room.get_room_in_direction(direction).id]['n'] = current_room.id
#                 if direction == 'w':
#                     graph[current_room.get_room_in_direction(direction).id]['e'] = current_room.id
#                 if direction == 'e':
#                     graph[current_room.get_room_in_direction(direction).id]['w'] = current_room.id
#                 is_next_room = True
#                 break
#         if is_next_room is False:
#             is_closest = False
#             # print(current_path.size())
#             while current_path.size() > 0 and is_closest is False:
#                 closest_room_to_explore = current_path.pop()
#                 # print(closest_room_to_explore[0].id)
#                 back_path.enqueue(add_room_to_back_path(closest_room_to_explore))
                
#                 for d in closest_room_to_explore[0].get_exits():
#                     if graph[closest_room_to_explore[0].id][d] == '?':
#                         stack.push(closest_room_to_explore[0])
#                         while back_path.size() > 0:
#                             b = back_path.dequeue()
#                             moves.append(b[1])
#                         is_closest = True
            
#     return moves

# def get_direction_from_room(graph, room, next_room_id):
#     for d in room.get_exits():
#         if graph[room.id][d] == next_room_id:
#             return d
#     return None

# def add_room_to_back_path(current_room):
#     d = current_room[1]
#     if d == 'n':
#         return [current_room, 's']
#     if d == 's':
#         return [current_room, 'n']
#     if d == 'w':
#         return [current_room, 'e']
#     if d == 'e':
#         return [current_room, 'w']
#     return None

# traversal_path = main(world.starting_room)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# traversal_path = []

g = Graph(world.starting_room)
traversal_path = g.get_moves()

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
