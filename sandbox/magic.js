var NumberGenerator = function NumberGenerator (fn) { this.nextValue = fn; this.n = 0; };
NumberGenerator.prototype.reset = function () { this.set(0); return this; };
NumberGenerator.prototype.set = function (newValue) { this.n = newValue; return this; };
NumberGenerator.prototype.next =
	function ()
	{
		var rv = this.n;
		this.set(this.nextValue(this.n));
		return rv;
	};

function nextValue (n)
{
	var rv = n+5;
   if (rv%100 % 60 == 0)
   {
   	rv = rv - 60 + 100;
   }

   return rv;
}

var ng = new NumberGenerator(nextValue);

$.fn.addDateTimePickerSection = function () { addDateTimePickerSection(this); };

$.fn.addThumbnails =
	function ()
	{
		var el = $(this);

		addThumbnailsHeader(el);
		addAmThumbnails(el);
		addPmThumbnails(el);
	}
	
$.fn.fillThumbnailPanel = function (n) { fillThumbnailPanel(this, n); }	

$.fn.initMap =
	function ()
	{
		console.log("Initializing map ...");
		var mapProp = {
			center: new google.maps.LatLng(31.0, -99.75),
	   	zoom: 6,
	   	mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		$.euclid.map = new google.maps.Map(this[0], mapProp);
		$.euclid.kmlProp = { map: $.euclid.map };
	}



function addThumbnailsHeader (el)
{
	el.append($.parseHTML(HTML.thumbnailsHeader));
}


function addAmThumbnails (el)
{
	var am = createDiv('am', 'default thumbnailSection');
	el.append(am);

	return el;
}

function addPmThumbnails (el)
{
	var pm = createDiv('pm', 'default thumbnailSection');
	el.append(pm);

	return el;
}

function addDateTimePickerSection (elParent)
{
	var dtpc = createDateTimePickerContainer();

	elParent.append(dtpc);
}


function createDateTimePickerContainer ()
{
	var dtpc = $.parseHTML(HTML.dateTimePickerContainer);
	var dtpArgs = { 'theme': 'dark', 'step': 5 };
	$('datetimepicker', dtpc).datetimepicker(dtpArgs);

	return dtpc;
}


function createDiv (id, classes)
{
	var div = $(document.createElement('div')).attr('id', id).addClass(classes);

	return div;
}

function addAviPanel (elParent)
{
	var html = HTML.aviPanel;
	var aviPanel = $.parseHTML(html);
	elParent.append(aviPanel);
}


function addImagePanel (elParent)
{
	var html = HTML.imagePanel;
	var imagePanel = $.parseHTML(html);
	elParent.append(imagePanel);
}


function addMapPanel (elParent)
{
	var html = HTML.mapPanel;
	var mapPanel = $.parseHTML(html);
	elParent.append(mapPanel);
}


function createImage (src) 
{
	return $(document.createElement('img')).attr('src', src);
}


function createTwoSections (borderColor1, borderColor2, leftWidth)
{
	var left = createSection('left', leftWidth, borderColor1);
	var right = createSection('right', 1.0-leftWidth, borderColor2);

	$('body').empty().append(left).append(right);
}


function createSection (id, width, borderColor)
{
	var section = $(document.createElement('div'));
	var width = 100*width + '%';
	section.attr('id', id).addClass('section').css('width', width).css('border-color', borderColor);

	return section;
}


function fillThumbnailPanel (el, n)
{
	var urlStub = location.protocol + "//" + location.host + "/euclid/png/20150706/20150706-";
	ng.set(n);
	for (var i=0; i<144; ++i)
	{
		var alt = (10000 + ng.next() + "").slice(-4);
		var url = urlStub + alt + ".png";
		var img = createImage(url).attr('alt', alt);
		el.append(img);
	}

	return el;
}


function onModeButton ()
{
	var id = $(this).attr('id');
	var btn = $('#' + id, '#modeButtons');
	btn.parent().addClass('selected');
	btn.parent().siblings().removeClass('selected');
	
	var sel = "#pnl-" + id;
	$('.panel', '#left').hide();
	$(sel).show();
}


var HTML = {};
HTML.dateTimePickerContainer = 
"<div id='dtPickerContainer' class='header'>" +
"	<div>" +
"		<span>Date <input id='datetimepicker'/></span>" +
"	   <span id='modeButtons'>" +
"			<label class='modeButton'><input type='radio' name='grp' id='map'/>map</label>" +
"   		<label class='modeButton'><input type='radio' name='grp' id='png'/>png</label>" +
"      	<label class='modeButton'><input type='radio' name='grp' id='avi'/>avi</label>" +
"		</span>" +
"   </div>" +
"</div>";

HTML.aviPanel =
"	<div class='panel' id='pnl-avi'>" +
"	 	<div>(Under Construction) ...</div>" +
"	</div>";

HTML.imagePanel =
"	<div class='panel' id='pnl-png'>" +
"	 	<img id='bigImage' class='fullChild' src='ercotContourMap-20150601-234501.png'/> " +
"	</div>";

HTML.mapPanel =
"	<div class='panel' id='pnl-map'>" +
"		<div id='googleMap'>Map!</div>" +
"	</div>";

HTML.thumbnailsHeader =
"	<div id='thumbnailHeadings' class='header'>" +
"		<div><span id='headingsAm'>am</span><span id='headingsPm'>pm</span></div>" +
"	</div>";

