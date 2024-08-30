import os
import requests
import pickle
import kroger_TREE as cum
from kroger_TREE import Node

# Replace with your actual values

url = "https://api-ce.kroger.com/v1/connect/oauth2/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic " + AUTHORIZATION
}
data = {
    "grant_type": "client_credentials",
    "scope": SCOPE
}


def refresh_token(): # Returns the new token if needed
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        token_data = response.json()

        # Extract and use the access token as needed
        access_token = token_data.get("access_token")
        print("Expires in ", token_data.get("expires_in"))
    else:
        print(f"Error: {response.status_code}")

    # Save the file as a pickle
    with open('access_token.pkl', 'wb') as file:
        pickle.dump(access_token, file)

    return access_token


def get_store_num(headers, area_code=26505):
    """ This method returns the closest store number for given area_code
    
    Args:
        headers (map):      The Authorization code for API calls
        area_code (int):    The area code to look for, default Morgantown, WV
        
    RETURNS:
        int: The closest store number"""
    

    # Make the Location API request
    message = requests.get(f'https://api-ce.kroger.com/v1/locations/?filter.zipCode.near={area_code}', headers=headers)
    if message.status_code == 200:
        data = message.json()
    else:
        print(f"Location API Error: {message.status_code}")
        return

    for item in data.get('data'):
        store_num = item.get('locationId')
        print(item.get("name"), store_num)
        return store_num


def product_search(headers, store_number, search_term, limit=10):
    second_part = requests.get(f"https://api-ce.kroger.com/v1/products?filter.term={search_term}&\
                               filter.locationId={store_number}&filter.limit={limit}", headers=headers)
    if second_part.status_code == 200:
        data2 = second_part.json()
    else:
        print(f"Error: {second_part.status_code}")
        return

    for item in data2.get('data'):
        print('Product ID:',item.get("productId"))
        print('Description:', item.get("description"))
        #print('Items:', item.get("items"))
        #print(item.get('images'))
        print()
    print(len(data2.get('data')))
    return data2.get('data')

def id_check(headers, store_number, product_id):
    response = requests.get(f"https://api-ce.kroger.com/v1/products/{product_id}?filter.locationId={store_number}", headers=headers)
    return response.status_code == 200
     

if __name__ == '__main__':
    FILENAME = 'access_token.pkl'
    access_token = ""

    # Product Data
    headers2 = {
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }


    # Check if the file exists and it is not empty
    if os.path.exists(FILENAME) and os.path.getsize(FILENAME) > 0:
        with open(FILENAME, 'rb') as file: # 'rb' for reading binary
            acess_token = pickle.load(file)

    try:
        get_store_num(headers2)
    except:
        access_token = refresh_token()

    store_num = get_store_num(headers2)

####################################

    # Bring in kroger_data.pkl
    kroger_tree = None
    FILENAME2 = 'kroger_data.pkl'
    if os.path.exists(FILENAME2) and os.path.getsize(FILENAME2) > 0:
        with open(FILENAME2, 'rb') as file:
            kroger_tree = pickle.load(file)
    else:
        print("No tree found!")
        quit()


    for department in kroger_tree.childern:
        for food in department.childern:
            flag = True
            print(f"_________{food} (ID)_________ (q to go to next)")
            
            while(flag):
                product_id = input("-------:")
                if product_id == "q":
                    flag = False
                    break

                # Check if valid product_ID
                if id_check(headers2, store_num, product_id):
                    cum.add_product_ID(product_id, food, department)
                else:
                    print("The product ID was invalid")

            if not flag:
                break

    # Save any updates
    with open('kroger_data.pkl', 'wb') as file:
        pickle.dump(kroger_tree, file)
    print("Kroger_tree updated")