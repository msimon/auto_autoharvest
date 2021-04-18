#!/usr/bin/env python3
import sys
import argparse
import requests
from decimal import Decimal
from web3 import Web3
from pydash import _
from time import time
from datetime import datetime

AUTO_CONTRACT = "0x0895196562C7868C5Be92459FaE7f877ED450452"
AUTO_ABI = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"AUTO","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"AUTOMaxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"AUTOPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"AUTOv2","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"contract IERC20","name":"_want","type":"address"},{"internalType":"bool","name":"_withUpdate","type":"bool"},{"internalType":"address","name":"_strat","type":"address"}],"name":"add","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"burnAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_wantAmt","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"inCaseTokensGetStuck","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_inputAmt","type":"uint256"}],"name":"migrateToAUTOv2","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ownerAUTOReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingAUTO","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IERC20","name":"want","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accAUTOPerShare","type":"uint256"},{"internalType":"address","name":"strat","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"set","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"stakedWantTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_wantAmt","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"withdrawAll","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

PANCAKE_SWAP_CONTRACT = '0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F'
PANCAKE_SWAP_ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

AUTO_TOKEN_CONTRACT = "0xa184088a740c695E156F91f5cC086a06bb78b827"
WRAP_BNB_TOKEN_CONTRACT = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"

AUTO_FARM_INFO_URL = 'https://api.autofarm.network/bsc/get_farms_data'
PANCAKE_PRICE_URL = "https://api.pancakeswap.com/api/v1/price"
PANCAKE_ASSUMED_SLIPPAGE = Decimal(0.5 / 100)
AUTO_WBNB_POOL_ID = 6

def decode_hex(contract, hex):
    function_def, params = contract.decode_function_input(hex)
    print(function_def)
    print(params)

def deduct_slippage(amount):
    return int(amount * (1 - PANCAKE_ASSUMED_SLIPPAGE))

### Main function
def auto_compound(wallet_address, private_key, min_amount_to_harvest, compound_strategy):
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
    auto_contract = w3.eth.contract(address=AUTO_CONTRACT, abi=AUTO_ABI)
    pancake_swap_contract = w3.eth.contract(address=PANCAKE_SWAP_CONTRACT, abi=PANCAKE_SWAP_ABI)

    auto_farms_data = requests.get(AUTO_FARM_INFO_URL).json()
    # Inject key (id) in pool dict
    auto_pools = [{**o, **{'pool_id': int(k)}} for (k, o) in _.get(auto_farms_data, 'pools', {}).items()] 

    def get_auto_wbnb_price():
        pancake_swap_price = requests.get(PANCAKE_PRICE_URL).json()
        auto_price_usd = Decimal(_.get(pancake_swap_price, 'prices.AUTO', 0))
        wbnb_price_usd = Decimal(_.get(pancake_swap_price, 'prices.WBNB', 0))
        return auto_price_usd, wbnb_price_usd

    auto_price_usd, wbnb_price_usd = get_auto_wbnb_price()

    if not auto_pools or not auto_price_usd or not wbnb_price_usd:
        print("Missing pool and/or price data. Exiting...")
        exit()
 
    def contract(address):
        abi = requests.get(f"https://api.bscscan.com/api?module=contract&action=getabi&address={address}").json()['result']
        return w3.eth.contract(address=address, abi=abi)

    def transaction(contractFunc):
        tx = contractFunc.buildTransaction({
            'from': wallet_address,
            'nonce': w3.eth.getTransactionCount(wallet_address),
            'gas': 500000
        })
        signed_tx = w3.eth.account.signTransaction(tx, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt

    def deposit(pool, amount):
        tx_receipt = transaction(auto_contract.functions.deposit(pool.pool_id, amount))
        print(f"...end.\n tx hash = {tx_receipt['transactionHash'].hex()}")

    def withdraw_auto_token_if_necessary(pool):
        current_pending_auto_gwei = auto_contract.functions.pendingAUTO(pool.pool_id, wallet_address).call()
        current_pending_auto_eth = w3.fromWei(current_pending_auto_gwei, 'ether')

        if current_pending_auto_eth * auto_price_usd > min_amount_to_harvest:
            print("\n")
            print(f"- Current pending auto for pool id {pool.pool_id}: {current_pending_auto_eth} = ${current_pending_auto_eth * auto_price_usd:.2f}. Withdrawing...")
            # withdrawing a pool with 0 only withdraw the reward = Harvest
            tx_receipt = transaction(auto_contract.functions.withdraw(pool.pool_id, 0))
            print(f"...done.\n tx hash = {tx_receipt['transactionHash'].hex()}")
            return current_pending_auto_gwei
        return 0

    def swap_auto_for_token(amount, token_contract):
        # Can't swap auto for auto lol
        if token_contract.address == AUTO_TOKEN_CONTRACT:
            return amount

        # If requested token is other than WBNB, then route throught WBNB (ex: AUTO -> WBNB -> USDC)
        # If requested token is WBNB, then wire directly (ex: AUTO -> WBNB)
        # TODO: find a way to get optimal path (contract/api/manual?)
        path = [AUTO_TOKEN_CONTRACT] + _.uniq([WRAP_BNB_TOKEN_CONTRACT, token_contract.address]) 
        symbol = token_contract.functions.symbol().call()
        amounts_out = pancake_swap_contract.functions.getAmountsOut(
            amountIn=amount,
            path=path,
        ).call()

        amount_min = deduct_slippage(_.last(amounts_out))
        
        print(f"- Swapping AUTO {amount} for {amount_min} {symbol} on pancakeswap...", end='')

        tx_receipt = transaction(
            pancake_swap_contract.functions.swapExactTokensForTokens(
                amountIn=amount,
                amountOutMin=amount_min,
                path=path,
                to=wallet_address,
                deadline=int(time()) + 60 * 5 # give 5 minutes deadline
            )
        )
        print(f"...done.\n tx hash = {tx_receipt['transactionHash'].hex()}")

        # TODO: Ask bro: isn't the slippage already deducted from result ? (logs[2].data)
        received_amt_gwei = int(_.get(tx_receipt, 'logs[2].data'), 16)
        return deduct_slippage(received_amt_gwei)

    def add_liquidity(token0_contract, amount0, token1_contract, amount1):
        tx_receipt = transaction(
            pancake_swap_contract.functions.addLiquidity(
                tokenA=token0_contract.address,
                tokenB=token1_contract.address,
                amountADesired=amount0,
                amountBDesired=amount1,
                amountAMin=0,
                amountBMin=0,
                to=wallet_address,
                deadline=int(time()) + 60 * 5 # give 5 minutes deadline
            )
        )
        print(f"...done.\n tx hash = {tx_receipt['transactionHash'].hex()}")

        liquidity_created = int(_.get(tx_receipt, 'logs[4].data'), 16)
        return liquidity_created

    def auto_compound_same_pool(pool):
        harvested_auto_amt_gwei = withdraw_auto_token_if_necessary(pool)

        if harvested_auto_amt_gwei > 0:
            pool_contract = contract(_.get(pool, 'poolInfo.want'))

            # @TODO: Ask bro: Is there a better way to know if the contract is a pair or an actual token ?
            # https://pancakeswap.info/pairs
            # https://pancakeswap.info/tokens
            is_pair = len(_.map(['token0', 'token1'], lambda f: pool_contract.find_functions_by_name(f))) == 2

            if is_pair:
                half_harvested_auto_amt_gwei = int(harvested_auto_amt_gwei / 2)
                token0_contract = contract(pool_contract.functions.token0().call())
                token1_contract = contract(pool_contract.functions.token1().call())
                token0_amount = swap_auto_for_token(half_harvested_auto_amt_gwei, token0_contract)
                token1_amount = swap_auto_for_token(half_harvested_auto_amt_gwei, token1_contract)
                token = add_liquidity(token0_contract, token0_amount, token1_contract, token1_amount)
                deposit(pool, token)
            else:
                token = swap_auto_for_token(harvested_auto_amt_gwei, pool_contract)
                deposit(pool, token)

    connected = w3.isConnected()

    if connected:
        print(f"Using strategy: {compound_strategy}")
        if compound_strategy == "same-pool":
            # @TODO: Should we filter pools to get the ones were stacked > 0 only ?
            _.for_each(auto_pools, auto_compound_same_pool)
        elif compound_strategy == "auto-wbnb-lp":
            auto_wbnb_pool = _.find(auto_pools, lambda pool: pool.pool_id == AUTO_WBNB_POOL_ID)
            
            if not auto_wbnb_pool:
                print("Missing AUTO/WBNB Pool. Exiting...")
                exit(-1)

            print(f"Checking each pool to see if auto rewards meet the ${min_amount_to_harvest} threshold")
            # @TODO: Should we filter pools to get the ones were stacked > 0 only ?
            harvested_auto_amt_gwei = _.reduce(auto_pools, lambda acc, pool: acc + withdraw_auto_token_if_necessary(pool), 0)
            harvested_auto_amt_eth = w3.fromWei(harvested_auto_amt_gwei, 'ether')
            print(f"- Total harvested: Auto {harvested_auto_amt_eth} = ${harvested_auto_amt_eth * auto_price_usd:.2f}")
            if harvested_auto_amt_gwei > 0:
                half_harvested_auto_amt_gwei = int(harvested_auto_amt_gwei / 2)
                auto_token_contract = contract(AUTO_TOKEN_CONTRACT)
                wbnb_token_contract = contract(WRAP_BNB_TOKEN_CONTRACT)
                wbnb_amt_gwei = swap_auto_for_token(half_harvested_auto_amt_gwei, wbnb_token_contract)
                liquidity_created = add_liquidity(auto_token_contract, half_harvested_auto_amt_gwei, wbnb_token_contract, wbnb_amt_gwei)
                deposit(auto_wbnb_pool, liquidity_created)
    else:
        print("Connection Error!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='compound_daily_interest', add_help=True)
    parser.add_argument('--wallet_address', action='store', required=True)
    parser.add_argument('--private_key', action='store', required=True)
    parser.add_argument('--min_amount_to_harvest', action='store', type=float, required=True)
    parser.add_argument('--compound_strategy', action='store', required=True, choices=['auto-wbnb-lp', 'same-pool'])

    args = parser.parse_args(sys.argv[1:])

    print('==================================')
    print(f"Ran at {datetime.now()}")
    print('==================================')

    auto_compound(
        args.wallet_address,
        args.private_key,
        args.min_amount_to_harvest,
        args.compound_strategy
    )

    print("\n")
