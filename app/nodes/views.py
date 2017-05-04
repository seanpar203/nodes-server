# Flask
from flask_socketio import emit, send
from flask import Blueprint, jsonify, request

# DB connector.
from app import db, socketio

# Models
from app.models import Node

# Utils
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
        nodes = Node.query.filter_by(name='Root')
        return jsonify([node.serialize for node in nodes]), 200


@node_app.route('/<pk>/', methods=['GET', 'PUT', 'DELETE'])
def node_detail(pk):
    """ Get, Update & Delete specific Node data.
    
    Args:
        pk (int): Value of node id.

    Returns:
        (Object): Value of specific Node. 
    """

    def get_object():
        """ Helper function for getting model.
         
        Notes:
            Since this is a closure I don't need to pass id param to it.
        """
        instance = Node.query.get(int(pk))

        if not instance:
            raise ObjectDoesntExist(f"Node with id {pk} doesn't exist")
        else:
            return instance

    # Attempt to get the object based id before even doing any processing.
    try:
        node = get_object()

    except ObjectDoesntExist as error:
        return jsonify(error.message), 400

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


@socketio.on('connect')
def handle_connect():
    print('connected')


@socketio.on('update:node')
def handle_update():
    nodes = Node.query.filter_by(name='Root')
    json = jsonify([node.serialize for node in nodes])
    emit('update', json, broadcast=True)
