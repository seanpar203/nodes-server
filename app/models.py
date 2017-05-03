from app import db


class Node(db.Model):
    """ Node class that stores names. """

    __tablename__ = 'node'

    # ------------------------------------------
    #   Relationships
    # ------------------------------------------

    parent_id = db.Column(db.Integer, db.ForeignKey('node.id'), index=True)
    parent = db.relationship(
        'Node',
        remote_side='Node.id',
        backref='sub_nodes',
    )

    # ------------------------------------------
    #   Attributes
    # ------------------------------------------

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    # ------------------------------------------
    #   Methods
    # ------------------------------------------

    def __init__(self, name):
        """ Creates new Node.

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

    @property
    def serialize(self):
        return {
            'id':        self.id,
            'name':      self.name,
            'parent_id': self.parent_id,
            'children':  [node.serialize for node in self.sub_nodes]
        }

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
