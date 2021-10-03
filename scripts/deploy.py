from brownie import FundMe, config, network
from scripts.util import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENV


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed_address"
        ]
    else:
        price_feed_address = deploy_mocks()
    print("Deploying contract...")
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
