
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

class InteractiveBricksScene(Scene):
    def construct(self):

        calculator = BricksCalculator()
        self.current_brick_idx = 0
        len_full_brick = calculator.len_full_brick 
        len_half_brick = calculator.len_halfbrick 
        len_head_joint = calculator.len_headjoint 
        height_brick = calculator.height_brick 
        height_bed_joint = calculator.height_bedjoint 
        rows, cols = calculator.calculate_bricks()
        # Calculate total wall width for centering
        wall_width = (calculator.len_brick_headjoint * cols + calculator.len_halfbrick)
        x_center_offset = -wall_width / 2  

        self.bricks = VGroup()
        self.all_bricks_flat = [] 
     
        start_x = -wall_width / 2
        for row in range(rows):
            row_bricks = VGroup()
            y = row * (height_brick + height_bed_joint)

            # x offset for stretcher bond
            x_offset = 0 if row % 2 == 0 else (len_half_brick+len_head_joint)/2
            if row % 2 == 0:
                x = start_x 
            
                for col in range(cols):
                
                    brick_center = x + len_full_brick / 2
                    rect = Rectangle(
                      width=len_full_brick,
                      height=height_brick,
                      color=WHITE,
                      fill_opacity=0.5
                    )
                    rect.move_to([brick_center, y, 0])
                    row_bricks.add(rect)
                    self.all_bricks_flat.append(rect)
                    #self.bricks.add(rect) 
                    x += len_full_brick + len_head_joint
           
                # Add half-brick at end
                half_brick_center_x = x + len_half_brick / 2
                half = Rectangle(width=len_half_brick, height=height_brick, color=WHITE, fill_opacity=0.5)
                half.move_to([half_brick_center_x, y, 0])
                row_bricks.add(half)
                self.all_bricks_flat.append(half)
                    #self.bricks.add(half)
                    
            else:
                x = start_x
                half_brick_center_x = x + len_half_brick / 2
                half = Rectangle(width=len_half_brick, height=height_brick, color=WHITE, fill_opacity=0.5)
                half.move_to([half_brick_center_x, y, 0])
                row_bricks.add(half)
                self.all_bricks_flat.append(half) 
                #self.bricks.add(half)
                x += len_half_brick + len_head_joint

                for col in range(cols):
                    brick_center_x = x + len_full_brick / 2
                    rect = Rectangle(width=len_full_brick, height=height_brick, color=WHITE, fill_opacity=0.5)
                    rect.move_to([brick_center_x, y, 0])
                    row_bricks.add(rect)
                    self.all_bricks_flat.append(rect) 
                    x += len_full_brick + len_head_joint

            self.bricks.add(row_bricks)

        self.add(self.bricks) 
        
        instructions = VGroup(
            Text("Press ENTER to highlight next brick", font_size=24),
            Text("Press BACKSPACE to remove brick", font_size=24),
            Text("Press R to reset the frame", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP).scale(0.8)
        instructions.to_edge(UP)
        self.add(instructions)    
        self.interactive_embed()

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        
        if symbol == pyglet_key.ENTER:
            if self.current_brick_idx < len(self.all_bricks_flat):
                brick = self.all_bricks_flat[self.current_brick_idx]
                
                brick.set_fill(GREY, opacity=1.0)
                brick.set_stroke(RED, width=2)  
                
                print(f"Highlighted brick {self.current_brick_idx + 1} of {len(self.all_bricks_flat)}")
                
                self.current_brick_idx += 1
                
                self.renderer.update_frame(self)
            else:
                print("All bricks highlighted!")
        
        elif symbol == pyglet_key.BACKSPACE:
            if self.current_brick_idx >0:
                self.current_brick_idx -=1
                idx = self.current_brick_idx

                brick = self.all_bricks_flat[idx]
                brick.set_fill(WHITE, opacity=0.5)
                brick.set_stroke(WHITE, width=1)

                print(f"Removed brick {idx}")
                self.renderer.update_frame(self)

        # Reset bricks with 'R' key
        elif symbol == pyglet_key.R:
            for brick in self.all_bricks_flat:
                brick.set_fill(WHITE, opacity=0.5)
                brick.set_stroke(WHITE, width=1)
            self.current_brick_idx = 0
            print("Reset all bricks")
            self.renderer.update_frame(self)
        
        super().on_key_press(symbol, modifiers)
