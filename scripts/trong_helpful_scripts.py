from brownie import (network,accounts,config,
                     MockV3Aggregator,VRFCoordinatorMock,LinkToken,Contract,interface)

#https://github.com/PatrickAlphaC/smartcontract-lottery/tree/main/scripts
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
def get_account(index=None,id=None):

    # account[0]
    # account.add("env")
    # account.load("id")

    if index:
        print("Get acccount by index")
        return accounts[index]
    if id:
        return accounts.load(id)    
        print("Get acccount by id")
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        print("Get acccount on local")
        return accounts[1] 

    print("Get acccount on testnet")    
    return accounts.add(config["wallets"]["from_key"])

#https://github.com/smartcontractkit/chainlink-mix/tree/main/contracts/test (Recommend)
#https://github.com/smartcontractkit/chainlink/tree/develop/contracts/src
contract_to_mock={
"eth_usd_price_feed":MockV3Aggregator,
"vrf_coordinator":VRFCoordinatorMock,
"link_token":LinkToken,
}

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.
        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """

    contract_type=contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(f"{ contract_name} has been gotten on local")
        if len(contract_to_mock)<=0:
            deploy_mocks()
        # x=contract_type[-1] 
        contract = contract_type[-1]
         # MockV3Aggregator[-1]
     
    else:
        print(f"{contract_name} has been gotten on testnet")
        x_address=config["networks"][network.show_active()][contract_name]
        # pass address as paramerter to contract abi
        contract=Contract.from_abi(contract_type._name,x_address,contract_type.abi) 
       
    return contract  

DECIMALS=8
INITIAL_VALUE = 200000000000       
def deploy_mocks(decimals=DECIMALS,init_val=INITIAL_VALUE):
    print("Due to no any mock ,so  we deployed mock MockV3Aggregator,LinkToken and VRFCoordinatorMock")
    account=get_account()
    MockV3Aggregator.deploy(decimals,init_val,{"from": account})  
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})

    print("Mock has been Deployed!")    

def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    # get account if it is None
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")

    tx = link_token.transfer(contract_address, amount, {"from": account})
    # optoinal by  calling via interface 
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})


    tx.wait(1)
    print("Fund contract!")
    return tx

    