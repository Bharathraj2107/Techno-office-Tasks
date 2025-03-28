import asyncio
import logging
from typing import Optional

# Configure logging for the status message 
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class SimpleMotorEmulator:
    def __init__(self, motor_id: int):
        """Initialize with motor ID and default position 0"""
        self.motor_id = motor_id
        self.current_position = 0.0# Start at position 0
        self.is_moving = False
        self.speed = 10.0# units per second
        log.info(f"Motor {motor_id} initialized at position 0")

    async def move_up(self, distance: float):
        """Move motor up by specified distance"""
        if self.is_moving:
            log.warning("Motor is already moving!")
            return
            
        self.is_moving = True
        target = self.current_position + distance
        log.info(f"Moving motor {self.motor_id} up to {target}")
        
        while self.current_position < target:#condition checking
            self.current_position += self.speed * 0.1# Update position
            log.debug(f"Current position: {self.current_position}")
            await asyncio.sleep(0.1)# movement delay of 0.1 seconds
            
        self.is_moving = False
        log.info(f"Motor {self.motor_id} reached position {self.current_position}")

    async def move_down(self, distance: float):
        """Move motor down by specified distance"""
        if self.is_moving:
            log.warning("Motor is already moving!")
            return
            
        self.is_moving = True
        target = self.current_position - distance
        log.info(f"Moving motor {self.motor_id} down to {target}")
        
        while self.current_position > target:
            self.current_position -= self.speed * 0.1#Update position
            log.debug(f"Current position: {self.current_position}")
            await asyncio.sleep(0.1)# delay of 0.1 seconds 
            
        self.is_moving = False
        log.info(f"Motor {self.motor_id} reached position {self.current_position}")

    async def get_position(self) -> float:
        """Get current position with simulated delay"""
        await asyncio.sleep(0.2)# delay of 0.2 seconds
        return self.current_position

    async def stop(self):
        """Stop the motor immediately"""
        self.is_moving = False
        log.info(f"Motor {self.motor_id} stopped at position {self.current_position}")
        log.info("It has reached the start position from where it has started")


async def main():
    motor = SimpleMotorEmulator(1)#unique identifier for the motor so we used 1
    
    # Move up and down
    await motor.move_up(10)# Move up 10 units
    await motor.move_up(30)# Move up 30 units
    await motor.move_up(50)# Move up 50 units
    print(f"Current position: {await motor.get_position()}")
    
    await motor.move_down(30)# Move down 30 units
    await motor.move_down(30)# Move down 30 units
    await motor.move_down(30)# Move down 30 units
    #It reaches the beginning position and stops
    print(f"Current position: {await motor.get_position()}")
    
    await motor.stop()

# Run the example
asyncio.run(main())