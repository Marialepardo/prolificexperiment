console.log('JavaScript file loaded');
// Initialize global variables 
var     lButtonsMT, timeEnter;
var     sNames  = '';
var     sDT     = '';
var     sCurrent = '';
var     sTypeReveal = 'cell';

// When page is loaded
window.addEventListener('DOMContentLoaded', () => {

    // Activate all mousetracking buttons
    lButtonsMT = document.getElementsByClassName(sTypeReveal);
    for (let i=0; i<lButtonsMT.length; i++) {
        let elem = lButtonsMT[i];
        console.log(elem.title)
        CreateMT(elem,elem.id);
    }

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
    // Update to current label
   // if (sNames.length>0) {
     //   sNames = `${sNames},${id}`;
    //} else {
      //  sNames = `${id}`;
        //console.log('sNames updated to:', sNames);
    //}
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
    var tableContainer = document.getElementById('table-container');
    var rows = tableContainer.getElementsByClassName('row');
    
    // Iterate through all rows to identify and hide the second and third rows of lValues
    for (let i = 0; i < rows.length; i++) {
        var row = rows[i];
        var cells = row.getElementsByClassName('mt-tgt');
        
        // Check if the row contains lValues by the presence of mt-tgt cells
        if (cells.length > 0) {
            // Hide cells in the second and third rows (i == 1 and i == 2 for zero-based index)
            if (i == 1 || i == 2) {
                for (let j = 0; j < cells.length; j++) {
                    cells[j].classList.add('hide');
                }
            } else {
                for (let j = 0; j < cells.length; j++) {
                    cells[j].classList.remove('hide');
                }
            }
        }
    }
}

// here it ends 


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
    console.log('endDecPage:', dec, sNames, sDT);
    endPage();
}