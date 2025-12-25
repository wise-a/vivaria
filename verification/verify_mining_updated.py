from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath('index.html')}")
        page.wait_for_selector("#gameCanvas")

        # Wait for stationary
        print("Waiting for player to settle...")
        for i in range(50):
            p_state = page.evaluate("() => { return {vx: player.vx, vy: player.vy, cx: camera.x}; }")
            if abs(p_state['vx']) < 0.05 and abs(p_state['vy']) < 0.05:
                print(f"Settled at loop {i}. Camera: {p_state['cx']:.2f}")
                break
            page.wait_for_timeout(100)

        state = page.evaluate("() => { return {x: player.x, y: player.y, width: player.width, height: player.height, cameraX: camera.x, cameraY: camera.y, TILE_SIZE: TILE_SIZE}; }")

        # Scan for solid block
        start_r = int((state['y'] + state['height']) / state['TILE_SIZE'])
        start_c = int((state['x'] + state['width']/2) / state['TILE_SIZE'])

        target_r = -1
        target_c = -1

        # Look down
        rows = page.evaluate("ROWS")
        for r in range(start_r, min(start_r + 10, rows)):
            tid = page.evaluate(f"world[{r}][{start_c}]")
            if tid != 0 and tid != 5: # Not Air, Not Water
                target_r = r
                target_c = start_c
                break

        if target_r == -1:
            print("No solid block found below player!")
            return

        target_id = page.evaluate(f"world[{target_r}][{target_c}]")
        print(f"Found target at {target_r}, {target_c}, ID={target_id}")

        initial_count = page.evaluate(f"inventory[{target_id}]")

        # Calculate click coordinates
        target_world_x = target_c * state['TILE_SIZE'] + state['TILE_SIZE']/2
        target_world_y = target_r * state['TILE_SIZE'] + state['TILE_SIZE']/2

        client_x = target_world_x - state['cameraX']
        client_y = target_world_y - state['cameraY']

        print(f"Clicking at {client_x}, {client_y}")

        # SHORT CLICK
        page.mouse.move(client_x, client_y)
        page.mouse.down()
        page.wait_for_timeout(50)
        page.mouse.up()

        new_count = page.evaluate(f"inventory[{target_id}]")
        if new_count == initial_count:
            print("Success: Block intact after short click.")
        else:
            print("Error: Block broke too fast!")

        # LONG CLICK
        page.mouse.down()
        # Monitor progress
        for i in range(5):
             page.wait_for_timeout(200)
             prog = page.evaluate("miningProgress")
             print(f"Progress: {prog}")

        page.wait_for_timeout(1000)
        page.mouse.up()

        final_id = page.evaluate(f"world[{target_r}][{target_c}]")
        if final_id == 0:
            print("Success: Block became Air.")
        else:
            print(f"Error: Block ID is {final_id}")

        page.screenshot(path="verification/final_mining_test.png")

        browser.close()

if __name__ == "__main__":
    run()
