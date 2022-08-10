To properly work of programm you need to give 'editor' access on sheet to this email: fi-acc@adstogs-fi.iam.gserviceaccount.com
This is apps service-account email.
###########################################################################################################################################################################################################################################################################################################################################
There is "info_storage.json" file in repository. It's contain setting to AdsToGS script and look like example below, when unused:
{
	"credence" : "",
	"ads" :	[
		{
		"access_token":"",
		"ad_account_id": "",
		"sp_sheet_id": "",
		"columns_list": [
				],
		"letter_list": [
				]
		}
		]
}

You need to fill "credence" value with name of your google sheet API-KEY json file, like "project-aa-abc1234567890.json"
###########################################################################################################################################################################################################################################################################################################################################
To add FB ad account in work you need:
Open "info-storage.json" with notepad or notebook and add data to "ads":
										[
										{
										Three pairs of 'key':'value'
										and table settings	
										},
										{
										"access_token":"EAAIxXxxXXXXXXXXXXxxxxXXxxxXXXXXXXXXXXXXxxxxxxxxxxxxxxXX",
										"ad_account_id":"act_12345678901234",
										"sp_sheet_id":"ABCabc1234567890",
										"columns_list": [
												"date_start",
              											"campaign_name",
              											"ad_name",
         											"spend",
               											"clicks",
               											"cpc"
												],
										"letter_list":	[
												"A",
												"B",
												"C",
												"D",
												"E",
												"F"
												]
										}
										You can add up to 50 accounts
										]
You can write settings in any sequences 'access_token', 'ad_account_id, 'sp_sheet_id', "columns_list", "letter_list"
List of letters need to correspond to list of columns by indexes, like in example: "date_start":"A", "campaign_name":"B" ... , as you want to see it in your sheet
###########################################################################################################################################################################################################################################################################################################################################
Where to get this params:

ad_account_id - FB ad account identifier. Written in ads_manager, to the right of account name in theparentheses.

sh_sheet_id - google sheet identifier. Written in sheet adress bar after "https://docs.google.com/spreadsheets/d/" and before "/edit#gid"

access_token - to get this param you need to "partner" FB application by fb_app_id and follow by 3 steps: Sign into your developer account; 
On the Apps page, select an app to open the dashboard for that app; On the Dashboard, navigate to Settings > Advanced > Security > Client token.

columns_list - choose from api facebook_business using syntax that facebook used itself

letter_list - choose letter to all columns in columns_list in the sequence you need to write it to sheet. 
Every letter correspond column name by index in list, like in example: "date_start":"A", "campaign_name":"B" ... 
###########################################################################################################################################################################################################################################################################################################################################
ver1.2 The script, when launched, enters cash in the advertising account with non-zero expenses into the table. 
If there is already data for the current date, then it will delete the old ones and write back all the CURRENT data in the advertising account with non-zero spending.


