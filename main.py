import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1Jjl6VS73nd5RMz1RvNOQR3_VaINuQ9w1CKp6k4Y3qX8"


def get_credentials():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    return credentials


def rgb_to_hex(rgb):
    red = rgb.get('red', 0)
    green = rgb.get('green', 0)
    blue = rgb.get('blue', 0)

    # return "#{:02x}{:02x}{:02x}".format(red * 255, green * 255, blue * 255)
    return "#{:02x}{:02x}{:02x}".format(int(red * 255), int(green * 255), int(blue * 255))


def get_background_color(service, col, row):
    try:
        cell_a_format = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID,
                                                   fields="sheets.data.rowData.values.effectiveFormat.backgroundColor",
                                                   ranges=f"Sheet1!{col}{row}").execute()
        cell_a_background_color = cell_a_format["sheets"][0]["data"][0]["rowData"][0]["values"][0]["effectiveFormat"][
            "backgroundColor"]
        hex_color = rgb_to_hex(cell_a_background_color)
        return hex_color
    except HttpError as error:
        print(f"Error: {error}")
        print(error.content)


def add_and_update_values(service, spreadsheet_id, row):
    try:
        num1 = int(service.values().get(spreadsheetId=spreadsheet_id, range=f"Sheet1!A{row}").execute().get("values")[0][0])
        num2 = int(service.values().get(spreadsheetId=spreadsheet_id, range=f"Sheet1!B{row}").execute().get("values")[0][0])
        calculation_result = num1 + num2
        print(f"Processing {num1} + {num2}")

        service.values().update(spreadsheetId=spreadsheet_id, range=f"Sheet1!C{row}", valueInputOption="USER_ENTERED",
                                body={"values": [[f"{calculation_result}"]]}).execute()

        service.values().update(spreadsheetId=spreadsheet_id, range=f"Sheet1!D{row}", valueInputOption="USER_ENTERED",
                                body={"values": [["Done"]]}).execute()

    except HttpError as error:
        print(f"Error: {error}")
        print(error.content)


def calculate_totals(service, col):
    try:
        roommate_colors = {
            "#34a853": "caleb",
            "#4285f4": "david",
            "#46bdc6": "lucus",
            "#fabb04": "mason",
            "#ea4335": "matthew",
            "#ff6c01": "peter",
            "#ffffff": "all"
        }
        sheets = service.spreadsheets()
        row = 1  # Start from the first row
        while True:
            cell_value = sheets.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=f"Sheet1!{col}{row}"
            ).execute().get("values", [[]])[0]

            # Check if the cell is empty
            if not cell_value:
                break

            # Process the cell value
            num = float(cell_value[0])
            color = get_background_color(service, col, row)
            roommate = roommate_colors[color]
            print(f"Who is splitting: {roommate}")
            print(f"Processing {col}{row}: {num}")
            calculate_individual_payment(service, roommate, num)

            # Increment row for the next iteration
            row += 1
    except HttpError as error:
        print(f"Error: {error}")
        print(error.content)


def calculate_individual_payment(service, roommate, num):
    sheets = service.spreadsheets()
    roommate_cells = {
        "caleb": 2,
        "david": 3,
        "lucus": 4,
        "mason": 5,
        "matthew": 6,
        "peter": 7
    }
    if roommate == "all":
        new_num = num / 6
        for row in range(2, 8):
            cell_value = sheets.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=f"Sheet1!B{row}"
            ).execute().get("values", [[]])[0]
            current_payment = float(cell_value[0])

            calculation_result = current_payment + new_num
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!B{row}", valueInputOption="USER_ENTERED",
                                body={"values": [[f"{calculation_result}"]]}).execute()
    else:
        row = roommate_cells[roommate]
        cell_value = sheets.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Sheet1!B{row}"
        ).execute().get("values", [[]])[0]
        current_payment = float(cell_value[0])

        calculation_result = current_payment + num
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!B{row}", valueInputOption="USER_ENTERED",
                                body={"values": [[f"{calculation_result}"]]}).execute()


def main():
    credentials = get_credentials()
    service = build("sheets", "v4", credentials=credentials)

    calculate_totals(service, "E")


if __name__ == '__main__':
    main()