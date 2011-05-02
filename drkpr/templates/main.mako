<%!
    import drkpr.models as model
%>

<%inherit file="base.html"/>

<%def name="display_system_setting()">
<div class="dk-tab" id="tab_system_setting">
</div>
</%def>

<%def name="display_user_profile()">
<div class="dk-tab" id="tab_profile">
</div>
</%def>

<%def name="display_user_management()">
<div class="dk-tab" id="tab_um">
    <div class="paginatorA"></div>
    <div id="user_table"> </div>
    <div class="paginatorA"></div>
</div>
</%def>

<%def name="display_key_management()">
<div class="dk-tab" id="tab_km">
</div>
</%def>

<%def name="generate_content_tabs()">
<div  class="yui3-loading" id="content">
    <ul>
	<li><a href="#tab_km" class="tablabel" tabkey="5"> ${_('Key Management')} </a></li>
	<li><a href="#tab_um" class="tablabel" tabkey="1"> ${_('User Management')} </a></li>
	<li><a href="#tab_system_setting" class="tablabel" tabkey="2"> ${_('System Setting')} </a></li>
	<li><a href="#tab_profile" class="tablabel" tabkey="6"> ${_('User Profile')} </a></li>
    </ul>

    <div>
	${self.display_key_management()}
	${self.display_user_management()}
	${self.display_system_setting()}
	${self.display_user_profile()}
    </div>
</div>


</%def>

##-----------------------------------------------------------------------------
<%def name="body()">
<div class="yui3-g dk-main">
    <div class="yui3-u-1-5" >
	<div id="side" class="yui3-menu" role="menu">
	    <div class="yui3-menu-content">
		<ul class="first-of-type">
%if session.get("user") and ":%s:" % model.ROLE_SYSADMIN in ":%s:" % session.get("user").roles:
		    <li class="yui3-menuitem"><a class="yui3-menuitem-content" tabkey="1">${_("User Management")}</a></li>
		    <li class="yui3-menuitem"><a class="yui3-menuitem-content" tabkey="2">${_("System Management")}</a></li>
%endif
		    <li class="yui3-menuitem"><a class="yui3-menuitem-content" tabkey="3">${_("Online Utilities")}</a></li>
		    <li class="yui3-menuitem"><a class="yui3-menuitem-content" tabkey="4">${_("Account Activity")}</a></li>
		    <li class="yui3-menuitem"><a class="yui3-menuitem-content" tabkey="5">${_("Security Creditials")}</a></li>
		    <li class="yui3-menuitem"><a class="yui3-menuitem-content" tabkey="6">${_("Personal Information")}</a></li>
		</ul>
	   </div>
	</div>
    </div>

    <div class="yui3-u-4-5">
    ${self.generate_content_tabs()}
    </div>
</div>

