/*
{
               	const props = Object.assign({}, state, eventHandlers);
               	return props;       	
               }
      };

*/


const e = React.createElement;
const r = ReactDOM.render;
const id = function (id) { return document.getElementById(id); };


function createBlankEntry ()
{
	const blankEntry = {text: '', title: ''};

	return blankEntry;
}


function div (el, id, props=null)
{
	props = Object.assign({}, props, {id: id});
	const div = React.createElement('div', props, el);

	return div;
}

class Entry extends React.Component
{
	constructor ()
	{
		super();
	}


	render ()
	{
		const elTitle = e('span', {className: 'entryTitle'}, this.props.title);
		const elText =  e('span', {className: 'entryText'},  this.props.text);
		const elDiv =   e('div',  {className: 'entry'}, elTitle, elText);
		
		return elDiv;
	}
}
Entry.propTypes = 
{
	text: PropTypes.string.isRequired,
	title: PropTypes.string.isRequired
};


class AddEntryForm extends React.Component
{
	constructor ()
	{
		super();
	}

	onSubmit (ev)
	{
		ev.preventDefault();
		console.log('onSubmit()');
		this.props.onSubmit();
		this.refs.title.focus();
	}


	onTextChange (ev)
	{
		console.log('onTextChange()');
		const onChange = this.props.onChange;
		const updatedValue = Object.assign({}, this.props.value, {text: ev.target.value});
		onChange(updatedValue);
	}

	onTitleChange (ev)
	{
		console.log('onTitleChange()');
		const onChange = this.props.onChange;
		const updatedValue = Object.assign({}, this.props.value, {title: ev.target.value});
		onChange(updatedValue);
	}

	render ()
	{
		var oldEntry = this.props.newEntry;

		const elTitle =  e('input',  {type: 'text', ref: 'title', placeholder: '(Title)', value: this.props.value.title, onChange: this.onTitleChange.bind(this)});
		const elText =   e('input',  {type: 'text', ref: 'text',  placeholder: '(Text)',  value: this.props.value.text,  onChange: this.onTextChange.bind(this)});
		const elSubmit = e('button', {type: 'submit'}, '+');
		const elForm =   e('form', {onSubmit: this.onSubmit.bind(this)}, elTitle, elText, elSubmit);

		return elForm;
	}
}
AddEntryForm.propTypes =
{
	value: PropTypes.object.isRequired,
	onChange: PropTypes.func.isRequired,
	onSubmit: PropTypes.func.isRequired
};


class Page extends React.Component
{
	constructor ()
	{
		super();
	}

	render ()
	{
		var newEntry = {text: '', title: ''};

		const entries = this.props.entries.map(function (entry) { return e(Entry, entry); });
		const elForm = e(AddEntryForm, {value: this.props.newEntry, onChange: this.props.onUpdateEntry, onSubmit: this.props.onSubmitNewEntry});
		const elFormDiv = div(elForm);
		const elMain = e('div', null, entries, elFormDiv);

		return elMain;
	}
}
Page.propTypes =
{
	entries:  PropTypes.array.isRequired,
	newEntry: PropTypes.object.isRequired,
	onUpdateEntry: PropTypes.func.isRequired,
	onSubmitNewEntry: PropTypes.func.isRequired
};	


function updateEntry (newEntry)
{
	updateState({newEntry: newEntry});
	console.log('Updating Entry: ' + newEntry.title + ', ' + newEntry.text);
}


function submitNewEntry ()
{
	$.addEntry();
	updateState();
}


var $ = 
     {
     	state : {},
		eventHandlers:
      {
    		onUpdateEntry: updateEntry,
	    	onSubmitNewEntry: submitNewEntry
      },
      addEntry: function ()
                {
                	const newKey = this.state.entries.length + 1;
                	const newEntry = this.state.newEntry;
                	newEntry['key'] = newKey;
	               console.log(' Entry: ' + newEntry.key + ', ' + newEntry.title + ', ' + newEntry.text);
	               this.state.entries.push(newEntry);
	               this.state.newEntry = createBlankEntry();
                },
      toProps: function ()
               {
               	const props = Object.assign({}, this.state, this.eventHandlers);
               	return props;       	
               }
      };

function updateState (changes = {})
{
	$.state = Object.assign({}, $.state, changes);
	updateApp();
}

function updateApp ()
{
	const props = $.toProps();
	const el = e(Page, props);
	const main = id('main');
	r(el, main);
}


function initState ()
{
	const entries = [
	                	{ key: 1, title: 'Thing!!!', text: 'A sample entry. It does not mean anything at this time.' },
                   	{ key: 2, title: 'Second Entry', text: 'Another sample entry. To help establish proper layout.' }
                   ];
	const newEntry = { text: 'Base', title: '3rd'};
	const newState = { entries, newEntry };

	updateState(newState);
}

initState();
console.log('Done');
