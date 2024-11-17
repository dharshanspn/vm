from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import pytz
import requests
import multiprocessing

troubleshooting_both_token = '7972332699:AAHs1ZGYQFXRtVELFou8zZ08IrWAE__cDRc'
troubleshooting_chatID =  '6966110728'


def telegram_both_sendtext(both_message, both_token, both_chatID):
    send_text = 'https://api.telegram.org/bot' + both_token + '/sendMessage?chat_id=' + both_chatID + \
                '&parse_mode=MarkdownV2&text=' + str(both_message).replace('.', '\\.')  # Escape the dot character
    response = requests.get(send_text)
    return response.json()

def login_to_chegg(username, password,driver):
    try:


        # Open the Chegg website and log in
        driver.get("https://expert.chegg.com/auth")
        time.sleep(3)

        #print(driver.find_element(By.XPATH, "/html/body").text)

        # Username
        element = driver.find_element(By.XPATH, "/html/body/div/main/section/div/div/div/form/div[1]/div/div[1]/div/input")  # Replace with the correct XPath
        element.send_keys(username)
        #element.send_keys(Keys.ENTER)
        time.sleep(3)

        # Password
        passw = driver.find_element(By.XPATH, "/html/body/div/main/section/div/div/div/form/div[1]/div/div[2]/div/input")  # Replace with the correct XPath
        passw.send_keys(password)
        passw.send_keys(Keys.ENTER)
        time.sleep(3)
        # if login is succesfull, it sets flag to false and exits loop, thus exiting the function 
        return False
    except Exception as e:
        login_texts = f"Login Failed \\- {username}"
        # if login is unsuccesfull, it sets flag to True and comtinues loop, and send notification thus exiting the function
        telegram_both_sendtext(login_texts,troubleshooting_both_token,troubleshooting_chatID)
        return True



def refresh_chegg(driver,accept_option,start_time,end_time,user_both_token,user_both_chatID,account_name):
    start_time = int(start_time)
    end_time = int(end_time)
    i = 1
    while True:
        try:
            
            limit_texts = f"Limit hit on {account_name} for {i} time"
            question_texts = f"Question found on {account_name}"



            # Navigate to the authoring page
            driver.get("https://expert.chegg.com/qna/authoring/answer")
            time.sleep(3)
            while True:

                driver.get("https://expert.chegg.com/qna/authoring/answer")
                time.sleep(3)
                limit = driver.current_url
                limit_text = f"{limit}"

                if limit_text != "https://expert.chegg.com/qna/authoring/answer":
                    time.sleep(3)
                    driver.get("https://expert.chegg.com/qna/authoring/answer")
                    time.sleep(3)
                    limit = driver.current_url
                    limit_text = f"{limit}"
                    if limit_text != "https://expert.chegg.com/qna/authoring/answer":
                        time.sleep(3)
                        driver.get("https://expert.chegg.com/qna/authoring/answer")
                        time.sleep(3)
                        limit = driver.current_url
                        limit_text = f"{limit}"
                        if limit_text != "https://expert.chegg.com/qna/authoring/answer":
                            time.sleep(3)
                            driver.get("https://expert.chegg.com/qna/authoring/answer")
                            time.sleep(3)
                            limit = driver.current_url
                            limit_text = f"{limit}"

                            # Define the time zone (UTC+5:30)
                            tz = pytz.timezone('Asia/Kolkata')
                            # Get the current time in UTC+5:30
                            now = datetime.now(tz)
                            # Define the target time (12:30 PM)
                            target_time = now.replace(hour=12, minute=30, second=0, microsecond=0)
                            # If the current time is already past 12:30 PM, set the target time to the next day
                            if now > target_time:
                                target_time += timedelta(days=1)
                            # Calculate the difference in seconds
                            n = (target_time - now).total_seconds()
                            if i == 1 or 1 % 50 == 0:
                                telegram_both_sendtext(limit_texts,troubleshooting_both_token,troubleshooting_chatID)
                                i = i+1
                            #time.sleep(n)

                driver.get("https://expert.chegg.com/qna/authoring/answer")
                time.sleep(5)
                message = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/div[2]/div[1]")
                text_to_copy = message.text

                if text_to_copy == "Thank you for your efforts on Chegg Q&A! Unfortunately, no Qs are available in your queue at the moment.":
                    driver.refresh()
                    
                else:
                    #Teleram of User
                    telegram_both_sendtext(question_texts,user_both_token,user_both_chatID)
                    if(accept_option):
                        try:
                            # Check if the submit button is present
                            submit_button = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div/footer/div/div[1]/div[2]/button/span/span[1]"))
                            )

                            # Get the text of the button
                            button_text = submit_button.text
                            #print(button_text)

                            # Proceed only if the button text is "Start Solving"
                            if button_text == "Start Solving":
                                try:
                                    # Try clicking the button
                                    submit_button.click()
                                    #telegram_both_sendtext(question_texts,user_both_token,user_both_chatID)
                                    #print(f"Accepted")
                                except ElementClickInterceptedException:
                                    #print("Element is not clickable due to an overlay, using JavaScript click")
                                    # Fallback: click using JavaScript
                                    driver.execute_script("arguments[0].click();", submit_button)
                                    #telegram_both_sendtext(question_texts,user_both_token,user_both_chatID)
                                    #print("Clicked using JavaScript")

                            else:
                                #print(f"Button text is not 'SUBMIT'. It's '{button_text}'.")
                                driver.refresh()

                        except (NoSuchElementException, TimeoutException):
                            #print("Button not found, refreshing.")
                            driver.refresh()
                        except Exception as e:
                            time.sleep(1)
                            driver.refresh()
                            time.sleep(1)
                    time.sleep(720)
                    driver.refresh()


                # Define the time zone (UTC+5:30)
                tz = pytz.timezone('Asia/Kolkata')
                # Get the current time in UTC+5:30
                now = datetime.now(tz)
                current_hour = now.hour        
                if (current_hour >= end_time):
                    #print("OT")
                    return 2
                if (current_hour <= start_time ):
                    wait = (start_time - current_hour)*3600
                    time.sleep(wait)

                    #print("OT")
                    
        except Exception as e:
            time.sleep(1)
            driver.refresh()
    # Quit the WebDriver
    driver.quit()



