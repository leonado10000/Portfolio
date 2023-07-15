function run(){
    console.log(" ¯\\_(ツ)_/¯ ")
}

function im(n){
    if (n==1){
        document.querySelector(".G").style.opacity = "0";
        document.querySelector(".G").style.transition= "250ms";
        
        if(screen.width>=600){
            document.querySelector(".G").style.maxWidth = "150px";
            document.querySelector(".G2").style.maxHeight = "230px";
        }
        else{
            document.querySelector(".G").style.maxWidth = "100px";
            document.querySelector(".G2").style.maxHeight = "125px";
        }
        document.querySelector(".G2").style.opacity = "1";
        document.querySelector(".G2").style.transition= "400ms";
    }
    if (n==2){
        document.querySelector(".I").style.opacity = "0";
        document.querySelector(".I").style.transition= "230ms";
        if(screen.width>=600){
            document.querySelector(".I").style.maxWidth = "150px";
            document.querySelector(".I2").style.maxHeight = "230px";
        }
        else{
            document.querySelector(".I").style.maxWidth = "100px";
            document.querySelector(".I2").style.maxHeight = "125px";
        }
        document.querySelector(".I2").style.opacity = "1";
        document.querySelector(".I2").style.transition= "400ms";
    }
    if (n==3){
        document.querySelector(".K").style.opacity = "0";
        document.querySelector(".K").style.transition= "230ms";
        if(screen.width>=600){
            document.querySelector(".K").style.maxWidth = "150px";
            document.querySelector(".K2").style.maxHeight = "230px";
        }
        else{
            document.querySelector(".K").style.maxWidth = "100px";
            document.querySelector(".K2").style.maxHeight = "125px";
        }
        document.querySelector(".k2").style.opacity = "1";
        document.querySelector(".K2").style.transition= "400ms";
    }
//     document.querySelectorAll(".img1").forEach((m)=>{
//         m.style.opacity = "1";
//         m.style.transition= "300ms";
//     })
}
function out(n){
    if (n==1){
        document.querySelector(".G").style.opacity = "1";
        document.querySelector(".G").style.transition= "200ms";
        if(screen.width>=600){
            document.querySelector(".G").style.maxWidth = "200px";
            document.querySelector(".G2").style.maxHeight = "200px";
        }
        else{
            document.querySelector(".G").style.maxWidth = "115px";
            document.querySelector(".G2").style.maxHeight = "115px";
        }
        document.querySelector(".G2").style.opacity = "0";
        document.querySelector(".G2").style.transition= "200ms";
    }
    if (n==2){
        document.querySelector(".I").style.opacity = "1";
        document.querySelector(".I").style.transition= "200ms";
        if(screen.width>=600){
            document.querySelector(".I").style.maxWidth = "200px";
            document.querySelector(".I2").style.maxHeight = "200px";
        }
        else{
            document.querySelector(".I").style.maxWidth = "115px";
            document.querySelector(".I2").style.maxHeight = "115px";
        }
        document.querySelector(".I2").style.opacity = "0";
        document.querySelector(".I2").style.transition= "200ms";
    }
    if (n==3){
        document.querySelector(".K").style.opacity = "1";
        document.querySelector(".K").style.transition= "200ms";
        if(screen.width>=600){
            document.querySelector(".K").style.maxWidth = "220px";
            document.querySelector(".K2").style.maxHeight = "200px";
        }
        else{
            document.querySelector(".K").style.Height = "115px";
            document.querySelector(".K2").style.maxHeight = "115px";
        }
        document.querySelector(".k2").style.opacity = "0";
        document.querySelector(".K2").style.transition= "200ms";
    }
}
function toSocial(){
    if(screen.width<=599){
    document.querySelector("body").style.gridTemplateRows = "1fr 5fr 1fr";
    document.querySelector("body").style.transition = "300ms";
    }
    document.querySelector(".btns").style.display = "none";
    document.querySelector(".socialM").style.display = "grid";
    document.querySelector(".A").style.background = "darkslategray";
    document.querySelector(".C").style.background = "darkslategray";
    document.querySelector(".A").style.transition = "500ms";
    document.querySelector(".C").style.transition = "500ms";
}
function toProject(){
    document.querySelector(".btns").style.display = "none";
    document.querySelector(".projects").style.display = "grid";
    document.querySelector("body").style.background = "black";
    document.querySelector(".B").style.backgroundImage = "linear-gradient(90deg ,black 20%,ivory 30%,black 42%,black 50%,black 60%,ivory 70%,black 80%)";
    document.querySelector(".A").style.background = "darkslategray";
    document.querySelector(".C").style.background = "darkslategray";

    document.querySelector(".B").style.transition = "500ms";
    document.querySelector(".A").style.transition = "500ms";
    document.querySelector(".C").style.transition = "500ms";

}
function reload(){
    location.reload()
}
function prjover(np){
    if (np==1){
        document.querySelector(".limg").style.opacity = ".3";
        document.querySelector(".limg").style.transition = "300ms";
    }
    if (np==2){
        document.querySelector(".cimg").style.opacity = ".3";
        document.querySelector(".cimg").style.transition = "300ms";
    }
    if (np==3){
        document.querySelector(".rimg").style.opacity = ".3";
        document.querySelector(".rimg").style.transition = "300ms";
    } 
}
function prjout(np){
    if (np==1){
        document.querySelector(".limg").style.opacity = "1";
        document.querySelector(".limg").style.transition = "200ms";
    }
    if (np==2){
        document.querySelector(".cimg").style.opacity = "1";
        document.querySelector(".cimg").style.transition = "200ms";
    }
    if (np==3){
        document.querySelector(".rimg").style.opacity = "1";
        document.querySelector(".rimg").style.transition = "200ms";
    } 
    changerim();    
}

function changerim(){
    let lwidth = document.querySelector(".limg").clientWidth;
    let lheight = document.querySelector(".limg").clientHeight;
    document.querySelector(".Pdivl").style.maxHeight = lheight;
    document.querySelector(".Pdivl").style.maxWidth = lwidth;
    document.querySelector(".limg").style.borderRadius = "20px";

    lwidth = document.querySelector(".cimg").clientWidth;
    lheight = document.querySelector(".cimg").clientHeight;
    document.querySelector(".Pdivc").style.maxHeight = lheight;
    document.querySelector(".Pdivc").style.maxWidth = lwidth;
    document.querySelector(".cimg").style.borderRadius = "20px";

    lwidth = document.querySelector(".rimg").clientWidth;
    lheight = document.querySelector(".rimg").clientHeight;
    document.querySelector(".Pdivr").style.maxHeight = lheight;
    document.querySelector(".Pdivr").style.maxWidth = lwidth;
    document.querySelector(".rimg").style.borderRadius = "20px";
}