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
		this.arg.appendChild(document.createTextNode(child));
	}
	else
	{
		this.arg.appendChild(child);
	}

	return this;
}


function css (key, value)
{
	this.arg.style[key] = value;

	return this.arg;
}


function hide ()
{
	this.arg.style.visibility = 'none';

	return this.arg;

}

function show ()
{
	this.arg.style.visibility = 'visible';

	return this.arg;
}





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
			var o = new O(el);
			return o;
		}
		else if (arg.isClass())
		{
			var cls = arg.substring(1);
			var els = document.getElementsByClassName(cls)
			var el = els[0];
			var o = new O(el);
			return o;
		}
		else
		{
			var els = document.getElementsByTagName(arg);
			return els;
		}
	}
	else if (typeof(arg) == 'object')
	{
		var o = arg;
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