import os
import sys
from playwright.sync_api import sync_playwright

def reproduce_bugs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for game to load
        page.wait_for_timeout(1000)

        print("--- Bug 1: Auto-step ---")
        # Setup: Flat world with one block at x=5
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
                window.obsX = obsX;
            }
        """)

        # Move right
        page.keyboard.down("ArrowRight")
        page.wait_for_timeout(500)
        page.keyboard.up("ArrowRight")

        # Check if passed the obstacle
        passed = page.evaluate("player.x > window.obsX * TILE_SIZE")
        print(f"Passed obstacle? {passed} (Expected: True if fixed, False if bugged)")

        print("--- Bug 2: Place inside player ---")
        # Setup: Player standing still. Try place block at feet.
        page.evaluate("""
            () => {
                mode = 'BUILD';
                selectedBlock = 3; // Stone
                inventory[3] = 10;
                // Player at integer coordinates to be sure
                player.x = 100; player.y = 100;
                player.vx = 0; player.vy = 0;

                // Let's try to place at (3,4).
                // Player at 100,100 occupies (3,3) and (3,4).
                // 100/32 = 3.125
                mouseTile.c = 3; mouseTile.r = 4;
                // Trigger mousedown
                let e = new MouseEvent('mousedown', {
                    bubbles: true, cancelable: true, view: window
                });
                canvas.dispatchEvent(e);
            }
        """)

        is_blocked = page.evaluate("world[4][3] === 3")
        print(f"Block placed inside player? {is_blocked} (Expected: False if fixed, True if bugged)")

        print("--- Bug 3: Flower Inventory ---")
        # Trigger New World
        page.evaluate("confirmNewWorld(150, 60)")

        # Check inventory for flower (ID 20)
        inv_val = page.evaluate("inventory[20]")
        print(f"Inventory[20] after new world: {inv_val} (Expected: 0 if fixed, undefined if bugged)")

        # Simulate mining a flower
        page.evaluate("inventory[20]++")
        inv_val_after = page.evaluate("inventory[20]")
        print(f"Inventory[20] after mining: {inv_val_after} (Expected: 1 if fixed, null/NaN if bugged)")

        browser.close()

if __name__ == "__main__":
    reproduce_bugs()
