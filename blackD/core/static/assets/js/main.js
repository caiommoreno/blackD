function setActive() {
	var activePage = window.location.href.split("/", 20)[3];	
	var btn = document.getElementById(activePage);
	btn.className += ' active'; 
};

