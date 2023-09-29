from playwright.sync_api import sync_playwright

def take_screenshot_from_url(url, session_data):
    with sync_playwright() as playwright:
        webkit = playwright.webkit
        browser = webkit.launch()
        browser_context = browser.new_context(device_scale_factor=2)
        browser_context.add_cookies([session_data])
        page = browser_context.new_page()
        page.goto(url)
        screenshot_bytes = page.locator(".code").screenshot()
        browser.close()
        return screenshot_bytes

# def take_screenshot_from_url(url, session_data, width=1920, height=1080, quality=80):
#     with sync_playwright() as playwright:
#         webkit = playwright.webkit
#         browser = webkit.launch()
#         browser_context = browser.new_context()
#         browser_context.add_cookies([session_data])
#         page = browser_context.new_page()
        
#         # Set the viewport size to control the size of the screenshot
#         page.set_viewport_size(width=width, height=height)
        
#         page.goto(url)

#         # Take a screenshot with the specified options
#         screenshot_bytes = page.screenshot()
        
#         browser.close()
#         return screenshot_bytes


