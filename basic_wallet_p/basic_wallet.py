import json
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
