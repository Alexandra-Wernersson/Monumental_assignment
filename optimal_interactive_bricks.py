from manim import *
from manim.opengl import *

class BricksCalculator():
    """
    Basic class to calculate the maximum number of half/full bricks for a masonary wall
    """
    def __init__(self): 
        self.max_len = 2.3
        self.len_full_brick = 0.21
        self.len_brick_headjoint = 0.22
        self.len_halfbrick = 0.1
        self.len_halfbrick_headjoint = 0.11
        self.len_headjoint = 0.01
        self.max_height = 2
        self.height_brick_bedjoint = 0.0625
        self.height_bedjoint = 0.0125    
        self.height_brick = 0.05

    def calculate_bricks(self):
        """
        Function to caluclate the number of bricks & joints that fit on a wall.
        """

        if (self.max_len) % (self.len_brick_headjoint) != 0:
            # We are ending on a half brick given that we're dealing with a stretcher bond pattern
            number_full_bricks_headjoint = round((self.max_len - self.len_halfbrick) / self.len_brick_headjoint)

        else:
            number_full_bricks_headjoint = self.max_len / self.len_bricks_headjoint

        # Calculate the height
        if self.max_height % self.height_brick_bedjoint ==0:
            number_bricks_bedjoint = self.max_height/self.height_brick_bedjoint
        else:
        #Only case it doesn't match is when you end on a brick
            number_bricks_bedjoint = (self.max_height-self.height_bedjoint)/self.height_brick_bedjoint + 1

        return int(number_bricks_bedjoint), int(number_full_bricks_headjoint)

class build_bricks:
    """
    Class which vizualizes the built brick wall with different colors for each build order.
    """
    def __init__(self, bricks_per_row=11, total_bricks=352):
        self.bricks_per_row = bricks_per_row
        self.total_bricks = total_bricks
        self.build_orders = []
        self.built_bricks = set()
        self.rows = []
        self.generate_wall_layout()
        self.colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        self.order_colors = {}

    def generate_wall_layout(self):
        brick_index = 0
        row = 0

        while brick_index < self.total_bricks:
            row_data = []
            is_even = row % 2 == 0

            if is_even:
                # Start with a half brick
                row_data.append((brick_index, "half"))
                brick_index += 1

                for _ in range(self.bricks_per_row - 1):
                    if brick_index >= self.total_bricks:
                        break
                    row_data.append((brick_index, "full"))
                    brick_index += 1
            else:
                for _ in range(self.bricks_per_row - 1):
                    if brick_index >= self.total_bricks:
                        break
                    row_data.append((brick_index, "full"))
                    brick_index += 1

                if brick_index < self.total_bricks:
                    row_data.append((brick_index, "half"))
                    brick_index += 1

            self.rows.append(row_data)
            row += 1

    def get_flat_order(self):
        """Flatten the layout into a list of brick indices, in row-major order."""
        return [brick[0] for row in self.rows for brick in row]

    def predict_next_build_order(self, previous_build):
        return [brick + 66 for brick in previous_build]
    
    def add_build_order(self, brick_list, label):
        self.build_orders.append({"bricks":brick_list, "label": label})
        self.built_bricks.update(brick_list)
    
    def get_order_by_label(self, label):
        for order in self.build_orders:
            if order["label"] == label:
                return order["bricks"]
        return []

