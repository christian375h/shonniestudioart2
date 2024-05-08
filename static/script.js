function toggleMenu(){
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");

    menu.classList.toggle("open");
    icon.classList.toggle("open");
}

function openLink(tabName){
    var projectLinks = document.getElementsByClassName("selected-links");
    var projectTabs = document.getElementsByClassName("selected-tabs");

    for(projectLink of projectLinks){
        projectLink.classList.remove("active-selected-link");
    }
    for(projectTab of projectTabs){
        projectTab.classList.remove("active-selected-tab");
    }
    event.currentTarget.classList.add("active-selected-link");
    document.getElementById(tabName).classList.add("active-selected-tab");
}
