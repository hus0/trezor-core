from apps.stellar.layout import *
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text

from trezor.messages.StellarAccountMergeOp import StellarAccountMergeOp
from trezor.messages.StellarAssetType import StellarAssetType
from trezor.messages.StellarAllowTrustOp import StellarAllowTrustOp
from trezor.messages.StellarBumpSequenceOp import StellarBumpSequenceOp
from trezor.messages.StellarChangeTrustOp import StellarChangeTrustOp
from trezor.messages.StellarCreateAccountOp import StellarCreateAccountOp
from trezor.messages.StellarCreatePassiveOfferOp import StellarCreatePassiveOfferOp
from trezor.messages.StellarManageDataOp import StellarManageDataOp
from trezor.messages.StellarManageOfferOp import StellarManageOfferOp
from trezor.messages.StellarPathPaymentOp import StellarPathPaymentOp
from trezor.messages.StellarPaymentOp import StellarPaymentOp
from trezor.messages.StellarSetOptionsOp import StellarSetOptionsOp
from ubinascii import hexlify


async def confirm_source_account(ctx, source_account: bytes):
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, 'Source account:',
                   ui.MONO, *split(format_address(source_account)),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)


async def confirm_allow_trust_op(ctx, op: StellarAllowTrustOp):
    if op.is_authorized:
        text = 'Allow'
    else:
        text = 'Revoke'
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, text + ' Trust',
                   ui.NORMAL, "of '" + op.asset_code + "' by:",
                   ui.MONO, *split(trim_to_rows(format_address(op.trusted_account), 3)),
                   icon_color=ui.GREEN)

    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)


async def confirm_account_merge_op(ctx, op: StellarAccountMergeOp):
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, 'Account Merge',
                   ui.NORMAL, 'All XLM will be sent to:',
                   ui.MONO, *split(trim_to_rows(format_address(op.destination_account), 3)),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)


async def confirm_bump_sequence_op(ctx, op: StellarBumpSequenceOp):
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, 'Bump Sequence',
                   ui.NORMAL, 'Set sequence to',
                   ui.MONO, str(op.bump_to),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)


async def confirm_change_trust_op(ctx, op: StellarChangeTrustOp):
    if op.limit == 0:
        text = 'Delete'
    else:
        text = 'Add'
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, text + ' Trust',
                   ui.NORMAL, 'Asset: ' + op.asset.code,
                   ui.NORMAL, 'Amount: ' + format_amount(op.limit, ticker=False),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    await confirm_asset_issuer(ctx, op.asset)


async def confirm_create_account_op(ctx, op: StellarCreateAccountOp):
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, 'Create Account',
                   ui.NORMAL, 'with ' + format_amount(op.starting_balance),
                   ui.MONO, *split(trim_to_rows(format_address(op.new_account), 3)),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)


async def confirm_create_passive_offer_op(ctx, op: StellarCreatePassiveOfferOp):
    if op.amount == 0:
        text = 'Delete Passive Offer'
    else:
        text = 'New Passive Offer'
    await _confirm_offer(ctx, text, op)


async def confirm_manage_offer_op(ctx, op: StellarManageOfferOp):
    if op.offer_id == 0:
        text = 'New Offer'
    else:
        if op.amount == 0:
            text = 'Delete'
        else:
            text = 'Update'
        text += ' #' + str(op.offer_id)
    await _confirm_offer(ctx, text, op)


# todo scale? this is inconsistent with T1 (op.amount should? use divisibility)
async def _confirm_offer(ctx, text, op):
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, text,
                   ui.NORMAL, 'Sell ' + str(op.amount) + ' ' + op.selling_asset.code,
                   ui.NORMAL, 'For ' + str(op.price_n / op.price_d),
                   ui.NORMAL, 'Per ' + format_asset_code(op.buying_asset),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    await confirm_asset_issuer(ctx, op.selling_asset)
    await confirm_asset_issuer(ctx, op.buying_asset)


# todo done
async def confirm_manage_data_op(ctx, op: StellarManageDataOp):
    from trezor.crypto.hashlib import sha256
    if op.value:
        text = 'Set'
    else:
        text = 'Clear'
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, text + ' data value key',
                   ui.MONO, *split(op.key),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    if op.value:
        digest = sha256(op.value).digest()
        digest_str = hexlify(digest).decode()
        content = Text('Confirm operation', ui.ICON_CONFIRM,
                       ui.BOLD, ' Value (SHA-256):',
                       ui.MONO, *split(digest_str),
                       icon_color=ui.GREEN)
        await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)


