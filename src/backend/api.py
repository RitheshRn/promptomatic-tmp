from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import logging
from promtomatic.main import (
    process_input,
    save_feedback,
    feedback_store,
    optimize_with_feedback,
    optimization_sessions
)
from flask_cors import cross_origin
import json

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)  # Changed to INFO level
logger = logging.getLogger(__name__)

@app.route('/optimize', methods=['POST'])
def optimize_prompt_endpoint():
    session_id = None
    try:
        data = request.json
        human_input = data.get('human_input')
        print("API received input:", human_input)  # Debug log
        
        result = process_input(raw_input=human_input)
        print("API received result from process_input:", result)  # Debug log
        
        # Ensure result has all required fields and fix nested structure
        response = {
            'result': result.get('result', ''),  # Get the actual result string
            'session_id': result.get('session_id', None),
            'metrics': result.get('metrics', None)
        }
        
        # If result is nested, unnest it
        if isinstance(response['result'], dict):
            response = {
                'result': response['result'].get('result', ''),
                'session_id': response['result'].get('session_id', None),
                'metrics': response['result'].get('metrics', None)
            }
        
        print("API sending response:", response)  # Debug log
        return jsonify(response)
    except Exception as e:
        print("API error:", str(e))  # Debug log
        # Try to parse the error message if it's JSON
        try:
            error_data = json.loads(str(e))
            session_id = error_data.get('session_id')
            error_response = {
                'error': error_data.get('error', str(e)),
                'session_id': session_id,
                'result': None,
                'metrics': None
            }
            print("API sending error response:", error_response)  # Debug log
            return jsonify(error_response), 500
        except json.JSONDecodeError:
            error_response = {
                'error': str(e),
                'session_id': session_id,
                'result': None,
                'metrics': None
            }
            print("API sending error response:", error_response)  # Debug log
            return jsonify(error_response), 500

@app.route('/optimize-with-feedback', methods=['POST'])
@cross_origin()
def optimize_with_feedback_endpoint():
    try:
        data = request.json
        session_id = data.get('session_id')
        print(f"Received optimize-with-feedback request for session: {session_id}")  # Debug log
        
        if not session_id:
            return jsonify({
                'error': 'No session_id provided',
                'result': None,
                'metrics': None
            }), 400
            
        # Get the session
        session = optimization_sessions.get(session_id)
        if not session:
            print(f"Session not found: {session_id}")  # Debug log
            return jsonify({
                'error': f'Session {session_id} not found',
                'result': None,
                'metrics': None
            }), 404
            
        # Get the latest feedback for this session using the proper method
        session_feedbacks = feedback_store.get_feedback_for_prompt(session_id)
        if not session_feedbacks:
            print(f"No feedback found for session: {session_id}")  # Debug log
            return jsonify({
                'error': 'No feedback found for this session',
                'result': None,
                'metrics': None
            }), 400
            
        # Call optimize_with_feedback with the session_id
        result = optimize_with_feedback(session_id)
        print(f"Optimization result: {result}")  # Debug log
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in optimize_with_feedback_endpoint: {str(e)}")  # Debug log
        return jsonify({
            'error': str(e),
            'session_id': session_id if 'session_id' in locals() else None,
            'result': None,
            'metrics': None
        }), 500

@app.route('/comments', methods=['POST'])
@cross_origin()
def add_comment():
    try:
        data = request.json
        print(f"Received data in /comments endpoint: {data}")  # Debug log
        
        # Validate required fields
        required_fields = ['text', 'startOffset', 'endOffset', 'feedback', 'promptId']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            print(f"Missing required fields: {missing_fields}")  # Debug log
            return jsonify({
                "success": False, 
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
            
        result = save_feedback(
            text=data['text'],
            start_offset=data['startOffset'],
            end_offset=data['endOffset'],
            feedback=data['feedback'],  # Changed from comment to feedback
            prompt_id=data['promptId']
        )
        return jsonify({"success": True, "comment": result})
    except Exception as e:
        print(f"Error in add_comment endpoint: {str(e)}")  # Debug log
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/comments', methods=['GET'])
@cross_origin()
def get_comments():
    try:
        # Convert comments to JSON-serializable format
        comments_json = [{
            "id": comment.id,
            "text": comment.text,
            "startOffset": comment.start_offset,
            "endOffset": comment.end_offset,
            "comment": comment.comment,
            "promptId": comment.prompt_id,
            "createdAt": comment.created_at.isoformat()
        } for comment in feedback_store]
        
        return jsonify({"success": True, "comments": comments_json})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/session/<session_id>', methods=['GET'])
@cross_origin()
def get_session(session_id):
    try:
        if session_id not in optimization_sessions:
            return jsonify({
                'error': 'Session not found'
            }), 404
            
        session = optimization_sessions[session_id]
        return jsonify({
            'success': True,
            'session': session.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/session/<session_id>/log', methods=['GET'])
@cross_origin()
def get_session_log(session_id):
    try:
        logger.info(f"Attempting to get log for session: {session_id}")
        
        if session_id not in optimization_sessions:
            logger.error(f"Session not found: {session_id}")
            return jsonify({
                'error': 'Session not found'
            }), 404
            
        session = optimization_sessions[session_id]
        logger.info("Found session, formatting log...")
        
        try:
            log_content = session.logger.format_log()
            logger.info("Log formatted successfully")
            
            # Even if there was an error in the optimization process,
            # we still want to return the log
            response = make_response(log_content)
            response.headers['Content-Type'] = 'text/plain'
            response.headers['Content-Disposition'] = f'attachment; filename=session_{session_id}_log.txt'
            logger.info("Response prepared successfully")
            return response
            
        except Exception as format_error:
            logger.error(f"Error formatting log: {str(format_error)}")
            return jsonify({
                'error': f'Error formatting log: {str(format_error)}'
            }), 500
        
    except Exception as e:
        logger.error(f"Unexpected error in get_session_log: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)