x = 12  # Starting row index (inclusive) Row starts from 0 x=2 means Row 3
y = 17  # Ending row index (exclusive) 15 Row pomints to 14 row, but since it starts from 0 it points to 15 row


# Access secrets from environment variables
repo_owner = "dharshanspn"
repo_name = "colect"
file_path = "data.json"
token = "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"
login_admin_bohit_token = "7980653551:AAGlL9xLHU-aMD6VwULWtkVQzkdwD0O8X98"
admin_chatID = "6966110728"





# GitHub API URL to get raw content of the file
url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'

# Fetch the JSON file metadata from the private repo
response = requests.get(url)

if True:
    # Debug: Print the full response to check the structure
    print("Response JSON structure:", response.json())

    # Get the download URL for the file
    download_url = response.json().get('download_url')

    # Fetch the raw file content using the download URL
    file_response = requests.get(download_url)

    if file_response.status_code == 200:
        # Load the JSON data from the file content
        data = file_response.json()
    else:
        print(f"Failed to fetch the file content: {file_response.status_code}")
        exit(1)
else:
    print(f"Failed to fetch file metadata: {response.status_code}")
    print(response.text)  # Print the error message from the response body
    exit(1)

# First row contains the headers (column names)
headers = data[0]

# Define your range of rows to process (x to y)


accounts = []
for row in data[x:y]:
    # Skip row if any cell is empty or only contains spaces
    if any(cell is None or str(cell).strip() == "" for cell in row):
        continue

    # Skip row if "Status" is False
    status_index = headers.index("Status")
    if row[status_index] is False:
        continue

    # Add account to list if it passes both checks
    account = dict(zip(headers, row))
    accounts.append(account)
    
def refresh_account(account):
    username = account["Username"]
    password = account["Password"]
    user_both_chatID = str(account["user_both_chatID"])
    account_name = account["Account_name"]
    user_both_token = account["user_both_token"]  # Same token for all accounts
    start_time = account["start_time"]
    end_time = account["end_time"]
    accept_option = account["accept_option"]
    
    
    # Set up Chrome WebDriver for this account
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-images")  # Disables images loading
    options.add_argument("--disable-extensions")


    # Each account gets its own Chrome instance
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 600)


    # Attempt to log in
    flag_login = True
    while flag_login:
        flag_login = login_to_chegg(username, password, driver)
    login_texts = f"both currently active on {account_name}"
    #telegram_both_sendtext(login_texts,user_both_token,user_both_chatID)
    telegram_both_sendtext(login_texts,login_admin_bohit_token,admin_chatID)


    # Start refreshing for the account
    refresh_chegg(driver, accept_option, start_time, end_time, user_both_token, user_both_chatID, account_name)
    #exit_texts = f"Loop exit on {account_name}"
    #telegram_both_sendtext(exit_texts,user_both_token,user_both_chatID)  
if __name__ == "__main__":
    # Create a process for each account
    processes = []
    for account in accounts:
        process = multiprocessing.Process(target=refresh_account, args=(account,))
        processes.append(process)
        process.start()

    # Optionally join the processes to ensure the script waits for all to finish
    for process in processes:
        process.join()
