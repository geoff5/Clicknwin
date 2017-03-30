function checkUser(user)//AJAX call to check if a given username exists
{
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


function reveal(panel, id)//Makes scratch card panels disappear.  Once all are gone, makes an AJAX call to redeem the card in the database and add funds to user balance if neccessary
{
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

function getPanels(id)//AJAX call to retrieve panel list from server
{
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

function calcPrice()//calculates the price of selected amount of cards 
{
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
    req.open("POST", "/getCardPrice")
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('type=' + type);
}

function getCardType(id)//AJAX call to get the type of card about to be redeemed
{
    var game = ""
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            var response = JSON.parse(req.responseText);
            game = response.cardType;
        }
    }
    req.open("POST", "/getCardType", false);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('id=' + id);
    return game
}

function drawCard(id)//uses HTML canvas to draw card design by using AJAX call to retrive card's prize
{
    panelArray = getPanels(id);
    cardType = getCardType(id);
    var x = 70;
    var y = 50;

    if (cardType == "Standard")
    {
        design = "#FF0000"
    }
    else if (cardType == "Premium")
    {
        design = "#003399"
    }
    else
    {
        design = "#00CC00"
    }

    var canvas = document.getElementById("card");
    var ctx = canvas.getContext("2d");
    ctx.fillStyle = design;
    ctx.fillRect(0, 0, 600, 300);
    ctx.font = "15px Engravers MT";
    ctx.fillStyle = "white";
    ctx.textAlign = "left";
    ctx.fillText("ClickNWin", 350, 50);
    ctx.fillText(cardType + " Game", 350, 100);
    ctx.fillText("Great Prizes", 350, 150)

    if (cardType == "") {
        var canvas = document.getElementById("card");
        var ctx = canvas.getContext("2d");
        ctx.fillStyle = "#000000";
        ctx.fillRect(0, 0, 600, 300);
        ctx.font = "15px Engravers MT";
        ctx.fillStyle = "white";
        ctx.textAlign = "left";
        ctx.fillText("No card to redeem", 350, 50);
    }


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

function checkAdmin()//AJAX call to check a given admin username is not already taken
{
    var user = document.getElementById("username").value;
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            var response = JSON.parse(req.responseText);
            if (response.exists == true) {
                document.getElementById("userError").innerText = "Username already exists.  Try another";
                document.getElementById("userError").className = "error";
            }
            else {
                document.getElementById("userError").innerText = "";
                document.getElementById("userError").className = "";
            }
            
        }
    }

    req.open("POST", "/checkAdmin");
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('user=' + user);
}

function checkGame()//Ajax Call to check that a given game name is not already taken
{
    var game = document.getElementById("gameName").value;
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            response = JSON.parse(req.responseText)
            if (response.exists == true) {
                document.getElementById("gameError").innerText = "Name already taken.  Please select another"
                document.getElementById("gameError").className = "error"
            }
            else {
                document.getElementById("gameError").innerText = ""
                document.getElementById("gameError").className = ""
            }
        }
    }
    req.open("POST", "/checkGame");
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('game=' + game);
}

function getGame(game)//AJAX to retrieve game information from the database
{
    var data = []
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            response = JSON.parse(req.responseText)
            data = response.data;
            document.getElementById("gameName").value = data[0]
            document.getElementById("gamePrice").value = data[1]
            document.getElementById("prize1").value = data[2]
            document.getElementById("prize1Chance").value = data[3]
            document.getElementById("prize2").value = data[4]
            document.getElementById("prize2Chance").value = data[5]
            document.getElementById("prize3").value = data[6]
            document.getElementById("prize3Chance").value = data[7]
            document.getElementById("prize4").value = data[8]
            document.getElementById("prize4Chance").value = data[9]
            calcNoWinChance()
            document.getElementById("sButton").disabled = false;
        }
    }

    req.open("POST", "/getGame");
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('game=' + game);
}