/**
* This function is called to toggle a div and arrow image.
*/
function showHideDiv(divId,img){
	basePath=document.forms[0].basePath.value;
	div=document.getElementById(divId)
	img=document.getElementById(img)
	if (div.style.display=="block") {
		div.style.display="none";
		img.src= "/misapp/images/ico_arrow_collapse.gif";
	} else {
		div.style.display="block";
		img.src= "/misapp/images/ico_arrow_expand.gif";
	}
}

/**
* This function is called to toggle a div.
*/
function toggleDiv(divId){
	div=document.getElementById(divId)
	if (div.style.display=="block") {
		div.style.display="none";
	} else {
		div.style.display="block";
	}
}

/**
* This function is called open the specific report
* in a new window from Reports and Extracts Index.
*/
function showPortletTypeA(name, url) {
	window.open(url, name, "toolbar=no,resizable=yes,width=845,height=500,scrollbars=yes");
}