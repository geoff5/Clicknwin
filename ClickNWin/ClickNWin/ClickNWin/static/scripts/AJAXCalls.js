function checkUser(user) {
    var req = new XMLHttpRequest();
    var sPath = window.location.pathname;
    var sPage = sPath.substring(sPath.lastIndexOf('/') + 1);
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            var response = JSON.parse(req.responseText);
            if (!response.exists && sPage == "buyCards") {
                document.getElementById("userError").style.backgroundColor = "#EB4141";
                document.getElementById("userError").innerText = "This user does not exist.  Please try again";
                return false;
            }
            else if (response.exists && sPage == "register") {
                document.getElementById("userError").style.backgroundColor = "#EB4141";
                document.getElementById("userError").innerText = "This username already exists.  Please try another";
                return false;
            }
            else {
                document.getElementById("userError").style.backgroundColor = "White";
                document.getElementById("userError").innerText = "";
            }
        }
    }

    req.open("POST", "/checkUser");
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('user=' + user);
}

function reveal(panel, id) {
    document.getElementById(panel).hidden = true;
    var checkHidden = []
    checkHidden.push(document.getElementById("panel1").hidden);
    checkHidden.push(document.getElementById("panel2").hidden);
    checkHidden.push(document.getElementById("panel3").hidden);
    checkHidden.push(document.getElementById("panel4").hidden);
    checkHidden.push(document.getElementById("panel5").hidden);
    checkHidden.push(document.getElementById("panel6").hidden);

    for (var i = 0; i < checkHidden.length; i++) {
        if (checkHidden[i] == false) {
            return false;
        }
    }

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            var response = JSON.parse(req.responseText);
            if (response.prize != '') {
                alert("Congratulations, you have won €" + response.prize + ". This prize will now be credited to your account balance ");
            }
            else {
                alert("Sorry, that card was not a winner.  Please try again");
            }
        }
    }

    req.open("POST", "/cardRedeemed");
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('id=' + id);
}

function drawCard(id) {
    panelArray = getPanels(id)
    var x = 70;
    var y = 50;

    var canvas = document.getElementById("card");
    var ctx = canvas.getContext("2d");
    ctx.fillStyle = "#FF0000";
    ctx.fillRect(0, 0, 600, 300);
    ctx.font = "15px Engravers MT";
    ctx.fillStyle = "white";
    ctx.textAlign = "left";
    ctx.fillText("ClickNWin", 350, 50);
    ctx.fillText("Standard Game", 350, 100);
    ctx.fillText("Great Prizes", 350, 150)

    while (panelArray.length > 0) {
        pick = Math.floor(Math.random() * (panelArray.length)) + 0;
        ctx.fillText("€" + panelArray[pick], x, y);
        panelArray.splice(pick, 1);
        y += 100
        if (panelArray.length == 3) {
            x += 120;
            y = 50;
        }
    }
}

function getPanels(id) {
    panels = []
    var req = new XMLHttpRequest()
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            var response = JSON.parse(req.responseText);
            panels = response.card
        }
    }
    req.open("POST", "/getCard", false);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('id=' + id);
    return panels
}

function calcPrice() {
    var type = document.getElementById("cardTypes").value;
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            var response = JSON.parse(req.responseText);
            var price = response.price;
            var quantity = parseFloat(document.getElementById("quantity").value);
            var total = price * quantity;
            total = total.toFixed(2);
            total = total.toString();
            document.getElementById("price").value = '€' + total;

        }
    }
    req.open("POST", "/getCardPrice");
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('type=' + type);
}