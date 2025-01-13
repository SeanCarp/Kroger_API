import os
import time
import pickle

# Node Class
class Node:
    def __init__(self, data):
        self.data = data
        self.childern = []

    def add_child(self, child): # Checks for Duplicates
        print(f"trying to add {child}")

        if not child in list(map(str, self.childern)):
            self.childern.append(child)
            print(f"{child} was added.\n")
        else:
            print("Child already entered")

    def child_search(self, child):
        for item in self.childern:
            if child.lower() == item.__str__():
                return item
        

# Root Initialization
def root_init():
    root = Node('root')
    print(f"{root}, has been created\n")

    global NODES, DEPARTMENTS
    NODES = {}
    DEPARTMENTS = {"fresh_fruit": ["apples", "bananas", "oranges", "berries", "managos"],
                    "fresh_vegetable": ["carrots", "spinach", "broccoli", "bell_peppers", "tomatoes"],
                    "meat": [], 
                    "seafood": [], 
                    "deli": [], 
                    "bakery": [], 
                    "pantry": [],
                    "dairy_eggs": [],
                    "frozen": [], 
                    "organic": [], 
                    "beverages": [], 
                    "candy": [], 
                    "canned_packaged": [], 
                    "general": []}
    for item in DEPARTMENTS:    # Creates the childern for root
        NODES[item] = Node(item.lower())
        root.add_child(NODES[item])
    return root


# Department Updator function
def update_departments(food_list, department):
    for item in food_list:          
        NODES[department].add_child(Node(item.lower()))
    print(f"{department}, has been updated")

def add_food(food, department):
    NODES[department].add_child(Node(food.lower()))
    print(f"{food} was added to {department}")

def add_product_ID(product_ID, food, department=None): # 
    if department is None:
        for dep in root:
            if dep.child_search(food).__str__() == food:
                department = dep

    try:
        food.add_child(product_ID)
    except:
        print(f"Error {department} or {food} not found")


def kroger_Tree():
    start_time = time.time()


    FILENAME = 'kroger_data.pkl'
    kroger_tree = None

    # Check if the file exists and it is not empty
    if os.path.exists(FILENAME) and os.path.getsize(FILENAME) > 0:
        with open(FILENAME, 'rb') as file:  # 'rb' for reading binary
            kroger_tree = pickle.load(file)

        for item in kroger_tree.childern:
            for food in item.childern:
                for product_ID in food.childern:
                    print(product_ID)

    else:
        global root
        root = root_init()
        update_departments(DEPARTMENTS["fresh_fruit"], "fresh_fruit")
        update_departments(DEPARTMENTS["fresh_vegetable"], "fresh_vegetable")   

        with open('kroger_data.pkl', 'wb') as file:
            pickle.dump(root, file)


    print("Everything done")
    print(f"Completed in {time.time()-start_time} sec")









if __name__ == '__main__':
    kroger_Tree()

