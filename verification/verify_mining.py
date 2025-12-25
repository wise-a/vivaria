from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Load local file
        page.goto(f"file://{os.path.abspath('index.html')}")

        # Wait for game to initialize (canvas present)
        page.wait_for_selector("#gameCanvas")

        # Take initial screenshot
        page.screenshot(path="verification/before_mining.png")

        # Simulate mining
        # Center of screen is approximately where the player mines if they click
        # Player is at (150*32)/2 = 2400.
        # But camera follows player.
        # Mouse click coordinates are relative to viewport.
        # Player is centered in viewport.
        # viewport size is standard (e.g., 1280x720) or whatever browser defaults to.
        # Player height is 44, width 20.
        # Player feet at center X, center Y? No, player.y=0 initially then gravity.
        # Let's wait a bit for gravity to settle.
        page.wait_for_timeout(2000)

        # Click below player to mine dirt/ground
        viewport = page.viewport_size
        center_x = viewport['width'] / 2
        center_y = viewport['height'] / 2 + 50 # 50px below center

        page.mouse.click(center_x, center_y)

        # Wait a moment
        page.wait_for_timeout(500)

        # Take screenshot
        page.screenshot(path="verification/after_mining.png")

        browser.close()

if __name__ == "__main__":
    run()
