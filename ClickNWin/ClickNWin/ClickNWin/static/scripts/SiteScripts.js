function formValidation() {
    var pass1 = document.getElementById("password").value;
    var pass2 = document.getElementById("cpassword").value;

    var sPass1 = String(pass1);
    var sPass2 = String(pass2);

    if(pass1 != pass2)
    {
        document.getElementById("passMatch1").innerText = "Passwords do not match";
        document.getElementById("passMatch2").innerText = "Passwords do not match";
        return false;
    }
    
    else{
        
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

function validateCardNo(number)
{
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
        //alert("number = " + numArray[i] + "\n total = " + total);
    }

    if (total % 10 != 0)
    {
        document.getElementById("invalidCard").innerText = "Invalid card number.  Please re-enter"
    }
}

function clearMessage(id)
{
    document.getElementById(id).innerText = "";
}

function validateDate(expiryYear)
{
    var expiryMonth = document.getElementById("expiryMonths").value;
    var year = new Date().getFullYear();
    var month = new Date().getMonth();

    if(expiryYear == year && expiryMonth < month)
    {
        document.getElementById("invalidDate").innerText = "Invalid Expiry Date.  Please re-enter";
    }


}