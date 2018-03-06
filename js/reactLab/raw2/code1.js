const sumOf = (n, fn) =>
  Array.from(Array(n).keys())
     .reduce((a, n) => a + fn(n), 0)

function getBoxStyle(n) {
  const baseSize = 100
  const baseAngle = 50 * Math.PI/180
  const ratio = Math.sqrt(Math.tan(baseAngle)**2 + 1)/2

  return {
    position: 'absolute',
    width: baseSize*ratio**n,
    height: baseSize*ratio**n,
    left: '60%',
    top: sumOf(n, i =>
      baseSize*ratio**i*Math.cos(i*baseAngle)
    ),
    marginLeft: sumOf(n, i =>
      -baseSize*ratio**i*Math.sin(i*baseAngle)
    ),
    fontFamily: 'sans-serif',
    transform: `rotate(${n*baseAngle}rad)`,
    transformOrigin: 'top left',
    backgroundColor: '#61dafb',
    textAlign: 'center',
    lineHeight: baseSize*ratio**n+'px',
    fontSize: '18px'
  }
}

function getSquareContent (i)
{
	var content;

	if (i%15 == 0)
	{
		content = el('strong', {}, 'FizzBuzz');
	}
	else if (i%3 == 0)
	{
		content = el('strong', {}, 'Fizz');
	}
	else if (i%5 == 0)
	{
		content = el('strong', {}, 'Buzz');
	}
	else
	{
		content = ''+i;
	}

	return content;
}


const el = React.createElement;
const render = ReactDOM.render;
const id  = function (id) { return document.getElementById(id); };

const main = id('main');
console.log('main=' + main);

var boxes = [];
for (i=0; i<15; ++i)
{
	const box = el('div', { style: getBoxStyle(i), key: i }, getSquareContent(i+1));
	boxes.push(box);
}
const divBoxes = el('div', {}, boxes);
render(divBoxes, main);

/*
const square = el('div', {className: 'square'});
const squareHolder = el('div', {className: 'squareHolder'}, square, square);
render(squareHolder, main);
*/

/*
const elImg = el('img', {src: 'https://imgs.xkcd.com/comics/random_number.png'});
const elLink = el('a', {href: 'https://xkcd.com/221/'}, elImg);
render(elLink, main);
*/


console.log('Done.');
