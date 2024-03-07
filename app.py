from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)


def find_first_non_null(input_list,start_index):
    n=len(input_list)
    while(start_index<n):
      if(input_list[start_index]!="None"):
        return start_index
      start_index+=1
    return -1

def find_number_at_index(filename, number, index):

  found_lines = []
  with open(filename, "r") as file:
    for line in file:
      # Split the line based on commas and remove leading/trailing whitespaces
      line_data = [x.strip() for x in line.split(",")]
      # Check if the line has enough data for the specified index
      if len(line_data) > index and line_data[index] != "None" and str(number) == line_data[index]:
        found_lines.append(line.strip())  # Store the entire line

  return found_lines

def fill(sequence_from_file,input_list):
    filled_list = input_list.copy()
    for i in range(len(sequence_from_file)):

      if(input_list[i]=="None" and sequence_from_file!="None"):
        filled_list[i]=sequence_from_file[i]
    return filled_list

def generate_arrays(input_list, all_arrays, index=0):
    if index >= len(input_list):
        return
    i = find_first_non_null(input_list, index)
    if i == -1:
        return
    number = input_list[i]
    arr = find_number_at_index("output5.txt", number, i)
    for seq in arr:
        array = []
        for num in seq.split(','):
            if num.strip() == 'None':
                array.append('None')
            else:
                array.append(int(num))
        new_input_list = fill(array, input_list)
        all_arrays.append(new_input_list[:])
        generate_arrays(new_input_list, all_arrays, max(i + 1, len(array)))
    

@app.route('/fill', methods=['POST'])
def fill_null_values():
    data = request.json
    
    input_list=data['values']
    
    print(input_list)
    
    all_arrays = []
    generate_arrays(input_list, all_arrays)
    unique_arrays = [list(x) for x in set(tuple(x) for x in all_arrays)]
    print(len(unique_arrays))
    return jsonify({'result': unique_arrays})

if __name__ == '__main__':
    app.run(port=8000,debug=True)  # Run the Flask app in debug mode
