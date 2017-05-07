# Modules
from random import randint

# db
from app import db


class Node(db.Model):
    """ Node class that stores names. """

    __tablename__ = 'node'

    # ------------------------------------------
    #   Relationships
    # ------------------------------------------

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('node.id', ondelete='CASCADE'),
        index=True,
    )
    parent = db.relationship(
        'Node',
        remote_side='Node.id',
        backref='sub_nodes',
        lazy='joined'
    )

    # ------------------------------------------
    #   Attributes
    # ------------------------------------------

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    can_have_children = db.Column(db.Boolean, default=True)
    min_num = db.Column(db.SmallInteger, nullable=True)
    max_num = db.Column(db.SmallInteger, nullable=True)

    # ------------------------------------------
    #   Methods
    # ------------------------------------------

    def __init__(self, name):
        """ Creates new Node.

        Args:
            name (str): A unique Node name.
        """
        max_rand = 970
        self.name = name
        self.min_num = randint(1, max_rand)
        self.max_num = randint(self.min_num, max_rand + 30)

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
            'min_num':           self.min_num,
            'max_num':           self.max_num,
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
