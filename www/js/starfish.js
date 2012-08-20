/**
 * Created with PyCharm.
 * User: xbfool
 * Date: 12-8-16
 * Time: AM10:27
 * To change this template use File | Settings | File Templates.
 */

var init_command_dict = function(obj){
    obj.command_dict = {
        echo_get:{
            url:'/echo',
            get_param:'name=simsun',
            post_param:''
        },
        echo_post:{
            url:'/echo',
            get_param:'name=simsun',
            post_param:'{"postname":"simsun"}'
        },
        user_update:{
            url:'/user_update',
            get_param:'',
            post_param:''
        },
        user_info_all:{
            url:'/user_info_all',
            get_param:'',
            post_param:''
        },
        user_info_relation:{
            url:'/user_info_relation',
            get_param:'',
            post_param:''
        },
        user_set_like_videos:{
            url:'/user_set_like_videos',
            get_param:'',
            post_param:''
        },
        get_hotest_list:{
            url:'/get_hotest_list',
            get_param:'',
            post_param:''
        },
        get_user_list:{
            url:'/get_user_list',
            get_param:'',
            post_param:''
        },
        get_video_comments:{
            url:'/get_video_comments',
            get_param:'',
            post_param:''
        },
        query_videos:{
            url:'/query_videos',
            get_param:'',
            post_param:''
        }
    };

};

var get_request = function(url, get){
    $.ajax({
            type:"GET",
            url:url + "?" + get,
            contentType: "application/json; charset=utf-8",
            success:function(data) {
                $("#result").html(data);
            },
            dataType:"html",
            statusCode: {
                404: function() {
                    $('#server_result').val('404');
                },
                200: function() {
                    $('#server_result').val('200');
                },
                503: function() {
                    $('#server_result').val('503');
                }

            }
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
            data:post,
            statusCode: {
                404: function() {
                    $('#server_result').val('404');
                },
                200: function() {
                    $('#server_result').val('200');
                },
                503: function() {
                    $('#server_result').val('503');
                }

            }
        }

    )
};