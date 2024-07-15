from nogu import config
import pytest


if __name__ == "__main__":
    config.mysql_url += "-test"  # use a different database for testing
    pytest.main(["-s", "-q", "-p no:warnings"])
