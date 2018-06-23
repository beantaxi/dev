// Create a new go file
// Read the just like in the other thing
// Use decoder, see what happens
// - It should output objects
// Try and read specific objects

import "
	application/json
	io/ioutil
	os
"

type Thing struct {
	Id, Name string
}



func openDecoder () Decoder {
	const json_path := "sample.json"
	f = os.Open()
	var decoder *Decoder = NewDecoder(f)
	return decoder 
}


func main () {
	decoder := openDecoder()
}
