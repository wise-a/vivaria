# **Vivaria (v7.0)**

**Vivaria** is a lightweight, browser-based 2D sandbox survival game inspired by titles like *Terraria* and *Minecraft*. Built entirely in HTML5 and Vanilla JavaScript, it features a fully destructible world, dynamic lighting, fluid physics, and a crafting system.

## **How to Run**

Simply download the index.html file and open it in any modern web browser (Chrome, Firefox, Edge, Safari). No installation or internet connection is required.

## **Controls**

| Action | Key / Input | Description |
| :---- | :---- | :---- |
| **Move** | WASD or Arrow Keys | Move left/right and jump. |
| **Jump** | Space, W, or Up Arrow | Jump (hold in water to swim). |
| **Toggle Mode** | E | Switch between **Mining** and **Building** modes. |
| **Action** | Mouse Click | **Mine** block (in Mine Mode) or **Place** block (in Build Mode). |
| **Crafting** | C | Open/Close the crafting menu. |
| **Menu/Close** | Esc | Close open overlays (Crafting, New World, etc.). |

## **Features**

* **Procedural Generation:** Every new world is unique, featuring distinct biomes including Forests, Deserts (with tumbleweeds), and Snowlands (with icebergs).  
* **Dynamic Day/Night Cycle:** Watch the sky change from dawn to dusk. Light levels affect visibility, requiring torches or campfires at night.  
* **Physics Engine:**  
  * **Fluids:** Water flows dynamically and settles into ponds.  
  * **Gravity:** Sand or other loose blocks will fall if unsupported.  
  * **Buoyancy:** Objects and players float in water.  
* **Cellular Automata:** Mud can dry into dirt; water seeks equilibrium.
* * **Save System:** Your progress can be saved to your browser's LocalStorage. You can also **Export** your save to a .json file and **Import** it later on a different device.

## **📖 Beginner's Tutorial**

### **1\. Understanding Modes**

Vivaria uses a unique "Mode" system toggled by pressing **E**:

* **Mining Mode (Red HUD):** Clicking any block destroys it and adds it to your inventory.  
* **Building Mode (Green HUD):** Clicking empty space places the currently selected block from your inventory.

### **2\. First Steps**

1. **Gather Wood:** You spawn in a world with trees. Ensure you are in **Mining Mode** and click the tree trunks (Raw Wood) to collect them.  
2. **Gather Stone & Coal:** Dig down into the ground (Dirt and Stone). Look for black-speckled blocks (Coal Ore). You will need these for light.  
3. **Crafting:** Press **C** to open the crafting menu.  
   * Craft **Wood Planks** using Raw Wood.  
   * Craft **Sticks** using Raw Wood.  
   * Craft **Torches** using Planks \+ Coal.

### **3\. Advanced Exploration**

* **Biomes:** Travel left or right to find sandy Deserts or freezing Snow biomes.  
* **Ores:** Dig deeper to find **Gold Ore** and the rare **Diamond Ore**.

## **Crafting Recipes**

| Item | Output | Ingredients |
| :---- | :---- | :---- |
| **Wood Planks** | 4 | 1 Raw Wood |
| **Sticks** | 10 | 1 Raw Wood |
| **Torches** | 8 | 1 Wood Plank \+ 1 Coal Ore |
| **Campfire** | 1 | 1 Torch \+ 2 Sticks |

## **Technical Details**

* **Engine:** Custom HTML5 engine.  
* **Resolution:** Adjustable world sizes (Standard: 150x60, Large: 300x100, Massive: 600x150).  
* **Rendering:** Pixel-art style using Press Start 2P font and programmatic drawing (no external image assets required).