class InteractiveBricksScene(Scene):
    def construct(self):
        calculator = BricksCalculator()
        rows, cols = calculator.calculate_bricks()

        self.build_logic = build_bricks(bricks_per_row=11, total_bricks=352)
        self.build_logic.add_build_order([0, 1, 2, 3, 11, 12, 13, 22, 23, 24, 33, 34, 44, 45, 55, 66], label="order_1")
        self.build_logic.add_build_order([4, 5, 6, 7, 14, 15, 16, 17, 26, 27, 28], label="order_2")
        self.build_logic.add_build_order([8, 9, 10, 18, 19, 20, 21, 29, 30, 31, 32, 40, 41, 42, 43, 52, 53, 54, 63, 64, 65, 75, 76, 86, 87, 98, 109], label="order_3")
        self.build_logic.add_build_order([25, 36,   37,   38, 39,  
                   48,   49,   50,   
                  59,   60,   
                    71,    ], label="order_4")
        self.build_logic.add_build_order([35,   36,   
                  46,   47,   
                  56,   57,   58,
                  67,   68,   69,
                  77,   78,   79,
                  88,   89,   90 ,
                  99,  100,  
                  110,  111,
                  121,  
                  132], label="order_5")
        self.build_logic.add_build_order([51, 61, 62, 73, 74, 84, 85, 96, 97, 107, 108, 119, 120, 130, 131, 142], label="order_6")
       
        # Assign colors for the first 6 orders
        for i in range(1, 7):
            label = f"order_{i}"
            color = self.build_logic.colors[i % len(self.build_logic.colors)]
            self.build_logic.order_colors[label] = color

        for i in range(7,22):
            next_label = f"order_{i}"
            prev_label = f"order_{i-5}"
            prev_order = self.build_logic.get_order_by_label(prev_label)
            if not prev_order:
               print(f"Warning: No bricks found for label {prev_label}")
               continue
            next_order = self.build_logic.predict_next_build_order(prev_order)
            next_order = [b for b in next_order if b not in self.build_logic.built_bricks]
            color = self.build_logic.colors[i % len(self.build_logic.colors)]
            self.build_logic.order_colors[next_label] = color
            self.build_logic.add_build_order(next_order, label=next_label)
        
        # Last build orders are a bit special so I add them manually
        self.build_logic.add_build_order([268, 270, 278, 279, 280, 281, 289, 290, 291, 292], label = "order_22")
        self.build_logic.add_build_order([293, 304, 316, 327, 339, 350, 351, 303, 315, 326, 338, 349], label="order_23")
        self.build_logic.add_build_order([289, 302, 301, 313, 314, 324, 325, 336, 337, 347, 348], label="order_24")   
        self.build_logic.add_build_order([299, 300, 310, 311,  320, 321,  331, 332,   341, 342 ], label="order_25")
        self.build_logic.add_build_order([312, 322, 323, 333, 334, 335, 343, 344, 345, 346], label="order_26")
        for i in range(22, 27):
            label = f"order_{i}"
            color = self.build_logic.colors[i % len(self.build_logic.colors)]
            self.build_logic.order_colors[label] = color
        
        # Flatten the build order list
        self.flat_build_order = [idx for order in self.build_logic.build_orders for idx in order["bricks"]]

        self.current_build_index = 0
        self.all_bricks_flat = []
        self.brick_map = {}

        
        calculator = BricksCalculator()
        len_full_brick = calculator.len_full_brick 
        len_half_brick = calculator.len_halfbrick 
        len_head_joint = calculator.len_headjoint 
        height_brick = calculator.height_brick 
        height_bed_joint = calculator.height_bedjoint
        rows, cols = calculator.calculate_bricks()
        # Calculate total wall width for centering
        wall_width = (calculator.len_brick_headjoint * cols + calculator.len_halfbrick)
        x_center_offset = -wall_width / 2  # To center the wall horizontally

        # Layout the bricks
        self.bricks = VGroup()
        for row_idx, row in enumerate(self.build_logic.rows):
            row_group = VGroup()
            y = row_idx * (height_brick + height_bed_joint)
            x = x_center_offset

            for brick_index, brick_type in row:
                width = len_half_brick if brick_type == "half" else len_full_brick
                rect = Rectangle(width=width, height=height_brick, fill_opacity=0.5, color=WHITE)
                rect.move_to([x + width / 2, y, 0])
                row_group.add(rect)

                self.brick_map[brick_index] = rect
                self.all_bricks_flat.append(rect)
                x += width + len_head_joint

            self.bricks.add(row_group)

        self.add(self.bricks)

        instructions = VGroup(
            Text("Press ENTER to highlight next brick", font_size=24),
            Text("Press BACKSPACE to remove brick", font_size=24),
            Text("Press R to reset the frame", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP).scale(0.8)
        self.add(instructions)

        self.interactive_embed()

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        if symbol == pyglet_key.ENTER:
            if self.current_build_index < len(self.flat_build_order):
                idx = self.flat_build_order[self.current_build_index]
                if idx in self.brick_map:
                    brick = self.brick_map[idx]
                    color = GREY
                    for order in self.build_logic.build_orders:
                        if idx in order["bricks"]:
                            color = self.build_logic.order_colors.get(order["label"], GREY)
                            break

                    brick.set_fill(GREY, opacity=1.0)
                    brick.set_stroke(color, width=2)
                print(f"Laid brick {idx}")
                self.current_build_index += 1
                self.renderer.update_frame(self)
            else:
                print("All bricks laid.")
        elif symbol == pyglet_key.BACKSPACE:
            if self.current_build_index >0:
                self.current_build_index -=1
                idx = self.flat_build_order[self.current_build_index]

                color = WHITE
                for order in self.build_logic.build_orders:
                        if idx in order["bricks"]:
                            color = self.build_logic.order_colors.get(order["label"], GREY)
                            break
 
                brick = self.brick_map[idx]
                brick.set_fill(WHITE, opacity=0.5)
                brick.set_stroke(WHITE, width=1)

                print(f"Removed brick {idx}")
                self.renderer.update_frame(self)
        elif symbol == pyglet_key.R:
            for brick in self.all_bricks_flat:
                brick.set_fill(WHITE, opacity=0.5)
                brick.set_stroke(WHITE, width=1)
            self.current_build_index = 0
            self.renderer.update_frame(self)
            print("Wall reset.")

