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
    can_have_children = db.Column(db.Boolean, default=True)

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
        """ Returns a json serializable dict.
        
        Notes:
            What's cool about this is that the children's key recursively keeps
            calling itself on all of the children of each new node. Causing the
            output to look like which is pretty powerful.
            
            - Root
                - level_1  
                    - level_2
                        - level_3
                - level_1  
                    - level_2
                        - level_3
                - level_1  
                    - level_2
                        - level_3
        
        Returns:
            dict: Key value pairs of essential Node data.
        """
        base = {
            'id':                self.id,
            'name':              self.name,
            'parent_id':         self.parent_id,
            'can_have_children': self.can_have_children

        }
        if self.can_have_children:
            return {**base, 'children': [c.serialize for c in self.sub_nodes]}
        else:
            return base

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
