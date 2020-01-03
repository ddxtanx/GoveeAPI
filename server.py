from flask import Flask, request
import time
import pexpect
from constants import server_secret, server_port
app = Flask(__name__)

console = pexpect.spawn("bash")
@app.route('/alarm', methods=["POST", "GET"])
def alarm():
    if request.method == "POST":
        rdict = request.form.to_dict()
        if "alarm" in rdict.keys():
            alarm = request.form["alarm"].replace(" at ", "").replace(" : ", ":").replace(" . ", ".").replace(" .", ".")
            correct_ampm_alarm = alarm.replace("a.m.", "AM").replace("p.m.", "PM")
            is_day_before = (time.strftime("%p") == "PM")
            time_str = correct_ampm_alarm + " tomorrow" if is_day_before else correct_ampm_alarm
            command_str = f"at {time_str} -f ./start_bright_increase.sh"
            print(command_str)
            console.sendline(command_str)
            return "done"
        else:
            return "Bad request"
    else:
        return "Empty request"

@app.route('/strobe', methods=["GET"])
def strobe():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        console.sendline("sudo python3 tool.py strobe --period .3")
        return "done"
    else:
        return "Bad request"

@app.route('/end_strobe')
def end():
    console.sendintr()
    return "Done"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)
