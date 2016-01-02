/*eslint strict:0*/
/*global, console, require*/
var fs = require("fs");
var casper = require("casper").create({
    //  verbose: true,
    //  logLevel: "debug",
    warning: false,
    webSecurityEnabled: false
});

 var user = casper.cli.get(0);
 var password = casper.cli.get(1);

casper.userAgent("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36");
casper.start("http://assessment.nnva.gov/PT/search/commonsearch.aspx?mode=address", function() {
   this.echo("click agree ")
   this.click("#btAgree");
});

casper.then(function() {
    // now search for 'phantomjs' by fillin the form again
    this.echo("filling out address");
    this.fillSelectors("form", {
      "input[name='inpNumber']": "7304",
      "input[name='inpStreet']": "WARWICK"
    }, false);

    this.click("#btSearch");
});



casper.then(function(){
  // Grab the Parcel number from the Reverse Lookup
  this.echo('evaluating');
  this.echo(this.evaluate(function(){return document.querySelector(".DataletHeaderTop").querySelector("td").innerText.slice(7)}))
});


casper.run(function() {
  this.exit();
});
