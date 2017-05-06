from app.exceptions import ObjectDoesntExist


def get_object(model, pk):
    """ Helper function for getting model.

        Args:
            model (object): ORM model to perform query.
            pk (int): model id to get.
    """
    instance = model.query.get(int(pk))

    if not instance:
        raise ObjectDoesntExist(f"Node with id {pk} doesn't exist")
    else:
        return instance
