import slugify
import requests
import subprocess
from subprocess import PIPE

def make_dolthub_pull_request(title, branch_name, description = ""):
    """
    Sends a pull request to DoltHub.
    """
    headers ={
    # "Host":"www.dolthub.com",
    "Referer": "https://www.dolthub.com/repositories/dolthub/menus/pulls/new",
    # "Origin": "https://www.dolthub.com",
    "Cookie": "__stripe_mid=b360e7e7-97ac-4175-b67c-07e825a2a8c713ff79; G_ENABLED_IDPS=google; amplitude_id_fef1e872c952688acd962d30aa545b9edolthub.com=eyJkZXZpY2VJZCI6IjcxMTQ5Njc3LWU2YTItNDgyYS04ZTE4LTM2ZTg4MTU0ZDRjM1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTYyNDE1MjEyNDgxNCwibGFzdEV2ZW50VGltZSI6MTYyNDE1MjEyNTU1NCwiZXZlbnRJZCI6MSwiaWRlbnRpZnlJZCI6MSwic2VxdWVuY2VOdW1iZXIiOjJ9; dolthubToken=ldst.v1.9le5o4rs4187dvmtpesfco0o21mboovri39ca7atmes8hdp2i5cg; __stripe_sid=e72c0db8-0fbc-40ff-8dff-4e1eb35424b681e16a",
    }

    json={
      "operationName": "CreatePullRequestWithForks",
      "variables": {
        "title": title,
        "description": description,
        "fromBranchName": branch_name,
        "toBranchName": "master",
        "fromBranchOwnerName": "spacelove",
        "fromBranchRepoName": "menus",
        "toBranchOwnerName": "dolthub",
        "toBranchRepoName": "menus",
        "parentOwnerName": "dolthub",
        "parentRepoName": "menus"
      },
      "query": "mutation CreatePullRequestWithForks($title: String!, $description: String!, $fromBranchName: String!, $toBranchName: String!, $fromBranchRepoName: String!, $fromBranchOwnerName: String!, $toBranchRepoName: String!, $toBranchOwnerName: String!, $parentRepoName: String!, $parentOwnerName: String!) {\n  createPullWithForks(\n    title: $title\n    description: $description\n    fromBranchName: $fromBranchName\n    toBranchName: $toBranchName\n    fromBranchOwnerName: $fromBranchOwnerName\n    fromBranchRepoName: $fromBranchRepoName\n    toBranchOwnerName: $toBranchOwnerName\n    toBranchRepoName: $toBranchRepoName\n    parentRepoName: $parentRepoName\n    parentOwnerName: $parentOwnerName\n  ) {\n    _id\n    pullId\n    __typename\n  }\n}\n"
    }

    response = requests.post("https://www.dolthub.com/graphql/", headers = headers, json = json)
    
    print("\n")
    errors = response.json().get('errors')
    if errors:
        print(f"Pull request for {title} failed:\n")
        for error in errors:
            print(error['message'] + "\n")
        return response
    
    elif response.status_code == 200:
        print(f"Successfully submitted pull request for: {title}\n")
        return response
    else:
        print("Something went wrong\n")
        return response

# from selenium import webdriver
# driver = webdriver.Firefox()
# from time import sleep
# import pandas as pd
# import re
# from selenium.common.exceptions import NoSuchElementException
# invalid_chars = [":registered:", ":tm:", ":copyright:","℠", "*", '"']

