########################################################################
#
#  Copyright 2024 Johns Hopkins University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Contact: usdtinfo@jhu.edu
# Website: https://usdiseasetracker.org/
#
########################################################################
import requests
from pathlib import Path

def upload_usdt_data(refresh_token_filepath, data_filepath, verbose = False):
    """
    upload csv data file to USDT project.
    """
    # Get access token using refresh token
    token_url = "https://auth.usdiseasetracker.org/realms/usdt-dataupload/protocol/openid-connect/token"

    refresh_token = refresh_token_filepath.read_text(encoding = "utf-8").strip()
    payload = {
        "grant_type": "refresh_token",
        "client_id": "usdt-application",
        "refresh_token": refresh_token
    }

    response1 = requests.post(token_url, data = payload)
    response1_output = response1.json()
    access_token = response1_output['access_token']
    print(f'\nrefresh token response status = {response1.status_code}')
    if verbose:
        for key in response1_output:
            print(f'{key} : {response1_output[key]}')
        
    print('\nData file is being uploaded, please wait for a success or failure message...')
            
    # Upload data file using access token
    upload_url = "https://usdtupload.org/api/upload"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    # read the data file contents and upload to USDT
    with open(data_filepath, "rb") as f:
        response2 = requests.post(upload_url, headers = headers, files = {"datafile": f})
    response2_output = response2.json()
    print(f'-\nupload response status = {response2.status_code}\n-')
    for key in response2_output:
        if key != 'errors':
            print(f'{key} : {response2_output[key]}')
        else:
            errors = response2_output[key]
            print(f'{key} :')
            for error in errors:
                for error_key in error:
                    print(f'\t{error_key} : {error[error_key]}')
                print('\t-')