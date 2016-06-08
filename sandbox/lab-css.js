$.fn.fillWithKitties = 
	function (x, y, n)
	{
		fillWithKitties(this, x, y, n);
	};

$.fn.setThumbnails =
	function (dt, start)
	{		
		this.css('visibility', 'hidden');

		var mmt = new moment(dt, "MMM DD");
		var sDate = mmt.format('YYYYMMDD');
		var urlStem = location.protocol + "//" + location.host + "/euclid/png/" + sDate;
		console.log(urlStem);
		ng.set(start);
		var imgs = $('img', this);
		for (var i=0; i<144; ++i)
		{
			var n = ng.next();
			var sTime = (10000 + n + "").slice(-4);
			var filename = sDate + "-" + sTime + ".png";
			var url = urlStem + "/" + filename;
			console.log(url);
			$(imgs[i]).attr('src', url);
		}
		
		
		this.css('visibility', 'visible');
	};

$(onLoad);

var NumberGenerator = function NumberGenerator (fn) { this.nextValue = fn; this.set(0); };
NumberGenerator.prototype.reset = function () { this.set(0); return this; };
NumberGenerator.prototype.set = function (newValue) { this.n = newValue; return this; };
NumberGenerator.prototype.next =
	function ()
	{
		var rv = this.n;
		this.set(this.nextValue(this.n));
		return rv;
	}

function nextValue  (n) 
{
	var rv = n+5;
	if (rv%100 % 60 == 0)
	{
		rv = rv - 60 + 100;
	}

	return rv;
}

var ng = new NumberGenerator(nextValue);

function onLoad ()
{
	$('#left').fillWithKitties(12, 12, 0);
	$('#right').fillWithKitties(12, 12, 1200);
/*
sizeMainImage(25);
	
	$('img', '#thumbnails').click(onThumbnailClick);

	setDate('Jul 06');
*/

	$('#datetimepicker').datetimepicker(
	{
		dateFormat: 'mm/dd/yy hh:MM',
		onChangeDateTime: onChangeDateTime,
		step: 5,
		theme: 'dark'
	});
}


function fillWithKitties (sel, x, y, n)
{
	sel.empty();

	var url = 'http://lorempixel.com/100/100/cats';
	var width = 100.0 / x;
	ng.set(n);
	for (var i=0; i<x; ++i)
	{
		for (var j=0; j<y; ++j)
		{
			var img = $(document.createElement('img'));
			img.attr('src', url);
			img.attr('alt', (10000 + ng.next() + "").slice(-4));
			sel.append(img);
		}
	}
	$('img', sel).css('width', width + '%');
}


function highlight (n)
{
	var alt = n;
	if ($.isNumeric(alt))
	{
		var alt = (10000 + alt + "").slice(-4);
	}
	
	$('img', '#thumbnails').css('border-color', 'transparent');
	var img = $("img[alt='" + alt + "']", '#thumbnails');
	img.css('border-color', 'blue');
	return img;	
}


function onThumbnailClick ()
{
	var alt = $(this).attr('alt');
	console.log(alt);
	highlight(alt);

	var src = $(this).attr('src');
	$('#bigImage').attr('src', src);
}


function onChangeDateTime (dateTime, src)
{
	dateTimeHasChanged();
}

function dateTimeHasChanged (dateTime)
{
}

function setDate (dt)
{
	var mmt = new moment(dt, "MMM DD");
	var sDate = mmt.format('YYYYMMDD');
	var urlStem = location.protocol + "//" + location.host + "/euclid/png/" + sDate;
	console.log(urlStem);

	$('#left').setThumbnails(dt, 0);
	$('#right').setThumbnails(dt, 1200);

/*
	ng.reset();
	for (var i=0; i<288; ++i)
	{
		var n = ng.next();
		var sTime = (10000 + n + "").slice(-4);
		var filename = sDate + "-" + sTime + ".png";
		var url = urlStem + "/" + filename;
		console.log(url);
	}
*/
}


function setupHeatMaps (el)
{
	el.empty();
	setupMainImage(el);
	setupThumbnails(el);
//	$('#left').fillWithKitties(12, 12, 0);
//	$('#right').fillWithKitties(12, 12, 1200);
	$('img', '#thumbnails').click(onThumbnailClick);
	setDate('Jul 06');
}


function setupMainImage (el)
{
	var container = $(document.createElement('div'));
	container.attr('id', 'main').attr('class', 'section');

	var child = $(document.createElement('div'));
	child.attr('id', 'child');

	var img = $(document.createElement('img'));
	img.attr('id', 'bigImage').addClass('fullChild').attr('src', 'ercotContourMap-20150601-234501.png');

	child.append(img);
	container.append(child);
	el.append(container);
}


function setupThumbnails (el)
{
	var container = $(document.createElement('div')).attr('id', 'thumbnails').addClass('section');
	var left = $(document.createElement('div')).attr('id', 'left').addClass('default').addClass('thumbnailSection');
	var right = $(document.createElement('div')).attr('id', 'right').addClass('default').addClass('thumbnailSection');

	for (var i=0; i<144; ++i)
	{
		var img = $(document.createElement('img'));
		left.append(img);
	}

	for (var i=0; i<144; ++i)
	{
		var img = $(document.createElement('img'));
		right.append(img);
	}

	container.append(left).append(right);
	el.append(container);
}


function sizeMainImage (n)
{
	var mainWidth = n;
	var mainBottomPadding = n;
	var rightWidth = 100 - n;
	$('#main').css('width', mainWidth + '%');
	$('#main').css('padding-bottom', mainWidth + '%');
	$('#thumbnails').css('width', rightWidth + '%');
}
