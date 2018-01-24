from lib.commons import hash160_from_address, btc_to_satoshis
from lib.elliptic import Curve
from lib.keys import PrivateKey
from lib.transaction import TransactionInput, SpendType, TransactionOutput, Transaction, Script


def create_spend_p2pkh(utxo_tx_hash, utxo_index, utxo_address, utxo_amount_btc, amount_btc, fee_btc, to_address,
                       change_address, private_key):
    if amount_btc > utxo_amount_btc:
        raise RuntimeError("Cannot spend more than it's available in the UTXO")

    if amount_btc < utxo_amount_btc and change_address is None:
        raise RuntimeError("Must provide a change address to spend less than it's available in the UTXO")

    prev_script = Script.OP_DUP + Script.OP_HASH160 + hash160_from_address(utxo_address) + Script.OP_EQUALVERIFY + Script.OP_CHECKSIG

    tx_input = TransactionInput(utxo_tx_hash, utxo_index, prev_script.hex(), SpendType.P2PKH)

    # Outputs
    hash160 = int.from_bytes(hash160_from_address(to_address), 'big')

    tx_output = TransactionOutput(btc_to_satoshis(amount_btc), hash160, SpendType.P2PKH)
    tx_change = TransactionOutput(btc_to_satoshis(utxo_amount_btc - amount_btc - fee_btc), hash160, SpendType.P2PKH)

    tx = Transaction()
    tx.add_inputs(tx_input)
    tx.add_outputs(tx_output, tx_change)

    public_key = Curve().pub_key(private_key)

    signed = tx.sign(private_key, public_key)

    return signed.serialize()


if __name__ == '__main__':
    raw = create_spend_p2pkh("de3cf6dfb752deadbb5f5407538e0dfec0c3e14927c3b46592811ba584fabd30",
                             1,
                             "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4",
                             1.21716322,
                             1,
                             0.0002,
                             "mvHNaj9NDV9RwkFzV6m28M5LJBz7r5vNwQ",
                             "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4",
                             PrivateKey(0x22861a6e8a0670f6388847e83bbea3ed580280b612c11470998baf11ed95d032))

    print(raw.hex())
