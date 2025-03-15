from diff import mainStart
import os
import getpass
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Function to get secure user input
def get_credentials():
    username = input("Username: ")
    password = getpass.getpass("Password: ")  # Hides password input
    return username, password

# Function to initialize the WebDriver
def initialize_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run browser in headless mode (without GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Path to the ChromeDriver executable
    driver_path = "./chromedriver.exe"  # Update this with your path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to login using Selenium
def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(2)

    # Locate the username, password fields, and login button
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    # Enter credentials and log in
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()
    
    # Wait for login to complete
    time.sleep(5)
    
    # Check if login is successful (e.g., by checking if the profile icon is visible)
    try:
        driver.find_element(By.XPATH, "//img[contains(@alt, 'profile picture')]")
        print("[+] Login successful.")
    except:
        print("[!] Login failed. Please check your credentials.")
        driver.quit()
        exit()

def scrollToEndOfFollowing(driver,nameOfScrolled):
    scrollable_element_xpath = "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"

    # Find the scrollable element
    scrollable_element = driver.find_element(By.XPATH, scrollable_element_xpath)

    # Scroll continuously until reaching the bottom
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

    while True:
        # Scroll to the bottom of the scrollable element
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
        time.sleep(6)  # Wait for the content to load (adjust as needed)
        print(f"[+] Scrolling {nameOfScrolled}")
        # Check if the scroll height is the same as before, meaning we've reached the bottom
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
        if new_height == last_height:
            break  # Exit the loop if no new content was loaded
        last_height = new_height  # Update the last height for the next iteration
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element) #scroll one more time for safe measure
    print(f"[+] Reached end of {nameOfScrolled}!")

def checkIfInstaBroken():
    text_to_find = "You'll see all the people who follow you here."
    retVal = False
    try:
        element = driver.find_element(By.XPATH, f"//div[contains(text(), \"{text_to_find}\")]")
        retVal = True
    except NoSuchElementException:
        print("Insta is not Broken.")
    
    return retVal
    


def readAndPrintNames(driver,isFollowers):
    # if isFollowers:
    #     xpath_pattern = "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{index}]/div/div/div/div[2]/div/div/span/span"
    #     xpath_pattern1 = "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{index}]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span"
    # else:              
    #     xpath_pattern = "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{index}]/div/div/div/div[2]/div/div/span/span"
    #     xpath_pattern1 = "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{index}]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span"                    
    names = driver.find_elements(By.XPATH, "//div[@role='dialog']//span/span")
    userNames = driver.find_elements(By.XPATH,"//div[@role='dialog']//a[contains(@href, '/')]/div/div/span")
    
    index = 1  # This assumes the first element starts with index 1

    end_of_list_reached = False
    listOfUsers = []
    # Loop to go through the elements till the end of the list
    for i in range(min(len(userNames), len(names))):
        print(f"User number {i+1}:{userNames[i].text}:{names[i].text}")
        
        listOfUsers.append(f"{userNames[i].text}:{names[i].text}")

    
    # while not end_of_list_reached:
    #     try:
    #         # Construct the XPath for the current item
    #         current_xpath = xpath_pattern.format(index=index)
    #         current_xpath1 = xpath_pattern1.format(index=index)
    #         # Try to find the element
    #         userElem = driver.find_element(By.XPATH, current_xpath1)
    #         element = driver.find_element(By.XPATH, current_xpath)
            
    #         # Process the element (e.g., print the text or any other action)
    #         print(f"Element at index {index}: UserName:{userElem.text}:Name:{element.text}")
    #         listOfUsers.append(userElem.text + ":"+element.text)
    
    #         # Increment the index to move to the next item
    #         index += 1
        
    #     except Exception as e:
    #         # If an exception occurs, we can assume we've reached the end of the list
    #         print("Reached the end of the list or element not found.")
    #         end_of_list_reached = True

    print("Finished iterating through the list.")
    numOfUsers = len(listOfUsers)
    print(f"Total of {numOfUsers} users found")
    return listOfUsers


# Function to fetch followers and following
def get_follow_data(driver, target_user):
    driver.get(f"https://www.instagram.com/{target_user}/")
    time.sleep(2)
    
    # Get followers and following links
    followers_link = driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
    following_link = driver.find_element(By.PARTIAL_LINK_TEXT, "following")
    try:    
        followers_link.click()
        time.sleep(6)
        if checkIfInstaBroken():
            raise Exception("Followers not working") 

        scrollToEndOfFollowing(driver=driver,nameOfScrolled="followers")
        time.sleep(6)
        followers = readAndPrintNames(driver=driver,isFollowers=True)
    except:
        print("[!] Failed to get followers.")
        followers=[]
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(6)
    
    try:
        following_link.click()
        time.sleep(6)
        if checkIfInstaBroken():
            raise Exception("Followers not working") 
        scrollToEndOfFollowing(driver=driver, nameOfScrolled="following")
        time.sleep(6)
        following = readAndPrintNames(driver=driver,isFollowers=False)
    except:
        print("[!] Failed to get following.")
        following =[]
        
    

    time.sleep(2)

    return followers, following

# Function to save data to file
def save_to_file(followers, following, target_user):
    filename = f"{target_user}_instagram_data.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Followers:\n")
        file.write("\n".join(followers) + "\n\n")
        file.write("Following:\n")
        file.write("\n".join(following))
    
    print(f"[+] Data saved to {filename}")

# Main script execution
if __name__ == "__main__":
    
    x = int(input("Would you like to diff or create a new file (0 for diff, 1 for new data file): "))
    if x == 0:
        oldFile = input("Enter oldFile path: ")
        NewFile = input("Enter NewFile path: ")
        mainStart(oldFile,NewFile)
    elif x == 1:
    
        USERNAME, PASSWORD = get_credentials()
        TARGET_USER = input("Target Account: ")

        driver = initialize_driver()
        login_instagram(driver, USERNAME, PASSWORD)
        
        followers, following = get_follow_data(driver, TARGET_USER)
        save_to_file(followers, following, TARGET_USER)
        
        driver.quit()  # Close the WebDriver after use
    else:
        print("Improper usage, try again")
