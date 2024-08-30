# I need to figure out the more about the API Calls and when to use 
# refresh tokens

import os
import pickle
import requests
import kroger_TREE

# Replace with your actual values
AUTHORIZATION = os.getenv("AUTHORIZATION")
headers_1 = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic " + AUTHORIZATION
}

SCOPE = os.getenv("SCOPE")
data = {
    "grant_type": "client_credentials",
    "scope": SCOPE
}


#################################
#   FUNCTIONS
#################################
def load_token():
    """ Reads the loaded token and makes sure that will not error

    Returns:
        binary: The brand new token"""
    if os.path.exists(FILENAME) and os.path.getsize(FILENAME) > 0:
        with open(FILENAME, 'rb') as file: # 'rb' reading binary
            return pickle.load(file)
        
    return "Empty_String"    
    
def refresh_token():
    """ Gets a new token to try

    Returns:
        binary: The new token
    """

    URL = os.getenv("URL")
    response = requests.post(URL, headers=headers_1, data=data)

    # Checks if the request was successful (status code 200)
    if response.status_code == 200:
        token_data = response.json()

        # Extract and use the access token as needed
        access_token = token_data.get("access_token")
        print("Expires in ", token_data.get("expires_in"))
    else:
        print(f"Error: {response.status_code}")
        return


    # Save the file as pickle (binary file)
    with open('access_token.pkl', 'wb') as file:
        pickle.dump(access_token, file)

    return access_token

def get_store_num(header_, area_code=26505):
    """This method returns the closest store number for given area_code
    
    Args:
        header_ (map):      The Authorization code for API calls
        area_code (int):    The area code to look for, default Morgantown, WV
        
    Returns:
        int: The closest store number"""
    
    # Make the Location API request
    store_num_message = requests.get(f'https://api-ce.kroger.com/v1/locations/?filter.zipCode.near={area_code}', headers=header_)
    if store_num_message.status_code == 200:
        data = store_num_message.json()
    
        for item in data.get('data'): # Returns the closest one
            store_num = item.get('locationId')
            print(item.get("name"), store_num)
            return store_num
    
    raise Exception(f"Location API Error: {store_num_message.status_code}")

def product_search(header_, store_number, search_term, limit=10):
    """This method returns the list of items that were match in the Kroger catelog
       If it errors out it raises an exception.
    
    Args:
        header_(map):       The Authorization code for API calls
        store_number(str):  The Kroger Store Number for lookup
        search_term(str):   The item that the User wants to search for
        limit(int):         The maximum number of items that can be returned
        
    Returns:
        list:       Contains all of the item_data that matches the item search"""
    search_message = requests.get(f'https://api-ce.kroger.com/v1/products?filter.term={search_term}&\
                               filter.locationId={store_number}&filter.limit={limit}', headers=header_)
    if search_message.status_code == 200:
        data2 = search_message.json()

        for item in data2.get('data'):
            print('Product ID:', item.get("productId"))
            print('Description:', item.get("description"))
            #print('Items:', item.get("items"))
            #print(item.get('images'))
            print()

        print("Items found:", len(data2.get('data')))
        return data2.get('data')

    raise Exception(f"Product SEARCH API ERROR: {search_message.status_code}")

def product_details(header_, product_id):
    detail_message = requests.get(f"https://api-ce.kroger.com/v1/products/{product_id}", headers=header_)
    if detail_message.status_code == 200:
        return detail_message.json().get("data")
    
    raise Exception(f"Product DETAILS API ERROR: {detail_message}")
        
    


#################################
# Main run
#################################
if __name__ == '__main__':
    """ So instead of re-entering the authorization everytime,
    it saves a token for 300sec (5 mins).
    """
    FILENAME = 'access_token.pkl'
    access_token = load_token()

    # Product Data
    bearer_header = {
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }

    # Since this is the first api call it the only API call that typically fails
    try:
        store_num = get_store_num(bearer_header)
    except:
        bearer_header["Authorization"] = "Bearer " + refresh_token()
        store_num = get_store_num(bearer_header)


    #################################
    # Building of Kroger Tree
    #################################
    kroger_tree = None
    TREE_FILE = 'kroger_data.pkl'
    if os.path.exists(TREE_FILE) and os.path.getsize(TREE_FILE) > 0:
        with open(TREE_FILE, 'rb') as file:
            kroger_tree = pickle.load(file)
    else:
        print('No tree found! Making new one now!')

        # Make new Kroger Tree

    for department in kroger_tree.childern:
        for food in department.childern:
            flag_ = True
            print(f"_______{food} (ID)_____ (n to go to next item)")

            while(flag_):
                product_id = input("------:")
                if product_id == "q":
                    flag_ = False
                    break

                try: 
                    product_details(bearer_header, store_num, product_id)
                    kroger_TREE.add_product_ID(product_id, food, department)
                except:
                    print("The product ID was invalid")

            if not flag_:
                break


    what_he_said = input("What would you like to SEARCH for\n")
    print(type(product_search(bearer_header, store_num, what_he_said)))


