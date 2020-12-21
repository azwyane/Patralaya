

  const inputs = document.querySelectorAll("input");


function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
  let nextSibiling=parent.nextElementSibling;
  if(nextSibiling) nextSibiling.style.display="block";
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");

	}
   let nextSibiling=parent.nextElementSibling;
  if(nextSibiling) nextSibiling.style.display="none";
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("input", addcl);
	input.addEventListener("blur", remcl);
});

