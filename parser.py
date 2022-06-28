from selenium.webdriver.common.keys import Keys
import time


SCROLL_PAUSE_TIME = 0.5


def pars_friends(driver) -> list:
    counter_buttons = driver.find_elements_by_class_name("page_counter")
    friend_button = None
    for button in counter_buttons:
        accessible_name_list = button.accessible_name.split()
        if (accessible_name_list[len(accessible_name_list) - 1] == "друзей" or
            accessible_name_list[len(accessible_name_list) - 1] == "друга" or
            accessible_name_list[len(accessible_name_list) - 1] == "друг") and \
                accessible_name_list[len(accessible_name_list) - 2] != "общих":
            friend_button = button
            break
    if friend_button is None:
        return []

    friend_button.click()
    time.sleep(SCROLL_PAUSE_TIME)

    layer_stl = driver.find_element_by_id("layer_stl")
    last_height = layer_stl.value_of_css_property("margin-top")

    while True:
        driver.find_element_by_class_name("fans_fan_ph").send_keys(Keys.END)

        time.sleep(SCROLL_PAUSE_TIME)

        new_height = layer_stl.value_of_css_property("margin-top")
        if new_height == last_height:
            time.sleep(1)

            driver.find_element_by_class_name("fans_fan_ph").send_keys(Keys.END)

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = layer_stl.value_of_css_property("margin-top")
            if new_height == last_height:
                break
        last_height = new_height

    fans_fan_lnks = driver.find_elements_by_class_name("fans_fan_lnk")
    friends_lnk_list = []
    for fans_fan_lnk in fans_fan_lnks:
        friend_name = fans_fan_lnk.accessible_name
        friend_lnk = fans_fan_lnk.get_attribute("href")
        friends_lnk_list.append([friend_lnk, friend_name])

    driver.find_element_by_class_name("fans_fan_ph").send_keys(Keys.ESCAPE)

    return friends_lnk_list


def pars_groups(driver, profile_lnk: str, profile_name: str, user_groups_lnk_list: list) -> list:
    try:
        driver.get(url=profile_lnk)
    except Exception:
        return []
    time.sleep(1)
    profile_more_info_link = driver.find_elements_by_class_name("profile_more_info_link")
    if profile_more_info_link:
        profile_more_info_link[0].click()
    else:
        return []

    profile_label_link = driver.find_elements_by_class_name("profile_label_link")
    if profile_label_link:
        profile_label_link[0].click()
    else:
        return []

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(1)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                time.sleep(1)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(SCROLL_PAUSE_TIME)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
        last_height = new_height

    group_rows_title = driver.find_elements_by_class_name("group_row_title")
    friends_groups_list = []
    for group_row_title in group_rows_title:
        group_lnk = group_row_title.get_attribute("href")
        if group_lnk in user_groups_lnk_list:
            group_name = group_row_title.accessible_name
            friends_groups_list.append([group_lnk, group_name, profile_lnk, profile_name])

    return friends_groups_list


def pars_user_groups(driver, profile_lnk: str) -> list:
    try:
        driver.get(url=profile_lnk)
    except Exception:
        return []
    time.sleep(1)
    profile_more_info_link = driver.find_elements_by_class_name("profile_more_info_link")
    if profile_more_info_link:
        profile_more_info_link[0].click()
    else:
        return []

    profile_label_link = driver.find_elements_by_class_name("profile_label_link")
    if profile_label_link:
        profile_label_link[0].click()
    else:
        return []

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(1)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height

    groups_lnk = driver.find_elements_by_class_name("group_row_title")
    groups_lnk_list = []
    for group_lnk in groups_lnk:
        lnk = group_lnk.get_attribute("href")
        groups_lnk_list.append(lnk)

    return groups_lnk_list


def parsing(driver, url: str) -> list:
    try:
        driver.get(url=url)
        driver.maximize_window()
        login_button = driver.find_element_by_class_name("quick_login_button")
        login_button.click()
        while True:
            time.sleep(3)
            if driver.find_elements_by_id("top_profile_link"):
                break

        friends_lnk_list = pars_friends(driver)
        if len(friends_lnk_list) == 0:
            return []

        user_groups_lnk_list = pars_user_groups(driver, url)
        if len(user_groups_lnk_list) == 0:
            return []

        friends_groups_list = []
        for friend in friends_lnk_list:
            friend_groups_lnk_list = pars_groups(driver, friend[0], friend[1], user_groups_lnk_list)
            if friend_groups_lnk_list:
                friends_groups_list.extend(friend_groups_lnk_list)

        return friends_groups_list

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
