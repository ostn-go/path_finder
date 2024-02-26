from flask import Flask, jsonify, request
import numpy as np
import heapq
import time
import json
from collections import deque
import collections


app = Flask(__name__)


def is_valid(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[y][x] != 1

def shortest_path_test(grid, start, end):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1),(1, 1), (-1, -1), (1, -1), (-1, 1)]

    queue = deque([(start[0], start[1], [])])  # Initialize the queue with the start position and path
    visited = set()

    while queue:
        x, y, path = queue.popleft()
        path = path + [(x, y)]  # Update the path with the current coordinates

        if (x, y) == end:
            return path  # We've reached the end, return the path

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if is_valid(new_x, new_y, grid) and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.append((new_x, new_y, path))

    return []


def convert_to_2d(original_list, columns):
    elements_per_column = len(original_list) // columns
    result = [original_list[i:i + elements_per_column] for i in range(0, len(original_list), elements_per_column)]
    return result

# Define a route to receive POST requests with beacon data
@app.route('/pathCoordinates', methods=['POST'])
def process_post_data():
    print("Started operation")
    # Get the JSON data from the POST request
    request_data = request.get_json()
    # Ensure that the request contains a "beacon_data" field
    # if "beacon_data" not in request_data:
    #     return jsonify({"error": "Missing 'beacon_data' field in the request body"}), 400

    start_position = (request_data["xStart"], request_data["yStart"])  # Start position (x, y, floor)
    goal_position = (request_data["xEnd"], request_data["yEnd"],)  # Target position (x, y, floor)

    building = convert_to_2d(request_data["floorData"],request_data["crossAxisCount"])

    shortest_path = shortest_path_test(building, start_position, goal_position)
    print(shortest_path.pop())

    coordinate_list = [{"x": x, "y": y} for x, y in shortest_path]
    json_data = json.dumps(coordinate_list)
    print(json_data)

    return json_data

if __name__ == '__main__':
    app.run(debug=True,port=5000)
