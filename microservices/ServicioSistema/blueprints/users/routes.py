from flask import Blueprint, request, jsonify
#import boto3
import os

users_bp = Blueprint('users_bp', __name__)
#cognito_client = boto3.client('cognito-idp', region_name=os.getenv('AWS_REGION', 'us-east-1'))
#USER_POOL_ID = os.getenv('USER_POOL_ID')
#CLIENT_ID = os.getenv('CLIENT_ID')

@users_bp.route('/users', methods=['POST'])
def create_user():
    #try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']

        """ response = cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ],
            TemporaryPassword=password,
            MessageAction='SUPPRESS'
        ) """

        return jsonify({'message': f'Usuario {username} creado exitosamente.', 'response': "response"}), 201

@users_bp.route('/users', methods=['PUT'])
def edit_user():
    #try:
        data = request.get_json()
        username = data['username']
        attributes = data['attributes']

        user_attributes = [{'Name': key, 'Value': value} for key, value in attributes.items()]

        """ response = cognito_client.admin_update_user_attributes(
            UserPoolId=USER_POOL_ID,
            Username=username,
            UserAttributes=user_attributes
        ) """

        return jsonify({'message': f'Usuario {username} actualizado exitosamente.', 'response': "response"}), 200
    #except KeyError as e:
    #    return jsonify({'error': f'Faltan parámetros necesarios: {str(e)}'}), 400
    #except Exception as e:
    #    return jsonify({'error': f'Error al actualizar el usuario: {str(e)}'}), 500
