"use strict";

console.log("UNIX-Time:", Math.round(Date.now()/1000));
console.log("LocalTime:", Date());

class Ttime {
  constructor(utc) {
    this.time = new Date(utc);
    this.year = this.time.getFullYear();
    this.month = ("0" + (this.time.getMonth()+1)).slice(-2);
    this.date = ("0" + this.time.getDate()).slice(-2);
    this.hours = ("0" + this.time.getHours()).slice(-2);
    this.minutes = ("0" + this.time.getMinutes()).slice(-2);
  }
}

document.addEventListener('DOMContentLoaded', function(){
  // UTC -> LocalTime
  const Tnow = new Ttime(Date.now());
  const nodes = document.querySelectorAll('span.utc');
  nodes.forEach((node) => {
    let Tstamp = new Ttime(node.innerText * 1000);
    let res;
    if ( Tstamp.year !== Tnow.year ) {
      res = Tstamp.year + "/" + Tstamp.month + "/" + Tstamp.date;
    } else if ( Tstamp.month !== Tnow.month || Tstamp.date !== Tnow.date ) {
      res = Tstamp.month + "/" + Tstamp.date;
    } else {
      res = Tstamp.hours + ":" + Tstamp.minutes;
    }
    node.innerText = res;
  })
},false);
