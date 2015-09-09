function extendWith (dest, source)
{
	for (var prop in source)
	{
		if (source.hasOwnProperty(prop))
		{
			dest[prop] = source[prop];
		}
	}
}

Object.prototype.extendWith =
	function (src)
	{
		for (var prop in src)
		{
			if (src.hasOwnProperty(prop))
			{
				this[prop] = src[prop];
			}
		}

		return this;
	};

function isClass (s)
{
	return s[0] == '.';
}

function isId (s)
{
	return s[0] == '#';
}


String.prototype.isClass = function () { return isClass(this); };
String.prototype.isId = function () { return isId(this); };


function append (child)
{
	if (typeof(child) == 'string')
	{
		this.appendChild(document.createTextNode(child));
	}
	else
	{
		this.appendChild(child);
	}

	return this;
}


function css (key, value)
{
	this.style[key] = value;

	return this;
}


function hide ()
{
	this.style.visibility = 'hidden';

	return this;

}

function show ()
{
	this.style.visibility = 'visible';

	return this;
}


var proto = { 
              append: append,
              css: css,
              hide: hide,
              show: show
            };
              


function O (arg)
{
	this.arg = arg;
	this.append = append;
	this.css = css;
	this.hide = hide;
	this.show = show;

	return this;
}


function $ (arg)
{
	if (typeof(arg) == 'string')
	{
		if (arg.isId())
		{
			var id = arg.substring(1);
			var el = document.getElementById(id);
			el.extendWith(proto);
			return el;
		}
		else if (arg.isClass())
		{
			var cls = arg.substring(1);
			var els = document.getElementsByClassName(cls)
			els.append = function (arg) { for (var i=0; i<this.length; ++i) { var el = $(els[i]); el.append(arg); } return els; };
			els.css = function (prop, value) { for (var i=0; i<this.length; ++i) { var el = $(els[i]); el.css(prop, value); } return els; };
			els.hide = function (prop, value) { for (var i=0; i<this.length; ++i) { var el = $(els[i]); el.hide(prop, value); } return els; };
			els.show = function (prop, value) { for (var i=0; i<this.length; ++i) { var el = $(els[i]); el.show(prop, value); } return els; };
			return els;
		}
		else
		{
			var els = document.getElementsByTagName(arg);
			return els;
		}
	}
	else if (typeof(arg) == 'object')
	{
		arg.extendWith(proto);	
		return arg;
	}
	else if (typeof(arg) == 'function')
	{
		$.onLoad(arg);
	}
	else
	{
		alert("wtf??? " + arg);
	}
}

$.onLoad =
	function f (fn)
	{
		onload = fn;
	};
