function registerFormValidation()//preforms validation on the registration form
{
    var pass1 = document.getElementById("password").value;
    var pass2 = document.getElementById("cpassword").value;
    var sPass1 = String(pass1);
    var sPass2 = String(pass2);
    var username = document.getElementById("username").value;
    var dob = document.getElementById("dob").value;
    var today = new Date()
    var birth = new Date(dob);
   
    var diff = today - birth.getTime();
    ageMs = new Date(diff);
    age = Math.abs(ageMs.getUTCFullYear() - 1970);

    var user = document.getElementById("userError").innerText;

    if(pass1 != pass2)//outputs error messages if passwords do not match and prevents form submit
    {
        document.getElementById("passMatch1").className = "error"
        document.getElementById("passMatch2").className = "error"
        document.getElementById("passMatch1").innerText = "Passwords do not match";
        document.getElementById("passMatch2").innerText = "Passwords do not match";
        return false;
    }
    else
    {
        document.getElementById("passMatch1").className = ""
        document.getElementById("passMatch2").className = ""
        document.getElementById("passMatch1").innerText = "";
        document.getElementById("passMatch2").innerText = "";
    }
   
    if (diff < 0)
    {
        document.getElementById("ageError").className = "error";
        document.getElementById("ageError").innerText = "Incorrect date entered";
        return false
    }
    else
    {
        document.getElementById("ageError").className = "";
        document.getElementById("ageError").innerText = "";
    }

    if(age < 18)//if age is too low, do not submit form and output error message
    {
        document.getElementById("ageError").className = "error";
        document.getElementById("ageError").innerText = "Your age must be 18 or greater";
        return false;
    }
    else
    {
        document.getElementById("ageError").className = "";
        document.getElementById("ageError").innerText = "";
    }
    if (user != "")//if user error message still displayed, then do not submit form
    {
        return false;
    }


}

function populateDates()//used on addPayment cards to prepare selectable dates
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

function validateCardNo()//uses the Luhn algorithm to validate card number is correct
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
        document.getElementById("invalidCard").style.backgroundColor = "#EB4141";
        document.getElementById("invalidCard").innerText = "Invalid card number.  Please re-enter"
        return true;
    }
    return false;
}


function validateDate()//ensures a card expiry date is valid
{
    var expiryYear = document.getElementById("expiryYears").value;
    var expiryMonth = document.getElementById("expiryMonths").value;
    var year = new Date().getFullYear();
    var month = new Date().getMonth();
    console.log(expiryMonth)
    console.log(month);

    if(expiryYear == year && expiryMonth <= month)
    {
        document.getElementById("invalidDate").style.backgroundColor = "#EB4141";
        document.getElementById("invalidDate").innerText = "Invalid Expiry Date.  Please re-enter";
        return true;
    }
    return false;
}

function validateCreditCardForm()//performs validations when adding a new credit to an account
{

    var cardNumber = validateCardNo();
    var date = validateDate();

    if(date == true || cardNumber == true)
    {
        return false;
    }
}

function addInput()//adds a user field if scratch card is being bought for a friend
{
    var check = document.getElementById("myself").checked;
    if (check)
    {
        document.getElementById("selectedUser").value = ""
        document.getElementById("userSelect").style.display = 'none'
        document.getElementById("userSelect").required = false
    }
    else
    {
        document.getElementById("userSelect").style.display = 'block'
        document.getElementById("userSelect").required = true
    }
}


function validateCardPurchase()//validates scratch card purchases
{
    var quantity = document.getElementById("quantity").value;
    if (quantity == '0')
    {
        document.getElementById("quantityError").innerText = "Please select a quantity greater than 0";
        document.getElementById("quantityError").className = "error";
        return false
    }
    
    var balance = document.getElementById("balance").innerText;
    var price = document.getElementById("price").value;
    price = price.substring(1, price.length);
    balance = parseFloat(balance);
    price = parseFloat(price);
    if (price > balance)
    {
        alert("You do not have enough funds to buy these cards.  Please top up and try again");
        return false
    }

    var user = document.getElementById("userError").innerText;
    if (user != "") {
        return false;
    }
}

