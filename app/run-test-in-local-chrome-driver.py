# run this from the local command line
#
# e.g.:
# source venv/bin/activate
# cd app
# python run-test-in-local-chrome-driver.py

from selenium import webdriver

from extension.jsm.extension_ui_customers import app_specific_action
from selenium_ui.conftest import Dataset
from selenium_ui.jsm.modules_customers import login, log_out
# from selenium_ui.jsm_ui_agents import test_0_selenium_agent_a_login, \
#     test_2_selenium_agent_z_logout, test_1_selenium_agent_add_comment

# from selenium_ui.jsm_ui_agents import test_1_selenium_aws_opsitems
from selenium_ui.jsm_ui_customers import test_0_selenium_customer_a_login, test_2_selenium_customer_z_log_out

driver = webdriver.Chrome()

jsm_datasets = Dataset().jsm_dataset()

# print(">>> login...")
# login(driver, jsm_datasets)
print(">>> app_specific_action...")
app_specific_action(driver, jsm_datasets)
print(">>> log_out...")
# log_out(driver, jsm_datasets)
# print(">>> done")

# test_0_selenium_agent_a_login(driver, jsm_datasets, [])
# test_1_selenium_aws_opsitems(driver, jsm_datasets, [])
# test_1_selenium_agent_add_comment(driver, jsm_datasets, [])
# test_2_selenium_agent_z_logout(driver, jsm_datasets, [])
