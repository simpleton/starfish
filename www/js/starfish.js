/**
 * Created with PyCharm.
 * User: xbfool
 * Date: 12-8-16
 * Time: AM10:27
 * To change this template use File | Settings | File Templates.
 */
var hello_test = function() {
    $.ajax({
        type:"GET",
        url:$.starfishd_url + "/hello?" + $('#param').val(),
        contentType: "application/json; charset=utf-8",
        success:function(data) {
            $("#result").html(data);
        },
        dataType:"html"
    });
};