async def confirm_path_payment_op(ctx, op: StellarPathPaymentOp):
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, 'Path Pay ' + format_amount(op.destination_amount, ticker=False),
                   ui.BOLD, format_asset_code(op.destination_asset) + ' to:',
                   ui.MONO, *split(trim_to_rows(format_address(op.destination_account), 3)),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    await confirm_asset_issuer(ctx, op.destination_asset)
    # confirm what the sender is using to pay
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.NORMAL, 'Pay using',
                   ui.BOLD, format_amount(op.send_max, ticker=False),
                   ui.BOLD, format_asset_code(op.send_asset),
                   ui.NORMAL, 'This amount is debited',
                   ui.NORMAL, 'from your account.',
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    await confirm_asset_issuer(ctx, op.send_asset)


async def confirm_payment_op(ctx, op: StellarPaymentOp):
    content = Text('Confirm operation', ui.ICON_CONFIRM,
                   ui.BOLD, 'Pay ' + format_amount(op.amount, ticker=False),
                   ui.BOLD, format_asset_code(op.asset) + ' to:',
                   ui.MONO, *split(trim_to_rows(format_address(op.destination_account), 3)),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    await confirm_asset_issuer(ctx, op.asset)


async def confirm_set_options_op(ctx, op: StellarSetOptionsOp):
    if op.inflation_destination_account:
        content = Text('Confirm operation', ui.ICON_CONFIRM,
                       ui.BOLD, 'Set Inflation Destination',
                       ui.MONO, *split(format_address(op.inflation_destination_account)),
                       icon_color=ui.GREEN)
        await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    if op.clear_flags:
        text = _format_flags(op.clear_flags)
        content = Text('Confirm operation', ui.ICON_CONFIRM,
                       ui.BOLD, 'Clear Flags',
                       ui.MONO, *text,
                       icon_color=ui.GREEN)
        await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    if op.set_flags:
        text = _format_flags(op.set_flags)
        content = Text('Confirm operation', ui.ICON_CONFIRM,
                       ui.BOLD, 'Set Flags',
                       ui.MONO, *text,
                       icon_color=ui.GREEN)
        await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    thresholds = _format_thresholds(op)
    if thresholds:
        content = Text('Confirm operation', ui.ICON_CONFIRM,
                       ui.BOLD, 'Account Thresholds',
                       ui.MONO, *thresholds,
                       icon_color=ui.GREEN)
        await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    if op.home_domain:
        content = Text('Confirm operation', ui.ICON_CONFIRM,
                       ui.BOLD, 'Home Domain',
                       ui.MONO, *split(op.home_domain),
                       icon_color=ui.GREEN)
        await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
    if op.signer_type is not None:
        if op.signer_weight > 0:
            text = 'Add Signer'
        else:
            text = 'Remove Signer'
        if op.signer_type == consts.SIGN_TYPE_ACCOUNT:
            text += ' (acc)'
            content = Text('Confirm operation', ui.ICON_CONFIRM,
                           ui.BOLD, text,
                           ui.MONO, *split(format_address(op.signer_key)),
                           icon_color=ui.GREEN)
            await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
        elif op.signer_type in [consts.SIGN_TYPE_PRE_AUTH, consts.SIGN_TYPE_HASH]:
            if op.signer_type == consts.SIGN_TYPE_PRE_AUTH:
                text += ' (auth)'
            else:
                text += ' (hash)'
            content = Text('Confirm operation', ui.ICON_CONFIRM,
                           ui.BOLD, text,
                           ui.MONO, *split(hexlify(op.signer_key).decode()),
                           icon_color=ui.GREEN)
            await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)
        else:
            raise ValueError('Stellar: invalid signer type')


def _format_thresholds(op: StellarSetOptionsOp) -> ():
    text = ()
    if op.master_weight is not None:
        text += ('Master Weight: ' + str(op.master_weight), )
    if op.low_threshold is not None:
        text += ('Low: ' + str(op.low_threshold), )
    if op.medium_threshold is not None:
        text += ('Medium: ' + str(op.medium_threshold), )
    if op.high_threshold is not None:
        text += ('High: ' + str(op.high_threshold), )
    return text


def _format_flags(flags: int) -> ():
    if flags > consts.FLAGS_MAX_SIZE:
        raise ValueError('Stellar: invalid')
    text = ()
    if flags & consts.FLAG_AUTH_REQUIRED:
        text += ('AUTH_REQUIRED', )
    if flags & consts.FLAG_AUTH_REVOCABLE:
        text += ('AUTH_REVOCABLE', )
    if flags & consts.FLAG_AUTH_IMMUTABLE:
        text += ('AUTH_IMMUTABLE', )
    return text


def format_asset_code(asset: StellarAssetType) -> str:
    if asset is None or asset.type == consts.ASSET_TYPE_NATIVE:
        return 'XLM (native)'
    return asset.code


async def confirm_asset_issuer(ctx, asset: StellarAssetType):
    if asset is None or asset.type == consts.ASSET_TYPE_NATIVE:
        return
    content = Text('Confirm issuer', ui.ICON_CONFIRM,
                   ui.BOLD, asset.code + ' issuer:',
                   ui.MONO, *split(format_address(asset.issuer)),
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)