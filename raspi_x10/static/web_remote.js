$(document).ready(function() {
    refresh_status();

    $(".away-mode").click(function(event) {
        $.getJSON("/away_mode")
            .done(function(json) {
                update_away_mode(json.AwayMode);
            })
            .fail(function(){
                alert("Failed to toggle Away Mode");
            });
        event.preventDefault();
    });

    $("#refresh-status").click(function(event) {
        refresh_status();
        event.preventDefault();
    });
});


function refresh_status() {
    $.getJSON("/status")
        .done(function(json) {
            update_away_mode(json.AwayMode);
        })
        .fail(function() {
            alert("Failed to refresh status");
        });
}


function update_away_mode(state) {
    if(state) {
        toggle_button($("#away-mode"), true);
        toggle_button($("#people-home"), false);
    } else {
        toggle_button($("#away-mode"), false);
        toggle_button($("#people-home"), true);
    }
}


function toggle_button(btn, selected) {
    if(selected) {
        btn.removeClass("btn-default").addClass("btn-info");
    } else {
        btn.removeClass("btn-info").addClass("btn-default");
    }
}
