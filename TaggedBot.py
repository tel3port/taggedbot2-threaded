from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import csv
import globals as gls
from random import randint
import os
import traceback
import time
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


class MainTaggedBot2:
    current = 0
    new_tab = 1

    def __init__(self, username, password, my_proxy):
        self.username = username
        self.password = password
        self.my_proxy = my_proxy
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-dev-sgm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-gpu")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        my_proxy_address = self.my_proxy.get_address()
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": my_proxy_address,
            "ftpProxy": my_proxy_address,
            "sslProxy": my_proxy_address,

            "proxyType": "MANUAL",

        }
        # self.driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        print("my ip address", my_proxy_address)

    def login(self):
        print("logging me in....")
        self.driver.get(gls.login_url)
        self.driver.maximize_window()
        email_xpath = '//*[contains(@name,"username")]'
        pw_xpath = '//*[contains(@name,"password")]'
        sign_in_btn_xpath = '//*[contains(@id,"submit_button")]'

        time.sleep(25)

        # click login button
        try:
            # fill up the credential fields
            self.driver.find_element_by_xpath(pw_xpath).send_keys(self.password)
            time.sleep(5)
            self.driver.find_element_by_xpath(email_xpath).send_keys(self.username)
            self.driver.find_element_by_xpath(sign_in_btn_xpath).click()

            print("login success...")
        except Exception as e:
            print("the login issue is: ", e)
            print(traceback.format_exc())
            pass

    # -------------------- user link extractor and saver section -------------------------------------------------------

    @staticmethod
    def append_to_csv(saved_links_list, my_csv):
        try:
            this_csv = open(my_csv, gls.append)
            csv_writer = csv.writer(this_csv)
            for one_link in saved_links_list:
                csv_writer.writerow([str(one_link)])
                print("row (hopefully) written into csv")

        except Exception as em:
            print('append_to_csv Error occurred ' + str(em))
            print(traceback.format_exc())
            pass

        finally:
            print(" append_to_csv() done")

            pass

    @staticmethod
    def read_links_from_csv(my_csv):
        list_of_links = []
        try:
            with open(my_csv, gls.read) as rdr:
                reader = csv.reader(rdr, delimiter=",")
                for single_row in reader:
                    list_of_links.append(single_row)

        except IOError as x:
            print("read_links_from_csv problem reading the user_accounts csv", x)
            print(traceback.format_exc())
            pass

        except Exception as e:
            print("read_links_from_csv the problem is: ", e)
            print(traceback.format_exc())
            pass

        finally:
            print("number of links: ", len(list_of_links))
            return list_of_links

    @staticmethod
    def read_complements_from_csv(my_csv):
        list_of_complements = []
        try:
            with open(my_csv, gls.read) as rdr:
                reader = csv.reader(rdr, delimiter=",")
                for single_row in reader:
                    list_of_complements.append(single_row)

        except IOError as x:
            print("read_complements_from_csv problem", x)
            print(traceback.format_exc())
            pass

        except Exception as e:
            print("read_complements_from_csv the problem is: ", e)
            print(traceback.format_exc())
            pass

        finally:
            print("number of comps: ", len(list_of_complements))
            return list_of_complements

    @staticmethod
    def read_phrases_from_csv(my_csv):
        list_of_phrases = []
        try:
            with open(my_csv, gls.read) as rdr:
                reader = csv.reader(rdr, delimiter=",")
                for single_row in reader:
                    list_of_phrases.append(single_row)

        except IOError as x:
            print("read_phrases_from_csv problem", x)
            print(traceback.format_exc())
            pass

        except Exception as e:
            print("read_phrases_from_csv the problem is: ", e)
            print(traceback.format_exc())
            pass

        finally:
            print("number of phrases: ", len(list_of_phrases))
            return list_of_phrases

    # -------------------- bot functions section -----------------------------------------------------------------------

    def follow_and_dm_single_user(self, user_link, s_comp, random_lander):
        print("follow_and_dm_single_user started")
        time.sleep(7)
        try:
            self.driver.get(user_link)

            friend_button_xpath = '//*[contains(@id,"add-friend-button")]'
            message_btn_xpath = '//*[contains(@id,"message-button")]'
            dm_textbox_xpath = '//*[contains(@id,"im_input")]'
            send_btn_xpath = '//*[contains(@id,"im_send_button")]'

            friend_element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, friend_button_xpath)))
            time.sleep(15)

            friend_element.click()
            print(f"{user_link} friend requested!")
            time.sleep(7)

            global current
            current = self.driver.current_window_handle
            message_element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, message_btn_xpath)))
            message_element.click()
            time.sleep(5)

            global new_tab
            new_tab = [tab for tab in self.driver.window_handles if tab != current][0]
            self.driver.switch_to.window(new_tab)
            self.driver.find_element_by_xpath(dm_textbox_xpath).send_keys(f'{s_comp[0]}.Is this really you? {random_lander}')
            time.sleep(5)
            self.driver.find_element_by_xpath(send_btn_xpath).click()

            print(f"single dm sent to {user_link}")

            # self.driver.close()
            time.sleep(5)

            self.driver.switch_to.window(current)
            print("follow_and_dm_single_user finished")

        except Exception as e:
            print("follow_DM_single_user the problem is: ", e)
            print(traceback.format_exc())
            pass

        finally:
            pass

    def status_updater_text(self, homepage_link, single_update, single_lander):
        print("starting text status update")
        try:

            self.driver.get(homepage_link)

            status_textbox_xpath = '//*[contains(@placeholder,"you doing today?")]'
            post_btn_xpath = '//*[contains(@ng-click,"postStatus()")]'

            self.driver.execute_script("window.scrollBy(0,500)", "")
            time.sleep(10)

            self.driver.find_element_by_xpath(status_textbox_xpath).send_keys(f'{single_update[0]} {single_lander}')

            time.sleep(5)
            self.driver.find_element_by_xpath(post_btn_xpath).click()

            print("text status update done")

        except Exception as e:
            print("the status_updater_text issue is: ", e)
            print(traceback.format_exc())
            pass

    def user_status_liker_commenter(self):
        pass

    def clean_up(self):
        try:

            self.driver.get('http://www.tagged.com/home.html?dataSource=Explore&ll=nav')
            time.sleep(10)

            account_button_xpath = '//*[contains(@id,"nav_account")]'
            log_out_xpath = '//*[@id="navheader"]/div/div/ul/li[3]/div/ul/li[11]'

            account_element = self.driver.find_element_by_xpath(account_button_xpath)
            log_out_element = self.driver.find_element_by_xpath(log_out_xpath)

            time.sleep(5)
            actions = ActionChains(self.driver)
            actions.move_to_element(account_element).move_to_element(log_out_element).click().perform()

            time.sleep(7)
            self.driver.delete_all_cookies()
            time.sleep(5)

            # self.driver.switch_to.window(new_tab)
            # self.driver.quit()
            print("clean up hopefully done")
        except Exception as e:
            print("clean_up fn the problem is: ", e)
            print(traceback.format_exc())
            pass

        finally:
            pass

    # -------------------- bot's entry point ---------------------------------------------------------------------------


