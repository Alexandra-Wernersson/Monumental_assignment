### Make a class that vizualizes and calculates the brick wall

class Bricks_Calculate_Visualize():

    """
    Basic class to calculate the maximum number of half/full bricks 
    for a masonary wall as well as a simple vizualisation of the results.
    """

    def __init__(self):
        self.max_len = 2.3
        self.len_brick_headjoint = 0.22
        self.len_halfbrick = 0.1
        self.len_halfbrick_headjoint = 0.11
        self.max_height = 2
        self.height_brick_bedjoint = 0.0625
        self.height_bedjoint = 0.0125
        self.full_brick = "░░░░"
        self.full_brick_headjoint = "░░░░|"
        self.headjoint_full_brick = "|░░░░"
        self.half_brick = "░░"
        """
        Parameters
        ----------
        max_len: Maximum length of wall(m).
        len_brick_headjoint: Length of a brick plus head joint (m).
        len_halfbrick: Length of a half brick (m).
        len_halfbrick_headjoint: Length of a half brick plus head joint (m).
        max_height: Maximum height of wall (m).
        height_brick_bedjoint: Height of brick plus bed joint (m).
        height_bedjoint: Height of bed joint (m).
        """
 
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
            Number_brick_bedjoint = self.max_height/self.height_brick_bedjoint
        else:
        #Only case it doesn't match is when you end on a brick
            
            Number_brick_bedjoint = (self.max_height-self.height_bedjoint)/self.height_brick_bedjoint + 1
        Total_number_of_fullbricks = number_full_bricks_headjoint*Number_brick_bedjoint
        Total_number_of_halfbricks = self.max_height/self.height_brick_bedjoint
        Total_number_of_bricks = Total_number_of_fullbricks + Total_number_of_halfbricks
        
        return Number_brick_bedjoint, number_full_bricks_headjoint, Total_number_of_fullbricks, Total_number_of_halfbricks, Total_number_of_bricks

    def visualize_bricks(self):
        visualize_height = int(self.calculate_bricks()[0] / 2)
        visualize_length = int(self.calculate_bricks()[1])
        print(f"Number of full bricks horizontally: { visualize_length}", "Number of half bricks: 1")
        print(f"Number of bricks vertically: {visualize_height}")
        print(f"Total number of full bricks: {int(self.calculate_bricks()[2])}")
        print(f"Total number of half bricks: {int(self.calculate_bricks()[3])}")
        print(f"Total number of bricks: {int(self.calculate_bricks()[4])}")
        for _ in range(visualize_height):
            print(self.full_brick_headjoint * visualize_length + self.half_brick)
            print(self.half_brick + visualize_length * self.headjoint_full_brick)
       
if __name__ == "__main__":
    brick_class = Bricks_Calculate_Visualize() 
    brick_class.visualize_bricks()
