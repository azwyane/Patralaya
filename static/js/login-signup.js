

  const inputs = document.querySelectorAll("input");


function addcl(objs){
	let parent = objs.parentNode.parentNode;
	parent.classList.add("focus");
  let nextSibiling=parent.nextElementSibling;
  if(nextSibiling) nextSibiling.style.display="block";
}

function remcl(objs){
	let parent = objs.parentNode.parentNode;
	if(objs.value == ""){
		parent.classList.remove("focus");

	}
   let nextSibiling=parent.nextElementSibling;
  if(nextSibiling) nextSibiling.style.display="none";
}

	inputs.forEach(input=>{
  if (["text","password","email"].includes(input.type) && input.value!=="") addcl(input)
})


inputs.forEach(input => {
	input.addEventListener("focus", addcl.bind(null,input));
	input.addEventListener("input", addcl.bind(null,input));

	input.addEventListener("blur", remcl.bind(null,input));
});

