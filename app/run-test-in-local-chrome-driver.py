# run this from the local command line
#
# e.g.:
# source venv/bin/activate
# cd app
# python run-test-in-local-chrome-driver.py

from selenium import webdriver

from selenium_ui.conftest import Dataset
from selenium_ui.jsm_ui_agents import test_0_selenium_agent_a_login, \
    test_2_selenium_agent_z_logout, test_1_selenium_agent_add_comment

from selenium_ui.jsm_ui_agents import test_1_selenium_aws_opsitems

driver = webdriver.Chrome(executable_path="../chromedriver")

jsm_datasets = Dataset().jsm_dataset()

test_0_selenium_agent_a_login(driver, jsm_datasets, [])
test_1_selenium_aws_opsitems(driver, jsm_datasets, [])
#test_1_selenium_agent_add_comment(driver, jsm_datasets, [])
test_2_selenium_agent_z_logout(driver, jsm_datasets, [])
