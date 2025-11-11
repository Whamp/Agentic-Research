from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory key-value store
data_store = {}

@app.route('/mcp', methods=['POST'])
def mcp_handler():
    try:
        payload = request.get_json()
        tool_name = payload.get('tool_name')
        params = payload.get('params', {})

        if tool_name == 'get':
            key = params.get('key')
            if key in data_store:
                return jsonify({'success': True, 'value': data_store[key]})
            else:
                return jsonify({'success': False, 'error': f'Key "{key}" not found.'}), 404

        elif tool_name == 'set':
            key = params.get('key')
            value = params.get('value')
            if key is not None and value is not None:
                data_store[key] = value
                return jsonify({'success': True, 'message': f'Key "{key}" set successfully.'})
            else:
                return jsonify({'success': False, 'error': 'Missing key or value.'}), 400

        elif tool_name == 'delete':
            key = params.get('key')
            if key in data_store:
                del data_store[key]
                return jsonify({'success': True, 'message': f'Key "{key}" deleted successfully.'})
            else:
                return jsonify({'success': False, 'error': f'Key "{key}" not found.'}), 404

        else:
            return jsonify({'success': False, 'error': f'Tool "{tool_name}" not found.'}), 404

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
