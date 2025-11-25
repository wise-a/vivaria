import os
from playwright.sync_api import sync_playwright

def visual_verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for game to load
        page.wait_for_timeout(1000)

        # 1. Setup auto-step scenario and take screenshot
        # Move player next to a block and move right
        page.evaluate("""
            () => {
                // Clear world
                for(let r=0; r<ROWS; r++) for(let c=0; c<COLS; c++) world[r][c] = 0;
                // Floor
                for(let c=0; c<COLS; c++) world[40][c] = 1;
                // Obstacle
                let obsX = Math.floor(player.x/TILE_SIZE) + 2;
                world[39][obsX] = 1;
                player.y = 39 * TILE_SIZE; // On ground
                player.vx = 0; player.vy = 0;
            }
        """)

        # Move right
        page.keyboard.down("ArrowRight")
        page.wait_for_timeout(500)
        page.keyboard.up("ArrowRight")

        page.screenshot(path="verification/auto_step.png")
        print("Screenshot saved to verification/auto_step.png")

        browser.close()

if __name__ == "__main__":
    visual_verify()
