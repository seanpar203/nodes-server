class ObjectDoesntExist(Exception):
    """ Exception for when a object wasn't found in DB"""

    def __init__(self, message):
        """ Sets the error message to 'message' attr.
        
        Args:
            message (str): Value of error message. 
        """
        self.message = message
