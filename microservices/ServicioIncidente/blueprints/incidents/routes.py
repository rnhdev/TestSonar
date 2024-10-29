from flask import Blueprint, request, jsonify
import json
from ServicioIncidente.commands.incident_create import CreateIncident
from ServicioIncidente.commands.incident_exists import ExistsIncident
from ServicioIncidente.commands.incident_get_all import GetAllIncidents
from ServicioIncidente.commands.incident_get import GetIncident
from ServicioIncidente.commands.incident_update import UpdateIncident
from ServicioIncidente.commands.attachment_exists import ExistsAttachment
from ServicioIncidente.commands.attachment_create import CreateAttachment
from ServicioIncidente.commands.attachment_get_all import GetAllAttachments
from ServicioIncidente.commands.attachment_get import GetAttachment
from ServicioIncidente.utils import decode_user, build_incident_id

incidents_bp = Blueprint('incident_bp', __name__)

@incidents_bp.route('/incidents', methods=['POST'])
def create_incident():
    auth_header = request.headers.get('Authorization')

    try:
        user = decode_user(auth_header)
        data = request.get_json()
        type = data.get('type')
        description = data.get('description')
        contact = data.get('contact', "")
        
        if not type or not description or len(description) < 1:
            return "Invalid parameters", 400
        
        if contact and len(contact) > 0:
            contact = json.dumps(contact)

        id = build_incident_id()
        
        data = CreateIncident(id, type, description, contact, user["id"], user["name"]).execute()

        return jsonify({
            "id": data.id,
            "type": data.type,
            "description": data.description,
            "contact": json.loads(data.contact),
            "user_issuer_id": data.user_issuer_id,
            "user_issuer_name": data.user_issuer_name,
            "createdAt": data.createdAt,
            "updatedAt": data.updatedAt
        }), 201
    except KeyError:
        return "Invalid parameters", 400
    except Exception as e:
        return jsonify({'error': f'Create incident failed. Details: {str(e)}'}), 500

    
@incidents_bp.route('/incidents/<incident_id>/attachments', methods=['PUT'])
def create_attachment(incident_id):
    auth_header = request.headers.get('Authorization')

    try:
        user = decode_user(auth_header)
        data = request.get_json()
        id = data.get('media_id')
        file_name = data.get('media_name')
        file_uri = data.get('media_uri')
        content_type = data.get('content_type')
        
        if not id or not incident_id or not file_name or not content_type or not file_uri:
            return "Invalid parameters", 400
        
        if not ExistsIncident(incident_id).execute():
            return "Incident not found", 404
        
        if ExistsAttachment(id).execute():
            return "Media id already exists", 400
        
        data = CreateAttachment(id, incident_id, file_name, file_uri, content_type,\
                                user["id"], user["name"]).execute()

        return jsonify({
            "id": data.id,
            "name": data.file_name,
            "uri": data.file_uri,
            "content_type": data.content_type,
            "user_attacher_id": data.user_attacher_id,
            "user_attacher_name": data.user_attacher_name,
            "createdAt": data.createdAt,
            "updatedAt": data.updatedAt
        }), 201
    except Exception as e:
        return jsonify({'error': f'Create attachment failed. Details: {str(e)}'}), 500

@incidents_bp.route('/incidents', methods=['GET'])
def get_all_incidents():
    try:
        incidents = GetAllIncidents().execute()

        result = []
        for incident in incidents:
            incident_data = {
                "id": incident.id,
                "type": incident.type,
                "description": incident.description,
                "contact": json.loads(incident.contact) if incident.contact else None,
                "user_issuer_id": incident.user_issuer_id,
                "user_issuer_name": incident.user_issuer_name,
                "createdAt": incident.createdAt,
                "updatedAt": incident.updatedAt,
                "attachments": [
                    {
                        "id": attachment.id,
                        "file_name": attachment.file_name,
                        "file_uri": attachment.file_uri,
                        "content_type": attachment.content_type,
                    } for attachment in (incident.attachments or [])
                ]
            }
            result.append(incident_data)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Get all incidents failed. Details: {str(e)}'}), 500

