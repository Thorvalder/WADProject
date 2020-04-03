//This is for the search box on artists.html/saved-artists.html

const list = document.querySelector('#artist-list ul');



//
const searchBox = document.forms['search_artists'].querySelector('input');

searchBox.addEventListener('keyup',function(tex){
	const term = tex.target.value.toLowerCase();
	
	const artist_blocks = list.getElementsByClassName('artist_block');
	const artists = list.getElementsByClassName('username_js');
	var i = 0;
	Array.from(artists).forEach(function(artist){
		//next line probs isnt firstElementChild
		const username = artist.textContent;
		//next line may create problems with unique usernames
		if(username.toLowerCase().indexOf(term)!=-1){
			artist_blocks[i].style.display = 'block';
			//artist.style.display = 'block';
		} else {
			artist_blocks[i].style.display = 'none';
			//artist.style.display = 'none';
		}
		i = i + 1;
	})
})