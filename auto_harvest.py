#!/usr/bin/env python3
import sys
import argparse
import requests
from decimal import Decimal
from web3 import Web3
from pydash import _
from time import time
from datetime import datetime

ADDR_SIZE = 66
ROOT_ADDR = "0x0000000000000000000000000000000000000000000000000000000000000000"
AUTO_CONTRACT = "0x0895196562C7868C5Be92459FaE7f877ED450452"
AUTO_ABI = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"AUTO","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"AUTOMaxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"AUTOPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"AUTOv2","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"contract IERC20","name":"_want","type":"address"},{"internalType":"bool","name":"_withUpdate","type":"bool"},{"internalType":"address","name":"_strat","type":"address"}],"name":"add","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"burnAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_wantAmt","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"inCaseTokensGetStuck","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_inputAmt","type":"uint256"}],"name":"migrateToAUTOv2","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ownerAUTOReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingAUTO","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IERC20","name":"want","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accAUTOPerShare","type":"uint256"},{"internalType":"address","name":"strat","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"set","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"stakedWantTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_wantAmt","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"withdrawAll","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

PANCAKE_SWAP_CONTRACT = '0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F'
PANCAKE_SWAP_ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

AUTO_TOKEN_CONTRACT = "0xa184088a740c695E156F91f5cC086a06bb78b827"
WRAP_BNB_TOKEN_CONTRACT = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"

AUTO_FARM_INFO_URL = 'https://api.autofarm.network/bsc/get_farms_data'
PANCAKE_PRICE_URL = "https://api.pancakeswap.info/api/tokens"
PANCAKE_ASSUMED_SLIPPAGE = Decimal(0.5 / 100)
AUTO_WBNB_POOL_ID = 6


def decode_hex(contract, hex):
    function_def, params = contract.decode_function_input(hex)
    print(function_def)
    print(params)

### Main function
def auto_compund(wallet_address, private_key, min_amount_to_harvest):
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
    auto_contract = w3.eth.contract(address=AUTO_CONTRACT, abi=AUTO_ABI)
    pancake_swap_contract = w3.eth.contract(address=PANCAKE_SWAP_CONTRACT, abi=PANCAKE_SWAP_ABI)

    auto_farms_data = requests.get(AUTO_FARM_INFO_URL).json()
    auto_pool_ids = _.get(auto_farms_data, 'pools', {}).keys()

    def get_auto_wbnb_price():
        pancake_swap_price = requests.get(PANCAKE_PRICE_URL).json()
        auto_price_usd = Decimal(_.get(pancake_swap_price, f'data.{AUTO_TOKEN_CONTRACT}.price', 0))
        wbnb_price_usd = Decimal(_.get(pancake_swap_price, f'data.{WRAP_BNB_TOKEN_CONTRACT}.price', 0))
        return auto_price_usd, wbnb_price_usd

    auto_price_usd, wbnb_price_usd = get_auto_wbnb_price()

    if not auto_pool_ids or not auto_price_usd or not wbnb_price_usd:
        print("Missing pool and/or price data. Exiting...")
        exit()

    def withdraw_auto_token_if_necessary(acc_auto_withdraw_gwei, pool_id):
        pool_id = int(pool_id)
        current_pending_auto_gwei = auto_contract.functions.pendingAUTO(pool_id, wallet_address).call()
        current_pending_auto_eth = w3.fromWei(current_pending_auto_gwei, 'ether')

        if current_pending_auto_eth * auto_price_usd > min_amount_to_harvest:
            print(f"- Current pending auto for pool id {pool_id}: {current_pending_auto_eth} = ${current_pending_auto_eth * auto_price_usd:.2f}. Withdrawing...", end='')
            # withdrawing a pool with 0 only withdraw the reward = Harvest
            tx = auto_contract.functions.withdraw(pool_id, 0).buildTransaction({
                'from': wallet_address,
                'nonce': w3.eth.getTransactionCount(wallet_address),
                'gas': 500000
            })
            signed_tx = w3.eth.account.signTransaction(tx, private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(f"...done.\n tx hash = {tx_receipt['transactionHash'].hex()}")
            return acc_auto_withdraw_gwei + current_pending_auto_gwei
        return acc_auto_withdraw_gwei


    connected = w3.isConnected()

    if connected:
        harvested_auto_amt_gwei = _.reduce(auto_pool_ids, withdraw_auto_token_if_necessary, 0)
        harvested_auto_amt_eth = w3.fromWei(harvested_auto_amt_gwei, 'ether')
        print(f"- Total harvested: Auto {harvested_auto_amt_eth} = ${harvested_auto_amt_eth * auto_price_usd:.2f}")
        if harvested_auto_amt_gwei > 0:
            ## SELL HALF AUTO FOR WBNB

            half_harvested_auto_amt_gwei = int(harvested_auto_amt_gwei / 2)
            # get expceted WBNB amount from pancake
            amounts_out = pancake_swap_contract.functions.getAmountsOut(
                amountIn=half_harvested_auto_amt_gwei,
                path=[AUTO_TOKEN_CONTRACT, WRAP_BNB_TOKEN_CONTRACT],
            ).call()

            wbnb_amt_gwei = int(amounts_out[1] * (1 - PANCAKE_ASSUMED_SLIPPAGE))

            print(f"- Swapping AUTO {half_harvested_auto_amt_gwei} for WBNB {wbnb_amt_gwei} on pancakeswap...", end='')
            tx = pancake_swap_contract.functions.swapExactTokensForTokens(
                    amountIn=half_harvested_auto_amt_gwei,
                    amountOutMin=wbnb_amt_gwei,
                    path=[AUTO_TOKEN_CONTRACT, WRAP_BNB_TOKEN_CONTRACT],
                    to=wallet_address,
                    deadline=int(time()) + 60 * 5 # give 5 minutes deadline
                ).buildTransaction({
                    'from': wallet_address,
                    'nonce': w3.eth.getTransactionCount(wallet_address),
                    'gas': 500000
                }
            )
            signed_tx = w3.eth.account.signTransaction(tx, private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(f"...done.\n tx hash = {tx_receipt['transactionHash'].hex()}")

            transfer_log = _.find(tx_receipt['logs'], lambda x: x['address'] == WRAP_BNB_TOKEN_CONTRACT)
            if not transfer_log or not transfer_log.get('data'):
                print(f"Error: Could not find log for the WBNB transfer. Transaction must have failed.")
                exit(-1)

            ## ADD LIQUIDITY TO PANCAKE SWAP. SWAP AUTO & WBNB FOR WBNB-AUTO LP TOKEN
            received_wbnb_amt_gwei = int(transfer_log['data'], 16)

            wbnb_amt_gwei = int(received_wbnb_amt_gwei * (1 - PANCAKE_ASSUMED_SLIPPAGE))
            print(f"- Add lidquidity AUTO-WBNB: AUTO {half_harvested_auto_amt_gwei} for WBNB {wbnb_amt_gwei} on pancakeswap...", end='')
            tx = pancake_swap_contract.functions.addLiquidity(
                    tokenA=AUTO_TOKEN_CONTRACT,
                    tokenB=WRAP_BNB_TOKEN_CONTRACT,
                    amountADesired=half_harvested_auto_amt_gwei,
                    amountBDesired=wbnb_amt_gwei,
                    amountAMin=0,
                    amountBMin=0,
                    to=wallet_address,
                    deadline=int(time()) + 60 * 5 # give 5 minutes deadline
                ).buildTransaction({
                    'from': wallet_address,
                    'nonce': w3.eth.getTransactionCount(wallet_address),
                    'gas': 500000
                }
            )
            signed_tx = w3.eth.account.signTransaction(tx, private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(f"...done.\n tx hash = {tx_receipt['transactionHash'].hex()}")

            def find_transfer_lp_logs(log):
                # Search for the log transfering money to your wallet
                # Transfer log have 3 topics: function hash, from, to.
                # Looking for `from = 0x0` & `to = wallet_address`
                topics = log['topics']
                if len(topics) == 3 and topics[1].hex() == ROOT_ADDR:
                    # extract the leading 0 from the address in the log
                    addr = '0x' + topics[2].hex()[ADDR_SIZE-len(wallet_address)+2:]
                    return addr == wallet_address.lower()

            transfer_lp_log = _.find(tx_receipt['logs'], find_transfer_lp_logs)
            if not transfer_lp_log or not transfer_lp_log.get('data'):
                print(f"Error: Could not find log for the LP transfer. Transaction must have failed.")
                exit(-1)

            liquidity_created = int(transfer_lp_log['data'], 16)

            print(f"- Add {w3.fromWei(liquidity_created, 'ether')} token back into AUTO-WBNB LP vault...", end='')
            tx = auto_contract.functions.deposit(AUTO_WBNB_POOL_ID, liquidity_created).buildTransaction({
                'from': wallet_address,
                'nonce': w3.eth.getTransactionCount(wallet_address),
                'gas': 500000
            })
            signed_tx = w3.eth.account.signTransaction(tx, private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(f"...end.\n tx hash = {tx_receipt['transactionHash'].hex()}")
    else:
        print("Connection Error!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='compound_daily_interest', add_help=True)
    parser.add_argument('--wallet_address', action='store', required=True)
    parser.add_argument('--private_key', action='store', required=True)
    parser.add_argument('--min_amount_to_harvest', action='store', type=float, required=True)

    args = parser.parse_args(sys.argv[1:])

    print('==================================')
    print(f"Ran at {datetime.now()}")
    print('==================================')

    auto_compund(
        args.wallet_address,
        args.private_key,
        args.min_amount_to_harvest
    )

    print("\n")
