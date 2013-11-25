/*
  This file is part of Dispatcher

  Dispatcher is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  Dispatcher is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with Dispatcher.  If not, see <http://www.gnu.org/licenses/>.
*/

var print_messages = function () {
    var msgs = document.getElementsByClassName("message");
    for (var i=0; i<msgs.length; i+=1) {
        var msg = msgs[i];
        console.info("MESSAGE #"+i+":\n"+msg.innerHTML+"\n\n\n");
    }
};


var post_message = function (panel, sender, stamp, content) {
    //var target = document.getElementById(panel);
    var query = $("#"+panel+">.viewport");
    var target = query[0];

    var magnet_scroll = false;
    var scroll_height = Math.max(target.scrollHeight, target.clientHeight);
    if (scroll_height - target.scrollTop == target.clientHeight) {
        var magnet_scroll = true;
    }

    var sender_div = document.createElement("div");
    sender_div.className = "sender";
    sender_div.appendChild(document.createTextNode(sender));

    var stamp_div = document.createElement("div");
    stamp_div.className = "timestamp";
    stamp_div.appendChild(document.createTextNode(stamp));

    var message = document.createElement("div");
    message.className = "message";
    message.appendChild(sender_div);
    message.appendChild(stamp_div);
    message.appendChild(document.createTextNode(content));
    target.appendChild(message);

    if (magnet_scroll) {
        scroll_height = Math.max(target.scrollHeight, target.clientHeight);
        target.scrollTop = scroll_height - target.clientHeight;
    }
};