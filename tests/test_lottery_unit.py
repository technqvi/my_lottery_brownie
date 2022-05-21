from brownie import  Lottery, accounts,config,network,exceptions
import pytest
import scripts.deploy_lottery as x_deploy
import scripts.helpful_scripts as x_help
from web3 import Web3


def test_get_entrance_fee():
    if network.show_active() not in  x_help.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    x=x_deploy.deploy_lottery()
    # act 2000 eth/usd and entryFee=50 usd  so it is 50/2000=0.025

    expected_entrance_fee=Web3.toWei( 0.025,"ether")
    actual_entrance_fee=x.getEntranceFee()
    assert  expected_entrance_fee==actual_entrance_fee
    print (actual_entrance_fee)


def test_check_started_mode():
    if network.show_active() not in  x_help.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
     pytest.skip()
    x=x_deploy.deploy_lottery()

    with pytest.raises(exceptions.VirtualMachineError):
        x.enter({"from": x_help.get_account(),"value":x.getEntranceFee()})

def test_start_enter_lottery():
    if network.show_active() not in  x_help.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
     pytest.skip()

    x=x_deploy.deploy_lottery()
    account=x_help.get_account()
    x.startLottery({"from":account})
    x.enter({"from":account,"value": x.getEntranceFee()})
    assert x.players(0)==account


def test_end_lottery():
    if network.show_active() not in  x_help.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
     pytest.skip()

    x=x_deploy.deploy_lottery()

    account=x_help.get_account()
    x.startLottery({"from":account})
    x.enter({"from":account,"value": x.getEntranceFee()})
    x_help.fund_with_link(x)
    x.endLottery({"from":account})

    assert x.lottery_state()==2

def test_pick_winner_correctly_trong():

    x=x_deploy.deploy_lottery()
    
    account0=x_help.get_account(index=0)
    account1=x_help.get_account(index=1)
    account2=x_help.get_account(index=2)
    account3=x_help.get_account(index=3)

    x.startLottery({"from":account0})
    x.enter({"from":account0,"value": x.getEntranceFee()})
    x.enter({"from":account1,"value": x.getEntranceFee()})
    x.enter({"from":account2,"value": x.getEntranceFee()})
    x.enter({"from":account3,"value": x.getEntranceFee()})

    x_help.fund_with_link(x)

    tx=x.endLottery({"from":account0})
    request_id=tx.events["RequestedRandomness"]["requestId"]

    STATIC_RNG=999
    x_help.get_contract("vrf_coordinator").callBackWithRandomness(request_id,STATIC_RNG,
    x.address,{"from":account0})

     # 777 % 3 =0 (account 0-3 to bet lottery)

    print("==============3 Assertions==============")

    starting_bal_of_acc=account3.balance()
    print("start bal of accout ",starting_bal_of_acc)
    bal_of_lottery=x.balance()
    print("start bal of contract ",bal_of_lottery)

    assert x.recentWinner()==account3
    assert x.balance()==0
    assert account3.balance()==starting_bal_of_acc+bal_of_lottery 

    print("new bal of account ",account0.balance())
     

def test_can_pick_winner_correctly():
    # Arrange
    if network.show_active() not in x_help.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = x_deploy. deploy_lottery()
    account =x_help. get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": x_help. get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": x_help. get_account(index=2), "value": lottery.getEntranceFee()})

    x_help. fund_with_link(lottery)

    print("==============3 Assertions==============")

    starting_balance_of_account = account.balance()
    print("start bal of accout ",starting_balance_of_account)

    balance_of_lottery = lottery.balance()
    print("start bal of contract ",balance_of_lottery)

    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    x_help. get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    # 777 % 3 = 0
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery

    print("new bal of account ",account.balance())

    
