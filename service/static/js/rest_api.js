$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promotion_id").val(res.promotion_id);
        $("#promotion_name").val(res.promotion_name);
        $("#promotion_code").val(res.promotion_code);
        $("#promotion_value").val(res.promotion_value);

        $("#promotion_type").val(res.promotion_type);
        $("#promotion_description").val(res.promotion_description);
        if (res.active == true) {
            $("#promotion_available").val("true");
        } else {
            $("#promotion_available").val("false");
        }
        $("#promotion_scope").val(res.promotion_scope);
        $("#start_date").val(res.start_date);
        $("#end_date").val(res.end_date);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promotion_name").val("");
        $("#promotion_type").val("");
        $("#promotion_code").val("");
        $("#promotion_value").val("");
        $("#promotion_type").val("");
        $("#promotion_description").val("");
        $("#promotion_active").val("");
        $("#promotion_scope").val("");
        $("#start_date").val("");
        $("#end_date").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#promotion_name").val();
        let type = $("#promotion_type").val();
        let active = $("#promotion_available").val() == "true";
        let scope = $("#promotion_scope").val();
        let date = $("#promotion_date").val();

        let data = {
            "name": name,
            "type": type,
            "active": active,
            "scope": scope,
            "date": date
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {

        let promotion_id = $("#promotion_id").val();
        let name = $("#promotion_name").val();
        let type = $("#promotion_type").val();
        let active = $("#promotion_available").val() == "true";
        let scope = $("#promotion_scope").val();
        let date = $("#promotion_date").val();

        let data = {
            "name": name,
            "type": type,
            "active": active,
            "scope": scope,
            "date": date
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/promotions/${promotion_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions/${promotion_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/promotions/${promotion_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#promotion_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Promotion
    // ****************************************

    $("#search-btn").click(function () {

        let promotion_date = $("#search_promotion_date").val();
        let promotion_types = $("#search_promotion_type").val().join(",");
        let promotion_scopes = $("#search_promotion_scope").val().join(",");

        let queryString = ""

        if (promotion_date) {
            queryString += 'datetime=' + promotion_date
        }
        if (promotion_types) {
            if (queryString.length > 0) {
                queryString += '&promotion_type=' + promotion_types
            } else {
                queryString += 'promotion_type=' + promotion_types
            }
        }
        if (promotion_scopes) {
            if (queryString.length > 0) {
                queryString += '&promotion_scope=' + promotion_scopes
            } else {
                queryString += 'promotion_scope=' + promotion_scopes
            }
        }

        console.log(queryString)

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Value</th>'
            table += '<th class="col-md-2">Code</th>'
            table += '<th class="col-md-2">Description</th>'
            table += '<th class="col-md-2">Type</th>'
            table += '<th class="col-md-2">Scope</th>'
            table += '<th class="col-md-2">Active</th>'
            table += '<th class="col-md-2">Start Date</th>'
            table += '<th class="col-md-2">End Date</th>'
            table += '</tr></thead><tbody>'
            let firstPromotion = "";
            for(let i = 0; i < res.length; i++) {
                let promotion = res[i];
                table += `<tr id="row_${i}"><td>${promotion.promotion_id}</td><td>${promotion.promotion_name}</td><td>${promotion.promotion_value}</td><td>${promotion.promotion_code}</td><td>${promotion.promotion_description}</td><td>${promotion.promotion_type}</td><td>${promotion.promotion_scope}</td><td>${promotion.active}</td><td>${promotion.start_date}</td><td>${promotion.end_date}</td></tr>`;
                if (i == 0) {
                    firstPromotion = promotion;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstPromotion != "") {
                update_form_data(firstPromotion)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
