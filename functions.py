import math

def point_distance(x, y, a, b):
    sdx = (a - x)**2
    sdy = (b - y)**2
    dist = math.sqrt(sdx + sdy)
    return dist

def point_direction(x, y, a, b):
    dx = a - x
    dy = b - y
    deg = math.atan2(-dy, dx)
    return math.degrees(deg)

def sign(a):
    if a == 0:
        return 0
    return abs(a) / a

def flood_fill(x, y, arr, num, touched_ind):
    # Implement BFS
    queue = [(x, y)]
    visited = set()

    if num == touched_ind:
        return

    while queue:
        cx, cy = queue.pop(0)
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        if 0 <= cx < len(arr[0]) and 0 <= cy < len(arr) and arr[cy][cx] == touched_ind:
            arr[cy][cx] = num

            queue.append((cx + 1, cy))
            queue.append((cx - 1, cy))
            queue.append((cx, cy + 1))
            queue.append((cx, cy - 1))