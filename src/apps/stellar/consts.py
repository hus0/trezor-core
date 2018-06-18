from trezor.messages import wire_types
from micropython import const

STELLAR_CURVE = 'ed25519'
TX_TYPE = bytearray('\x00\x00\x00\x02')

# source: https://github.com/stellar/go/blob/3d2c1defe73dbfed00146ebe0e8d7e07ce4bb1b6/xdr/Stellar-transaction.x#L16
# Inflation not supported see https://github.com/trezor/trezor-core/issues/202#issuecomment-393342089
op_codes = {
    'StellarAccountMergeOp': const(8),
    'StellarAllowTrustOp': const(7),
    'StellarBumpSequenceOp': const(11),
    'StellarChangeTrustOp': const(6),
    'StellarCreateAccountOp': const(0),
    'StellarCreatePassiveOfferOp': const(4),
    'StellarManageDataOp': const(10),
    'StellarManageOfferOp': const(3),
    'StellarPathPaymentOp': const(2),
    'StellarPaymentOp': const(1),
    'StellarSetOptionsOp': const(5),
}

op_wire_types = [
    wire_types.StellarAccountMergeOp,
    wire_types.StellarAllowTrustOp,
    wire_types.StellarBumpSequenceOp,
    wire_types.StellarChangeTrustOp,
    wire_types.StellarCreateAccountOp,
    wire_types.StellarCreatePassiveOfferOp,
    wire_types.StellarManageDataOp,
    wire_types.StellarManageOfferOp,
    wire_types.StellarPathPaymentOp,
    wire_types.StellarPaymentOp,
    wire_types.StellarSetOptionsOp,
]

# https://github.com/stellar/go/blob/e0ffe19f58879d3c31e2976b97a5bf10e13a337b/xdr/xdr_generated.go#L584
ASSET_TYPE_NATIVE = const(0)
ASSET_TYPE_ALPHANUM4 = const(1)
ASSET_TYPE_ALPHANUM12 = const(2)

# https://www.stellar.org/developers/guides/concepts/accounts.html#balance
# https://github.com/stellar/go/blob/3d2c1defe73dbfed00146ebe0e8d7e07ce4bb1b6/amount/main.go#L23
AMOUNT_DIVISIBILITY = const(7)

# https://github.com/stellar/go/blob/master/network/main.go
NETWORK_PASSPHRASE_PUBLIC = 'Public Global Stellar Network ; September 2015'
NETWORK_PASSPHRASE_TESTNET = 'Test SDF Network ; September 2015'

# https://www.stellar.org/developers/guides/concepts/accounts.html#flags
FLAG_AUTH_REQUIRED = const(1)
FLAG_AUTH_REVOCABLE = const(2)
FLAG_AUTH_IMMUTABLE = const(4)
FLAGS_MAX_SIZE = 7

# https://github.com/stellar/go/blob/e0ffe19f58879d3c31e2976b97a5bf10e13a337b/xdr/Stellar-transaction.x#L275
MEMO_TYPE_NONE = 0
MEMO_TYPE_TEXT = 1
MEMO_TYPE_ID = 2
MEMO_TYPE_HASH = 3
MEMO_TYPE_RETURN = 4

# https://github.com/stellar/go/blob/3d2c1defe73dbfed00146ebe0e8d7e07ce4bb1b6/xdr/xdr_generated.go#L156
SIGN_TYPE_ACCOUNT = const(0)
SIGN_TYPE_PRE_AUTH = const(1)
SIGN_TYPE_HASH = const(2)


def get_op_code(msg) -> int:
    if msg.__qualname__ not in op_codes:
        raise ValueError('Stellar: op code unknown')
    return op_codes[msg.__qualname__]
