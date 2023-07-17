function html2flask() {
    
    var itemName = document.getElementById("itemname").value;
    var result

    if(itemName==""){
        $("#errMsgForm").text("Please enter item name!")
        return;
    }else{
        $("#errMsgForm").text("")
    }
    var hasEgg = document.getElementById("eggCheck").checked;
    var eggOptions = document.getElementById("eggOptions").value;
    var hasNuts = document.getElementById("nutsCheck").checked;
    var nutsOptions = document.getElementById("nutsOptions").value;
    var hasMilk = document.getElementById("milkCheck").checked;
    var milkOptions = document.getElementById("milkOptions").value;

    var server_data = [
        {"customerID": 0},
        {"item": itemName},
        {"hasEgg": hasEgg},
        {"eggOptions": eggOptions},
        {"hasNuts": hasNuts},
        {"nutsOptions": nutsOptions},
        {"hasMilk": hasMilk},
        {"milkOptions": milkOptions},
      ];
    
    $.ajax({
        type: "POST",
        url: "/proc_allergen_db",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json', 
        success: function(result) {
            console.log("Result:");
            console.log(result);
            var markup = "<tr><td><input type='checkbox' name='record'></td><td>" + result.item + "</td><td>" + result.eggScore + "</td><td>" + result.nutsScore + "</td><td>" + result.milkScore + "</td></tr>";
            $("table tbody:last").append(markup);
          } 
      });
    
    // add row to table

    
    
    // clear form
    document.getElementById("itemname").value = "";
    document.getElementById("eggCheck").checked = false;
    document.getElementById("nutsCheck").checked = false;
    document.getElementById("milkCheck").checked = false;
    document.getElementById("eggOptions").value = "No";
    document.getElementById("nutsOptions").value = "No";
    document.getElementById("milkOptions").value = "No";
}

// https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file