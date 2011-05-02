<%inherit file="base.html"/>

<%def name="body()">
<div class="yui3-g dk-main">
    <div class="yui3-u-1-5" >
<!--
	<div id="side" class="yui3-menu" role="menu">
	    <div class="yui3-menu-content">
		<ul class="first-of-type">
		    <li class="yui3-menuitem"><a class="yui3-menuitem-content">${_("System")}</a></li>
		    <li class="yui3-menuitem"><a class="yui3-menuitem-content">${_("User")}</a></li>
		    <li class="yui3-menuitem"><a class="yui3-menuitem-content">${_("Key")}</a></li>
		</ul>
	   </div>
	</div>
-->
    </div>

    <div class="yui3-u-4-5">
	<div  id="content">
	    <ul>
		<li><a href="#tab_login" class="tablabel"> ${_('Login')} </a></li>
		<li><a href="#tab_register" class="tablabel"> ${_('Register')} </a></li>
	    </ul>

	    <div>
		<div class="dk-tab" id="tab_login">
		    <form id="loginform" method="post">
			<br>
			<div>
			    <label for="username">${_("Username/Email")} : &nbsp;</label>
			    <input id="username" name="username" type="text"/>
			</div>
			<div>
			    <label for="passwd">${_("Password")} : &nbsp;</label>
			    <input id="passwd" name="passwd" type="password"/>
			</div>
			<div class="submit">
			    <label for="submit">&nbsp;</label>
			    <button type="button" id="submit_login">${_("Submit")}</button>
			</div>
			<br>
		    </form>
		</div>

		<div class="dk-tab" id="tab_register">
		    <form id="registerform" method="post">
			<br>
			<div>
			    <label for="username">${_("Username")} : &nbsp;</label>
			    <input id="username" name="username" type="text"/>
			</div>
			<div>
			    <label for="passwd">${_("Password")} : &nbsp;</label>
			    <input id="passwd" name="passwd" type="password"/>
			</div>
			<div>
			    <label for="passwd2">${_("Repeat Password")} : &nbsp;</label>
			    <input id="passwd2" name="passwd" type="password"/>
			</div>
			<div>
			    <label for="email">${_("Email")} : &nbsp;</label>
			    <input id="email" name="email" type="text"/>
			</div>
			<div>
			    <label for="phone_mobile">${_("Mobile Phone")} : &nbsp;</label>
			    <input id="phone_mobile" name="phone_mobile" type="text"/>
			</div>
			<div>
			    <label for="phone_office">${_("Office Phone")} : &nbsp;</label>
			    <input id="phone_office" name="phone_office" type="text"/>
			</div>
			<div>
			    <label for="phone_home">${_("Home Phone")} : &nbsp;</label>
			    <input id="phone_home" name="phone_home" type="text"/>
			</div>
			<div>
			    <label for="org">${_("Organization")} : &nbsp;</label>
			    <input id="org" name="org" type="text"/>
			</div>
			<div>
			    <label for="title">${_("Title")} : &nbsp;</label>
			    <input id="title" name="title" type="text"/>
			</div>
			<div>
			    <label for="addr">${_("Address")} : &nbsp;</label>
			    <input id="addr" name="addr" type="text"/>
			</div>

			<div class="submit">
			    <label for="submit">&nbsp;</label>
			    <button type="button" id="submit_register">${_("Submit")}</button>
			</div>
			<br>
		    </form>
		</div>

	    </div>
        </div>
    </div>
</div>

<script src="${request.application_url}/static/yui3/yui/yui-min.js"> </script>
<script type="text/javascript">
YUI({ filter: 'raw' }).use(
	"yui", "node", "node-menunav", "tabview",
	"io-form", "json-parse",
	function(Y) {
    //left menu
//    var menu = Y.one("#side");
//    menu.plug(Y.Plugin.NodeMenuNav);
//    menu.get("ownerDocument").get("documentElement").removeClass("yui3-loading");

    //right tab panel
    var tabview = new Y.TabView({srcNode:'#content'});
    tabview.render();

    //login
    Y.one("#submit_login").on("click", function(e) {
	var onSuccess = function(id, response, args) {
	    data = Y.JSON.parse(response.responseText);
	    if(data.status == "failed") {
		alert("failed");
	    } else {
		Y.config.win.location = "${url.route('main', action='index')}";
	    }
	};

	var onFailure = function(id, response, args) {
	    alert("${_('Login failed!')}");
	};

	var cfg = {
	    method: "POST",
	    form: {
		id: "loginform",
	    },
	}

	Y.io("${url.route('auth', action='login')}", cfg);
	Y.on('io:success', onSuccess);
	Y.on('io:failure', onFailure);
    });

    //register
    Y.one("#submit_register").on("click", function(e) {
	var onSuccess = function(id, response, args) {
	    data = Y.JSON.parse(response.responseText);
	    if(data.status == "FAILURE") {
		alert("${_('Register Failed!')}");
	    } else {
		//switch to login tab
		tabview.selectChild(0);
	    }
	};

	var onFailure = function(id, response, args) {
	    alert("${_('Register failed!')}");
	};

	var cfg = {
	    method: "POST",
	    form: {
		id: "registerform",
	    },
	};

	Y.io("${url.route('auth', action='register')}", cfg);
	Y.on('io:success', onSuccess);
	Y.on('io:failure', onFailure);
    });


});
</script>

</%def>


