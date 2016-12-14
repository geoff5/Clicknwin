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

function getBalance()
{
    var bal = document.getElementById("balance").innerText;
    bal = parseFloat(bal);
    bal += 1;
    bal = bal.toFixed(2);
    bal = bal.toString();
    document.getElementById("balance").innerText = bal;
}