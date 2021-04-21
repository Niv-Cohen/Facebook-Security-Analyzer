from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from ..modules.Connection import Connection
from ..modules.Account import account_encoder
from ..modules.User import User


import time
from datetime import date
from ..modules.Account import Account
import json

year_not_registered = "//*[contains(text(),'Born on ') or contains(text(),'No posts available')]"

root_user = "Niv Cohen"

friends_user_xpath = "//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id']"

family_member_xpath = "//div[@class='nc684nl6']"

friendship_duration_xpath = "//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v knj5qynh oo9gr5id hzawbc8m']"

all_users = set([])


def scrap(name, email, password):
    driver = init_sel()
    # login(driver, email, password)
    login(driver, email, password)
    time.sleep(5)
    redirect(driver, "Niv Cohen")
    user = extract_user(driver, 0)
    with open('BasicGraph.json', 'w') as outfile:
        json.dump(user, outfile, indent = 4,cls = account_encoder)
    return json.dumps(user, indent=4, cls = account_encoder)


def init_sel():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()
    return driver


def login(driver, email, password):
    driver.get("https://www.facebook.com/")
    search_email = driver.find_element_by_id("email")
    time.sleep(2)
    search_email.send_keys(email)
    search_pass = driver.find_element_by_id("pass")
    time.sleep(3)
    search_pass.send_keys(password)
    time.sleep(4)
    search_button = redirect_by_xpath(driver,"//div[@class='_6ltg']")
    search_button[0].click()

def background_click(driver):
    time.sleep(0.5)
    actions = ActionChains(driver)
    actions.double_click()
    actions.perform()
    time.sleep(0.5)

def redirect(driver, next_page, inital_click = True):
    if inital_click:
        background_click(driver)

    try:
        element = WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable((By.LINK_TEXT, next_page))
        )
        print(element.text)
        element.click()
        time.sleep(2)
    except:
        return False
    finally:
        print("redirected to " + next_page)


def redirect_by_xpath(driver, xpath):
    time.sleep(0.5)
    try:
        sleep_time = 7
        if xpath == year_not_registered:
            sleep_time = 3
        element = WebDriverWait(driver, sleep_time).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        print(xpath)
        return element
    finally:
        print(xpath)


def extract_total_friends(driver):
    total_friends = driver.find_element_by_partial_link_text('Friends').text
    temp = total_friends.partition("Friends\ufeff")
    if temp[2] == '':
        return -1
    return int(temp[2])


def extract_profile_summary(driver, connection_degree):
    summary = {}
    fields = ['work', 'education', 'current_town', 'homeTown', 'status']
    elements = redirect_by_xpath(driver, "//div[@class='c9zspvje']")
    time.sleep(2)
    for i in range(len(elements)):
        temp_data = elements[i].text.partition("\nShared")
        if temp_data[0] != '' and not temp_data[0].startswith('Add ') and not temp_data[0].startswith('No '):
            summary[fields[i]] = temp_data[0]
    total_friends = extract_total_friends(driver)
    age_of_account = extract_age_of_account(driver, connection_degree)
    print(summary)
    print("Age: "+str(age_of_account))
    return summary, total_friends, age_of_account


def scrap_about(driver, connection_degree):
    time.sleep(2)
    redirect(driver, "About")
    return extract_profile_summary(driver, connection_degree)


def extract_friendship_duration(driver):
    upper_navigation_bar = redirect_by_xpath(driver, "//div[@class='ku2zlfd4 q3mryazl']/div/div")
    time.sleep(2)
    upper_navigation_bar[len(upper_navigation_bar) - 1].click()
    redirect(driver, 'See friendship', False)
    all_common_fields = redirect_by_xpath(driver, friendship_duration_xpath)
    for field in all_common_fields:
        if field.text.startswith("Your friend since "):
            beginning_of_friendship = field.text.replace("Your friend since ", "1 ")
            return calculate_age(beginning_of_friendship)
    return 0


def find_profile_filter(driver, filters):
    for filter in filters:
        if filter.text == 'Profile':
            return filter


def scroll_to_bottom(driver, elements_xpath):
    actions = ActionChains(driver)
    elements = driver.find_elements_by_xpath(elements_xpath)
    old_elements_amount = len(elements)
    while True:
        time.sleep(2)
        actions.send_keys(Keys.END)
        actions.perform()
        elements = driver.find_elements_by_xpath(elements_xpath)
        if len(elements) == old_elements_amount:
            break
        old_elements_amount = len(elements)
    return elements[len(elements) - 1].text


def extract_root_age(driver):
    upper_navigation_bar = redirect_by_xpath(driver, "//div[@class='ku2zlfd4 q3mryazl']/div/div")
    '''
    click the 3 dots icon
    '''
    upper_navigation_bar[len(upper_navigation_bar) - 1].click()
    redirect(driver, 'Activity log', False)
    filter_button = redirect_by_xpath(driver, "//span[text()='Filter']")
    filter_button[0].click()
    filters = redirect_by_xpath(driver,
                                "//div[@class='emxnvquj ni8dbmo4 tr9rh885 ciko2aqh']/div/div/div/div/div/div/div/div")
    profile_filter = find_profile_filter(driver, filters)
    profile_filter.click()
    save_changes_button = redirect_by_xpath(driver, "//div[@class='n1l5q3vz n851cfcs f4c7eilb']/div")
    save_changes_button[0].click()

    redirect_by_xpath(driver, "//span[text()='Profile']")[0].click()
    date_enrolled = scroll_to_bottom(driver,
                                     "//div[@class='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t pfnyh3mw d2edcug0 e5nlhep0 aodizinl']")
    return calculate_age(date_enrolled)


