/*eslint strict:0*/
/*global, console, require*/
var fs = require("fs");
var casper = require("casper").create({
    //  verbose: true,
    //  logLevel: "debug",
    warning: false,
    webSecurityEnabled: false
});


var addressUrl = "http://assessment.nnva.gov/PT/search/commonsearch.aspx?mode=address";
var addresses = [];

// Manually set number of lines on csv
var repeatTimes = 1182;
var count = 0;

casper.userAgent("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36");
casper.start(addressUrl, function() {
   this.echo("click agree ")
   this.click("#btAgree");

   stream = fs.open('nnData.csv', 'r');
   line = stream.readLine();
   i = 0;
   while(line) {
     // casper.echo(line);
     line = stream.readLine();
     var nextLine = line.split(',')
     var addrObj = {
       streetNum: nextLine[0],
       street: nextLine[1],
       owner: nextLine[2]
     };
     addresses.push(addrObj);
     i++;
   }
}).repeat(repeatTimes, function(){
  casper.thenOpen(addressUrl).then(function() {
      // now search for 'phantomjs' by fillin the form again
      this.echo("filling out address");
      this.echo(addresses[count]["streetNum"]);
      this.fillSelectors("form", {
        "input[name='inpNumber']": addresses[count]["streetNum"].replace(/"/g,""),
        "input[name='inpStreet']": addresses[count]["street"].replace(/"/g,"")
      }, false);

      this.click("#btSearch");
      // this.capture('foo.jpg', undefined, {
      //   format: 'jpg',
      //   quality: 75
      // });
  }).then(function(){
    // Grab the Parcel number from the Reverse Lookup
    this.echo('evaluating');
    this.echo(this.evaluate(function(){return document.querySelector(".DataletHeaderTop").querySelector("td").innerText.slice(7)}))
  })
  count++;
}).run(function() {
  this.exit();
});