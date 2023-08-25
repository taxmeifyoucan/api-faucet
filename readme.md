# ETH API faucet

A simple API for sending funds from a faucet. 

## Faucet

The faucet is publicly deployed for [Ephemery testnet](https://ephemery.dev) at https://api-faucet.bordel.wtf

To deploy your own, change variables in the code and run simply using `python3 main.py`. 


## API usage

#### Recieve testnet funds to your address: 

Sends given amount of ETH to given address. Returns txid.

Route: `/send-eth`

Type: POST

Content:

`to_address":"eth_address",
"amount_eth":amount_in_eth`

cURL example:

`curl -X POST "http://localhost:8000/send-eth" -H "accept: application/json" -H "Content-Type: application/json" -d '{"to_address":"0x1234567890123456789012345678901234567890","amount_eth":10}'`

#### Check status of the faucet:

Returns amount of ETH left in the faucet and its settings.

Route: `/status`

Type: GET

cURL example:

`curl "http://localhost:8000/status`

