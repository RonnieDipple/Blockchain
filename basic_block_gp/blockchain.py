import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
#tutorial https://www.youtube.com/watch?v=iRZBPDZ71Ak&feature=youtu.be

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block) # Or 'previous_hash': self.hash(self.chain[-1])



        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        string_block = json.dumps(block, sort_keys= True)#sort_keys= True is a flag makes sure all of the keys in the dictionary
        # are turned into a string in A - Z order,
        # if the order changed so would the hash every time we ran the function and we don't want that

        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        raw_hash = hashlib.sha256(string_block.encode())


        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes


        # TODO: Create the block_string

        # TODO: Hash this string using sha256

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        hex_hash = raw_hash.hexdigest()
        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     """
    #     block_string = json.dumps(block, sort_keys=True)
    # 
    #     """
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    # 
    #     proof = 0
    #     while self.valid_proof(block_string, proof) is False:
    #        proof +=1
    #     return proof
    #     # return proof

    @staticmethod
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
        return guess_hash[:6] == "000000" #increase this to increase mining time aka finding the hash
        # return True or False


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # Run the proof of work algorithm to get the next proof
    proof = blockchain.proof_of_work(blockchain.last_block)

    # Forge the new Block by adding it to the chain with the proof
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)


    response = {
        'new_block': block
    }

    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def last_block ():
    response = {
        'last_block': blockchain.last_block
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
       'chain': blockchain.chain,
        'length': len(blockchain.chain)
        # TODO: Return the chain and its current length
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
# Client Miners

# In the initial blockchain demonstration, we've created a small problem.  
# The `mine` endpoint is called on the server, 
# which means we're the ones spending all of the electricity to generate a new block.  
# This won't do at all!
# 
# Furthermore, the amount of work needed to actually mine a block is a bit low.  
# We need it to be harder to preserve the integrity of the chain.


# Task List

# *Server*
# Modify the server we created to:
# * Remove the `proof_of_work` function from the server.
# * Change `valid_proof` to require *6* leading zeroes.
# * Add an endpoint called `last_block` that returns the last block in the chain
# * Modify the `mine` endpoint to instead receive and validate or reject a new proof sent by a client.
#     * It should accept a POST
#     * Use `data = request.get_json()` to pull the data out of the POST
#         * Note that `request` and `requests` both exist in this project
#     * Check that 'proof', and 'id' are present
#         * return a 400 error using `jsonify(response)` with a 'message'
# * Return a message indicating success or failure.  
# Remember, a valid proof should fail for all senders except the first.
# 
# *Client Mining*
# Create a client application that will:
# * Get the last block from the server
# * Run the `proof_of_work` function until a valid proof is found, validating or rejecting each attempt.  
# Use a copy of `valid_proof` to assist.
# * Print messages indicating that this has started and finished.
# * Modify it to generate proofs with *6* leading zeroes.
# * Print a message indicating the success or failure response from the server
# * Add any coins granted to a simple integer total, and print the amount of coins the client has earned
# * Continue mining until the app is interrupted.
# * Change the name in `my_id.txt` to your name
# * (Stretch) Handle non-json responses sent by the server in the event of an error, without crashing the miner
# * Stretch: Add a timer to keep track of how long it takes to find a proof
