function toggleMenu(){
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");

    menu.classList.toggle("open");
    icon.classList.toggle("open");
}

function openLink(tabName){
    var projectLinks = document.getElementsByClassName("class-links");
    var projectTabs = document.getElementsByClassName("class-tabs");

    for(projectLink of projectLinks){
        projectLink.classList.remove("active-class-link");
    }
    for(projectTab of projectTabs){
        projectTab.classList.remove("active-class-tab");
    }
    event.currentTarget.classList.add("active-class-link");
    document.getElementById(tabName).classList.add("active-class-tab");
}