from app import db


class Node(db.Model):
    """ Account class that stores unique emails. """

    __tablename__ = 'node'

    # ------------------------------------------
    #   Relationships
    # ------------------------------------------

    parent_id = db.Column(db.Integer, db.ForeignKey('node.id'), index=True)
    parent = db.relationship(
        lambda: Node,
        remote_side=id,
        backref='sub_nodes',
    )

    # ------------------------------------------
    #   Attributes
    # ------------------------------------------

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Built-in Override Methods.
    def __init__(self, name):
        """ Creates new Account.

        Args:
            name (str): A unique Node name.
        """
        self.name = name

    def __str__(self):
        """ Returns Object string representation.

        Returns:
            str: representation of Node Object.
        """
        return '<Node {}>'.format(self.id)

    @classmethod
    def get_or_create(cls, name):
        """
        Gets or creates a new Node.
        
        Args:
            name: (str) - Value to name new Node.

        Returns:
            Node: (object) - Value of existing or created Node.

        """
        node = cls.query.filter_by(name=name).first()

        if not node:
            instance = cls(name)
            return instance
        else:
            return node
