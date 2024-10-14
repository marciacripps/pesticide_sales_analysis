let viz;

function initViz() {
    console.log("Initializing Tableau Viz...");

    const containerDiv = document.getElementById("vizContainer"),
        url = "https://public.tableau.com/views/pesticide_sales_17287054268960/Dashboard1";

    if (!containerDiv) {
        console.error("Container for Tableau Viz not found.");
        return;
    }

    console.log("Container found. Attempting to load Tableau Viz from URL:", url);


    let options = {
        hideTabs: true,
        onFirstInteractive: function () {
            console.log("Tableau Viz has been successfully loaded.");
        }
    };

    try {
    
        viz = new tableau.Viz(containerDiv, url, options);
        console.log("Tableau Viz initialized.");
    } catch (error) {
        console.error("Error initializing Tableau Viz:", error);
    }
}

window.onload = initViz;
