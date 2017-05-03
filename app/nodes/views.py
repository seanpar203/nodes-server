# Flask
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

# DB connector.
from app import db

# Models
from app.models import Node

# Create new flask blueprint
node_app = Blueprint('node', __name__)


@node_app.route('/', methods=['GET', 'POST'])
@cross_origin()
def node_list():
    """ Lists or creates nodes.
    
    Returns:
        (list | object): List of all nodes or a newly created node. 
    """
    if request.method == 'POST':

        try:
            name = request.json['name']

        except KeyError:
            return jsonify('Please send a name to call the new node'), 400

        else:
            node = Node.query.filter_by(name=name).first()

            if node:
                return jsonify(f'Node with name {name} already exists'), 400

            else:
                # Grab root node.
                root_node = Node.query.filter_by(name='Root').first()

                # Create new node & make relationship
                node = Node(name)
                node.parent = root_node

                # Add new node to session.
                db.session.add(node)
                db.session.commit()
                return jsonify(node.serialize), 201

    else:
        nodes = Node.query.filter_by(name='Root')
        return jsonify([node.serialize for node in nodes]), 200


@node_app.route('/<id>', methods=['GET', 'POST'])
@cross_origin()
def node_detail(id):
    """ Get, Update & Delete specific Node data.
    
    Args:
        id (int): Value of node id.

    Returns:

    """
    pass
