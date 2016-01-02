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

var addressUrl = "http://assessment.nnva.gov/PT/search/commonsearch.aspx?mode=address";
var addresses = [];

// Manually set number of lines on csv
var repeatTimes = 1182;
var count = 0;


// pass in javascript array to change to jsv
var toCsv = function toCsv(arr ){
  var csv = arr.join('","').concat("\"");
  csv = "\"".concat(csv);
  return csv;
}

casper.userAgent("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36");
casper.start(addressUrl, function() {
   // this.echo("click agree")
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
    var parcelId = this.evaluate(function(){return document.querySelector(".DataletHeaderTop").querySelector("td").innerText.slice(7)});
    var streetNum = addresses[count]["streetNum"].replace(/"/g,"");
    var street = addresses[count]["street"].replace(/"/g,"");
    var name = addresses[count]["owner"].replace(/"/g,"")
    // Attempt to serialize back to CSV and print out
    this.echo(toCsv([streetNum, street, name, parcelId]));
  })
  count++;
}).run(function() {
  this.exit();
});