function geturlparam(param){
    var url = window.location.search.substring(1);
    var urlvars = url.split('&');
    for (var i = 0; i < urlvars.length; i++) 
    {
        var paramname = urlvars[i].split('=');
        if (paramname[0] == param) 
        {
            return paramname[1];
        }
    }
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
    
    if(confirm('Are you sure to delete the items from the database?') == true){

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

function editrow(ctl){
    // https://www.codemag.com/article/1511031/CRUD-in-HTML-JavaScript-and-jQuery

    // Set the following variables as global variables so that they can be accessible by modal 
    var currentRow = $(ctl).parents("tr");
    var cols = currentRow.children("td");
    var edititemname = $(cols[2]).text();
    var editEggScore = $(cols[3]).text();
    var editNutsScore = $(cols[4]).text();
    var editMilkScore = $(cols[5]).text();
    var editWheatScore = $(cols[6]).text();
    var editFishScore = $(cols[7]).text();
    var editShellfishScore = $(cols[8]).text();
    var editSesamiScore = $(cols[9]).text();
    var editPeanutsScore = $(cols[10]).text();
    var editSoyScore = $(cols[11]).text();

    $('#editModal').modal('show');
   
    $('#editModal').on('shown.bs.modal', function (event) {
        $('#itemname').val(edititemname);
        // To make it simple, make item name just read only
        $('#itemname').attr('readonly',true)

        if(editEggScore=='X'){
            $("#eggCheck").prop('checked',true);
            $('#eggOptions').val('No');
        }else if(editEggScore=='*'){
            $("#eggCheck").prop('checked',true);
            $('#eggOptions').val('Yes');
        }else{
            $("#eggCheck").prop('checked',false);
            $('#eggOptions').val('No');
        }

        if(editNutsScore=='X'){
            $("#nutsCheck").prop('checked',true);
            $('#nutsOptions').val('No');
        }else if(editNutsScore=='*'){
            $("#nutsCheck").prop('checked',true);
            $('#nutsOptions').val('Yes');
        }else{
            $("#nutsCheck").prop('checked',false);
            $('#nutsOptions').val('No');
        }

        if(editMilkScore=='X'){
            $("#milkCheck").prop('checked',true);
            $('#milkOptions').val('No');
        }else if(editMilkScore=='*'){
            $("#milkCheck").prop('checked',true);
            $('#milkOptions').val('Yes');
        }else{
            $("#milkCheck").prop('checked',false);
            $('#milkOptions').val('No');
        }

        if(editWheatScore=='X'){
            $("#wheatCheck").prop('checked',true);
            $('#wheatOptions').val('No');
        }else if(editWheatScore=='*'){
            $("#wheatCheck").prop('checked',true);
            $('#wheatOptions').val('Yes');
        }else{
            $("#wheatCheck").prop('checked',false);
            $('#wheatOptions').val('No');
        }

        if(editFishScore=='X'){
            $("#fishCheck").prop('checked',true);
            $('#fishOptions').val('No');
        }else if(editFishScore=='*'){
            $("#fishCheck").prop('checked',true);
            $('#fishOptions').val('Yes');
        }else{
            $("#fishCheck").prop('checked',false);
            $('#fishOptions').val('No');
        }

        if(editShellfishScore=='X'){
            $("#shellfishCheck").prop('checked',true);
            $('#shellfishOptions').val('No');
        }else if(editShellfishScore=='*'){
            $("#shellfishCheck").prop('checked',true);
            $('#shellfishOptions').val('Yes');
        }else{
            $("#shellfishCheck").prop('checked',false);
            $('#shellfishOptions').val('No');
        }

        if(editSesamiScore=='X'){
            $("#sesamiCheck").prop('checked',true);
            $('#sesamiOptions').val('No');
        }else if(editSesamiScore=='*'){
            $("#sesamiCheck").prop('checked',true);
            $('#sesamiOptions').val('Yes');
        }else{
            $("#sesamiCheck").prop('checked',false);
            $('#sesamiOptions').val('No');
        }

        if(editPeanutsScore=='X'){
            $("#peanutsCheck").prop('checked',true);
            $('#peanutsOptions').val('No');
        }else if(editPeanutsScore=='*'){
            $("#peanutsCheck").prop('checked',true);
            $('#peanutsOptions').val('Yes');
        }else{
            $("#peanutsCheck").prop('checked',false);
            $('#peanutsOptions').val('No');
        }

        if(editSoyScore=='X'){
            $("#soyCheck").prop('checked',true);
            $('#soyOptions').val('No');
        }else if(editSoyScore=='*'){
            $("#soyCheck").prop('checked',true);
            $('#soyOptions').val('Yes');
        }else{
            $("#soyCheck").prop('checked',false);
            $('#soyOptions').val('No');
        }

    })
}

function updateitem(){
    var updateItemName = document.getElementById("itemname").value;
    alert(updateItemName);

}

function score2symbol(score){
    if(score==100){
        return ""
    }else if(score==50){
        return "*"
    }else{
        return "X";
    }
}

// https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file