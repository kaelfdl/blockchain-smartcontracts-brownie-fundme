import pytest
from brownie import accounts, network, exceptions
from scripts.util import get_account, LOCAL_BLOCKCHAIN_ENV
from scripts.deploy import deploy_fund_me


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx2 = fund_me.withdraw({"from": account})
    assert fund_me.addressToAmountFunded(account.address) == 0
    tx2.wait(1)


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("For local development only")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
