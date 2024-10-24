from time import sleep

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ChartScreenshotCapture:
    def __init__(self, symbol):
        self.driver = None

    def setup_driver(self):
        chromedriver_autoinstaller.install()
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def open_page(self):
        self.driver.get("https://dchart.vndirect.com.vn/")
        sleep(2)

    def set_symbol(self, symbol):
        try:
            self.driver.execute_script(f"localStorage.setItem('vnds.tradingView.widget.symbol', '{symbol}');")
            print(f"Symbol set to {symbol} and page refreshed.")
        except Exception as e:
            print(f"Error storing symbol and refreshing page: {e}")
        self.driver.refresh()
        sleep(2)

    def capture_screenshot(self):
        try:    
            screenshot_base64 = self.driver.execute_async_script("""
                const callback = arguments[0];
                
                const dom = document.querySelector("iframe[title='Financial Chart']").contentWindow;
                
                dom.tradingViewApi.takeClientScreenshot().then(screenshotCanvas => {
                    const dataUrl = screenshotCanvas.toDataURL();
                    callback(dataUrl);
                }).catch(error => {
                    callback(null);
                });
            """)

            if screenshot_base64:
                print("Screenshot captured successfully as Base64")
                return screenshot_base64.split(',')[1]  # Remove the data URL prefix
            else:
                print("Failed to capture screenshot.")
                return None
        
        except Exception as e:
            print(f"Error executing JavaScript for screenshot: {e}")
            return None

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def run(self, symbol):
        self.setup_driver()
        self.open_page()
        self.set_symbol(symbol)
        screenshot_base64 = self.capture_screenshot()
        self.close_driver()
        return screenshot_base64


if __name__ == "__main__":
    capture = ChartScreenshotCapture("HPG")
    screenshot_base64 = capture.run("HPG")
    print(screenshot_base64)
