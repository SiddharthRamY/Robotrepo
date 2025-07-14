def collision_avoidance_lidar(front, left, right):
    safe_distance = 30  # in cm
    critical_distance = 15

    if front < critical_distance and left < critical_distance and right < critical_distance:
        return {"speed": 0, "direction": "stop"}

    if front < safe_distance:
        if left > right:
            return {"speed": 5, "direction": "left"}
        elif right > left:
            return {"speed": 5, "direction": "right"}
        else:
            return {"speed": 3, "direction": "reverse"}

    if left < safe_distance and right >= safe_distance:
        return {"speed": 7.5, "direction": "right"}
    if right < safe_distance and left >= safe_distance:
        return {"speed": 7.5, "direction": "left"}

    if front >= 2 * safe_distance:
        return {"speed": 10, "direction": "forward"}

    return {"speed": 7, "direction": "forward"}
