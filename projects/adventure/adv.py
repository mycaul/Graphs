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
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
directions = {"n":"s", "s":"n", "e":"w", "w":"e"}
path = []
visited = {}

# start in room 0 and has all exits
# { 0: {'n': '?', 's': '?', 'w': '?', 'e': '?'} }
visited[player.current_room.id] = player.current_room.get_exits()

# while there are rooms remaining
while len(visited) < len(room_graph) - 1:
        # add room to visited dict and the exits it has access to
        # previous exit would be the last one in the stack
        # remove the previous direction so that it is not visited again

    if player.current_room.id not in visited:
        visited[player.current_room.id] = player.current_room.get_exits()
        prev_dir = path[-1]
        visited[player.current_room.id].remove(prev_dir)

    # if exits do not lead to any new rooms
    while len(visited[player.current_room.id]) == 0:
        # grab the direction that was just visited and remove it from the path
        # add that direction to the traversal path
        # player can now go in this direction

        prev_dir = path.pop()
        traversal_path.append(prev_dir)
        player.travel(prev_dir)

    # remove the exit from the visited dict
    # add the direction to the traversal path
    # find the opposite direction and add that direction to the path
    # player moves in exit direction
    exit = visited[player.current_room.id].pop(0)
    traversal_path.append(exit)
    path.append(directions[exit])
    player.travel(exit)

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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")