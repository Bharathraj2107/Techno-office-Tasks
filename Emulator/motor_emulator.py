import asyncio
import logging
from typing import Optional, Tuple, Callable, Any
from dataclasses import dataclass
from enum import Enum, auto

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)


class MotorState(Enum):#defines possible states of the motor
    """Enumeration for motor states"""
    IDLE = auto()#instead of writing the values  like 1 ,2 and so on we use auto python handles the numbering
    MOVING_UP = auto()
    MOVING_DOWN = auto()
    ERROR = auto()
    STOPPED = auto()

@dataclass
class MotorLimits:
    """Data class to store motor limits"""
    min_position: float = -100.0
    max_position: float = 100.0
    max_speed: float = 50.0
    acceleration: float = 5.0


class SimpleMotorEmulator:
    def __init__(
        self,
        motor_id: int,
        limits: Optional[MotorLimits] = None,
        callback: Optional[Callable[[int, MotorState, float], Any]] = None#it is triggered when the state of the motor changes
    ):
        """Initialize motor with configurable parameters.
        
        Args:
            motor_id: Unique identifier for the motor
            limits: Motor movement limits (optional)
            callback: Function to call on state changes (optional)
        """
        self.motor_id = motor_id
        self.current_position = 0.0
        self._state = MotorState.IDLE
        self.speed = 0.0  # Current speed (can vary with acceleration)
        self.target_speed = 10.0  # Default target speed
        self.target_position: Optional[float] = None
        self.limits = limits if limits else MotorLimits()#here it takes the limits value if the user as passed as argument or it takes the the motor limits default acceleration value  
        self.callback = callback
        self.error_message: Optional[str] = None
        self.movement_task: Optional[asyncio.Task] = None
        log.info(f"Motor {motor_id} initialized at position 0 with limits {self.limits}")

    @property
    def state(self) -> MotorState:
        """Get current motor state"""
        return self._state

    @state.setter#when the state of the motor changes  it calls the state setter 
    def state(self, new_state: MotorState):
        """Set motor state and trigger callback if available"""
        self._state = new_state#updates the state
        if self.callback:
            self.callback(self.motor_id, new_state, self.current_position)
        log.info(f"Motor {self.motor_id} state changed to {new_state.name}")

    async def move_to_position(self, position: float):
        """Move motor to absolute position with acceleration/deceleration"""
        if self.state == MotorState.ERROR:
            log.error("Motor is in error state, reset first")
            return

        if self.movement_task and not self.movement_task.done():
            self.movement_task.cancel()#if the movement task is already running, cancel it

        distance = position - self.current_position
        if distance > 0:
            self.state = MotorState.MOVING_UP
        elif distance < 0:
            self.state = MotorState.MOVING_DOWN
        else:
            return # Already at target

        self.target_position = position#sets target
        self.movement_task = asyncio.create_task(self._smooth_movement())#creates and starts the movement task

    async def _smooth_movement(self):
        """Handle smooth movement with acceleration and deceleration"""
        try:
            # Acceleration phase
            while (self.speed < self.target_speed and 
                   not self._reached_target() and
                   self.state in (MotorState.MOVING_UP, MotorState.MOVING_DOWN)):
                self.speed = min(self.speed + self.limits.acceleration * 0.1, #each time it adds 0.5 until the position is reached
                               self.target_speed, 
                               self.limits.max_speed)
                await self._move_step()
            
            # Constant speed phase
            while not self._reached_target() and self.state in (MotorState.MOVING_UP, MotorState.MOVING_DOWN):
                await self._move_step()
            
            # Deceleration phase
            while (self.speed > 0 and 
                   not self._reached_target() and
                   self.state in (MotorState.MOVING_UP, MotorState.MOVING_DOWN)):
                self.speed = max(self.speed - self.limits.acceleration * 0.1, 0)
                await self._move_step()

            if self._reached_target():
                self.state = MotorState.IDLE
                self.speed = 0.0
                self.target_position = None
        except asyncio.CancelledError:
            self.state = MotorState.STOPPED
            self.speed = 0.0
            log.info(f"Motor {self.motor_id} movement was cancelled")
        raise NotImplementedError()
        # except Exception as e:
        #     self.state = MotorState.ERROR
        #     self.error_message = str(e)
        #     log.error(f"Motor {self.motor_id} error: {e}")

    async def _move_step(self):
        """Perform a single movement step"""
        if self.state == MotorState.MOVING_UP:
            new_position = self.current_position + self.speed * 0.1
            if new_position > self.limits.max_position:
                raise ValueError(f"Cannot move beyond max position {self.limits.max_position}")
            self.current_position = new_position
        elif self.state == MotorState.MOVING_DOWN:
            new_position = self.current_position - self.speed * 0.1
            if new_position < self.limits.min_position:
                raise ValueError(f"Cannot move below min position {self.limits.min_position}")
            self.current_position = new_position
        
        log.debug(f"Motor {self.motor_id} position: {self.current_position:.2f}, speed: {self.speed:.2f}")
        await asyncio.sleep(0.1)

    def _reached_target(self) -> bool:
        """Check if motor has reached its target position"""
        if self.target_position is None:
            return False
        return abs(self.current_position - self.target_position) < 0.1

    async def get_position(self) -> float:
        """Get current position with simulated delay"""
        await asyncio.sleep(0.2)
        return self.current_position

    async def get_status(self) -> Tuple[MotorState, float, Optional[str]]:
        """Get complete motor status"""
        await asyncio.sleep(0.1)
        return (self.state, self.current_position, self.error_message)

    async def stop(self):
        """Stop the motor immediately with deceleration"""
        if self.movement_task and not self.movement_task.done():
            self.movement_task.cancel()
        self.state = MotorState.STOPPED
        log.info(f"Motor {self.motor_id} stopped at position {self.current_position}")

    async def reset(self):
        """Reset motor from error state"""
        if self.state == MotorState.ERROR:
            self.error_message = None
            self.state = MotorState.IDLE
            log.info(f"Motor {self.motor_id} reset from error state")

async def motor_callback(motor_id: int, state: MotorState, position: float):
    """Example callback function for state changes"""
    log.info(f"Callback: Motor {motor_id} is now {state.name} at position {position:.2f}")

async def main():
    # Create motor with limits and callback
    limits = MotorLimits(min_position=-50, max_position=150, max_speed=30)
    motor = SimpleMotorEmulator(1, limits=limits, callback=motor_callback)
    
    # Test movement with acceleration
    await motor.move_to_position(50)
    log.info(f"Current position: {await motor.get_position()}")
    
    # Test status reporting
    status = await motor.get_status()
    log.info(f"Motor status: {status}")
    
    # Test movement beyond limits (will go to error state)
    
    await motor.move_to_position(200)
    
    # Reset from error state
    await motor.reset()
    
    # Test stopping during movement
    move_task = asyncio.create_task(motor.move_to_position(30))
    await asyncio.sleep(0.5)
    await motor.stop()
    await move_task  # Wait for task to handle cancellation
    
    # Final position
    log.info(f"Final position: {await motor.get_position()}")

if __name__ == "__main__":      
    asyncio.run(main())