from fastapi import FastAPI, HTTPException
from web3 import Web3
from web3.exceptions import TransactionNotFound
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Set your provider
w3 = Web3(Web3.HTTPProvider(''))

#Faucet pub and priv key
sender_address = ""
private_key = ""

# Variables for max payout and wait time between payments
MAX_ETH=100
PAST_BLOCKS=25 #5 min

class TransactionData(BaseModel):
    to_address: str
    amount_eth: int

def validate_tx(to_address: str, amount_eth: int):
    if not w3.isConnected():
        raise HTTPException(status_code=500, detail="Web3 connection error")

    if not w3.isAddress(to_address):
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")

    if amount_eth <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    
    if amount_eth > 100:
        raise HTTPException(status_code=400, detail="Amount must be less than 100")
    
    block_number = w3.eth.blockNumber

    #TODO - while in mempool, it allows second transaction to be created
    for block in range(block_number, max(0, block_number - PAST_BLOCKS), -1):
        try:
            transactions = w3.eth.get_block(block)["transactions"]
            for tx_hash in transactions:
                tx = w3.eth.getTransaction(tx_hash)
                if tx.to.lower() == to_address.lower():
                    raise HTTPException(status_code=400, detail="Transaction to this address occurred in the past 25 blocks")
        except TransactionNotFound:
            continue
    

def build_tx(sender_address: str, private_key: str, to_address: str, amount_eth: int):
    amount_wei=w3.toWei(amount_eth, 'ether')
    nonce = w3.eth.getTransactionCount(sender_address)
    gas_price = w3.eth.gasPrice
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': amount_wei,
        'gas': 21000,  
        'gasPrice': gas_price,
    }

    signed_tx = w3.eth.account.signTransaction(tx, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    return tx_hash.hex()

@app.post("/send-eth")
async def send_eth(data: TransactionData):
    try:
        validate_tx(data.to_address, data.amount_eth)
        tx_hash = build_tx(sender_address, private_key, data.to_address, data.amount_eth)

        return JSONResponse(content={"transaction_hash": tx_hash})
    except HTTPException as e:
        raise e

@app.get("/status")
async def check_status():    
    balance=w3.eth.get_balance(sender_address)
    return JSONResponse(content={"Available ETH": balance/1000000000000000000, "Max ETH per tx": MAX_ETH, "Wait period sec": PAST_BLOCKS*12})
# Frontend at root path, change index.html to reflect your settings
@app.get("/")
async def read_root():
    with open("index.html") as f:
        content = f.read()
    return HTMLResponse(content=content)

# Run the FastAPI app
if __name__ == "__main__":
    import uvicornRe
    uvicorn.run(app, host="localhost", port=8100)
