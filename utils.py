import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

class SeasonTeamRecord():

    url = 'https://www.cpbl.com.tw/standings/seasonaction'
    
    """
    SeasonTeamRecord mainly scrapes data in https://www.cpbl.com.tw/standings/season which contains:
    match record, team pitch record, team batting record, team defence record.
    Accordingly 4 functions teamRecord, teamPitch, teamBat, teamDefence are provided.
    
    Note: There are global codes in CPBL.com and to avoid redundancy, the repeated codes are listed here.

    kind : str, optional
    A: 一軍例行賽
    C: 一軍總冠軍賽
    D: 二軍例行賽
    D9: 二軍例行賽（業餘）
    E: 一軍季後挑戰賽
    F: 二軍總冠軍賽
    H: 未來之星邀請賽
    G: 一軍熱身賽
    """

    def  teamRecord(self, kind = 'A', season = 0, date = None):
        """
        teamRecord scrapes team records

        Args:
            kind (str, optional): refers to class note. Defaults to 'A'.
            season (int, optional): There are two seasons in one year. Use 0 for all, 1 for first half season and 2 for second half. Defaults to 0.
            date (_type_, optional): record until data. Use format: yyyy/mm/dd. Defaults to None.

        Returns:
            pd.Dataframe
        """

        # Define the form data to be sent in the POST request
        form_data = {
                'Kindcode': kind,
                'SeasonCode': season,
                'GameEndDate': date
                }

        # Send the POST request and retrieve the HTML content
        res = requests.post(self.url, data=form_data, verify=False)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find all elements with class 'RecordTableWrap'
        tables = soup.find_all(class_='RecordTableWrap')

        # Find the first table within the RecordTableWrap elements
        table_element = tables[0].find('table')

        # Extract the table headers
        headers = [re.sub(r'\n+', '', header.text.strip()) for header in table_element.find_all('th')]

        # Extract the table data
        rows = table_element.find_all('tr')
        table_data = []
        for row in rows:
            row_data = [re.sub(r'\n+', '', cell.text.strip()) for cell in row.find_all('td')]
            if row_data:
                table_data.append(row_data)

        # Create a DataFrame using the table headers and data
        df = pd.DataFrame(table_data, columns=headers)

        # Remove the first character of the '排名球隊' column
        df['排名球隊'] = df['排名球隊'].str[1:]

        # Return the DataFrame
        return df

    def teamPitch(self, kind = 'A', season = 0, date = None):
        # Define the form data to be sent in the POST request
        form_data = {
                'Kindcode': kind,
                'SeasonCode': season,
                'GameEndDate': date
                    }

        # Send the POST request and retrieve the HTML content
        res = requests.post(self.url, data=form_data, verify=False)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find all elements with class 'RecordTableWrap'
        tables = soup.find_all(class_='RecordTableWrap')

        # Find the first table within the RecordTableWrap elements
        table_element = tables[1].find('table')

        # Extract the table headers
        headers = [re.sub(r'\n+', '', header.text.strip()) for header in table_element.find_all('th')]

        # Extract the table data
        rows = table_element.find_all('tr')
        table_data = []
        for row in rows:
            row_data = [re.sub(r'\n+', '', cell.text.strip()) for cell in row.find_all('td')]
            if row_data:
                table_data.append(row_data)

        # Create a DataFrame using the table headers and data
        df = pd.DataFrame(table_data, columns=headers)

        # Return the DataFrame
        return df

    def teamBat(self, kind = 'A', season = 0, date = None):
        # Define the form data to be sent in the POST request
        form_data = {
                'Kindcode': kind,
                'SeasonCode': season,
                'GameEndDate': date
                }

        # Send the POST request and retrieve the HTML content
        res = requests.post(self.url, data=form_data, verify=False)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find all elements with class 'RecordTableWrap'
        tables = soup.find_all(class_='RecordTableWrap')

        # Find the first table within the RecordTableWrap elements
        table_element = tables[2].find('table')

        # Extract the table headers
        headers = [re.sub(r'\n+', '', header.text.strip()) for header in table_element.find_all('th')]

        # Extract the table data
        rows = table_element.find_all('tr')
        table_data = []
        for row in rows:
            row_data = [re.sub(r'\n+', '', cell.text.strip()) for cell in row.find_all('td')]
            if row_data:
                table_data.append(row_data)

        # Create a DataFrame using the table headers and data
        df = pd.DataFrame(table_data, columns=headers)

        # Return the DataFrame
        return df

    def teamDefense(self, kind = 'A', season = 0, date = None):
        # Define the form data to be sent in the POST request
        form_data = {
                'Kindcode': kind,
                'SeasonCode': season,
                'GameEndDate': date
                }

        # Send the POST request and retrieve the HTML content
        res = requests.post(self.url, data=form_data, verify=False)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find all elements with class 'RecordTableWrap'
        tables = soup.find_all(class_='RecordTableWrap')

        # Find the first table within the RecordTableWrap elements
        table_element = tables[3].find('table')

        # Extract the table headers
        headers = [re.sub(r'\n+', '', header.text.strip()) for header in table_element.find_all('th')]

        # Extract the table data
        rows = table_element.find_all('tr')
        table_data = []
        for row in rows:
            row_data = [re.sub(r'\n+', '', cell.text.strip()) for cell in row.find_all('td')]
            if row_data:
                table_data.append(row_data)

        # Create a DataFrame using the table headers and data
        df = pd.DataFrame(table_data, columns=headers)

        # Return the DataFrame
        return df