def extract_node_age(driver):
    return get_age_of_account(driver)


def extract_age_of_account(driver, connection_degree):
    if connection_degree == 0:
        return extract_root_age(driver)
    return extract_node_age(driver)


def calculate_age(date_joined):
    date_arr = date_joined.split(' ')
    date_arr[1] = month_converter(date_arr[1])
    date_joined = date(int(date_arr[2]), date_arr[1], int(date_arr[0]))
    curr_date = date.today()
    number_of_days = curr_date - date_joined
    return number_of_days.days


def month_converter(month):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    return months.index(month) + 1


def insert_members(members):
    for member in members:
        if member.text not in all_users:
            all_users.add(member.text)


def get_age_of_account(driver):
    redirect(driver, "Posts")
    mid = None
    left = 2008
    right = date.today().year
    try:
        while left < right:
            filter_button = redirect_by_xpath(driver, "//span[text()='Filters']")[0]
            filter_button.click()

            if mid is None:
                redirect_by_xpath(driver, "//span[text()='Year']")[0].click()
            else:
                redirect_by_xpath(driver, "//span[text()='"+str(mid)+"']")[0].click()
            mid = left + (right - left) // 2
            print('clicking on year - '+str(mid))
            redirect_by_xpath(driver, "//span[text()='" + str(mid) + "']")[0].click()
            redirect_by_xpath(driver, "//span[text()='Done']")[0].click()
            time.sleep(1)
            try:
                redirect_by_xpath(driver, year_not_registered)
                left = mid + 1
            except:
                right = mid
    except:
        return 0
    return calculate_age("1 January "+str(left))


def extract_user(driver, connection_degree, user = None):
    friendship_duration = 0
    user_name = user.text if user is not None else root_user
    all_users.add(user_name)
    if user:
        redirect(driver, user_name)
    if user_name == "Gal Rubin" or user_name == "Lior Duani":
        print("stop")

    attributes, total_friends, age_of_account = scrap_about(driver, connection_degree)
    if connection_degree == 1:
        friendship_duration = int(extract_friendship_duration(driver))
        driver.back()

    elif connection_degree == 0:
        driver.back()
        driver.back()
    else:
        driver.back()
        return Account(user_name, {},
                       Connection(attributes, friendship_duration),
                       User(total_friends, age_of_account))
    if user_name == "Noa Kenner":
        print("Stop to check ")
    network = scrap_network(driver, connection_degree + 1)
    if connection_degree == 2:
        driver.back()
        driver.back()
        driver.back()
    elif connection_degree != 0:
        driver.back()
        driver.back()
        driver.back()

    return Account(user_name, network,
                   Connection(attributes, friendship_duration),
                   User(total_friends, age_of_account))


def scrap_network(driver, connection_degree):
    friends = {}
    redirect(driver, 'About')
    time.sleep(1)
    friends['family'] = extract_field_members(driver, connection_degree, 'Family')
    time.sleep(1)
    redirect(driver, 'Friends')
    friends['childhood_friends'] = extract_field_members(driver, connection_degree, 'Home Town')
    friends['childhood_friends'] += extract_field_members(driver, connection_degree, 'High School')
    friends['neighbors'] = extract_field_members(driver, connection_degree, 'Current City')
    if connection_degree == 1:
        print("stop")
    friends['colleague'] = extract_field_members(driver, connection_degree, 'Work')
    friends['co_students'] = extract_field_members(driver, connection_degree, 'University')

    return friends


def extract_field_members(driver, connection_degree, field):
    if field == 'Family':
        redirect(driver, "Family and relationships", False)
    else:
        is_exist = redirect(driver, field)
        if is_exist==False:
            return []

    field_members = []
    try:
        members = redirect_by_xpath(driver, family_member_xpath if field == 'Family' else friends_user_xpath)
    except:
        return []
    counter = 0
    index = 0

    if connection_degree == 1:
        insert_members(members)

    while index < len(members) and counter <5:
        members = redirect_by_xpath(driver, family_member_xpath if field == 'Family' else friends_user_xpath)
        time.sleep(1)
        if members[0].text == '':
            del members[0]
        if connection_degree != 1 and members[index].text in all_users:
            index += 1
            continue
        else:
            field_members.append(extract_user(driver, connection_degree, members[index]))
            time.sleep(2)
            if field != 'Family':
                try:
                    mutual_friends_of_members = redirect_by_xpath(driver, "//div[@class='aahdfvyu']")
                    member_mutual_friends = mutual_friends_of_members[index].text
                    member_mutual_friends = member_mutual_friends.replace(' mutual friends', '')
                    member_mutual_friends = member_mutual_friends.replace(' mutual friend', '')
                    member_mutual_friends = int(member_mutual_friends)
                    print("mutual friends: "+str(member_mutual_friends))
                    field_members[counter].set_mutual_friends(member_mutual_friends)
                except:
                    background_click(driver)
                    driver.back()
            counter += 1
            index += 1
    print(field_members)
    if field != 'Family':
        driver.back()
    return field_members


if __name__ == '__main__':
    scrap("Niv Cohen", "niv1018@gmail.com", "Nfn151294Nfn")
