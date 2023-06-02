import servsecrets
from datetime import datetime
import streamlit as st
import gspread as gs
import pandas as pd

class SheetManager:

    def __init__(self, creds: dict, sheets_key: str):
        self.creds = creds
        self.sheets_key = sheets_key
        self.gservaccount = gs.service_account_from_dict(self.creds)
        self.sheet_file = self.gservaccount.open_by_key(self.sheets_key)

    def load_data(self, sheet_number: int):
        worksheet = self.sheet_file.get_worksheet_by_id(sheet_number)

        return pd.DataFrame(
            worksheet.get_all_records(),
            columns= worksheet.get_all_values()[0]
        )

    def push_data(self, sheet_number: int, data: pd.DataFrame):
        old_data = self.load_data(sheet_number=sheet_number)
        worksheet = self.sheet_file.get_worksheet_by_id(sheet_number)

        new_data = pd.concat([old_data, data], ignore_index=True).fillna('')
        worksheet.update(
            [new_data.columns.values.tolist()] + new_data.values.tolist()
        )


if __name__ == '__main__':
    import generator
    import pytz

    manager = SheetManager(
        creds = servsecrets.service_acct_creds,
        sheets_key = st.secrets.GSheets.sheets_key
    )

    # Test Pull
    sample = manager.load_data(sheet_number=0)
    sample.head()

    # Test Push
    date_now = datetime.strftime(
        datetime.now(pytz.timezone('Asia/Singapore')),
        '%Y-%m-%dT%H:%M:%S.%f'
    )
    email_test = 'example2_email@gmail.com'
    osu_user_test = 'test_osu_user'
    discord_user_test = 'test_discord_user'
    test_reg_id = generator.generate_reg_id(
        str_input = ''.join(
            [date_now, email_test, osu_user_test, discord_user_test]
        )
    )


    new_data = pd.DataFrame({
        'date_created':[date_now],
        'reg_id':[test_reg_id],
        'email':[email_test],
        'osu_username':[osu_user_test],
        'discord_username':[discord_user_test],
        'days_attending':['Day 1, Day 3'],
        'has_consented':True
    })
    manager.push_data(sheet_number=0, data=new_data)

