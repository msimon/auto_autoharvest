#!/usr/bin/env python3
import json
import requests

AUTO_FARM_INFO_URL = 'https://api.autofarm.network/bsc/get_farms_data'


if __name__ == '__main__':
    auto_farms_data = requests.get(AUTO_FARM_INFO_URL).json()
    pool_ids_to_name = { pool_id:pool['wantName'] for pool_id, pool in auto_farms_data["pools"].items()}

    print(json.dumps(pool_ids_to_name, indent=1))
