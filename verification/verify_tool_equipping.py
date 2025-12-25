from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath('index.html')}")
        page.wait_for_selector("#gameCanvas")

        # Give player wood pickaxe
        page.evaluate(f"inventory[TILES.WOOD_PICK] = 1; updateHUD();")
        page.click(".icon-40")

        # Wait for player to settle
        print("Waiting for player to settle...")
        for i in range(50):
            p_state = page.evaluate("() => { return {vx: player.vx, vy: player.vy, cx: camera.x}; }")
            if abs(p_state['vx']) < 0.05 and abs(p_state['vy']) < 0.05:
                print(f"Settled. Camera: {p_state['cx']}")
                break
            page.wait_for_timeout(100)

        # Force spawn stone nearby
        state = page.evaluate("() => { return {x: player.x, y: player.y, width: player.width, height: player.height, cameraX: camera.x, cameraY: camera.y, TILE_SIZE: TILE_SIZE}; }")

        target_r = int((state['y'] + state['height']) / state['TILE_SIZE']) + 1
        target_c = int((state['x'] + state['width']/2) / state['TILE_SIZE'])

        page.evaluate(f"world[{target_r}][{target_c}] = TILES.STONE;")
        print(f"Spawned Stone at {target_r}, {target_c}")

        # Check Distance
        dist = page.evaluate(f"() => {{ let c = {target_c}; let r = {target_r}; let tileX = c * TILE_SIZE + TILE_SIZE/2; let tileY = r * TILE_SIZE + TILE_SIZE/2; let playerX = player.x + player.width/2; let playerY = player.y + player.height/2; return Math.sqrt((tileX-playerX)**2 + (tileY-playerY)**2); }}")
        print(f"Distance: {dist}")

        target_world_x = target_c * state['TILE_SIZE'] + state['TILE_SIZE']/2
        target_world_y = target_r * state['TILE_SIZE'] + state['TILE_SIZE']/2

        client_x = target_world_x - state['cameraX']
        client_y = target_world_y - state['cameraY']

        # Mine with Pickaxe
        page.mouse.move(client_x, client_y)
        page.mouse.down()

        # Monitor progress
        print("Mining...")
        for i in range(10):
            page.wait_for_timeout(50)
            prog = page.evaluate("miningProgress")
            im = page.evaluate("isMining")
            print(f"Progress: {prog}, isMining: {im}")

        page.mouse.up()

        final_id = page.evaluate(f"world[{target_r}][{target_c}]")
        if final_id == 0:
            print("Success: Stone broken.")
        else:
            print("Error: Stone didn't break.")

        browser.close()

if __name__ == "__main__":
    run()
