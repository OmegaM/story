/**
 * Created by OmegaMiao on 2015/9/20 18:49.
 */

function ajax_show(){
    $.getJSON("/story/1", function(data){
        var div_info = $("#info");
        div_info.children("br").remove();
        div_info.children("p").remove();
        div_info.append("<br><p>The author " + "<code>" + data.Story.author + "</code>" +
            " has been add a story " + "</p>" +
            "<p>" + "The title is " + "<code>" + data.Story.title + "</code></p>" +
            "<p>" + data.Story.content + "</p>");
    });
    return false;
}