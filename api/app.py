from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sum', methods=['GET', 'POST'])
def sum_route():
    try:
        if request.method == 'GET':
            a = request.args.get('a', default=None, type=float)
            b = request.args.get('b', default=None, type=float)
        else:
            data = request.get_json(force=True, silent=True) or {}
            a = data.get('a')
            b = data.get('b')

        if a is None or b is None:
            return jsonify({'error': 'provide a and b as query params or JSON body'}), 400

        result = a + b
        return jsonify({'a': a, 'b': b, 'sum': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Listen on all interfaces so Docker/k6 can reach it with --network host
    app.run(host='0.0.0.0', port=5000)
