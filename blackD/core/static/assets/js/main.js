function toTitleCase(string){
	return string.charAt(0).toUpperCase() + string.slice(1);
}
function setActive() {
	
	var activePage = window.location.href;
	activePage=activePage.split("/", 20);
	activePage=activePage[activePage.length -2];
	// activePage =toTitleCase(activePage);
	// if (activePage=="Visaogeral"){
	// 	activePage= "Visão Geral"
	// }
	var btn = document.getElementById(activePage);
	btn.className += ' active'; 

 	
};

