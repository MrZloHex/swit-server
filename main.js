socket.onopen = function () {
    new WebSocket("ws://localhost:8000");
    
    let state = 10;
    socket.send(JSON.stringify({"method": "state", "value": "webpage"}))
    //
    const element = document.getElementById("hei")
    let a = element.addEventListener("click", () => {
        let input = document.getElementById("lname").value;
        if(input != "0" || "") {

            let c = Number(input)
            alert(typeof(c)) 
            if (!c.isNaN && c != 'indefined' && c != 0) {
                state = c
            } else {
                state = 10
            }

        } else {
            state = 10
        }    //if isinstance(input, int) {

        //} else {
        //    
        //}
    });

    alert(a)
    

    document.getElementById('but1').onclick = function() {
        socket.send(JSON.stringify({
            "method": "move",  
            "value": "forward",
            "time": state,
        }));
    }
    
    document.getElementById('but2').onclick = function() {
        socket.send(JSON.stringify({
            "method": "move",  
            "value": "backward",
            "time": "0",
        }));
    }

    document.getElementById('but3').onclick = function() {
        socket.send(JSON.stringify({
            "method": "move",  
            "value": "left",
            "time": "0",
        }));
    }
    
    document.getElementById('but4').onclick = function() {
        socket.send(JSON.stringify({
            "method": "move",  
            "value": "right",
            "time": "0",
        }));
    }

    document.getElementById('but5').onclick = function() {
        socket.send(JSON.stringify({"method":"stop"}));
    }
}

