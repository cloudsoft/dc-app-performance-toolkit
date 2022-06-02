from .conftest import print_timing
from .navigator import Navigator


def aws_opsitems(driver):

    navigator = Navigator(driver)

    @print_timing("selenium_aws_opsitem")
    def opsitem():
        """create an ops item issue and resolve it"""
        navigator.create_ops_item(
            project="AWS",
            summary="new ops item",
            description="ops item description")
    opsitem()
