from facebook_business.adobjects.adaccount import AdAccount
import pandas as pd
from httplib2 import Http
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import json
from facebook_business.api import FacebookAdsApi
import tkinter
from tkinter import ttk


def date_format_change(date):
    return date.split('-')[2]+'.'+date.split('-')[1]

# Taking all FB Ads account insights by selected columns and selected date preset, divided by ad.
def take_ad_info(ad_acc_id, token):
    FacebookAdsApi.init(access_token=token)
    fields = [
        'ad_name',
        'spend',
        'clicks',
        'cpc',
        'campaign_name',
        'date_start',
    ]
    params = {
        # 'time_range': {"since":"2020-08-07","until":"2022-08-10"}, test preset
        'filtering': [],
        'level': 'ad',
        'breakdowns': [],
        'date_preset': 'today'
    }
    return AdAccount(ad_acc_id).get_insights(
        fields=fields,
        params=params,
    )


# Using pandas dataframe to contain data
def write_to_df(ad_info, columns_list):
    table_df = pd.DataFrame(columns=columns_list.keys())
    for ind, ad in enumerate(ad_info):
        for column in columns_list.keys():
            try:
                table_df.loc[ind, column] = float(ad.get(column))
            except:
                table_df.loc[ind, column] = ad.get(column)
    table_df = table_df.loc[table_df['spend'] != 0]
    table_df['date_start'] = table_df['date_start'].apply(date_format_change)
    print(table_df.head(1), '\n ... \n', table_df.tail(1))
    return table_df


# Writing data from 1 Ads manager Account from today to 1 google sheet. Rewriting if 'today' data already writen.
def write_to_gss(sheet_id, columns_dict, access_token, ad_acc_id, credence_file):
    dataframe = write_to_df(take_ad_info(ad_acc_id=ad_acc_id, token=access_token), columns_dict)
    # Authorizing to google sheet API by credence_file with API_KEY
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credence_file,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpauth = credentials.authorize(Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpauth,
                                        discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
    # Collecting data from authorized sheet
    results_get = service.spreadsheets().values().get(spreadsheetId=sheet_id,
                                    range=f"{columns_dict['date_start']}:{columns_dict['date_start']}").execute()
    list_of_dates = results_get.get('values')
    # Getting index of last filled row and number of 'today' data rows.
    prev_num = sum([1 if ele == list_of_dates[-1] else 0 for ele in list_of_dates])
    last_num = len(list_of_dates)
    # Write new data to sheet or rewriting 'today' data.
    if [datetime.datetime.today().strftime('%d.%m')] != list_of_dates[-1]:
        service.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body={
                'valueInputOption': 'RAW',
                'data': [{'majorDimension': 'COLUMNS', 'range': f'{columns_dict[column]}{last_num+1}',
                'values': [dataframe[column].tolist()]} for column in columns_dict.keys()]
        }).execute()
        print('New data added')

    else:
        service.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body={
                    'valueInputOption': 'RAW',
                    'data': [{'majorDimension': 'COLUMNS', 'range': f'{columns_dict[column]}{last_num - prev_num + 1}',
                    'values': [dataframe[column].tolist()]} for column in columns_dict.keys()]
        }).execute()
        print('Prevision data was rewritten')


def main():
    # File with program settings
    with open('info_storage.json') as file:
        settings = json.load(file)

    credence = settings['credence']
    for i in settings['ads']:
        access_token = i['access_token']
        ad_acc_id = i['ad_account_id']
        sp_sheet_id = i['sp_sheet_id']
        columns_dict_from_set = dict(zip(i['columns_list'], i['letter_list']))
        print('Write data to:\n', access_token, ad_acc_id, sp_sheet_id, columns_dict_from_set)
        write_to_gss(sp_sheet_id, columns_dict_from_set, access_token, ad_acc_id, credence)

    # Show end-state window
    root = tkinter.Tk()
    frm = ttk.Frame(root, padding=100)
    frm.grid()
    ttk.Label(frm, text="Done!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)
    root.mainloop()


if __name__ == '__main__':
    main()
