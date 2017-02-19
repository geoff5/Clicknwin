function formValidation() {
    var pass1 = document.getElementById("password").value;
    var pass2 = document.getElementById("cpassword").value;

    var sPass1 = String(pass1);
    var sPass2 = String(pass2);
    var username = document.getElementById("username").value;

    checkUser(username);
    var user = document.getElementById("userError").innerText;

    if(pass1 != pass2)
    {
        document.getElementById("passMatch1").innerText = "Passwords do not match";
        document.getElementById("passMatch2").innerText = "Passwords do not match";
        return false;
    }
    else if(user != "")
    {
        return false;
    }

}

function failedLogin(fail)
{
    if (fail == true)
    {
        document.getElementById("loginFail").innerText = "Username or Password is incorrect. Please try again."
    }
}

function populateDates()
{
    var months = document.getElementById("expiryMonths");
    var years = document.getElementById("expiryYears");

    for(var i = 1; i <= 12; i++)
    {
        var opt = document.createElement("option");
        opt.innerHTML = i;
        opt.value = i;
        months.appendChild(opt);
    }

    var year = new Date().getFullYear();

    for(var i = 0;i < 7;i++)
    {
        var opt = document.createElement("option");
        opt.innerHTML = year;
        opt.value = year;
        years.appendChild(opt);
        year++;
    }
}

function validateCardNo()
{
    number = document.getElementById("cardNumber").value;
    numArray = [];
    accepted = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9'];

    for(var i = number.length-1;i >= 0;i--)
    {
        for (var innerI = 0; innerI < accepted.length; innerI++)
        {
            if (number[i] === accepted[innerI])
            {
                numArray[i] = number.charAt(i);
                numArray[i] = parseInt(numArray[i]);
            }
        }
    }
    
    for (var i = 0; i < numArray.length; i++)
    {
        if(numArray[i] == null)
        {
            numArray.splice(i, 1);
        }
    }
    for(var i = numArray.length - 2;i >= 0;i -= 2)
    {
        numArray[i] *= 2;

        if (numArray[i] > 9)
        {
            numArray[i] -= 9;
        }
    }
    var total = 0;
    for (var i = 0;i < numArray.length;i++)
    {
        total += numArray[i];
    }

    if (total % 10 != 0)
    {
        document.getElementById("invalidCard").innerText = "Invalid card number.  Please re-enter"
        return true;
    }
    return false;
}


function validateDate()
{
    var expiryYear = document.getElementById("expiryYears").value;
    var expiryMonth = document.getElementById("expiryMonths").value;
    var year = new Date().getFullYear();
    var month = new Date().getMonth();

    if(expiryYear == year && expiryMonth < month)
    {
        document.getElementById("invalidDate").innerText = "Invalid Expiry Date.  Please re-enter";
        return true;
    }
    return false;
}

function validateForm()
{

    var cardNumber = validateCardNo();
    var date = validateDate();

    if(date == true || cardNumber == true)
    {
        return false;
    }
}

function addInput()
{
    var check = document.getElementById("myself").checked;
    if (!check)
    {
        document.getElementById("userSelect").innerHTML = "<label class='col-md-2 col-form-label form-label'>User</label><div class='col-md-4'><input type='text' id='selectedUser' name='selectedUser' onblur='checkUser(this.value)' /><span id='userError'></span></div>"
    }
    else
    {
        document.getElementById("userSelect").innerHTML = ""
    }
}

function calcPrice()
{
    var type = document.getElementById("cardTypes").value;
    var req = new XMLHttpRequest();
    req.onreadystatechange = function ()
    {
        if (req.readyState == 4 && req.status == 200)
        {
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

function validateCardPurchase() {
    var balance = document.getElementById("balance").innerText;
    var price = document.getElementById("price").value;
    price = price.substring(1, price.length);
    balance = parseFloat(balance);
    price = parseFloat(price);
    if (price > balance) {

        return false
    }
}

function checkUser(user)
{
    var req = new XMLHttpRequest();
    var sPath = window.location.pathname;
    var sPage = sPath.substring(sPath.lastIndexOf('/') + 1);
    req.onreadystatechange = function()
    {
        if (req.readyState == 4 && req.status == 200)
        {
            var response = JSON.parse(req.responseText);
            if (!response.exists && sPage == "buyCards")
            {
                document.getElementById("userError").innerText = "This user does not exist.  Please try again";
                return false;
            }
            else if(response.exists && sPage == "register")
            {
                document.getElementById("userError").innerText = "This usernme already exists.  Please try another";
                return false;
            }
            else
            {
                document.getElementById("userError").innerText = "";
            }
        }
    }

    req.open("POST", "/checkUser");
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send('user=' + user);
}