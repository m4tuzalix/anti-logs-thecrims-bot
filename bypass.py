
class bypass:
    def __init__(self, route):
        self.route = route

    def logs_bypass(self, action, exit_key):
        from random import randint
        self.action = action
        self.exit_key = exit_key
        first_input_timestamp = "158240674"
        cordx = randint(1020, 1040)
        cordy = randint(350,430)
        logs_itteration = randint(22,44)
       
        payload = {
                "victim_id":f"{self.exit_key}",
                "encountered_at":int(first_input_timestamp+str(randint(2400,3900))),
                "created_at":int(first_input_timestamp+str(randint(4500,5900))),
                "id":f"{self.exit_key}",
                "reason":"Manual exit", #/// in case when clicking enter club
                "exit_key":f"{self.exit_key}",
                "e_at": None,
                "input":[],
                "input_counters":{"mousemove":randint(60,190), "mousedown":randint(1,3)},
                "first_input_timestamp": int(first_input_timestamp+str(randint(2400,3900))),
                "action_timestamp":int(first_input_timestamp+str(randint(4500,5900))),
            }
        if self.action == "normal": #/// in case of other requests
            for element in ["victim_id","encountered_at","created_at","id","reason", "exit_key", "e_at"]:
                del payload[element]
            payload["input_counters"]["mousemove"] = randint(970,1020)
            logs_itteration = 100

        elif self.action == "exit":
            for element in ["victim_id","encountered_at","created_at","id"]:
                del payload[element]
            
        elif self.action == "enter":
            for element in ["victim_id","encountered_at","created_at","reason", "exit_key", "e_at"]:
                del payload[element]

        elif self.action == "kill":
            for element in ["id","reason", "exit_key", "e_at"]:
                del payload[element]
            user_id = int(self.exit_key)
            payload["victim_id"] = user_id

        for x in range(logs_itteration):
            first_input = randint(2400,3900)
            input_timestamp = first_input_timestamp+str(first_input)
            cord_sumbition = randint(3,7)
            final_cordx = cordx - cord_sumbition
            if cordy < 120:
                final_cordy = cordy + cord_sumbition
            else:
                final_cordy = cordy - cord_sumbition
            payload["input"].append({"type":"mousemove", "x":final_cordx, "y":final_cordy, "which":0, "target":"", "time":input_timestamp, "route":f"{self.route}"})
            cordx = final_cordx
            cordy = final_cordy
        return payload