if __name__ == "__main__":
    while 1:
        req_proxy = RequestProxy()  # you may get different number of proxy when  you run this at each time
        proxies = req_proxy.get_proxy_list()  # this will create proxy list
        random_proxy = proxies[randint(0, len(proxies) - 1)]
        # for proxy in proxies:
        #     print(f'proxy address: {proxy.get_address()}')
        #     print(f'proxy country: {proxy.country}')

        accounts = {"carn3lian@gmail.com": "WbJPTg2.C#NTya.",
                    "mnkimani05@gmail.com": "!E*bW3ZFKaiz3CT",
                    "testerslimited@gmail.com": "9UCQ4W88gx#E3pJ",
                    "marlinforce2018@gmail.com": "35Fa4YvZ4Hfn4!m",
                    "firefinchcreatives@gmail.com": "35Fa4YvZ4Hfn4!m"
                    }

        list_of_keys = list(accounts.keys())

        random_email_key = list_of_keys[randint(0, len(list_of_keys) - 1)]

        # gets a random account and does the do
        tagged_bot = MainTaggedBot2(random_email_key, accounts.get(random_email_key), random_proxy)

        def tagged_actions_sequence():
            phrase_list = tagged_bot.read_phrases_from_csv(gls.phrases_csv)
            single_phrase = phrase_list[randint(0, len(phrase_list) - 1)]
            complement_list = tagged_bot.read_complements_from_csv(gls.complements_csv)
            single_comp = complement_list[randint(0, len(complement_list) - 1)]
            static_user_url_list = tagged_bot.read_links_from_csv(gls.user_urls_csv)
            single_user_url = static_user_url_list[randint(0, len(static_user_url_list) - 1)]

            tagged_bot.follow_and_dm_single_user(user_link=single_user_url[0], s_comp=single_comp, random_lander=gls.single_lander_source())

            time.sleep(randint(5, 20))

            tagged_bot.status_updater_text(gls.status_home_page, single_phrase, gls.single_lander_source())

            time.sleep(randint(5, 20))


        def start_cycle():
            print(f"starting cycle num")
            tagged_bot.login()
            time.sleep(randint(30, 70))
            tagged_actions_sequence()
            time.sleep(randint(30, 70))
            tagged_bot.clean_up()
            time.sleep(randint(30, 70))

            print(f" cycle num done")

        start_cycle()
