# Flask
import json
from random import randint
from flask_socketio import emit, send
from flask import Blueprint, jsonify, request

# DB connector.
from app import db, socketio

# Models
from app.models import Node

# Utils
from app.helper_functions import get_object
from app.exceptions import ObjectDoesntExist

# Create new flask blueprint
node_app = Blueprint('node', __name__)


@node_app.route('/', methods=['GET', 'POST'])
def node_list():
    """ Lists or creates nodes.
    
    Notes:
        Before creating we make sure there isn't already a node with the same name.
        We also check to see if a name key exists on the request to prevent breaking
        the app.
    
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
        root_node = Node.query.filter_by(name='Root')
        return jsonify([node.serialize for node in root_node]), 200


@node_app.route('/<pk>/', methods=['GET', 'PUT', 'DELETE'])
def node_detail(pk):
    """ Gets, Updates, Deletes a specific node.
    
    Args:
        pk (int): Value of node id.

    Returns:
        (Object): Value of specific Node. 
    """
    # Attempt to get the object based id before even doing any processing.
    try:
        node = get_object(Node, pk)

    except ObjectDoesntExist as error:
        return jsonify(error.message), 404

    else:
        # ------------------------------------------
        #   GET
        # ------------------------------------------

        if request.method == 'GET':
            return jsonify(node.serialize), 200

        # ------------------------------------------
        #   PUT
        # ------------------------------------------

        if request.method == 'PUT':

            try:
                name = request.json['name']

            except KeyError:
                return jsonify('Please send a name to rename the node'), 400

            else:
                node.name = name
                db.session.commit()
                return jsonify(node.serialize), 200

        # ------------------------------------------
        #   DELETE
        # ------------------------------------------

        if request.method == 'DELETE':
            node.delete()
            db.session.commit()
            return jsonify('Successfully Deleted.'), 204


@node_app.route('/<pk>/nodes/', methods=['POST'])
def create_sub_nodes(pk):
    """ Creates sub nodes for a specific node.
    
    Args:
        pk (int): Value of node id. 

    Returns:
        (list): List of dictionaries of new sub nodes.
    """
    # Make sure the node exists.
    try:
        parent = get_object(Node, pk)

    except ObjectDoesntExist as error:
        return jsonify(error.message), 404

    else:

        # Make sure they sent sub node names.
        try:
            count = request.json['count']

        except KeyError:
            return jsonify('Missing amount of sub nodes to generate.'), 400

        else:

            if count:

                # Delete previous sub nodes.
                Node.query.filter_by(parent=parent).delete()
                db.session.commit()

                # Create new nodes.
                for i in range(count):
                    node_name = str(randint(parent.min_num, parent.max_num))
                    node = Node(name=node_name)
                    node.can_have_children = False
                    node.parent = parent
                    db.session.add(node)
                db.session.commit()

                # Return new node tree.
                return jsonify('New nodes Created.'), 200

            else:
                return jsonify('Sub node names are empty.'), 400


@socketio.on('connect')
def handle_connect():
    print('connected')


@socketio.on('update:nodes')
def handle_update():
    root_node = Node.query.filter_by(name='Root')
    data = json.dumps([node.serialize for node in root_node])
    emit('update', data, broadcast=True)
