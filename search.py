from jumper import JUMPER
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

if __name__ == "__main__":
    jumper = JUMPER()
    
    # Run the long_jump simulation
    logging.info("Starting the evolutionary process with long_jump fitness type.")
    jumper.Evolve_With_Fitness_Type("long_jump")  # Run evolution for long_jump fitness
    logging.info("Completed the evolutionary process with long_jump fitness type.")
    
    # # Run the high_jump simulation
    # logging.info("Starting the evolutionary process with high_jump fitness type.")
    # jumper.Evolve_With_Fitness_Type("high_jump")  # Run evolution for high_jump fitness
    # logging.info("Completed the evolutionary process with high_jump fitness type.")