function checkBalance(balance)//ensures user is able to redeem the requested amount from their balance
{
    var amount = document.getElementById("amount").value;
    amount = parseFloat(amount)
    amount = amount.toFixed(2);
    if (amount > balance)
    {
        alert("You do not have enough funds in your balance.  Please try a smaller amount");
        return false;
    }
    redeem = confirmRedeem();
    if(redeem == false)
    {
        return false;
    }
}

function topUpFormInput()//display elements for card payments or payapl payments
{

    if(document.getElementById("payBy2").checked)
    {
        document.getElementById("cardRow").style.display = "none";
        document.getElementById("cvvRow").style.display = "none";
        document.getElementById("paymentCards").required = false;
        document.getElementById("cvv").required = false;
    }

    else
    {
        document.getElementById("cardRow").style.display = "block";
        document.getElementById("cvvRow").style.display = "block";
        document.getElementById("paymentCards").required = true;
        document.getElementById("cvv").required = true;
    }
}

function confirmTopUp()//confirm the decison to top up balance
{
    var amount = document.getElementById("amount").value;
    var result = confirm("Are you sure you wish to top up your balance by €" + amount + ".  Press Ok to continue or Cancel to return.");
    return result;
}

function addAdminValidation()//validates the new admin form
{
    
    var pass1 = document.getElementById("password").value;
    var pass2 = document.getElementById("cpassword").value;

    if (pass1 != pass2) {
        document.getElementById("passMatch1").className = "error"
        document.getElementById("passMatch2").className = "error"
        document.getElementById("passMatch1").innerText = "Passwords do not match";
        document.getElementById("passMatch2").innerText = "Passwords do not match";
        return false;
    }
    else
    {
        document.getElementById("passMatch1").className = ""
        document.getElementById("passMatch2").className = ""
        document.getElementById("passMatch1").innerText = "";
        document.getElementById("passMatch2").innerText = "";
    }
    var error = document.getElementById("userError").innerText;
    if (error != "")
    {
        return false
    }
}

function newGameValidation()//ensures that newly created games have an overall chance value of 1
{
    var prize1 = parseFloat(document.getElementById("prize1Chance").value);
    var prize2 = parseFloat(document.getElementById("prize2Chance").value);
    var prize3 = parseFloat(document.getElementById("prize3Chance").value);
    var prize4 = parseFloat(document.getElementById("prize4Chance").value);
    var noWin = parseFloat(document.getElementById("notAWin").value);

    var overall = prize1 + prize2 + prize3 + prize4 + noWin;

    if (overall != 1)
    {
        document.getElementById("chanceError").innerText = "All chances do not add up to 1.  Please check and re-enter the prize chances";
        document.getElementById("chanceError").className = "error";
        return false;
    }
}

function calcNoWinChance()//when an admin is adding or modifying games, calculates the chance a card will not be a winner based on prize chances 
{
    var prize1 = document.getElementById("prize1Chance").value;
    var prize2 = document.getElementById("prize2Chance").value;
    var prize3 = document.getElementById("prize3Chance").value;
    var prize4 = document.getElementById("prize4Chance").value;
    prizes = [prize1, prize2, prize3, prize4]
    for (var i = 0; i < prizes.length; i++)
    {
        alert(prizes[i])
        for(var innerI = 0; innerI < prizes[i].length;innerI++)
        {
            alert(prizes[i].charAt(innerI))
            if(prizes[i].charAt(innerI) == 'e' || prizes[i].charAt(innerI) == 'E')
            {
                prizes[i] = prizes[i].substring(0, innerI - 1);
            }
        }
    }

    var noWin = 1
    for (var i = 0; i < prizes.length; i++)
    {
        noWin -= prizes[i]
    }
    noWin = noWin.toString();
    document.getElementById("notAWin").value = noWin;
}

function confirmRedeem()//confirm the decison to top up balance
{
    var amount = document.getElementById("amount").value;
    var result = confirm("Are you sure you wish to redeem €" + amount + " to your account.  Press Ok to continue or Cancel to return.");
    return result;
}