states = []

def add_state(state):
    global states
    states.append(round(state, 5))

def get_stats():
    return states
