import json
import hashlib
import requests
import sys
import json

#Need to hook up the miner for in wallet mining, wallet is working though
def proof_of_work(last_block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    """
    block_string = json.dumps(last_block, sort_keys=True)

    """
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """

    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    return proof
    # return proof



def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string + proof) contain 3
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"  # increase this to increase mining time aka finding the hash
    # return True or False


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    coins_mined = 0 # Placed by me so it does not reset to 0
    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        # new_proof = ???
        new_proof = proof_of_work(data['last_block'])

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        #  If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  variable made above

        if data['message'] == 'Yay you mined/forged a new block':
            coins_mined += 1
            print(f'{coins_mined} coins mined')
        else:
            # print the message from the server.
            print(data['message'])




#Just like the adventure game, terminal selection
#Not doing it in android/kotlin as it was too difficult for me, this needs work though
def main():
    data = load_data()
    if "id" not in data:
        id = input("Please, enter an id:")
        data["id"] = id
    else:
        print(f"Welcome {data['id']}")

    while True:
        menu = [
            "Pick one",
            "*Check Balance: 1",
            "*Manage Transactions: 2",
            "*Change ID: 3",
        ]
        for item in menu:
            print(item)
        option = input()

        if option == "3":
            id = input("Enter New ID:")
            data["id"] = id

        elif option == "2":
            print(f"Your balance is {data['balance']}")
        elif option == "1":
            menu = [
                "Choose an Option",
                "*See your Transactions: 1",
                "*Send a Transaction: 2",
            ]
            for item in menu:
                print(item)
            option = input()

            if option == "1":
                print(data["transactions"])

            elif option == "2":
                to = input("Input name of the person you are sending coins to")
                amount = int(input("How much are you sending?"))
                transaction = {"from": data["id"], "to": to, "amount": amount}
                data["balance"] -= amount

                data["transactions"].append(transaction)

        save_data(data)

def load_data():
    with open("json_cache.py") as f:
        data = json.load(f)
    return data


def save_data(data):
    file = open("json_cache.py", "w")
    file.write(str(json.dumps(data)))
    file.close()
main()
