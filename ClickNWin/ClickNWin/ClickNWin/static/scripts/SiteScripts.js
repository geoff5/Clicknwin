function formValidation() {
    var pass1 = document.getElementById("password").value;
    var pass2 = document.getElementById("cpassword").value;

    var sPass1 = String(pass1);
    var sPass2 = String(pass2);


    alert(pass1 + "\n" + pass2);
    if(pass1 != pass2)
    {
        alert("no match")
        //document.getElementById("cpassword").innerHTML = "Passwords do not match";
        return false;
    }
    
    else{
        
    }    
    
}