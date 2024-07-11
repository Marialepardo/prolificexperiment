console.log('JavaScript file loaded');
// Initialize global variables 
var     lButtonsMT, timeEnter;
var     sNames  = '';
var     sDT     = '';
var     sCurrent = '';
var     sTypeReveal = 'cell';
var     timedelay = ''; 

// When page is loaded
window.addEventListener('DOMContentLoaded', () => {
    //console.log("Calling disableMouseEvents");
    disableMouseEvents();
    setupCellVisibility();

    // Activate all mousetracking buttons
    setTimeout(() => {
        lButtonsMT = document.getElementsByClassName(sTypeReveal);
        Array.from(lButtonsMT).forEach(elem => {
            console.log(elem.title);
            CreateMT(elem, elem.id);
        });
    }, 4000);  // Wait for the maximum priming time before enabling interactions


    //lButtonsMT = document.getElementsByClassName(sTypeReveal);
    //for (let i=0; i<lButtonsMT.length; i++) {
     //   let elem = lButtonsMT[i];
      //  console.log(elem.title)
      //  CreateMT(elem,elem.id);
    //}

    // Decision Buttons 
    lDecBtns = document.getElementsByClassName("dec-btn");
    for (let i=0; i<lDecBtns.length; i++) {
        let elem    = lDecBtns[i];
        // Get column name from ID
        let dec     = elem.id.split('-')[1];
        console.log(dec)
        // Add on-click function 
        elem.addEventListener('click',()=>{
            console.log('dec')
            document.getElementById('sDec').value = dec;
            document.getElementById('sNames').value = sNames;
            document.getElementById('sDT').value = sDT;
            endPage();
        })
        
    }

    // Begin timer
    timeEnter = new Date();
    setInterval(()=>{
        if (sCurrent!='') {
            let now = new Date();
            let dt = (now - timeEnter)/1000;
            document.getElementById('test-text').innerHTML = `${sCurrent}:${dt}`
        }
    },50)
});

// *********************************************************************
// Function Name:   disableMouseEvents
// Functionality:   disabiling mouseevents at the beginning of the trial so that 
//                  mousetracking does not get enabled while price "priming is happening"
//                   
//
// input:           object id
//
// returns:         
// *********************************************************************
function disableMouseEvents() {
    const events = ['click', 'mousedown', 'mouseup', 'mousemove', 'mouseenter', 'mouseleave', 'contextmenu'];

    // Add event listeners to prevent default handling
    events.forEach(event => {
        document.addEventListener(event, preventDefault, true);
    });

    // Re-enable mouse events after the priming period
    setTimeout(() => {
        events.forEach(event => {
            document.removeEventListener(event, preventDefault, true);
        });
        console.log('Mouse events re-enabled');
    }, Math.random() * 2000 + 2000); // Random delay between 2000ms and 4000ms (save this number per round?)
}

function preventDefault(e) {
    e.preventDefault();
    e.stopPropagation();
}


// *********************************************************************
// Function Name:   setupCellVisibility
// Functionality:   
//                  function sets up the price priming mechanism for 2-4 seconds         
// *********************************************************************

//function setupCellVisibility() {
  // var price_cells = ['#cell-s1', '#cell-s2'];  // target cells by their IDs (here s because it is sustainability prime condition)
   // Initially show and then hide the image after a random time between 2-4 seconds
   //setTimeout(function() {
     //   $(price_cells.join(', ')).addClass('hide');  // Optionally add hide class after fade out
   //}, timedelay = Math.random() * 2000 + 2000);  //* 2000 + 2000 Randomize time between 2-4 seconds
//}

function setupCellVisibility() {
    var price_cells = ['#cell-s1', '#cell-s2'];  // target cells by their IDs
    // Initially show and then hide the image after a random time between 2-4 seconds
    timedelay = Math.random() * 2000 + 2000;  // Set timedelay
    setTimeout(function() {
        $(price_cells.join(', ')).addClass('hide');  // Optionally add hide class after fade out
        document.getElementById('timedelay').value = timedelay;  // Store timedelay in hidden input
    }, timedelay);
}


// *********************************************************************
// Function Name:   updateMT
// Functionality:   
//                  Updates global vars and inputs with latest active AOI
//
// input:           object id
//
// returns:         void
// *********************************************************************

function updateMT() {
    // Store/update current time
    let now = new Date();
    let dt = now - timeEnter;
    timeEnter = now;
    // Save dwell time on AOI
    if (sDT.length>0) {
        sDT =  `${sDT},${dt}`;
        sNames = `${sNames},${sCurrent}`;
    } else {
        sDT = `${dt}`;
        sNames = `${sCurrent}`;
        // If first fixation, also record time to first fixation
        document.getElementById('time2first').value = timeEnter - dt - startTime;
    }
}


// *********************************************************************
// Function Name:   hideEverything
// Functionality:   
//                  Hides all the elements with the class name mt-tgt
//
// input:           object id
//
// returns:         void
// *********************************************************************

// Original function
// function hideEverything() {
    // get all elements to be hidden
    // lTgt = document.getElementsByClassName('mt-tgt');
    // add hidden class
    //for (let i=0;i<lTgt.length; i++) {
     //   lTgt[i].classList.add('hide');
 //   }

//}

//New function so that the first row is not hidden 
function hideEverything() {
    var Cells = ['#cell-s1', '#cell-s2', '#cell-p1', '#cell-p2'];  // target cells by their IDs
    // Use jQuery to select and manipulate the elements
    
    $(Cells.join(', ')).addClass('hide');
}

// *********************************************************************
// Function Name:   activateMT
// Functionality:   
//                  Activate the elements mt-tgt with class tgt
//
// input:           object id
//
// returns:         void
// *********************************************************************

function activateMT(tgt) { 
    console.log(tgt)
    hideEverything();
    let lTgt = document.getElementsByClassName(`mt-tgt ${tgt}`);
    for (let i=0;i<lTgt.length; i++) {
        lTgt[i].classList.remove('hide');
    }
}

// *********************************************************************
// Function Name:   CreateMT
// Functionality:   
//                  Converts an html element into a mousetracking element
//
// input:           elem, object
//
// returns:         void
// *********************************************************************

function CreateMT(elem,tgt) {
    elem.addEventListener("mouseenter", ()=>{
        elem.classList.add('hover');
        timeEnter = new Date();
        sCurrent = elem.id;
        console.log('entering');
        activateMT(tgt)
    })
    elem.addEventListener("mouseleave", ()=>{
        elem.classList.remove('hover');
        sCurrent = elem.id;
        updateMT(elem.id)
        console.log('leaving')
        sCurrent = '';
        hideEverything();
    })
}

// *********************************************************************
// Function Name:   endDecPage
// Functionality:   
//                  function for the decision button/key
//
// input:           dec, decision to be recorded in variable
//
// returns:         void
// *********************************************************************

function endDecPage(dec) {
    // Store all mousetracking variables + decision for the page
    document.getElementById('iDec').value = dec;
    document.getElementById('sNames').value = sNames;
    document.getElementById('sDT').value = sDT;
    document.getElementById('timedelay').value = timedelay
    endPage();
}