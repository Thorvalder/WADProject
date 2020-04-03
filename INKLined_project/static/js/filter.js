
//Filter by tattoo style

const listOfArtists = document.querySelector('#artist-list ul');



//
const filterBox = document.forms['filter_by_style'].querySelector('select');

filterBox.addEventListener('click',function(tex){
	const term = tex.target.value.toLowerCase();
	
	const artist_blocks = listOfArtists.getElementsByClassName('artist_block');
	const artists = listOfArtists.getElementsByClassName('artist_styles');
	var i = 0;
	Array.from(artists).forEach(function(artist){
		//next line probs isnt firstElementChild
		const style = artist.textContent;
		//next line may create problems with unique usernames
		if(term=='none'){
			artist_blocks[i].style.display = 'block';
		}
		else{ 
			if(style.toLowerCase().indexOf(term)!=-1){
				artist_blocks[i].style.display = 'block';
				//artist.style.display = 'block';
			} else {
				artist_blocks[i].style.display = 'none';
				//artist.style.display = 'none';
			}
		}
		i = i + 1;
	})
})