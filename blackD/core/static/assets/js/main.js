function toTitleCase(string){
	return string.charAt(0).toUpperCase() + string.slice(1);
}
function setActive() {
	var pageName = window.location.href;
	var activePage = window.location.href;
	activePage=activePage.split("/", 20);
	activePage=activePage[activePage.length -2];	
	var btn = document.getElementById(activePage);
	btn.className += ' active'; 

 	console.log(pageName)
};

