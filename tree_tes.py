# root
#  |
#  - Department
#       |
#       - Foods
#           |
#           - Product ID

# Node Class
import pickle, os

FILENAME = 'kroger_tree.pkl'

class Node:
    def __init__(self, name):
        self.name = name
        self.childern = []  # Needs to be instance variable
    
    # Checks for Duplicates
    def add_child(self, child): 
        print(f"trying to add {child}")

        # Only adds if not found in list
        if not child in list(map(str, self.childern)):  # Must be like this bc they aren't String (nodes)
            self.childern.append(child)
            print(f"{child} was added.\n")
        else:
            print("Child already entered")

    def __str__(self) -> str:
        return self.name


    def child_search(self, child):
        for item in self.childern:  # If this works, change add_child()
            if child.lower() == item.data:
                return item
            
            
    def printTree(self, level=0):
        print(' ' * 4 * level + '-> ' + self.name)

        if len(list(map(str, self.childern))) > 0:
            for child in self.childern:
                child.printTree(level + 1)


# Creates a brand new tree and empties the departments
def root_init():
    root = Node('root')
    print(f"{root}, has been created\n")

    DEPARTMENTS = {"fresh_fruit": [],
                   "fresh_vegetable": [],
                   "meat": [],
                   "seafood": [],
                   "deli": [],
                   "bakery": [],
                   "pantry": [],
                   "dairy_eggs": [],
                   "frozen": [],
                   "beverages": [],
                   "candy": [],
                   "canned_packaged": [],
                   "general": []}

    for item in DEPARTMENTS.keys():
        root.add_child(Node(item))
    return root

def add_food(food, department, root):
    root[department].add_child(Node(food.lower()))

def add_product_ID(product_ID, food, root, department=None):
    if department is None:
        for dep in root:
            if dep.child_search(food).__str__() == food:
                department = dep

    try:
        food.add_child(product_ID)
    except:
        print(f"Error {department} or {food} not found")

if __name__ == '__main__':
    kroger_tree = None

    if os.path.exists(FILENAME):
        with open(FILENAME,'rb') as file:   # Read binary
            kroger_tree = pickle.load(file)

    else:
       kroger_tree = root_init()
 
    with open(FILENAME, 'wb') as file:  # Write binary
        pickle.dump(kroger_tree, file)

    kroger_tree.printTree()
    

        

