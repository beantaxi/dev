const el = React.createElement;
const render = ReactDOM.render;
const id = function (id) { return document.getElementById(id); };

const elMain = id('main');

function Center (props)
{
	const style = {textAlign: 'center'};
	return el('div', {style: style}, props.children);
}


const elText = el('h1', {}, 'Cream Puffs and Kimchi!!!');
const elCenter = el(Center, {}, elText);
render(elCenter, elMain);


/*
function XKCDComic (props)
{
	console.log(props);
	const elImg = el('img', {src: `https://imgs.xkcd.com/comics/${props.path}.png`, title: props.altText});
	const elComic = el('a', {href: `https://xkcd.com/${props.number}/`}, elImg);

	return elComic;
}

const elMain = id('main');

const elXkcd = el(XKCDComic, {path: 'compiling', number: 303, altText: "'Are you stealing those LCDs?' 'Yeah, but I'm doing it while my code compiles'"});
render(elXkcd, elMain);
*/
