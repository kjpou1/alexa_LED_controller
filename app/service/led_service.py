from app.io.io_inventory import IOInventory

class LEDService:
    """
    LEDService provides methods to control an LED.
    It interacts with the IOInventory to manage the LED state.
    """

    def turn_led_on(self):
        """
        Turns the LED on using the IOInventory.
        """
        IOInventory.turn_on('led')
    
    def turn_led_off(self):
        """
        Turns the LED off using the IOInventory.
        """
        IOInventory.turn_off('led')
