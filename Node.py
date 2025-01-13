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