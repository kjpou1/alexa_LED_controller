import logging
from gpiozero import LED, pi_info
from app.models.singleton import SingletonMeta

class IOInventory(metaclass=SingletonMeta):
    """
    IOInventory is a singleton class that manages I/O devices.
    It provides methods to add devices, retrieve them, and control their states.
    """
    _is_initialized = False
    _devices = {}

    def __init__(self):
        """
        Initializes the IOInventory and logs Raspberry Pi info.
        This is called only once due to the singleton pattern.
        """
        if not IOInventory._is_initialized:
            self.logger = logging.getLogger(__name__)
            pi = pi_info()
            self.logger.info(f"Running on a Raspberry Pi {pi}")
            IOInventory._is_initialized = True

    @classmethod
    def initialize(cls):
        """
        Convenience method to explicitly initialize the IOInventory.
        This can be expanded to include more initialization parameters if needed.
        """
        cls()

    @classmethod
    def add_device(cls, name, device):
        """
        Adds a device to the inventory.
        
        :param name: The name of the device.
        :param device: The device instance to add.
        """
        cls._devices[name] = device

    @classmethod
    def get_device(cls, name):
        """
        Retrieves a device from the inventory by name.
        
        :param name: The name of the device to retrieve.
        :return: The device instance, or None if not found.
        """
        return cls._devices.get(name)

    @classmethod
    def turn_on(cls, name):
        """
        Turns on the specified device.
        
        :param name: The name of the device to turn on.
        """
        device = cls.get_device(name)
        if device:
            device.on()
        else:
            cls._log_device_not_found(name)

    @classmethod
    def turn_off(cls, name):
        """
        Turns off the specified device.
        
        :param name: The name of the device to turn off.
        """
        device = cls.get_device(name)
        if device:
            device.off()
        else:
            cls._log_device_not_found(name)

    @classmethod
    def _log_device_not_found(cls, name):
        """
        Logs an error if a device is not found in the inventory.
        
        :param name: The name of the device not found.
        """
        logger = logging.getLogger(__name__)
        logger.error(f"Device '{name}' not found in inventory")

# Initialize the IOInventory and add the LED device
IOInventory.initialize()
IOInventory.add_device('led', LED(27, initial_value=False))
