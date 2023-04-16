import hashlib
import json

import algosdk
from algosdk.v2client import algod
from beaker import sandbox


def mintNFT(algod_client, creator_address, creator_private_key, asset_name, asset_unit_name):
    #...
    
    sp = algod_client.suggested_params()
    txn = algosdk.transaction.AssetConfigTxn(
        sender=creator_address,
        sp=sp,
        default_frozen=False,
        unit_name=asset_unit_name,
        asset_name=asset_name,
        manager=creator_address,
        reserve=creator_address,
        freeze=creator_address,
        clawback=creator_address,
        url="ipfs:://QmZHYWFzTrndsmcy1YeuFNf8Ff9YzysoPz6Su39zW8cFii#arc3",
        total=1,
        decimals=0,
    )

    stxn = txn.sign(creator_private_key)
    # Send the transaction to the network and retrieve the txid.
    txid = algod_client.send_transaction(stxn)
    print(f"Sent asset create transaction with txid: {txid}")
    # Wait for the transaction to be confirmed
    results = algosdk.transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

    # grab the asset id for the asset we just created
    created_asset = results["asset-index"]
    print(f"Asset ID created: {created_asset}")
    return created_asset  #your confirmed transaction's asset id should be returned instead


def transferNFT(algod_client, creator_address, creator_private_key, receiver_address, receiver_private_key, asset_id):

    opting(algod_client, receiver_address, receiver_private_key, asset_id)

    sp = algod_client.suggested_params()
    # Create transfer transaction
    xfer_txn = algosdk.transaction.AssetTransferTxn(
        sender=creator_address,
        sp=sp,
        receiver=receiver_address,
        amt=1,
        index=asset_id,
    )
    signed_xfer_txn = xfer_txn.sign(creator_private_key)
    txid = algod_client.send_transaction(signed_xfer_txn)
    print(f"Sent transfer transaction with txid: {txid}")

    results = algosdk.transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

    #

    pass

def opting(algod_client, receiver_address, receiver_private_key, asset_id):
        sp = algod_client.suggested_params()
        # Create opt-in transaction
        # asset transfer from me to me for asset id we want to opt-in to with amt==0
        optin_txn = algosdk.transaction.AssetOptInTxn(
            sender=receiver_address, sp=sp, index=asset_id
        )
        signed_optin_txn = optin_txn.sign(receiver_private_key)
        txid = algod_client.send_transaction(signed_optin_txn)
        print(f"Sent opt in transaction with txid: {txid}")

        # Wait for the transaction to be confirmed
        results = algosdk.transaction.wait_for_confirmation(algod_client, txid, 4)
        print(f"Result confirmed in round: {results['confirmed-round']}")
