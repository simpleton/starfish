/**
 * Created with PyCharm.
 * User: xbfool
 * Date: 12-8-16
 * Time: AM10:27
 * To change this template use File | Settings | File Templates.
 */

var init_url = function(){

}
var get_request = function(url, get){
    $.ajax({
            type:"GET",
            url:url + "?" + get,
            contentType: "application/json; charset=utf-8",
            success:function(data) {
                $("#result").html(data);
            },
            dataType:"html"
        }

    )
};

var post_request = function(url, get, post){
    $.ajax({
            type:"POST",
            url:url + "?" + get,
            contentType: "application/json; charset=utf-8",
            success:function(data) {
                $("#result").html(data);
            },
            dataType:"html",
            data:post
        }

    )
};