class Player():
    """
    Player class scrapes data under https://www.cpbl.com.tw/team/person?
    Most of the data requires a token to access the api. You can do to any player's page 
    and retrieve the RequestVerificationToken within script tag or from the header.
    """
    # TODO Token generate

    def __init__(self, token, acnt):
        self.token = token
        self.acnt = acnt

    def batting(self):
        """
        Retrieves batting data from the specified URL using a POST request.

        :return: A pandas DataFrame containing batting data.
        """

        url = 'https://www.cpbl.com.tw/team/getbattingscore'

        # Define the form data to be sent in the POST request
        form_data = {
                "acnt": self.acnt,
                "kindCode": "A"
                    }

        header = {
                'RequestVerificationToken': self.token,
                'x-requested-with': 'XMLHttpRequest'
                }

        try:
            response = requests.post(url, data=form_data, headers=header, verify=False)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful

            # Process the response here (if needed)
            result = response.json()  # Assuming the response is in JSON format
            print(result)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

        df = pd.read_json(response.json()['BattingScore'])
        df = df[['Name','TeamAbbrName','Year','Acnt','TotalTeamGames', 'TotalGames',
            'PlateAppearances', 'HitCnt', 'RunBattedINCnt', 'ScoreCnt',
            'HittingCnt', 'OneBaseHitCnt', 'TwoBaseHitCnt', 'ThreeBaseHitCnt',
            'HomeRunCnt', 'TotalBases', 'StrikeOutCnt', 'StealBaseOKCnt', 'Obp',
            'Slg', 'Avg', 'DoublePlayBatCnt', 'SacrificeHitCnt', 'SacrificeFlyCnt',
            'BasesONBallsCnt', 'IntentionalBasesONBallsCnt', 'HitBYPitchCnt',
            'StealBaseFailCnt', 'GroundOut', 'FlyOut', 'Goao', 'Ops', 'SB', 'TA',
            'Ssa', 'Xbh', 'Bbk']]
        return df

    def defence(self):
        """
        Sends a POST request to the given URL to retrieve the defense score data.
        
        :return: Returns a Pandas DataFrame containing the defense score data.
        """

        url = 'https://www.cpbl.com.tw/team/getdefencescore'

        # Define the form data to be sent in the POST request
        form_data = {
                "acnt": self.acnt,
                "kindCode": "A"
                    }

        header = {
                'RequestVerificationToken': self.token,
                'x-requested-with': 'XMLHttpRequest'
                }

        try:
            response = requests.post(url, data=form_data, headers=header, verify=False)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful

            # Process the response here (if needed)
            result = response.json()  # Assuming the response is in JSON format
            print(result)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

        res = json.loads(response.json()['DefenceScore'])
        flatten_data = []
        for item in list(res.values())[:-1]:
            flatten_data += item
        
        df = pd.DataFrame(flatten_data)

        # Print the DataFrame
        df = df[['TeamAbbrName','TotalTeamGames','Year',
            'TotalGames', 'DefendStationName', 'DefendCnt', 'PutoutCnt',
            'AssistCnt', 'ErrorCnt', 'JoinDoublePlayCnt', 'JoinTripplePlayCnt',
            'PassedBallCnt', 'CaughtStealingCnt', 'StealCnt', 'CSPct', 'Fpct',
            'TotalYearGames']]
        
        return df
    
    def matches(self, year = None):
        url = 'https://www.cpbl.com.tw/team/getfighterscore'

        # Define the form data to be sent in the POST request
        form_data = {
                "acnt": self.acnt,
                'year': year, 
            }

        header = {
                'RequestVerificationToken': self.token,
                'x-requested-with': 'XMLHttpRequest'
                }

        try:
            response = requests.post(url, data=form_data, headers=header, verify=False)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful

            # Process the response here (if needed)
            result = response.json()  # Assuming the response is in JSON format
            print(result)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

        df = pd.read_json(result['FighterScore'])
        df = df[['FightTeamName', 'TotalGames', 'PlateAppearances', 'HitCnt', 'RunBattedINCnt',
            'ScoreCnt', 'HittingCnt', 'OneBaseHitCnt', 'TwoBaseHitCnt',
            'ThreeBaseHitCnt', 'HomeRunCnt', 'TotalBases', 'DoublePlayBatCnt',
            'Avg', 'SacrificeHitCnt', 'SacrificeFlyCnt', 'BasesONBallsCnt',
            'IntentionalBasesONBallsCnt', 'HitBYPitchCnt', 'StrikeOutCnt',
            'StealBaseOKCnt', 'StealBaseFailCnt', 'SB', 'Obp', 'Slg', 'TA', 'Ops']]
        
        return df
    

    def statistics(self, year = "9999", fightingTeamNo = "AAA011"):
        """
        Retrieves statistics for a specific year and fighting team.

        Parameters:
            year (str): The year for which the statistics are retrieved. Defaults to "9999".
            fightingTeamNo (str): The code of the fighting team. Defaults to "AAA011".
            AEO011 富邦
            ACN011 中信
            AJK011 Lamigo
            AAA011 味全
            ADD011 統一
            AJL011 樂天

        Returns:
            pandas.DataFrame: The statistics as a pandas DataFrame.
        """

        url = 'https://www.cpbl.com.tw/team/getfightingscore'

        # Define the form data to be sent in the POST request
        form_data = {
                "acnt": self.acnt,
                "kindCode": "A",
                "year": year,
                "fightingTeamNo": fightingTeamNo,
            }

        header = {
                'RequestVerificationToken': self.token,
                'x-requested-with': 'XMLHttpRequest',
                }

        try:
            response = requests.post(url, data=form_data, headers=header, verify=False)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful

            # Process the response here (if needed)
            result = response.json()  # Assuming the response is in JSON format
            print(result)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

        df = pd.read_json(result['FightingScore'])
        df = df[['PitcherTeamName', 'HitterTeamName', 'PitcherAcnt',
            'PitcherName', 'PitcherTeamNo', 'HitterAcnt', 'HitterName',
            'HitterTeamNo', 'PlateAppearances', 'HitCnt', 'RunBattedINCnt',
            'HittingCnt', 'OneBaseHitCnt', 'TwoBaseHitCnt', 'ThreeBaseHitCnt',
            'HomeRunCnt', 'TotalBases', 'Avg', 'SacrificeHitCnt', 'SacrificeFlyCnt',
            'BasesONBallsCnt', 'IntentionalBasesONBallsCnt', 'HitBYPitchCnt',
            'StrikeOutCnt', 'GroundOut', 'FlyOut', 'Goao', 'Obp', 'Slg', 'Ops']]
        
        return df
    

    def followScore(self, year = 2023):
        url = 'https://www.cpbl.com.tw/team/getfollowscore'

        # Define the form data to be sent in the POST request
        form_data = {
                "acnt": self.acnt,
                "kindCode": "A",
                "year": year,
            }

        header = {
                'RequestVerificationToken': self.token,
                'x-requested-with': 'XMLHttpRequest',
                }

        try:
            response = requests.post(url, data=form_data, headers=header, verify=False)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful

            # Process the response here (if needed)
            result = response.json()  # Assuming the response is in JSON format
            print(result)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

        df = pd.read_json(result['FollowScore'])
        df = df[['FightTeamAbbrName', 'Year', 'KindCode', 'GameSno', 'GameDate',
            'HitterAcnt', 'HitterName', 'FieldNo', 'FightTeamCode', 'TeamNo',
            'TotalTeamGames', 'PlateAppearances', 'HitCnt', 'RunBattedINCnt',
            'ScoreCnt', 'HittingCnt', 'OneBaseHitCnt', 'TwoBaseHitCnt',
            'ThreeBaseHitCnt', 'HomeRunCnt', 'TotalBases', 'StrikeOutCnt',
            'StealBaseOKCnt', 'StealBaseFailCnt', 'Avg', 'SacrificeHitCnt',
            'SacrificeFlyCnt', 'BasesONBallsCnt', 'IntentionalBasesONBallsCnt',
            'HitBYPitchCnt', 'DoublePlayBatCnt', 'TripplePlayBatCnt', 'Lobs',
            'PutoutCnt', 'AssistCnt', 'JoinDoublePlayCnt', 'JoinTripplePlayCnt',
            'ErrorCnt', 'CaughtStealingCnt', 'PassedBallCnt']]

        return df