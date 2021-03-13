# Autofarm WBNB-AUTO auto-compound

This is a small script the connects to autoform's contract to auto-compound the WBNB-AUTO pool. Which autofarm does not do.
All it does is:
- Go over all the pools, withdraw any pools where you have more than `min_amount_to_harvest`.
- Once all the harvest is done, half of the AUTO is sold for WBNB to pancakeswap
- Add liquidity to the WBNB-AUTO liquidity pool in pancakeswap
- Re-invest the WBNB-AUTO LP into autofarm

## First thing first

This script needs your private key to sign the transaction and perform action on your behalf.

As always with anything that needs you private key CHECK THE CODE! and make sure nothing weird is done with it.

You're private key should only be used to signed transaction, so you can prove it's you that makes the transaction. If it is used anywhere else, run away!

This is the only type of line that should use your private key
```
w3.eth.account.signTransaction(tx, private_key)
```

## Dependencies
python3
library: web3, requests, pydash

First install python3. Then run `pip install -r requirements.txt` to install all dependencies

## How to run

```
python3 auto_harvest.py --wallet_address 0x2c0d3c15022222230e50f05f541f012074ad53d8 --private_key d71d0202bb0094119194822a1759e444aa77225d2af4a3255636d730e1eff86d --min_amount_to_harvest 100
```

Parameters:
- wallet_address: Your wallet address. Public info that you share with most Dapp or to get paid
- private_key: Private key used to signed transaction. Please ALWAYS ALWAYS keep that private and share it with NOBODY. If someone get access to your private key, it will control your wallet.
- min_amount_to_harvest: The minimum amount to harvest on each pool in autofarm. Think carefully about that since fees will eat your rewards, but not auto-compouding often will also reduce your gain.

## How to run on schedule

If you are on mac or linux, you can use crontab to run that at fixed interval.

Run `crontab -e` then in the editor, write something like:
```
0 * * * * /usr/local/bin/python3 /Users/mysuser/auto_harvest/auto_harvest.py --wallet_address 0x2c0d3c15022222230e50f05f541f012074ad53d8 --private_key d71d0202bb0094119194822a1759e444aa77225d2af4a3255636d730e1eff86d --min_amount_to_harvest 100 >> /tmp/auto_harvest.log 2>&1
```
You will need to replace the path of `/usr/local/bin/python3` & `/Users/mysuser/auto_harvest/auto_harvest.py` to your own paths.

Log will be written in `/tmp/auto_harvest.log`

That will run the script every hour at o'clock.

Check the doc for crontab: https://help.ubuntu.com/community/CronHowto


## If you feel like giving me money :)

You can send me any token on ETH or BSC to the following address: 0x6393F201F92d543302CAAe427e89beDc3754368F