@incidents_bp.route('/incidents/<incident_id>', methods=['GET'])
def get_incident(incident_id):
    try:
        incident = GetIncident(incident_id).execute()
        
        if not incident:
            return "Incident not found", 404

        return jsonify({
            "id": incident.id,
            "type": incident.type,
            "description": incident.description,
            "contact": json.loads(incident.contact) if incident.contact else None,
            "user_issuer_id": incident.user_issuer_id,
            "user_issuer_name": incident.user_issuer_name,
            "createdAt": incident.createdAt,
            "updatedAt": incident.updatedAt,
            "attachments": [
                {
                    "id": attachment.id,
                    "file_name": attachment.file_name,
                    "file_uri": attachment.file_uri,
                    "content_type": attachment.content_type,
                } for attachment in incident.attachments
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': f'Get incident failed. Details: {str(e)}'}), 500

@incidents_bp.route('/incidents/<incident_id>', methods=['PUT'])
def update_incident(incident_id):
    auth_header = request.headers.get('Authorization')

    try:
        user = decode_user(auth_header)
        data = request.get_json()
        type = data.get('type')
        description = data.get('description')
        contact = data.get('contact')

        if type is not None and (not type or len(type) < 1):
            return jsonify({"error": "Invalid type parameter"}), 400
        if description is not None and (not description or len(description) < 1):
            return jsonify({"error": "Invalid description parameter"}), 400
        if contact is not None and contact != "" and not isinstance(contact, dict):
            return jsonify({"error": "Invalid contact format, must be a dictionary"}), 400

        if contact is not None:
            contact = json.dumps(contact)

        updated_incident = UpdateIncident(incident_id, type=type, description=description, contact=contact).execute()

        return jsonify({
            "id": updated_incident.id,
            "type": updated_incident.type,
            "description": updated_incident.description,
            "contact": json.loads(updated_incident.contact) if updated_incident.contact else None,
            "user_issuer_id": updated_incident.user_issuer_id,
            "user_issuer_name": updated_incident.user_issuer_name,
            "createdAt": updated_incident.createdAt,
            "updatedAt": updated_incident.updatedAt
        }), 200

    except ValueError as e:
        if str(e) == "Incident not found":
            return jsonify({"error": "Incident not found"}), 404
        return jsonify({"error": f"Update incident failed. Details: {str(e)}"}), 400
        
    except Exception as e:
        return jsonify({'error': f'Update incident failed. Details: {str(e)}'}), 500

@incidents_bp.route('/incidents/<incident_id>/attachments', methods=['GET'])
def get_all_attachments(incident_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401

    try:
        user = decode_user(auth_header)
        if not user: 
            return jsonify({"error": "Unauthorized"}), 401

        attachments = GetAllAttachments(incident_id).execute()
        result = [
            {
                "id": attachment.id,
                "file_name": attachment.file_name,
                "file_uri": attachment.file_uri,
                "content_type": attachment.content_type,
                "user_attacher_id": attachment.user_attacher_id,
                "user_attacher_name": attachment.user_attacher_name,
                "createdAt": attachment.createdAt,
                "updatedAt": attachment.updatedAt
            }
            for attachment in attachments
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve attachments. Details: {str(e)}"}), 500

@incidents_bp.route('/incidents/<incident_id>/attachments/<attachment_id>', methods=['GET'])
def get_attachment(incident_id, attachment_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401

    try:
        user = decode_user(auth_header)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        attachment = GetAttachment(incident_id, attachment_id).execute()
        if not attachment:
            return jsonify({"error": "Attachment not found"}), 404

        result = {
            "id": attachment.id,
            "file_name": attachment.file_name,
            "file_uri": attachment.file_uri,
            "content_type": attachment.content_type,
            "user_attacher_id": attachment.user_attacher_id,
            "user_attacher_name": attachment.user_attacher_name,
            "createdAt": attachment.createdAt,
            "updatedAt": attachment.updatedAt
        }
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve attachment. Details: {str(e)}"}), 500
