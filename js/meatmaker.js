function meatMaker (o)
{
	o.meat = "MEAT!";
}

var loser = {};
console.log("before - " + loser.meat);
meatMaker(loser);
console.log("after - " + loser.meat);

