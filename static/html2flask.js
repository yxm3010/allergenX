function addrow() {
    
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
        success: location.reload()
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

function removerow(){
    var i = 0;
    const items = [];
    $("#dbtable input[type=checkbox]:checked").each(function () {
        var currentRow = $(this).closest("tr");
        var itemName = currentRow.find("td:eq(2)").text();
        items[i] = itemName;
        i += 1;
    });
    
    if(confirm('Are you sure to delete the following from the database?\n ${items}') == true){

        var serverData = [
            {"customerID": 0},
            {"items": items},
        ];

        $.ajax({
            type: "POST",
            url: "/del_allergen_db",
            data: JSON.stringify(serverData),
            contentType: "application/json",
            dataType: 'json',
            success: location.reload()
            })
    }
}

function score2symbol(score){
    if(score==100){
        return ""
    }else if(score==50){
        return "<i style='color:orange' class='bi bi-x-octagon'></i>"
    }else{
        return "<i style='color:red' class='bi bi-x-octagon-fill'></i>";
    }
}

// https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file