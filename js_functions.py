js_request_login = """
                    const username = arguments[0]
                    const password = arguments[1]
                    const token = get_HTML()["_token"]
                    const action = get_HTML()["action"]
                    const data = "username="+username+"&password="+password+"&token="+token+"&action="+action+"&pl=&env="

                    // sends the xhr request with the above data ^^^^
                    function send(method,url,data){
                        const xhr = new XMLHttpRequest();
                        const promise = new Promise(function(resolve,reject){
                            xhr.open(method, url)
                            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                            xhr.onload = function(){
                                const raw_content = String(xhr.response)
                                const start_index = raw_content.indexOf("request")
                                const end_index = raw_content.indexOf("</settings>")
                                const x_request = raw_content.substring(start_index+("request=").length+1, end_index-3)
                                resolve(x_request)
                            };
                            xhr.send(data)
                        });
                        return promise;
                    };
                    var x_req = "12"
                    // async function capturing the response
                    async function final(){
                        await send("POST", "https://www.thecrims.com/login",data).then((responseData)=>{
                                x_req = responseData
                                console.log(responseData)
                                
                        });
                    };

                    // returns dynamic attributes required to send the request
                    function get_HTML(){
                        const hidden_values = {};
                        var all_inputs = document.querySelectorAll(".form-signin input");
                        all_inputs.forEach((single)=>{
                            const single_name = single.getAttribute("name")
                            const single_value = single.getAttribute("value")
                            if(single_name === "_token" || single_name === "action"){
                                hidden_values[single_name] = single_value;
                            };
                        });
                        return(hidden_values);
                    };
                    final()
                    setTimeout(()=>{
                        alert(x_req)
                        window.location = "https://www.thecrims.com/newspaper#/newspaper"
                    },3000)
                """
js_get_victim_data = """
                    function get_data(){
                        const data = {}
                        const main_selector = document.querySelector("ul.unstyled.inline.user_list.nightlife_user_list-wvAHNDRXPPwuDdwQZDzyK_0 li")
                        const name_id = main_selector.querySelector("div:nth-child(1) span a img")
                        for(i=0; i<name_id.attributes.length;i++){
                        var attribute = name_id.attributes[i]
                        if(String(attribute.name).includes("data")){
                            var name = String(attribute.name).slice(5)
                            data[name] = attribute.value
                        }
                    }
                    const user_name_selector = main_selector.querySelector("div.user_list_username")
                    const respect_prof = user_name_selector.parentNode
                    data["proffesion"] = respect_prof.querySelector("div:nth-child(2)").innerText.trim();
                    data["respect"] = respect_prof.querySelector("div:nth-child(3)").innerText.trim().slice(9);
                    return data;
                }
                return get_data();
                """

js_get_clubs = """
            var data = ""
            const x_request = arguments[0]
            function get_clubs(xreq){
                $.ajax({
                        url: "https://www.thecrims.com/api/v1/nightclubs",
                        type: 'GET',
                        processData: false,
                        contentType: "application/json",
                        dataType: "json",
                        headers: {"x-request":xreq},
                        success: function (result) {
                        results = result["nightclubs"]
                        x= Math.floor(Math.random() * results.length)
                        data = results[x]["id"]
                        console.log(data)
                        },
                        error: function (result) {
                            console.log(result);
                        }
                    });
            }
            get_clubs(x_request)
            setTimeout(()=>{
                alert(data)
            },2000)
            """
js_main_requests_pattern = """
                            const json = arguments[0]
                            const post_route = arguments[1]
                            const x_request = arguments[2]
                            const move = arguments[3]
                            const arg = arguments[4]
                           
                           

                            
                            $.ajax({
                            url: post_route,
                            type: 'POST',
                            data: json,
                            processData: false,
                            contentType: "application/json",
                            dataType: "json",
                            headers: {"x-request":x_request},
                            success: function (result) {
                                if(move.length > 0){
                                    window.location = move
                                }
                                const drugs = Array.from(result["nightclub"]["products"]["drugs"])
                                const hookers = Array.from(result["nightclub"]["products"]["hookers"])
                                
                                var id = 0;
                                var entrance = "";

                                if(drugs.length != 0){
                                        id = drugs[0]["id"]
                                        entrance = "drug"
                                    }
                                else{
                                    id = hookers[0]["id"]
                                    entrance = "hooker"
                                }
                               
                                const hp_bar = document.querySelector("div.default-1CS8SFNfrzFfM38mxoY6af_0").offsetWidth
                                const current_hp = Math.round(100*hp_bar / 128);

                                if(current_hp < 50){
                                    new_json = JSON.parse(json)
                                    new_json.id = id
                                    console.log(id)
                                    restore_hp(x_request, JSON.stringify(new_json), entrance)
                                }
                            },
                            error: function (result) {
                                console.log(result);
                            }
                        });

                        function restore_hp(xreq, json_file, entrance){
                            console.log(json_file)
                            $.ajax({
                                url: "https://www.thecrims.com/api/v1/nightclub/"+String(entrance),
                                type: 'POST',
                                data: json_file,
                                processData: false,
                                contentType: "application/json",
                                dataType: "json",
                                headers: {"x-request":xreq},
                                success: function (result) {
                                    console.log(result)
                                    
                                },
                                error: function (result) {
                                    console.log(result);
                                }
                            });
                        }
                        """