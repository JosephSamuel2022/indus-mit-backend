from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

def fill_input_list(input_list, output_file):
    with open(output_file, 'r') as f:
        lines = f.readlines()
        index = 0
        while index < len(input_list):
            if input_list[index] == 'None':  # Check for the string 'None'
                # Find the first non-'None' value in the input list
                non_none_index = index
                while non_none_index < len(input_list) and input_list[non_none_index] == 'None':
                    non_none_index += 1
                if non_none_index == len(input_list):
                    break  # No more non-'None' values to fill
                y = input_list[non_none_index]
                # Find the line in the output file where y occurs at the xth index
                for line in lines:
                    line_values = [int(val) if val != 'None' else None for val in line.strip().split(',')]
                    if len(line_values) > index and line_values[index] == int(y):  # Convert y to int
                        # Fill the 'None' values before and after the xth index
                        for i in range(index, non_none_index):
                            if i < len(line_values) and input_list[i] == 'None':
                                input_list[i] = line_values[i]
                        index = non_none_index  # Move to the next non-'None' value
                        break
            else:
                index += 1 # Move to the next index in the input list
    
    

@app.route('/fill', methods=['POST'])
def fill_null_values():
    data = request.json
    
    input_list=data['values']
    
    print(input_list)
    output_file = 'output5.txt'  # Adjust this path as needed
    fill_input_list(input_list, output_file)
    print(input_list)
    return jsonify({'result': input_list})

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
