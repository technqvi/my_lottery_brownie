import scripts.trong_helpful_scripts as x_help
# import scripts.helpful_scripts_tutor  as x_help


from brownie import config,network,Lottery
from web3 import Web3
import time

def deploy_lottery():
    # account=get_account(id="peter1-dev")
    account=x_help.get_account()
    print(f"My account address is {account.address}")

    #These are list of parameter of constructor
    #constructor(address _priceFeedAddress ,address _vrfCoordinator, 
    # address _link,uint256 _fee,bytes32 _keyhash ) 
    x=Lottery.deploy(
        x_help.get_contract("eth_usd_price_feed").address,
        x_help.get_contract("vrf_coordinator").address,
        x_help.get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from":account} ,
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deploy lotter!")
def start_lottery():
    account=x_help.get_account()
    x=Lottery[-1]

    tx=x.startLottery({"from": account})
    tx.wait(1)
    print("The lottery is started !!!")

def play_lottery():
    account=x_help.get_account()
    x=Lottery[-1]
    fee_value=x.getEntranceFee() #+1000000000000000000
    print("Fee value is ")
    print(Web3.fromWei(fee_value, 'ether'))

    budget_value=fee_value+100000000000000000
    # budget_value=fee_value+100000000
    print("Budget value is ")
    print(Web3.fromWei(budget_value, 'ether'))

    tx=x.enter({"from":account,"value":budget_value})

    tx.wait(1)
    print("Play lottery !!!")


def end_lotter():
    account=x_help. get_account()
    x=Lottery[-1]
    tx=x_help.fund_with_link(x.address)
    print("funded chainlink aleady")
    tx.wait(1)
    
    end_tx=x.endLottery({"from":account})
    print("ended already")
    end_tx.wait(1)

    time.sleep(60)
    print(f"{x.recentWinner()} is new winner")




def main():

    
    deploy_lottery()
    print("================deployed================")
    start_lottery()
    print("================started================")
    play_lottery()
    print("================played================")
    end_lotter()
    print("================ended================")