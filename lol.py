from flask import Flask, request,jsonify
import os
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True

with open("flights_data.db", "r") as f:
    flights = f.readlines()
with open("userdata.db", "r") as f:
    userdata = f.readlines()

@app.route('/search',methods=['GET'])
def search_flights():
    date = request.json['date']
    source = request.json['source']
    dest = request.json['dest']
    result = ""
    for flight in flights:
        flight = [x.strip() for x in flight.strip().split(",")]
        if flight[1:4] == [date,source,dest]:
            val1 = flight[4]
            val2 = flight[5]
            result += "flight no-"+val1+" is available with "+val2+" seats left, "
            # result = '\n'.join(result)
    return jsonify(results=result)

@app.route('/book',methods=['POST'])
def booking():
    name = request.json['name']
    flight_name = request.json['flight_name']
    
    for line in userdata:
        if line.strip().split(",")[0].strip() == name and line.strip().split(",")[1].strip() == flight_name:
            if line.strip().split(",")[2].strip() == "booked":
                return jsonify(results="flight no-"+flight_name+"has already been booked by "+name+" ")
        else:
            with open("flights_data.db","w") as f:
                for line in flights:
                    if line.strip().split(",")[4].strip() == flight_name :
                        val = int(line.strip().split(",")[5])
                        val = val - 1
                        line = line.strip().split(",")[:5] + [val] 
                        line = ",".join(line)
                    f.write(line+"\n")

            string = name+","+flight_name+",booked"
            with open("userdata.db","w") as f:
                for line in userdata:
                    f.write(line+"\n")
                f.write(string)
            return jsonify(result="successfully booked")
    

@app.route('/cancel',methods=['POST'])
def cancellation():
    name = request.json['name'].strip()
    flight_name = request.json['flight_name'].strip()
    # string = name+","+flight_name+",cancelled"
    with open("userdata.db","w") as f:
        for line in userdata:
            if line.strip().split(",")[0].strip() == name and line.strip().split(",")[1].strip() == flight_name:
                line = line.strip().split(",")[:2] + ["cancelled"]
                line = ",".join(line)
            f.write(line+"\n")
    return jsonify(result="successfully cancelled")

if __name__=='__main__':
    app.run()