def scrape_uber_eats_menu(url, city, state):
    driver.get(url)
    driver.maximize_window()
    sleep(1)

    try:
        popup = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/div[2]/div[2]/button")
        popup.click()
    except:
        pass

    try:
        name = driver.find_element_by_xpath(
            "/html/body/div[1]/div/main/div[2]/div/div[3]/div[3]/div[1]/div[2]/div[2]/h1"
            ).text
        print(f"Looking up {name}...")
    except:
        print(f"No restaurant found at {url}")
        return

    menu_xpath = "/html/body/div[1]/div/main/div[4]/ul"
    try:
        menu = driver.find_element_by_xpath(menu_xpath)
    except:
        return

    item_location = driver.find_element_by_xpath(menu_xpath + "/li[1]/ul/li[1]/div/div/div/div[1]")

    menu_items = menu.find_elements_by_class_name(item_location.get_attribute("class").replace(" ", "."))

    item_name_class = driver.find_element_by_xpath(
        menu_xpath + "/li[1]/ul/li[1]/div/div/div/div[1]/div[1]/h4/div"
        ).get_attribute("class").replace(" ", ".")

    try:
        item_price_class = driver.find_element_by_xpath(
            menu_xpath + "/li[1]/ul/li[1]/div/div/div/div[1]/div[3]/div"
            ).get_attribute("class").replace(" ", ".")
    except NoSuchElementException:
        try: 
            item_price_class = driver.find_element_by_xpath(
                menu_xpath + "/li[1]/ul/li[1]/div/div/div/div[1]/div[2]/div"
                ).get_attribute("class").replace(" ", ".")
        except NoSuchElementException:
            return

    try:
        item_cals_class = driver.find_element_by_xpath(
            menu_xpath + "/li[1]/ul/li[1]/div/div/div/div[1]/div[2]/div[2]"
            ).get_attribute("class").replace(" ", ".")
    except NoSuchElementException:
        item_cals_class = None

    items_dict = {'name': [], 'price_usd': [], 'calories': []}

    for item in menu_items:  

        calories = ''

        # Get item name  
        try: 
            item_name = item.find_element_by_class_name(item_name_class).text
            item_name = item_name.upper().strip()
        except NoSuchElementException:
            continue
        
        if " CAL " in item_name:
            item_name, calories_raw = item_name.split(" CAL ")
            try:
                calories_max = re.findall("\d+", calories_raw)[-1]
                calories = float(calories_max)
            except: 
                pass

        # Price
        try:
            item_price_text = item.find_element_by_class_name(item_price_class).text
            item_price_text_cleaned = item_price_text.lower().strip()
            if item_price_text_cleaned in ["customize", "unavailable", ""]:
                continue
            item_price = float(item_price_text_cleaned.replace("$", ""))
        except (NoSuchElementException, ValueError):
            continue
        
        # Calories
        if item_cals_class is not None and calories == '':

            try:
                calories_raw = item.find_element_by_class_name(item_cals_class).text
                calories_max = re.findall("\d+", calories_raw)[-1]
                calories = float(calories_max)
            except NoSuchElementException:
                pass

        items_dict['name'].append(item_name)
        items_dict['price_usd'].append(item_price)
        items_dict['calories'].append(calories)

    df = pd.DataFrame(items_dict)

    df['restaurant_name'] = name.upper().strip()
    df['identifier'] = f'UBEREATS, {city.upper()}, {state.upper()}'
    df['sugars_g'] = ''
    df['cholesterol_mg'] = ''
    df['protein_g'] = ''
    df['fiber_g'] = ''
    df['fat_g'] = ''
    df['carbohydrates_g'] = ''
    df['sodium_mg'] = ''

    if len(df) == 0:
        print("No prices or caloric information found.")
        return

    for char in invalid_chars:
        df['name'] = df['name'].str.replace(char, "")
        df['restaurant_name'] = df['restaurant_name'].str.replace(char, "")

    branch_name = f"UberEATS-{city.title()}-{name.title()}"
    slug = slugify.slugify(branch_name)

    print("="*10 + "Data sample" + "="*10)
    print(df.loc[:,"name":"identifier"].head().to_markdown())
    print("="*30)

    df = df.drop_duplicates('name')

    df.to_csv(f"{slug}.csv", index = False)

    csv = os.path.abspath(f"{slug}.csv")

    print(f'Creating dolthub pull request for {name}')
    command = f"""
        cd ../menus;
        dolt checkout master;
        dolt branch -df {branch};
        dolt checkout -b {branch};
        dolt table import -u menu_items {csv};
        dolt add .;
        dolt commit -m "{name} price data";
        dolt push -f origin {branch};
        """
    description = "Scraped from UberEATS."
    ret = subprocess.run(command, stdout=PIPE, stderr=PIPE, shell=True)
    print(ret.stdout.decode())

    response = make_dolthub_pull_request(name, branch, description = description)


def create_and_push_new_branch(db, branch_name, csv_file, commit_message = "initial commit"):
    """
    Helper function. Creates a new branch.
    db: location of database
    branch_name: str
    csv_file: file
    commit_message: str
    """
    print(f'\nCreating branch {branch_name}...\n')
    command = f"""
        cd {db};
        dolt checkout master;
        dolt branch -df {branch_name};
        dolt checkout -b {branch_name};
        dolt table import -u menu_items {csv_file};
        dolt commit -am "{commit_message}";
        dolt push -f origin {branch_name};
        """
    # ret = subprocess.run(command, stdout=PIPE, stderr=PIPE, shell=True)
    ret = subprocess.run(command, capture_output = True, shell = True)
    print(ret.stdout.decode() + "\n")

def create_commit_push_branch(name, dataframe, database_location, table_name, commit_string = "first commit"):
    slug = slugify.slugify(name)
    pathname = database_location + "/"
    filename = f"{slug}.csv"
    dataframe.to_csv(pathname + filename, index = False)
    print(f'Creating branch {slug} for {name} and uploading to origin.')
    command = f"""
    cd {database_location};
    dolt checkout master;
    dolt branch -df {slug};
    dolt checkout -b {slug};
    dolt table import -u {table_name} {slug}.csv;
    dolt add .;
    dolt commit -m "{name} {commit_string}";
    dolt push -f origin {slug};
    cd ..;
    """
    ret = subprocess.run(command, stdout=PIPE, stderr=PIPE, shell=True)
    print(ret.stdout.decode())
    response = make_pull_request(name, slug)
    return response