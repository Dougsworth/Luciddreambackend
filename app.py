from flask import Flask, request, jsonify
from aijson import Flow
import asyncio

app = Flask(__name__)

async def analyze_dream(dream_content):
    flow = Flow.from_file('dream_analysis.ai.yaml')
    flow = flow.set_vars(dream_content=dream_content)
    result = await flow.run()

    # Assuming the result is a JSON string, try to load it as a dictionary
    try:
        import json
        result_dict = json.loads(result)
    except json.JSONDecodeError:
        result_dict = {"error": "Invalid JSON response"}

    return result_dict

@app.route('/analyze-dream', methods=['POST'])
def analyze_dream_endpoint():
    data = request.json
    dream_content = data.get('dream')
    analysis = asyncio.run(analyze_dream(dream_content))
    return jsonify({'analysis': analysis.get('analyze_dream', 'No analysis found'), 'keywords': analysis.get('keywords', [])})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