<script src="/yui3/yui/yui-min.js"> </script>
<script type="text/javascript">
YUI({
    filter: 'RAW',
    base: "../yui3/",
    combine: 0,
    groups: {
        gallery: {
	    base:'../yui3-gallery/',
	    patterns:  { 'gallery-': {} },
	},
    }
}).use("node-menunav", "dump",
	"yui", "tabview",
	"io-form", "json-parse",
	"datatable", "dataschema-array",
	"datasource-io", "datasource-jsonschema", "datatable-datasource",
	"gallery-aui-paginator",
	function(Y) {
//---------------------------------------------------------------------
    tabs = {}; tabs_hidden = [];

//left menu
    var menu = Y.one("#side");
    menu.plug(Y.Plugin.NodeMenuNav);
    menu.get("ownerDocument").get("documentElement").removeClass("yui3-loading");

    Y.all(".yui3-menuitem-content").on("click", function(e) {
	tabkey = e.target.getAttribute("tabkey");
	tab = tabs[tabkey];
	tab.get("contentBox").removeClass("yui3-tab-hidden");
	tab.get("boundingBox").removeClass("yui3-tab-hidden");
	tab.set("selected", 1);
	//remove tab from tabs_hidden
	var idx = tabs_hidden.indexOf(tabkey);
	if(idx != -1) {
	    tabs_hidden.splice(idx, 1);
	};
    });

//---------------------------------------------------------------------
    //right tab panel

    var Removeable = function(config) {
	Removeable.superclass.constructor.apply(this, arguments);
    };

    Removeable.NAME = 'removeableTabs';
    Removeable.NS = 'removeable';

    Y.extend(Removeable, Y.Plugin.Base, {
	REMOVE_TEMPLATE: '<a class="yui3-tab-remove" title="remove tab">x</a>',

	initializer: function(config) {
	    var tabview = this.get('host');
	    var	cb = tabview.get('contentBox');

	    cb.addClass('yui3-tabview-removeable');
	    cb.delegate('click', this.onRemoveClick, '.yui3-tab-remove', this);

	    // Tab events bubble to TabView
	    tabview.after('tab:render', this.afterTabRender, this);
	},

	onRemoveClick: function(e) {
	    e.stopPropagation();
	    var tab = Y.Widget.getByNode(e.target);
	    if (tab &&
		    //not last visible tab
		    (tabs_hidden.length != Object.keys(tabs).length - 1)) {
		tab.get("contentBox").addClass("yui3-tab-hidden");
		tab.get("boundingBox").addClass("yui3-tab-hidden");
		var tabkey = tab.get("boundingBox").one("a").getAttribute("tabkey");
		tabs_hidden.push(tabkey);
		//if the target is the selected one, the focus on the first visible.
		if (tab.get("selected")) {
		    for(var key in tabs) {
			if (tabs_hidden.indexOf(key) == -1) {
			    tabs[key].set("selected", 1);
			    break;
			}
		    }
		}
	    };
	},

	afterTabRender: function(e) {
	    // boundingBox is the Tab's LI
	    e.target.get('boundingBox').append(this.REMOVE_TEMPLATE);
	},

    });

    var tabview = new Y.TabView({
	srcNode:'#content',
	plugins: [Removeable],
    });

    tabview.render();
    Y.one("#content").removeClass("yui3-loading");

    // establish connection between menu & tab
    tabview.each(function(tab) {
	tabkey = tab.get("boundingBox").one("a").getAttribute("tabkey");
	tabs[tabkey] = tab;
    });

//---------------------------------------------------------------------
    //tabview.item(2).set("selected", 1);
    //tab_system_setting
    tabview.selectChild(2);

    //operation table
    var system_setting_columns = [
	{ key: "desc", label: "description" },
	{ key: "oper", label: "operation" },
	{ key: "note", label: "note"},
    ];
    var system_setting_data = [
	{ desc: "${_('Generate system master key')}",
	  oper: "<button class='operation' action='gen_master_key'> Act </button>",
	  note: ""
	},
	{ desc: "${_('Start/Stop Key generation service')}",
	  oper: "<button class='operation' action='toggle_service_key_gen'> Act </button>",
	  note: ""
	},
	{ desc: "${_('Publish system public parameters')}",
	  oper: "<button class='operation' action='publish_sys_params'> Act </button>",
          note: ""
        },
	{ desc: "${_('Publish revokation key list')}",
	  oper: "<button class='operation' action='public_revok_list'> Act </button>",
          note: ""
        },
    ];

    var system_setting_table = new Y.DataTable.Base({
	columnset: system_setting_columns,
	recordset: system_setting_data,
    }).render("#tab_system_setting");

    system_setting_table.get("boundingBox").one("table").setStyle("width", "100%");

    Y.all("#tab_system_setting .operation").on("click", function(e) {
	//alert(e.target.getAttribute("action"));
	var cfg = {
	    method: "POST",
	    data: "action=" + e.target.getAttribute("action"),
	};

	var onSuccess = function(id, response, args) {
	    r = Y.JSON.parse(response.responseText);
	    //alert(response.responseText);
	    if(r.status == "SUCCESS") {
		alert("done!");
	    } else {
		alert(r.message);
	    }
	};

	var onFailure = function(id, response, args) {
	    alert("sorry!");
	};

	Y.io("${url.route('main', action='gen_master_key')}", cfg);
	Y.on('io:success', onSuccess);
	Y.on('io:failure', onFailure);
    });
//---------------------------------------------------------------------
//user management
    var um_cols = [
	{ key: "username", label: "${_('username')}" },
	{ key: "master_email", label: "${_('email')}" },
	{ label: "edit",
	  formatter: function (obj) {
		var data = obj.data;
		return Y.Lang.sub("<button val=\"{username}\" class='btn'>edit</button>", data);
	  },
	},
    ];

    Y.on("click", function(e) {
	node = e.target;
	if (node.test('.btn')) {
	    alert(node.getAttribute("val"));
	}
    });

    var um_data = new Y.DataSource.IO({
	source: "${url.route('um', action='get_users')}"
    });
    um_data.plug(Y.Plugin.DataSourceJSONSchema, {
        schema: {
	    resultListLocator: "data",
            resultFields: ["username", "master_email", "status"]
        }
    });

    var um_table = new Y.DataTable.Base({
        columnset: um_cols,
        summary: "User Management",
        //caption: "Table with JSON data"
    });

    um_table.plug(Y.Plugin.DataTableDataSource, {
        datasource: um_data
    }).render("#user_table");
    tabview.selectChild(1);

    var user_count = 0;
    var paginator = new Y.Paginator({
	containers: '.paginatorA',
	page: 1,
	template: '{FirstPageLink} {PrevPageLink} {PageLinks} {NextPageLink} {LastPageLink} {RowsPerPageSelect}',
	maxPageLinks: 10,
	rowsPerPage: 10,
	circular: false,
	rowsPerPageOptions: [10, 20, 50 ],
	on: {
	    changeRequest: function(event) {
		var instance = this;
		var newState = event.state;
		var page = newState.page;
		var rowsPerPage = newState.rowsPerPage;
		um_table.datasource.load({request: "?offset=" + (page - 1) * rowsPerPage + "&size=" + rowsPerPage});

		instance.setState(newState);
	    }
	}
    });
    Y.io("${url('um', action='get_user_count')}", {
	on: {
	    success: function(id, o, args) {
		r = Y.JSON.parse(o.responseText);
		if(r.status == "SUCCESS") {
		    user_count = r.data;
		    paginator.set("total", user_count);
		    paginator.render();
		} else {
		    alert("get_user_count(): " + r.message);
		}
	    },
	}
    });
});

</script>

</%def>


